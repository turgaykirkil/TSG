import os
from datetime import datetime
import hashlib
import spacy
import logging
import re
import unicodedata
import time
from spacy.cli.download import download as spacy_download
from spacy.util import is_package
try:
    from transformers import pipeline as hf_pipeline  # type: ignore
except Exception:  # transformers yoksa da çalışabilsin
    hf_pipeline = None  # type: ignore

import json
from typing import Any, Optional, List, Dict, Set, Tuple
try:
    import httpx  # type: ignore
except Exception:
    httpx = None  # type: ignore
try:
    import requests  # type: ignore
except Exception:
    requests = None  # type: ignore

# Configure logging
logger = logging.getLogger(__name__)

MODEL_NAME = "tr_core_news_sm"
nlp_model = None
hf_ner = None  # Hugging Face NER pipeline (opsiyonel)

# LLM (LM Studio / OpenAI uyumlu) yapılandırması
LLM_ENABLED = os.getenv("USE_QWEN_LLM", "0").strip() in ("1", "true", "True")
LLM_BASE_URL = os.getenv("LLM_BASE_URL", "http://localhost:1234/v1").strip()
LLM_MODEL = os.getenv("LLM_MODEL", "qwen/qwen3-4b-thinking-2507").strip()
LLM_API_KEY = os.getenv("LLM_API_KEY", "").strip()
try:
    LLM_TIMEOUT = float(os.getenv("LLM_TIMEOUT", "30").strip())
except Exception:
    LLM_TIMEOUT = 30.0

# --- Başlık Tespiti Ayarları (Ortam Değişkenleri ile) ---
try:
    HEADER_CLUSTER_DIST = int(os.getenv("HEADER_CLUSTER_DIST", "200").strip())
except Exception:
    HEADER_CLUSTER_DIST = 200

# --- Bölme Sonrası Kısa Segment Birleştirme Eşiği ---
try:
    MIN_SPLIT_SEG_LEN = int(os.getenv("MIN_SPLIT_SEG_LEN", "320").strip())
except Exception:
    MIN_SPLIT_SEG_LEN = 320
try:
    HEADER_LOOKAHEAD_CHARS = int(os.getenv("HEADER_LOOKAHEAD_CHARS", "600").strip())
except Exception:
    HEADER_LOOKAHEAD_CHARS = 600
try:
    HEADER_MIN_SCORE = int(os.getenv("HEADER_MIN_SCORE", "2").strip())
except Exception:
    HEADER_MIN_SCORE = 2

# --- Otomatik Kaydetme (OCR çıktılarını dosyaya yaz) ---
# Varsayılanı KAPALI: Supabase'e doğrudan yazacağımız için yerel JSON kaydı devre dışı.
try:
    AUTO_SAVE_OCR = os.getenv("AUTO_SAVE_OCR", "0").strip() in ("1", "true", "True")
except Exception:
    AUTO_SAVE_OCR = False

# --- NLP Debug Loglama ---
# try:
#     DEBUG_NLP = os.getenv("DEBUG_NLP", "0").strip() in ("1", "true", "True")
# except Exception:
#     DEBUG_NLP = False
DEBUG_NLP = False

# --- OCR Normalizasyonu ve Yardımcı Regex Fonksiyonları ---
TURKISH_MONTHS = (
    "OCAK|SUBAT|MART|NISAN|MAYIS|HAZIRAN|TEMMUZ|AGUSTOS|EYLUL|EKIM|KASIM|ARALIK"
)

def is_upper_heavy(s: str, ratio: float = 0.7) -> bool:
    """Metnin harflerinin büyük harf oranı verilen eşikten yüksekse True döner.
    Rakam/işaretleri hariç tutar; Türkçe karakterlerle uyumlu çalışır.
    """
    letters = [ch for ch in s if ch.isalpha()]
    if not letters:
        return False
    upp = sum(1 for ch in letters if ch == ch.upper())
    return (upp / len(letters)) >= ratio

def _nlp_collect_after(idx: int, lines: List[str], initial: str = "") -> str:
    cand: List[str] = ([] if not initial else [initial])
    # Markdown-aware stop_line: allow optional # at start
    stop_line = re.compile(
        r"^\s*#*\s*(?:Eski\s*(?:Ticaret\s*)?Unva[nm](?:[ıiİI])?(?:t)?|(?:Ticaret\s*)?Unva[nm](?:[ıiİI])?(?:t)?|Adres|(?:Yu(?:ka(?:r|rn|n)?[ıi]?da)|Yukarıda|Yukarida)|Tescil|Tescile|MERS[İIiı]S|Ticaret\s*Sicil|Telefon|[İI]?lan\s*S[ıiuü]ra\s*No|Sira\s*No|S[ıi]ra\s*No|Dosya|ibraz\s+edilen|Kurucu|Uyruk|Tasfiye|\|)\b",
        re.IGNORECASE,
    )
    # Ekstra gürültü filtresi (herhangi bir yerde geçmesi yeterli)
    noise_pat = re.compile(r"(\||\b(Uyruk|Kurucu|Dosya\s*No|ibraz\s+edilen|tasdikli|karar[ıi])\b)", re.IGNORECASE)
    # Adres-benzeri içerik tespiti (satır içerik koruması)
    addressish = re.compile(r"\b(MAH\.?|MAHALLES[İI]|CAD\.?|CADDES[İI]|CD\.?|SOK\.?|SOKA[ĞG][ıi]|SK\.?|BLV\.?|BULVAR[ıi]?|NO\b|KAT\b|DA[İI]RE\b|APT\.?|S[İI]TE|OSB|İÇ\s*KAP[İI]|DIŞ\s*KAP[İI]|BLOK)\b|[A-ZÇĞİÖŞÜ]{2,}\s*/\s*[A-ZÇĞİÖŞÜ]{2,}", re.IGNORECASE)
    for j in range(idx + 1, min(idx + 5, len(lines))):
        nxt = lines[j].strip(" -*–·•\t").strip()
        if not nxt:
            continue
        # UNVAN/ADRES başlığı altında sık görülen "Madde 2-", "3. ILAN" benzeri gürültü satırlarını atla
        noise_skip = re.compile(r"^(\s*#*\s*(\d+\s*\.?\s*[İI]LAN|İlan\s*S[ıi]ra\s*No.*?\:?|MERS[İI]S\s*No.*?\:?|S[ıi]ra\s*No.*?\:?|Madde\s*\d+\s*[-–—:]?)\s*)$", re.IGNORECASE)
        if noise_skip.match(nxt):
            continue
        # "'dir." gibi tek başına hüküm cümlesini atla
        if re.match(r"^['’]?(?:dir|dır|dur|dür)\.?$", nxt, flags=re.IGNORECASE):
            continue
        if DEBUG_NLP: print(f"DEBUG_NLP _nlp_collect_after inspecting: {nxt!r}")
        if stop_line.search(nxt) or noise_pat.search(nxt):
            if DEBUG_NLP: print(f"DEBUG_NLP _nlp_collect_after STOP due to noise/header: {nxt!r}")
            break
        # Adres-benzeri satırsa birleştirmeyi kes
        if addressish.search(nxt):
            break
        cand.append(nxt)
        if len(cand) >= 4:
            break
    return re.sub(r"\s+", " ", " ".join(cand)).strip() if cand else ""

def normalize_text(text: str) -> str:
    """
    OCR kaynaklı yaygın karakter/satır bozulmalarını kısmen düzeltir.
    Aşırı agresif olmayan, güvenli dönüşümler uygular.
    """
    if not text:
        return text
    # Satır sonlarında kopmuş kelimeleri birleştirme ("-\n" -> "")
    s = re.sub(r"-\n\s*", "", text)
    # Çoklu boşlukları sadeleştir
    s = re.sub(r"[\t\x0b\x0c\r]+", " ", s)
    # '$' karakteri: bağlama göre düzelt
    # - Sayı/* içeren tokenlar içinde '$' -> '5' (örn. $65******42 -> 565******42)
    # - Kalan '$' -> 'Ş' (örn. KI$ILER -> KIŞILER)
    def _repl_dollar_num(match: re.Match) -> str:
        return match.group(0).replace("$", "5")
    s = re.sub(r"(?<!\w)(?:[0-9\*]*\$[0-9\*]*)+(?!\w)", _repl_dollar_num, s)
    s = s.replace("$", "Ş")
    # NBSP -> boşluk
    s = s.replace("\u00A0", " ")
    # Sayfa ayırıcılarını satıra çevir
    s = re.sub(r"---\s*Sayfa\s*\d+\s*---", "\n", s, flags=re.IGNORECASE)
    # Boşluk sadeleştirme: satır sonlarını koru (\n dokunma)
    s = re.sub(r"[ \t\x0b\x0c\r]+", " ", s)
    # Satır sonu etrafındaki boşlukları temizle
    s = re.sub(r"[ \t]+\n", "\n", s)
    s = re.sub(r"\n[ \t]+", "\n", s)
    # Çoklu boş satırları azalt
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s.strip()

def find_first(regex: str, text: str, flags=re.IGNORECASE):
    m = re.search(regex, text, flags)
    if not m:
        return None
    # Yakalama grubu varsa ilk dolu grubu döndür, yoksa tüm eşleşmeyi döndür
    try:
        if getattr(m, "lastindex", None):
            for i in range(1, (m.lastindex or 0) + 1):
                g = m.group(i)
                if g:
                    return g.strip()
        return m.group(0).strip()
    except Exception:
        try:
            return m.group(0).strip()
        except Exception:
            return None

def find_all(regex: str, text: str, flags=re.IGNORECASE):
    return [g.strip() for g in re.findall(regex, text, flags)]

def unique_list(seq):
    seen = set()
    out = []
    for x in seq:
        x_key = x if isinstance(x, str) else str(x)
        if x_key.lower() not in seen:
            seen.add(x_key.lower())
            out.append(x)
    return out

# Şehir/ilçe gibi yaygın yer adları (OCR varyantlarını da içerir)
LOCATION_TOKENS = {
    "ADANA","ADIYAMAN","AFYONKARAHISAR","AGRI","AMASYA","ANKARA","ANTALYA","ARTVIN","AYDIN",
    "BALIKESIR","BILECIK","BINGOL","BITLIS","BOLU","BURDUR","BURSA","CANAKKALE","CANKAYA",
    "CANKIRI","CORUM","DENIZLI","DIYARBAKIR","EDIRNE","ELAZIG","ERZINCAN","ERZURUM",
    "ESKISEHIR","GAZIANTEP","GIRESUN","GUMUSHANE","HAKKARI","HATAY","ICEL","MERSIN",
    "ISPARTA","ISTANBUL","IZMIR","KARS","KASTAMONU","KAYSERI","KIRKLARELI","KIRSEHIR",
    "KOCAELI","KONYA","KUTAHYA","MALATYA","MANISA","KAHRAMANMARAS","MARDIN","MUGLA",
    "MUS","NEVSEHIR","NIGDE","ORDU","RIZE","SAKARYA","SAMSUN","SIIRT","SINOP","SIVAS",
    "TEKIRDAG","TOKAT","TRABZON","TUNCELI","SANLIURFA","USAK","VAN","YOZGAT","ZONGULDAK",
    "AKSARAY","BAYBURT","KARAMAN","KIRIKKALE","BATMAN","SIRNAK","BARTIN","ARDAHAN","IGDIR",
    "YALOVA","KARABUK","KILIS","OSMANIYE","DUZCE","DUEZCE",
    # Sık görülen ilçe/semti ekle (ASCII varyantlarıyla)
    "ZEYTINBURNU","KAGITHANE","KAĞITHANE","PENDIK","PENDİK","BASAKSEHIR","BAŞAKŞEHİR",
    "IZMIT","İZMİT",
    "BAYRAMPASA","BAYRAMPAŞA","UMRANIYE","ÜMRANIYE","GOLBASI","GÖLBAŞI","ALTINDAG","ALTINDAĞ",
    "CANKAYA","ÇANKAYA","ESENLER","BAGCILAR","BAĞCILAR","BAKIRKOY","BAKIRKÖY","BEŞİKTAŞ",
    "BESIKTAS","KADIKOY","KADIKÖY","ŞİŞLİ","SISLI","MALTEPE","KARTAL","ÜSKÜDAR",
    "USKUDAR","FATIH","FATİH","BEYOĞLU","BEYOGLU",
    "SANCAKTEPE","SULTANBEYLI","SULTANBEYLİ","BEYLIKDUZU","BEYLİKDÜZÜ","ESENYURT",
    "AVCILAR","KUCUKCEKMECE","KÜÇÜKÇEKMECE","BUYUKCEKMECE","BÜYÜKÇEKMECE",
    "SARIYER","TUZLA","CEKMEKOY","ÇEKMEKÖY","GAZIOSMANPASA","GAZİOSMANPAŞA",
    "SULTANGAZI","SULTANGAZİ","ARNAVUTKOY","ARNAVUTKÖY",
    "TICARET","SICIL","MUDURLUGU","MÜDÜRLÜĞÜ","ODASI","BORSASI","BIRLIGI","BİRLİĞİ",
}

def _is_location_like(tok: str) -> bool:
    up = (tok or "").upper()
    if up in LOCATION_TOKENS:
        return True
    # Basit OCR varyantları: ANKARA, ANKARAI, CANKAYA, CANKAYAI, CANKATAI vb.
    if re.fullmatch(r"AN?KAR[AI]", up):
        return True
    if re.fullmatch(r"CANKA[A-Z]{1,6}", up):
        return True
    return False

# OCR gürültüsü/başlık benzeri tokenlar (büyük harf)
NOISE_TOKENS = {
    "CUMHURIYET","CUMHURIYETI","CUMHURIYETII","CUMHURIYETIN","UYRUKLU",
    "UYRUĞU","ADINA","HAREKET","EDEN","MUDURU","MÜDÜRÜ","ORTAGI","ORTAĞI",
    # Sektör/konu kelimeleri (kişi adı değil)
    "TICARETI","TİCARETİ","MADENI","MADENİ","YAG","YAĞ","ANTIFRIZ","ANTİFRİZ",
    "MUDURLUK","MÜDÜRLÜK","UNVAN","UNVANI","UNVANLI","SIRKETI","ŞİRKETİ","LTD","STI","ŞTİ",
    "TASFIYE","HALINDE","MUDURLUGUNDEN","MÜDÜRLÜĞÜNDEN",
}
# --- Yardımcı: kişi–maskeli kimlik eşlemesi (minimal çıktı zenginleştirme) ---
def _pair_masked_ids_to_persons(text: str, persons: List[dict], masked_ids: List[str]) -> List[dict]:
    """
    Verilen ilân metni içinde, PER* kişileri en yakın maskeli kimlikle (aynı satır veya takip eden 1-3 satır
    penceresinde adı geçiyorsa) eşler ve her eşleşen kişiye 'masked_ids' alanını (string) ekler.
    Eşleşmeyen kişi nesneleri olduğu gibi korunur. Tek maske varsa ve tek kişi varsa basit geri düş ile atanır.
    """
    try:
        if not text or not masked_ids:
            return persons
        lines = text.splitlines()
        # Maskeli kimliklerin geçtiği satır indekslerini bul
        id_positions: List[Tuple[str, int]] = []
        # Yalnızca maske paternine uyan kimlikleri dikkate al.
        # OCR toleransı: '5' sıklıkla '$' olarak gelebilir; (\d|\$) kabul edilir.
        # Opsiyonel tek harf önekini (örn. 'N********9') destekle.
        mask_re = re.compile(r"^(?:(?P<prefix>[A-Za-z])(?P<body>(?:\d|\$){1,4}\*{2,8}(?:\d|\$){1,3})|(?P<body2>(?:\d|\$){1,4}\*{2,8}(?:\d|\$){1,3}))$")
        for mi in masked_ids:
            token = (mi or "").strip()
            if not token:
                continue
            mtoken = mask_re.match(token)
            if not mtoken:
                # Harf/karakter içeren sahte maskeleri (örn. "1 ******TA") dışarıda bırak
                continue
            pfx = mtoken.groupdict().get("prefix") or ""
            body = mtoken.groupdict().get("body") or mtoken.groupdict().get("body2") or token
            mid_out = (pfx + body.replace("$", "5")) if pfx or "$" in body else (pfx + body if pfx else body)
            # Belge genelinde (tüm satırlar) önek araması: varsa onu kullan
            pfx_doc = ""
            try:
                doc_text = "\n".join(lines)
                mdoc = re.search(rf"(?P<pfx>[A-Za-z]){re.escape(token)}", doc_text)
                if mdoc and mdoc.groupdict().get("pfx"):
                    pfx_doc = mdoc.group("pfx")
            except Exception:
                pass
            for idx, raw in enumerate(lines):
                if token in raw:
                    eff_pfx = pfx_doc or pfx
                    out = (eff_pfx + body.replace("$", "5")) if eff_pfx or "$" in body else (eff_pfx + body if eff_pfx else body)
                    id_positions.append((token, idx, out))
                    break
        if not id_positions:
            return persons

        enriched: List[dict] = []
        assigned_person_idxs: Set[int] = set()
        used_id_indexes: Set[int] = set()
        # Aynı ismin birden çok maskeye aşırı yayılmasını engellemek için ilk atandığı satır ve id
        assigned_name_first_line: Dict[str, int] = {}
        assigned_name_to_id: Dict[str, str] = {}

        # Yardımcılar: konu/başlık gürültüsü ve sondaki tek küçük harf düzeltmesi
        TOPIC_NOISE_TOKENS = {
            # OCR ASCII ve Türkçe varyantlar
            "PAY", "DEVRI", "DEVRİ", "MUDURLER", "MÜDÜRLER", "YETKILILER", "YETKİLİLER",
        }
        TOPIC_NOISE_PHRASES = {
            "PAY DEVRI", "PAY DEVRİ",
        }
        def _is_topic_noise_name(name: str) -> bool:
            n = (name or "").strip()
            if not n:
                return False
            up = n.upper()
            if up in TOPIC_NOISE_PHRASES:
                return True
            toks = [t for t in re.split(r"\s+", up) if t]
            if 1 <= len(toks) <= 3 and all(t in TOPIC_NOISE_TOKENS for t in toks):
                return True
            return False

        def _strip_trailing_single_lower(nm: str) -> str:
            s = (nm or "").strip()
            if not s:
                return s
            # Tümü büyük harf(ler) + sonda tek bir küçük harf ise o küçük harfi at
            if re.fullmatch(r"[A-ZÇĞİÖŞÜ'’\- ]+[a-zçğıöşü]", s):
                return s[:-1].rstrip()
            return s

        # Kişi adlarının ilk göründüğü satır indeksini önceden hesapla
        person_first_line_idx: Dict[int, int] = {}
        lower_lines = [ln.lower() for ln in lines]
        for pi, p in enumerate(persons):
            name = (p.get("text") or "").strip().lower()
            if not name:
                person_first_line_idx[pi] = -1
                continue
            found_idx = -1
            for li, l in enumerate(lower_lines):
                if name and name in l:
                    found_idx = li
                    break
            person_first_line_idx[pi] = found_idx

        # 1) Birincil: ±3 satırlık pencere içinde eşle
        for id_order, (mid, i, mid_out) in enumerate(id_positions):
            # Daha geniş bağlam penceresi (±15 satır) — mevcut PER kişileriyle eşleşmeyi artırmak için
            s = max(0, i - 15)
            e = min(len(lines), i + 16)
            window_text = "\n".join(lower_lines[s:e])
            window_orig = "\n".join(lines[s:e])
            matched = False
            # ÖNCELİK: "<ADDRESS> adresinde ikamet eden <NAME>" bağlamı ile aday isim çıkar
            try:
                # Capture address before the phrase and name after it
                m = re.search(r"([A-ZÇĞİÖŞÜ0-9\.\s,/\-#]{5,150})\s+adresinde\s+ikamet\s+eden[,:]?\s+([A-ZÇĞİÖŞÜ$'’\-\s]{3,})", window_orig, flags=re.IGNORECASE)
                cand = None
                p_addr = None
                if m:
                    p_addr = m.group(1).strip()
                    cand = m.group(2)
                    # Satır sonu/durdurucu veya apostrof öncesinde kes
                    cand = re.split(r"[\n;:,’']", cand)[0]
                    # OCR normalizasyonu
                    cand = cand.replace("$", "Ş")
                    # Sondaki iyelik eki + opsiyonel "önceki" temizliği
                    cand = re.sub(r"\s*['’][iıiuü]n(?:\s+önceki)?\s*$", "", cand, flags=re.IGNORECASE).strip()
                    # Birden fazla boşluğu sadeleştir
                    cand = re.sub(r"\s+", " ", cand)

                if cand:
                    parts = [p for p in cand.split() if p]
                    if len(parts) >= 2 and all(len(x) >= 2 for x in parts[:2]):
                        p2 = {
                            "text": cand,
                            "label": "PER_MASKED",
                            "masked_ids": mid_out,
                            "address": p_addr # Capture the address!
                        }
                        enriched.append(p2)
                        used_id_indexes.add(id_order)
                        matched = True
            except Exception:
                pass
            if not matched:
                # ÖZEL DURUM: "<AD SOYAD> için müşterek olduğu yetkililer ( ... )" kalıbı
                try:
                    m_icin = re.search(
                        r"([A-ZÇĞİÖŞÜ$'’\-\s]{3,}?)\s+i[çc]in\s+m[üu][şs]terek(?:en)?\s+oldu\w*\s+yetkili\w*\s*\(",
                        window_orig,
                        flags=re.IGNORECASE,
                    )
                    if m_icin:
                        cand = m_icin.group(1)
                        cand = re.split(r"[\n;:,]", cand)[0]
                        cand = re.split(r"['’][aâeiıioöuüAÂEİIİOÖUÜ]", cand)[0]
                        cand = cand.replace("$", "Ş")
                        cand = re.sub(r"\s+", " ", cand).strip()
                        parts = [p for p in cand.split() if p]
                        if len(parts) >= 2 and all(len(p) >= 2 for p in parts):
                            enriched.append({"text": cand, "label": "PER_MASKED", "masked_ids": mid_out})
                            matched = True
                            used_id_indexes.add(id_order)
                except Exception:
                    pass
            if not matched:
                # 0.0) Markdown Tablo Satırı: "Maskeli ID bir tablo satırındaysa (|), satırdaki BÜYÜK HARFLİ hücreyi kişi olarak ata"
                if "|" in lines[i]:
                    try:
                        cells = [c.strip() for c in lines[i].split("|") if c.strip()]
                        for cell in cells:
                            if cell == mid or "Kimlik" in cell or "Uyruk" in cell or _is_location_like(cell):
                                continue
                            toks = cell.split()
                            if 2 <= len(toks) <= 4 and all(re.fullmatch(r"[A-ZÇĞİÖŞÜ'’\-]+", t) for t in toks) and any(len(t) >= 3 for t in toks):
                                cand = " ".join(toks)
                                cand = _strip_trailing_single_lower(cand)
                                if cand and not _is_topic_noise_name(cand):
                                    enriched.append({"text": cand, "label": "PER_MASKED", "masked_ids": mid_out})
                                    matched = True
                                    used_id_indexes.add(id_order)
                                    assigned_name_first_line.setdefault(cand.upper(), i)
                                    assigned_name_to_id.setdefault(cand.upper(), mid)
                                    break
                    except Exception:
                        pass

            if not matched:
                # 0) Doğrudan bağlama: "<ID> Kimlik Numara... <AD SOYAD>" kalıbı
                try:
                    # "Kimlik Numara" ve "Kimlik No" varyasyonlarını tolere et
                    patterns = [
                        rf"{re.escape(mid)}\s+Kimlik\s+Numara\w*\s+([A-ZÇĞİÖŞÜ$'’\-\s]{3,})",
                        rf"{re.escape(mid)}\s+Kimlik\s+No\W*\w*\s+([A-ZÇĞİÖŞÜ$'’\-\s]{3,})",
                    ]
                    mdir = None
                    for rx in patterns:
                        m = re.search(rx, window_orig, flags=re.IGNORECASE)
                        if m:
                            mdir = m
                            break
                    # Alternatif: ">> ... Aksi Karar Alıncaya" ifadesinden önce gelen büyük harfli isim
                    if not mdir:
                        m_alt = re.search(r"([A-ZÇĞİÖŞÜ$'’\-\s]{3,}?)\s*(?:;|,)?\s*Aksi\s+Karar\s+Al[ıi]n[ıi]ncaya", window_orig, flags=re.IGNORECASE)
                        if m_alt:
                            mdir = m_alt
                    if mdir:
                        cand_raw = mdir.group(1)
                        # OCR normalizasyonu
                        cand_raw = cand_raw.replace("$", "Ş")
                        # 0.a) Hızlı doğrudan büyük harfli isim yakalaması (2-4 token)
                        try:
                            mname = re.search(r"([A-ZÇĞİÖŞÜ'’\-]{2,}(?:\s+[A-ZÇĞİÖŞÜ'’\-]{2,}){1,3})(?![A-ZÇĞİÖŞÜ])", cand_raw)
                            if mname:
                                name0 = re.sub(r"\s+", " ", (mname.group(1) or "").strip())
                                name0 = _strip_trailing_single_lower(name0)
                                if name0 and not _is_topic_noise_name(name0) and not re.search(r"\baksi\s+karar\b", name0, flags=re.IGNORECASE):
                                    enriched.append({"text": name0, "label": "PER_MASKED", "masked_ids": mid_out})
                                    matched = True
                                    used_id_indexes.add(id_order)
                                    assigned_name_first_line.setdefault(name0.upper(), i)
                                    assigned_name_to_id.setdefault(name0.upper(), mid)
                        except Exception:
                            pass
                        if matched:
                            continue
                        # Token bazlı tarama: '/' kuralını ve STOP/lokasyon atlamayı uygula
                        toks = [t for t in re.split(r"[\s,;:()\[\]{}<>|\/\\\-]+", cand_raw.strip()) if t]
                        slash_near = "/" in (cand_raw[:120] or "")
                        STOP_HEAD = {"TURKIYE","TÜRKİYE","UYRUK","UYRUKLU","ADRESINDE","ADRESINDEKI","IKAMET","IKAMETEN"}
                        name_toks: List[str] = []
                        started = False
                        seen_lower_after_slash = False
                        def _upper_token_ok(t: str) -> bool:
                            # Sondaki apostrof + iyelik eki ("BAYRAM'in") toleransı
                            base = re.sub(r"['’][aâeiıioöuüAÂEİIİOÖUÜ]{1,3}$", "", t)
                            # OCR kırıntısı: tamamen büyük harf + sonda tek küçük harf (örn. BOSTANCIe) kabul
                            if re.fullmatch(r"[A-ZÇĞİÖŞÜ'’\-]{2,}[a-zçğıöşü]?", base):
                                return True
                            return False

                        for tok in toks:
                            up = tok.upper()
                            # Küçük harf görürsek işaretle/bitir
                            if re.search(r"[a-zçğıöşü]", tok):
                                # Özel tolerans: isim başladıysa ve token sadece sonda tek küçük harf içeriyorsa
                                # (örn. BOSTANCIe), küçük harfi atarak son token olarak kabul et
                                if started and re.fullmatch(r"[A-ZÇĞİÖŞÜ'’\-]{2,}[a-zçğıöşü]", tok):
                                    name_toks.append(tok[:-1])
                                    break
                                if slash_near and not started:
                                    seen_lower_after_slash = True
                                    continue
                                if started:
                                    break
                                continue
                            # Büyük harf token doğrulama
                            if not _upper_token_ok(tok):
                                if started:
                                    break
                                continue
                            # Başta STOP/lokasyonları atla
                            if not started and (up in STOP_HEAD or _is_location_like(tok)):
                                continue
                            # '/' bağlamında küçük harf segmentine kadar bekle
                            if slash_near and not seen_lower_after_slash and not started:
                                continue
                            # Gürültü tokenlarını atla
                            if up in NOISE_TOKENS:
                                if started:
                                    break
                                continue
                            started = True
                            name_toks.append(tok)
                            if len(name_toks) >= 4:
                                break
                        # Parçalı soyadı birleştirme (ör. BA + YRAM -> BAYRAM, BA + YRAKTAR -> BAYRAKTAR)
                        def _merge_split_upper(ts: List[str]) -> List[str]:
                            out: List[str] = []
                            j = 0
                            while j < len(ts):
                                cur = ts[j]
                                if j + 1 < len(ts):
                                    nxt = ts[j + 1]
                                    if len(cur) <= 2 and re.fullmatch(r"[A-ZÇĞİÖŞÜ'’\-]{2,}", nxt):
                                        merged = (cur + nxt).replace(" ", "")
                                        if re.fullmatch(r"[A-ZÇĞİÖŞÜ'’\-]{3,}", merged):
                                            out.append(merged)
                                            j += 2
                                            continue
                                out.append(cur)
                                j += 1
                            return out
                        name_toks = _merge_split_upper(name_toks)
                        if 2 <= len(name_toks) <= 4 and any(len(t) >= 3 for t in name_toks):
                            cand = re.sub(r"\s+", " ", " ".join(name_toks)).strip()
                            cand = _strip_trailing_single_lower(cand)
                            if cand and not re.search(r"\baksi\s+karar\b", cand, flags=re.IGNORECASE) and not _is_topic_noise_name(cand):
                                # Aynı isim farklı maskelere yayılmasın: yalnızca ilk yakın id'ye ata
                                name_key = cand.upper().strip()
                                cur_line = lines[i]
                                tail_line = cur_line[cur_line.find(mid) + len(mid):] if mid in cur_line else cur_line
                                # Eğer bu isim zaten başka bir id'ye atanmışsa, tekrar atama
                                # yapılmaz (bir-to-bir eşleme tercih edilir)
                                if name_key in assigned_name_to_id and assigned_name_to_id[name_key] != mid:
                                    pass
                                elif name_key in tail_line.upper() or name_key not in assigned_name_first_line:
                                    enriched.append({"text": cand, "label": "PER_MASKED", "masked_ids": mid_out})
                                    matched = True
                                    used_id_indexes.add(id_order)
                                    assigned_name_first_line.setdefault(name_key, i)
                                    assigned_name_to_id.setdefault(name_key, mid)
                                    for pi, p in enumerate(persons):
                                        if (p.get("text") or "").strip().upper() == cand.upper():
                                            assigned_person_idxs.add(pi)
                                            break
                except Exception:
                    pass
            if not matched and not any((pp.get("label") or "").upper() == "PER" for pp in persons):
                # 1) Basit tarama (yalnızca hiç PER bulunamadıysa):
                #    Kimlikten sonra 2–4 BÜYÜK harfli token dizisi (satır + sonraki 1-2 satır)
                #    YENİ: Eğer satır bir Markdown tablosu ise (| varsa), ismin ID'den önce gelme ihtimaline karşı tüm satırı tara.
                try:
                    cur_line = lines[i]
                    pos = cur_line.find(mid)
                    if "|" in cur_line:
                        ctx = cur_line.replace(mid, " ")
                    else:
                        tail = cur_line[pos+len(mid):] if pos >= 0 else ""
                        ctx = tail
                        if i + 1 < len(lines):
                            ctx += " " + lines[i + 1]
                        if i + 2 < len(lines):
                            ctx += " " + lines[i + 2]
                    slash_near = "/" in ctx[:120]
                    toks = [t for t in re.split(r"[\s,;:()\[\]{}<>|\/\\\-]+", ctx.strip()) if t]
                    name_toks: List[str] = []
                    started = False
                    seen_lower_after_slash = False
                    for tok in toks:
                        up = tok.upper()
                        # Slash bağlamında, küçük harf görüldüyse işaretle ve isim toplamaya hazır ol
                        if re.search(r"[a-zçğıöşü]", tok):
                            if slash_near and not started:
                                seen_lower_after_slash = True
                                continue
                            if started:
                                break
                            continue
                        # Büyük harfli, geçerli token mi?
                        if not _upper_token_ok(tok):
                            if started:
                                break
                            continue
                        # Adres bağlaçları 'ADRESINDE/ADRESINDEKI' isim dizisini keser
                        if up.startswith("ADRESINDE") or up.startswith("ADRESINDEKI") or up == "IKAMET" or up == "IKAMETEN":
                            if started and 2 <= len(name_toks) <= 4:
                                break
                            else:
                                continue
                        # Yer adı benzeri ise başta yut; başladıktan sonra sonlandır
                        if _is_location_like(tok):
                            if slash_near and not started and not seen_lower_after_slash:
                                continue
                            if started:
                                break
                            continue
                        # Gürültü tokenları (OCR/başlık) ise atla
                        if up in NOISE_TOKENS:
                            if started:
                                break
                            continue
                        # '/' kuralı: küçük harf segmentini görmeden başlamayız
                        if slash_near and not seen_lower_after_slash and not started:
                            continue
                        # Uygun: ekle
                        started = True
                        name_toks.append(tok)
                        if len(name_toks) >= 4:
                            break
                    # Parçalı soyadı birleştirme
                    def _merge_split_upper(ts: List[str]) -> List[str]:
                        out: List[str] = []
                        j = 0
                        while j < len(ts):
                            cur = ts[j]
                            if j + 1 < len(ts):
                                nxt = ts[j + 1]
                                if len(cur) <= 2 and re.fullmatch(r"[A-ZÇĞİÖŞÜ'’\-]{2,}", nxt):
                                    merged = (cur + nxt).replace(" ", "")
                                    if re.fullmatch(r"[A-ZÇĞİÖŞÜ'’\-]{3,}", merged):
                                        out.append(merged)
                                        j += 2
                                        continue
                            out.append(cur)
                            j += 1
                        return out
                    name_toks = _merge_split_upper(name_toks)
                    # Koşullar: 2-4 token ve en az bir token 4+ harf
                    if 2 <= len(name_toks) <= 4 and any(len(t) >= 4 for t in name_toks):
                        cand = re.sub(r"\s+", " ", " ".join(name_toks)).strip()
                        cand = _strip_trailing_single_lower(cand)
                        if cand and not _is_topic_noise_name(cand):
                            name_key = cand.upper().strip()
                            cur_line = lines[i]
                            tail_line = cur_line[cur_line.find(mid) + len(mid):] if mid in cur_line else cur_line
                            if name_key in assigned_name_to_id and assigned_name_to_id[name_key] != mid:
                                pass
                            elif name_key in tail_line.upper() or name_key not in assigned_name_first_line:
                                enriched.append({"text": cand, "label": "PER_MASKED", "masked_ids": mid_out})
                                used_id_indexes.add(id_order)
                                assigned_name_first_line.setdefault(name_key, i)
                                assigned_name_to_id.setdefault(name_key, mid)
                                matched = True
                except Exception:
                    pass
            if not matched:
                for pi, p in enumerate(persons):
                    if pi in assigned_person_idxs:
                        continue
                    label = (p.get("label") or "").upper()
                    # Yalnızca gerçek kişi etiketleri (PER, PER_MASKED); PER_REGEX vb. gürültüleri atla
                    if label not in ("PER", "PER_MASKED"):
                        continue
                    name = (p.get("text") or "").strip().lower()
                    if not name:
                        continue
                    # Konu/başlık gürültüsü (örn. PAY DEVRİ) kişi değildir
                    if _is_topic_noise_name(p.get("text") or ""):
                        continue
                    # Bariz gürültü: "Aksi Karar ..." kişi değildir
                    if "aksi karar" in name:
                        continue
                    if name in window_text:
                        p2 = dict(p)
                        # Aynı isim farklı masked_id'ye zaten atanmışsa atlama
                        name_key = (p2.get("text") or "").strip().upper()
                        if name_key in assigned_name_to_id and assigned_name_to_id[name_key] != mid:
                            pass
                        else:
                            p2["masked_ids"] = mid
                            enriched.append(p2)
                            assigned_person_idxs.add(pi)
                            used_id_indexes.add(id_order)
                            assigned_name_to_id.setdefault(name_key, mid)
                            matched = True
                            break


        # 2) Geri-düş: atanamayanlar için mesafe tabanlı açgözlü eşleştirme
        #    (kişi ilk göründüğü satır ile kimlik satırı arasındaki mutlak fark)
        remaining_ids = [(j, mid, i) for j, (mid, i) in enumerate(id_positions) if j not in used_id_indexes]
        candidates: List[Tuple[int, int, int, str]] = []  # (dist, id_order, pi, mid)
        for id_order, mid, i in remaining_ids:
            for pi, p in enumerate(persons):
                if pi in assigned_person_idxs:
                    continue
                # Yalnızca gerçek kişi etiketleri
                if (p.get("label") or "").upper() not in ("PER", "PER_MASKED"):
                    continue
                pli = person_first_line_idx.get(pi, -1)
                if pli < 0:
                    continue
                dist = abs(pli - i)
                candidates.append((dist, id_order, pi, mid))
        candidates.sort(key=lambda x: (x[0], x[1]))
        used_id_indexes2: Set[int] = set()
        for dist, id_order, pi, mid in candidates:
            if id_order in used_id_indexes or id_order in used_id_indexes2:
                continue
            if pi in assigned_person_idxs:
                continue
            # Aşırı uzak eşleşmeleri önlemek için eşik (örn. 40 satır)
            if dist > 40:
                continue
            p2 = dict(persons[pi])
            name_key = (p2.get("text") or "").strip().upper()
            if name_key in assigned_name_to_id and assigned_name_to_id[name_key] != mid:
                continue
            p2["masked_ids"] = mid
            enriched.append(p2)
            assigned_person_idxs.add(pi)
            used_id_indexes2.add(id_order)
            assigned_name_to_id.setdefault(name_key, mid)

        # 2b) Küresel ikinci geçiş: '<AD SOYAD> için müşterek ... yetkililer ( ... )' kalıbı
        #     penceresinde maskeli kimlik aynı veya önceki satırlarda olabilir; bu eşleşmeyi kaçırmayalım.
        try:
            glob_pat = re.compile(r"([A-ZÇĞİÖŞÜ$'’\-\s]{3,}?)\s+i[çc]in\s+m[üu][şs]terek(?:en)?\s+oldu\w*\s+yetkili\w*\s*\(", re.IGNORECASE)
            for gm in glob_pat.finditer("\n".join(lines)):
                s_g, e_g = gm.span()
                # Yakın çevrede (±2 satır) maskeli kimlik ara
                # Önce satır indeksi çıkar
                upto = ("\n".join(lines))[:s_g]
                line_idx = upto.count("\n")
                s2 = max(0, line_idx - 2)
                e2 = min(len(lines), line_idx + 3)
                win = "\n".join(lines[s2:e2])
                ids_in_win = list(set(t for t in masked_ids if t and t in win))
                if not ids_in_win:
                    # desen içindeki metinde maske varsa onu al
                    ids_in_win = mask_re.findall(win)
                if not ids_in_win:
                    continue
                cand = gm.group(1)
                cand = re.split(r"[\n;:,]", cand)[0]
                cand = re.split(r"['’][aâeiıioöuüAÂEİIİOÖUÜ]", cand)[0]
                cand = cand.replace("$", "Ş")
                cand = re.sub(r"\s+", " ", cand).strip()
                parts = [p for p in cand.split() if p]
                if len(parts) < 2 or any(len(p) < 2 for p in parts):
                    continue
                for mid in ids_in_win:
                    # Eğer aynı masked_id için başka bir isim atanmışsa ve bu özel desenle bulunan isim farklıysa,
                    # özel desen ("için müşterek ...") daha yüksek önceliğe sahiptir: mevcut kaydı güncelle.
                    replaced = False
                    for e in enriched:
                        if (e.get("masked_ids") or "").strip() == mid:
                            if (e.get("text") or "").strip().upper() != cand.upper():
                                e["text"] = cand
                                e["label"] = "PER_MASKED"
                            replaced = True
                            break
                    if not replaced:
                        name_key = cand.upper().strip()
                        if name_key not in assigned_name_to_id or assigned_name_to_id[name_key] == mid:
                            enriched.append({"text": cand, "label": "PER_MASKED", "masked_ids": mid_out})
                            assigned_name_to_id.setdefault(name_key, mid)
        except Exception:
            pass

        # Kalan kişileri olduğu gibi ekle
        for pi, p in enumerate(persons):
            if pi not in assigned_person_idxs:
                enriched.append(p)

        # Basit fallback: tek maske varsa ve HİÇ eşleşme yapılmadıysa bir PER'e ata
        if len(masked_ids) == 1:
            only_id = masked_ids[0]
            already_assigned = any((e.get("masked_ids") or "").strip() == only_id for e in enriched)
            if not already_assigned:
                for e in enriched:
                    if (e.get("label") or "").upper().startswith("PER") and "masked_ids" not in e:
                        e["masked_ids"] = only_id
                        break
        return enriched
    except Exception:
        return persons

def _clean_persons_for_minimal(items: List[dict]) -> List[dict]:
    """Minimal çıktı için kişi listesini sadeleştirir.
    - Yalnızca 'PER' ve 'PER_MASKED' etiketlerini korur (PER_REGEX vb. gürültüleri eler).
    - Aynı masked_ids değerine sahip kişilerden en uzun ismi tercih ederek tekilleştirir.
    - Aynı isim (text) tekrarlarını `_dedup_persons_pref_masked` mantığıyla temizler.
    """
    if not items:
        return []

    # 1) Etiket filtresi
    filtered = [
        p for p in items
        if ((p.get("label") or "").upper() in ("PER", "PER_MASKED"))
    ]

    # 1.1) Başlık/etiket benzeri sahte kişi kayıtlarını temizle
    def _is_heading_like(p: dict) -> bool:
        label = (p.get("label") or "").upper()
        text = (p.get("text") or "").strip().lower()
        masked = (p.get("masked_ids") or "").strip()
        if label != "PER_MASKED":
            return False
        # Maskeli kimlik atanmamışsa ve metin bilinen başlık kalıplarından biriyse dışla
        if masked:
            return False
        if not text:
            return True
        headings = [
            "yeni atanan",
            "temsilciler",
            "yönetim kurulu",
            "genel kurul",
            "iç yönergesi",
            "ic yönergesi",
            "yetkililer",
        ]
        return any(h in text for h in headings)

    filtered = [p for p in filtered if not _is_heading_like(p)]

    # 1.2) Kısmi/fragman kişi girdilerini temizle (örn. "KAYHAN TEKBAŞ'in önceki")
    def _is_partial_fragment(p: dict) -> bool:
        txt = (p.get("text") or "").strip()
        if not txt:
            return False
        # Güvenli tarafta kalmak için sadece maskeli kimlik atanMAmış olanlarda uygula
        if (p.get("masked_ids") or "").strip():
            return False
        low = txt.lower()
        # Yaygın tek tırnak varyantları: ' ve ’
        # Örnek hedef: "...'in önceki"
        if re.search(r"['’][iıiuü]n\s+önceki\b", low):
            return True
        # Cümle ortasında kesilmiş gibi duran son ekli parçalı adlar (sonda 'in/'ın/'un/'ün)
        if re.search(r"['’][iıiuü]n\s*$", low):
            return True
        return False

    filtered = [p for p in filtered if not _is_partial_fragment(p)]

    # 1.3) Gürültü ifadeleri: kişi olmayan metinleri ele (ör. "Aksi Karar Alıncaya")
    def _is_noise_person(p: dict) -> bool:
        txt = (p.get("text") or "").strip().lower()
        if not txt:
            return False
        # Yaygın gürültüler (kişi olmayan kalıplar)
        noise_patterns = [
            r"\baksi\s+karar\b",
            r"\bm[üu]sterek\b",
            r"listesinde\b",
            r"\bpay\s+devr[iı]\b",
            r"\bm[üu]d[üu]rler\b",
            r"\byetk[iı]liler\b",
            r"deg[iı]si[kğ]lik\b|değişiklik\b",
            r"temsil\s+yetkisinin\b",
            r"yetki\s+sekli\b|yetki\s+şekli\b",
            r"g[oö]rev\s+da[gğ]il[ıi]m[ıi]\b",
            # Adres/ikamet ve uyruk bağlamı kişi değildir
            r"\badresinde(ki)?\b",
            r"\bikamet\b",
            r"\buyruklu\b",
        ]
        if any(re.search(pat, txt) for pat in noise_patterns):
            return True
        return False

    filtered = [p for p in filtered if not _is_noise_person(p)]

    if not filtered:
        return []

    # 1.4) İsim metnini normalize et: görev/rol eklerini ve sondaki iyelik eklerini temizle
    #      Örn: "UFUK SOYLUOGLU Yönetim Kurulu Üyesi olarak" -> "UFUK SOYLUOGLU"
    #           "AHMET NURI ÖZ'in" -> "AHMET NURI ÖZ"
    def _normalize_person_text(name: str) -> str:
        if not name:
            return name
        s = name.strip()
        # 'olarak' ile başlayan rol ifadelerini at
        s = re.sub(r"\s+olarak.*$", "", s, flags=re.IGNORECASE)
        # Yaygın rol/görev kalıplarını sonundan buda (yönetim kurulu ..., müdür, tasfiye memuru vb.)
        s = re.sub(r"\b(yönetim\s+kurulu\s+[\wçğıöşü\s]*|müdür(?:ü)?|tasfiye\s+memuru|temsil\s+ve\s+ilzam[\w\s]*)\b.*$", "", s, flags=re.IGNORECASE)
        # 1) İyelikten sonra gelebilen üyelik ifadelerini (OCR varyantları dahil) önce buda
        #    Örn: "SERHAT ÇELIK'in önceki üyeligi" -> (üyelik atılır) -> "SERHAT ÇELIK'in"
        name2 = re.sub(r"\b(?:önceki\s+)?üyel\w*\b.*$", "", s, flags=re.IGNORECASE)
        # 2) Son durumda sondaki apostrof+iyelik ekini temizle (apostrof sonrası boşluk toleranslı)
        #    Üyelik kaldırıldıktan sonra trailing hale gelen "'in/'ın/'un/'ün" budanır
        name2 = re.sub(r"\s*['’]\s*[iıiuü]n\s*$", "", name2, flags=re.IGNORECASE)
        # 2b) Genel durum: isimden sonra gelen apostrof+iyelik ve devamını tamamen kes
        #     Örn: "ABDÜL BATUR 'in bu ..." -> "ABDÜL BATUR"
        name2 = re.sub(r"\s*['’]\s*[iıiuü]n\b.*$", "", name2, flags=re.IGNORECASE)
        # 2c) Sonda idari/fiil kalıpları ve devamını kes (OCR varyantlarıyla)
        name2 = re.sub(r"\b(belirlenmi[sş]tir|se[cç]ilmi[sş]tir|atanmi[sş]t[ıi]r|sona\s+ermi[sş]tir|sona\s+erdirilm[iı][sş]tir)\b.*$", "", name2, flags=re.IGNORECASE)
        # Baştaki yaygın kısaltma/ünvan gürültülerini temizle (T.C., TC, T C, T.A., TA, SN., SAYIN, BAY, BAYAN)
        # Not: sadece başta ayrı bir kelime olarak geçtiğinde temizle (ör. "TA SELIN" -> "SELIN")
        noise_prefix = re.compile(
            r"^(?:\s*(?:T\s*\.?\s*C|T\s*\.?\s*A|T\.?|C\.?|TC|TA|T\s*C|T\s*A|SN\.?|SAYIN|BAYAN|BAY)\.?\s+)+",
            re.IGNORECASE,
        )
        name2 = re.sub(noise_prefix, "", name2).strip()
        # Birden çok boşluğu sadeleştir
        name2 = re.sub(r"\s+", " ", name2).strip()
        # Parçalı büyük harfli soyadı birleştirme (BA YRAM -> BAYRAM)
        toks = [t for t in name2.split() if t]
        if toks and all(re.fullmatch(r"[A-ZÇĞİÖŞÜ'’\-]{1,}", t) for t in toks):
            out = []
            j = 0
            while j < len(toks):
                cur = toks[j]
                if j + 1 < len(toks):
                    nxt = toks[j + 1]
                    if len(cur) <= 2 and re.fullmatch(r"[A-ZÇĞİÖŞÜ'’\-]{2,}", nxt):
                        merged = (cur + nxt).replace(" ", "")
                        if re.fullmatch(r"[A-ZÇĞİÖŞÜ'’\-]{3,}", merged):
                            out.append(merged)
                            j += 2
                            continue
                out.append(cur)
                j += 1
            name2 = " ".join(out)
        return name2

    for p in filtered:
        if isinstance(p.get("text"), str) and p.get("text"):
            p["text"] = _normalize_person_text(p["text"]) or p["text"]

    # 1.5) Basit isim sezgisi: en az iki kelime (her biri >=2 harf)
    def _looks_like_name(name: str) -> bool:
        if not isinstance(name, str):
            return False
        parts = [t for t in (name or "").strip().split() if t]
        if len(parts) < 2:
            return False
        if any(len(t) < 2 for t in parts[:2]):
            return False
        return True

    filtered = [p for p in filtered if _looks_like_name(p.get("text"))]

    # 2) masked_ids'e göre en uzun isimli kişiyi koru
    by_mid: Dict[str, dict] = {}
    for p in filtered:
        mid = (p.get("masked_ids") or "").strip()
        if not mid:
            # masked id yoksa doğrudan eklemek üzere işaretle (mid key olarak '')
            mid = ""
        cur = by_mid.get(mid)
        if cur is None:
            by_mid[mid] = p
            continue
        # Mevcut ve aday arasında seçim:
        # - PER_MASKED mutlak öncelik: mevcut PER_MASKED ise koru; aday PER_MASKED ise değiştir.
        # - Etiketler aynıysa daha uzun metni tercih et.
        cur_label = (cur.get("label") or "").upper()
        p_label = (p.get("label") or "").upper()
        if p_label == "PER_MASKED" and cur_label != "PER_MASKED":
            by_mid[mid] = p
            continue
        if cur_label == "PER_MASKED" and p_label != "PER_MASKED":
            # Mevcut PER_MASKED korunur
            continue
        cur_len = len((cur.get("text") or "").strip())
        p_len = len((p.get("text") or "").strip())
        if p_len > cur_len:
            by_mid[mid] = p

    # 3) Aynı isim tekrarlarını TEMİZLEME: aynı isim için birden çok kayıt varsa
    #    - masked_ids'i olanı tercih et (PER_MASKED lehine)
    #    - eşitlik halinde daha uzun metni koru
    name_best: Dict[str, dict] = {}
    for p in by_mid.values():
        key = (p.get("text") or "").strip().upper()
        if not key:
            continue
        cur = name_best.get(key)
        if cur is None:
            name_best[key] = p
            continue
        # mevcut en iyi ile aday arasında seçim
        cur_has_mid = bool((cur.get("masked_ids") or "").strip())
        p_has_mid = bool((p.get("masked_ids") or "").strip())
        if p_has_mid and not cur_has_mid:
            name_best[key] = p
            continue
        if cur_has_mid and not p_has_mid:
            continue
        # her ikisi de aynıysa etiket önceliği (PER_MASKED) ve uzunluk
        cur_label = (cur.get("label") or "").upper()
        p_label = (p.get("label") or "").upper()
        if p_label == "PER_MASKED" and cur_label != "PER_MASKED":
            name_best[key] = p
            continue
        if cur_label == "PER_MASKED" and p_label != "PER_MASKED":
            continue
        if len((p.get("text") or "").strip()) > len((cur.get("text") or "").strip()):
            name_best[key] = p
    deduped = list(name_best.values())

    # 4) YALNIZCA masked_ids'i olan kişileri döndür
    deduped = [p for p in deduped if (p.get("masked_ids") or "").strip()]

    return deduped

def _dehyphenate_lines(s: str) -> str:
    """
    Satır sonunda tire ("-", "‐", "‑", "‒", "–", "—") ile kırılmış
    kelimeleri birleştirir ve kalan satır sonlarını boşlukla değiştirir.
    Girdi metninin orijinalini bozmadan, çıktı için okunabilir tek satır üretir.
    """
    if not s:
        return s
    text = s.replace("\r\n", "\n").replace("\r", "\n")
    # Tire ile kesilen kelimeleri satır sonu üzerinden birleştir
    text = re.sub(r"(?<=\w)[\-‐‑‒–—]\s*\n\s*(?=\w)", "", text)
    # Kalan satır sonlarını boşlukla değiştir ve boşlukları sıkılaştır
    text = re.sub(r"\s*\n\s*", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def extract_address_block_segment(raw_text: str) -> Optional[str]:
    """
    Orijinal ilân metni üzerinde, "Adres:" ile başlayıp "Yukarıdaki Bilgiler"
    (ve benzeri ifadeler) öncesine kadar olan adres bloğunu bulur ve aynen döndürür.

    Dönüş:
      - Bulunursa adres bloğu (orijinal biçimlendirme ile)
      - Bulunamazsa None
    """
    if not raw_text:
        return None

    # Başlangıç işareti: satır başında "Adres:" veya "Ticari Adres:" etiketi (kelime sınırı + zorunlu iki nokta)
    # Not: "adresinde" gibi kelimeleri yanlış eşleştirmemek için \b ve zorunlu ':' kullanıyoruz
    start_re = re.compile(r"^\s*(?:Ticari\s*)?Adres\b\s*[:：]\s*", re.MULTILINE | re.IGNORECASE)
    m_start = start_re.search(raw_text)
    if not m_start:
        return None
    start = m_start.end()

    # Bitiş işaretleri: "Yukarıdaki Bilgiler" ve OCR/ifade varyasyonları
    end_patterns = [
        r"^\s*Yukar[ıi]dak[ıi]\s+Bilgiler(?:\.|:)?\s*$",
        r"^\s*Yukar[ıi]da\s+(?:yaz[ıi]l[ıi]|belirt[ıi]len)\s+bilgiler(?:i|e|e\s*göre)?(?:\.|:)?\s*$",
        # OCR varyantları: Yukanda/Yukanida bilgileri verilen .../yazılı .../belirtilen ...
        r"^\s*Yu(?:ka(?:r|rn|n)?[ıi]?)\s+bilgile?ri\s+(?:verilen|yaz[ıi]l[ıi]|belirt[ıi]len)\b.*$",
        # Adres bloğundan sonra sık görülen başlık/durdurucu satırlar
        r"^\s*Vergi\s*Dairesi\s*[:：]",
        r"^\s*Sermaye\b",
        r"^\s*Tasfiyeden\s+Dolay[ıi].*Alacak",
        r"bir\s+veya\s+birka[çc]\s+m[üu]d[üu]r",
        r"Aksi\s+Karar\s+Al[ıi]n[ıi]ncaya",
        r"Kimlik\s+No",
        r"T[üu]rkiye\s+Cumhuriyeti\s+Uyruklu",
    ]
    end_re = re.compile("|".join(end_patterns), re.IGNORECASE | re.MULTILINE)
    m_end = end_re.search(raw_text, start)
    if not m_end:
        # Genel durdurucu satırlara geri düş (Yukarıda OCR varyantları dahil)
        stop_re = re.compile(r"^\s*(?:Yu(?:ka(?:r|rn|n)?[ıi]?da)|Yukarıda|Yukarida|Tescil|Tescile|MERS[İI]S|Ticaret\s*Sicil|Telefon|Tel|GSM|Faks|İlan\s*Sira\s*No|Ilan\s*Sira\s*No|Sira\s*No|Madde\b|.*GAZETE\S*|SAYI\s*:|Merkezin\s+Kay\w*\s+Oldu\w*\s+M[üu]d[üu]rl[üu](?:g[üu]|k)[’']?\s*:?|Vergi\s*Dairesi\s*:|Sermaye\b|Tasfiyeden\s+Dolay[ıi].*Alacak|bir\s+veya\s+birka[çc]\s+m[üu]d[üu]r|Aksi\s+Karar|Kimlik\s+No|T[üu]rkiye\s+Cumhuriyeti)", re.IGNORECASE | re.MULTILINE)
        m_end = stop_re.search(raw_text, start)
    end = m_end.start() if m_end else len(raw_text)

    block = raw_text[start:end].strip()
    return block if block else None

def extract_trade_name_block_segment(raw_text: str) -> Optional[str]:
    """
    Orijinal ilân metni üzerinde, "(Yeni) Ticaret Unvanı"/"Unvanı" başlığından
    başlayıp ilk "Adres:" (veya adres başlığı varyantları) satırına kadar olan bloğu
    aynen döndürür. Böylece aynı alanda yer alan birden fazla başlık (örn. Eski Unvanı)
    birlikte yakalanır.

    Dönüş:
      - Bulunursa unvan bloğu (orijinal biçimlendirme ile)
      - Bulunamazsa None
    """
    if not raw_text:
        return None

    # Başlangıç: satır başında (Yeni)? (Ticaret)? Unvan(ı)
    # OCR toleransı: 'Unvan' içinde 'n/m' karışıklığı (Unvam) ve ı/i/I/İ varyantları
    start_pat = re.compile(
        r"^\s*(?:Yeni\s*)?(?:Ticaret\s*)?Unva[nm](?:[ıiİI])?(?:t)?\s*[:：]?.*$",
        re.IGNORECASE | re.MULTILINE,
    )
    m_start = start_pat.search(raw_text)
    if not m_start:
        # Alternatif: yalın "Unvan(ı)" başlığı
        alt_start = re.compile(r"^\s*Unva[nm](?:[ıiİI])?(?:t)?\s*[:：]?.*$", re.IGNORECASE | re.MULTILINE)
        m_start = alt_start.search(raw_text)
        if not m_start:
            return None

    start = m_start.start()

    # Bitiş: ilk adres başlığı (Adres/Eski Adres/Yeni Adres/Merkezi vs.)
    addr_labels = [
        r"Adres",
        r"Eski\s*Adres",
        r"Yeni\s*Adres",
        r"Merkez(?:i)?",
        r"Şube\s*Adresi",
        r"İkametg[aâ]h\s*Adresi",
        r"Şirket\s*Merkezi",
        r"İşletmenin\s*Merkezi",
    ]
    # Adres başlığı: iki nokta zorunlu olmasın (OCR'de düşebilir)
    end_addr_re = re.compile(rf"^\s*(?:{'|'.join(addr_labels)})\b(?:\s*[:：])?", re.IGNORECASE | re.MULTILINE)
    m_end = end_addr_re.search(raw_text, start)
    if not m_end:
        # Genel durduruculara düş: Adres başlığı yoksa aşırı kapsama olmasın
        stop_re = re.compile(
            r"^\s*(?:Yu(?:ka(?:r|rn|n)?[ıi]?da)|Yukarıda|Yukarida|Tescil|Tescile|MERS[İI]S|Ticaret\s*Sicil|Telefon|Tel|GSM|Faks|İlan\s*Sira\s*No|Ilan\s*Sira\s*No|Sira\s*No|Madde\b)",
            re.IGNORECASE | re.MULTILINE,
        )
        m_end = stop_re.search(raw_text, start)
    end = m_end.start() if m_end else len(raw_text)

    block = raw_text[start:end].strip()
    return block if block else None

def load_spacy_model():
    """
    Loads the spaCy model, downloading it if it's not already installed.
    Returns the loaded nlp object.
    """
    global nlp_model
    if nlp_model is not None:
        return nlp_model

    # Eğer HF NER kullanılacaksa, spaCy modelini indirmeye/kurmaya çalışmayalım
    use_hf = os.getenv("USE_HF_NER", "1").strip() in ("1", "true", "True")
    if use_hf:
        logger.info("USE_HF_NER etkin; spaCy modeli yerine blank('tr') kullanılacak.")
        nlp_model = spacy.blank("tr")
        return nlp_model

    # Yüklü olan modelleri sırayla dene; indirme girişimi yok
    candidates = ["tr_core_news_sm", "xx_ent_wiki_sm"]

    for model_name in candidates:
        if not is_package(model_name):
            logger.info(f"spaCy model '{model_name}' yüklü değil; atlanıyor.")
            continue

        # Try loading
        try:
            loaded = spacy.load(model_name)
            logger.info(f"spaCy model '{model_name}' loaded successfully.")
            nlp_model = loaded
            return nlp_model
        except Exception as e:
            logger.warning(f"Failed to load model '{model_name}': {e}. Will try next option.")
            continue

    # Final fallback: blank Turkish pipeline (no NER, but regex rules will still work)
    logger.warning(
        "Falling back to spaCy blank('tr') pipeline. NER will be unavailable; regex-based fields will still be extracted."
    )
    nlp_model = spacy.blank("tr")
    return nlp_model

# Load the model on startup
nlp_model = load_spacy_model()

def load_hf_ner():
    """
    USE_HF_NER=1 ise Hugging Face NER pipeline'ını yükler, aksi durumda None döner.
    transformers yoksa veya model yüklenemezse güvenli şekilde None döner.
    """
    global hf_ner
    if hf_ner is not None:
        return hf_ner

    use_hf = os.getenv("USE_HF_NER", "1").strip() in ("1", "true", "True")
    if not use_hf:
        return None

    if hf_pipeline is None:
        logger.warning("transformers bulunamadı; HF NER devre dışı.")
        return None

    # Model kimliğini ortam değişkeninden oku; yoksa makul bir varsayılan dene
    candidates: List[str] = []
    env_model = os.getenv("HF_NER_MODEL", "").strip()
    if env_model:
        candidates.append(env_model)
    # Yaygın ve bakımlı bir Türkçe NER modeli
    candidates.append("savasy/bert-base-turkish-ner-cased")

    # CPU kullanımını zorla (device=-1) ve birden fazla adayı sırayla dene
    t_total = time.perf_counter()
    for model_id in candidates:
        try:
            logger.info("HF NER modeli yükleniyor: %s", model_id)
            t0 = time.perf_counter()
            ner = hf_pipeline(
                "token-classification",
                model=model_id,
                aggregation_strategy="simple",
                framework="pt",
                device=-1,
            )
            elapsed = time.perf_counter() - t0
            logger.info("HF NER '%s' yüklendi (%.2fs).", model_id, elapsed)
            hf_ner = ner
            return hf_ner
        except Exception as e:
            elapsed = time.perf_counter() - t0 if 't0' in locals() else 0.0
            logger.warning("HF NER modeli '%s' yüklenemedi (%.2fs): %s", model_id, elapsed, e)

    t_elapsed = time.perf_counter() - t_total
    logger.warning("HF NER modelleri yüklenemedi (toplam %.2fs); SpaCy/regex ile devam edilecek.", t_elapsed)
    return None


# --- Aksiyon ve Anahtar Kelime Tabanlı Ek Çıkarım Yardımcıları ---
def extract_money_spans(text: str) -> List[str]:
    """Metinden TL tutarlarını yakalar (ör. 2.775.000,00 TL)."""
    amts = re.findall(r"\b\d{1,3}(?:\.\d{3})*(?:,\d{2})?\s*(?:TL|Türk Lirasi|Türk Lirası)\b", text, flags=re.IGNORECASE)
    # Benzersiz sırayı koru
    out: List[str] = []
    seen: Set[str] = set()
    for a in amts:
        k = a.strip()
        kl = k.lower()
        if kl not in seen:
            seen.add(kl)
            out.append(k)
    return out

def extract_persons_from_keywords(text: str) -> List[dict]:
    """
    'Kimlik Numaralı <AD SOYAD>' kalıplarından kişi çıkarımı yapar.
    HF NER'i tamamlayıcı amaçlıdır.
    """
    # OCR normalizasyonu: birleşik aksanları birleştir ve I-acute varyantlarını düzelt
    text = unicodedata.normalize('NFC', text)
    text = text.replace("Í", "İ").replace("Í", "İ").replace("Ì", "İ")
    persons: List[dict] = []
    assigned_by_name: Dict[str, str] = {}
    used_ids: Set[str] = set()
    used_ids: Set[str] = set()
    used_ids: Set[str] = set()
    # Kural 3: Aynı masked_id için yalnızca ilk kişi alınmalı
    used_ids: Set[str] = set()
    assigned_by_name: Dict[str, str] = {}
    # Aynı ismin birden fazla maskeye bağlanmasını engelle
    assigned_by_name: Dict[str, str] = {}
    # İsim kalıbı (2-4 kelime), satır atlamasın diye sadece boşluk/tabne izin ver
    name_pat = r"([A-ZÇĞİÖŞÜ'][A-ZÇĞİÖŞÜ']+(?:[ \t]+[A-ZÇĞİÖŞÜ'][A-ZÇĞİÖŞÜ']+){1,3})"

    STOP_TOKENS = {
        "BILGILER", "BİLGİLER", "BILGILERI", "MADDE", "SERMAYE", "MERKEZI", "MERKEZ",
        "SIRKET", "SIRKETIN", "SIRKETI", "UNVAN", "UNVANI", "ISLETME", "HUSUSLAR",
        "ADRES", "KONUSU", "SAHIBI", "SAHIBINE", "TEMSiLCiLERINE", "TEMSILCILERINE",
        "GOREV", "YERLESIM", "VATANDASLIGI", "KAPSAMI", "YONETIM", "KURULU",
        "LERINE", "AIT", "AİT",
        # Ek başlık/alan gürültüleri
        "UYRUK", "TURKIYE", "CUMHURIYETI", "CUMHURIYET", "TC",
        "KIMLIK", "KIMLIK NO", "NO", "MERSIS", "MERSIS NO",
        # Gelişmiş gürültüler
        "İDARESİ", "İDARE", "TEKİRDAĞ", "TEKIRDAG", "ÇERKEZKÖY", "CERKEZKOY", "BAHÇELİEVLER", 
        "BAHÇELİ", "BAHCE", "BAHCE LIEVLER", "ÜSKÜDAR", "USKUDAR", "GÜNGÖREN", "GUNGOREN", 
        "EYÜPSULTAN", "EYUPSULLAN", "ESENYURT", "STANBUL", "ISTANBULT", "YOLU", "SOKAĞI", "SK", 
        "CAD", "KAPI", "MAHALLESİ", "MAH", "RESMİ", "ILAN", "PORTALI", "BASIN", "KURUMU", 
        "İLAN.GOV.TR", "KADIKOY", "ŞİŞL", "ŞİŞLİ", "İÇERİĞİ", "DEĞİŞEN", "MADDELERİN", "HALİ", 
        "AMAÇ", "KONU", "EĞİTİM", "DANIŞMANLIK", "REKLAM", "ORGANİZASYON", "ORGANİZAS", "MÜZİK", 
        "SİGORTA", "GENEL", "KURUL", "TASFİYE", "MADDESİ", "TÜRKİYE", "URKIYH", "CUMHUKITE", "SAYFA", "GAZETESİ",
        # ASCII ve OCR varyantları
        "GAZETESI", "SICILI", "TICARET", "TURKIYE", "MUDURLUGU", "MUDUR", "MUDURLER", "SECILENLER", 
        "UDURLUGE", "MUDURLUGE", "SEÇİLENLER", "SECILENLER", "TICARETI", "TİCARETİ", "LIMITED", "LİMİTED", 
        "SIRKETI", "ŞİRKETİ", "ANONIM", "ANONİM", "INSAAT", "İNŞAAT", "SANAYI", "SANAYİ", "PAZARLAMA", 
        "ITHALAT", "IHRACAT", "TURIZM", "TURİZM", "YETKILILER", "YETKİLİLER", "BİLGİLER", "SECILEN",
        "DEĞİŞİKLİK", "DEĞİŞİKLİĞİ", "GÖREV", "GOREV", "DAĞILIMINDAKİ", "DAGILIMINDAKI", "ORTAKLIK", 
        "BİLGİSİ", "BİLGİ", "BİLGİLERİ", "BİLGİLER", "TEK"
    }

    def is_probable_person_name(nm: str) -> bool:
        if "\n" in nm or "\r" in nm:
            return False
        toks = [t for t in re.split(r"\s+", nm) if t]
        if not (2 <= len(toks) <= 4):
            return False
        vowels = set("AEIİOÖUÜaeıioöuü")
        for t in toks:
            # stop token filtresi ve min/max uzunluk
            if t.upper() in STOP_TOKENS:
                return False
            if not (2 <= len(t) <= 20):
                return False
            if len(set(t) & vowels) == 0:
                return False
        return True

    # 1) "Kimlik Numaralı <AD SOYAD>"
    for m in re.finditer(rf"Kimlik[ \t]*Numara(?:l[ıi])?[ \t]*{name_pat}", text, flags=re.IGNORECASE):
        nm = m.group(1).strip()
        if nm and is_probable_person_name(nm):
            persons.append({"text": nm, "label": "PER_REGEX"})

    # 1b) Müsterek/müştereken kalıpları: "... (AD SOYAD) ile birlikte müştereken ..."
    # Parantez içindeki isim(ler)i yakala. Birden fazla isim virgül/ve ile ayrılabilir.
    try:
        must_pat = re.compile(r"m[üu]stere?k(?:en)?", re.IGNORECASE)
        paren_names = re.finditer(r"\(([^)]+)\)", text)
        for pm in paren_names:
            inner = pm.group(1) or ""
            if not inner or len(inner) < 3:
                continue
            # Yakın çevrede müsterek kelimesi var mı? (±120 karakter)
            s, e = pm.span()
            context = text[max(0, s-120): min(len(text), e+120)]
            if not must_pat.search(context):
                continue
            # İçerideki isimleri ayır
            # Örn: "AHMET YILMAZ, MEHMET DEMIR" veya "AHMET YILMAZ ve MEHMET DEMIR"
            cand_parts = re.split(r"\s*(?:,|\s+ve\s+)\s*", inner)
            for cand in cand_parts:
                cand = cand.strip()
                # Büyük harf ağırlıklı kişi adı filtresi
                if not cand or len(cand) < 3:
                    continue
                # Harf setini sınırlı tut, sayıları ayıkla
                cand2 = re.sub(r"[^A-ZÇĞİÖŞÜ'’\-\s]", " ", cand)
                cand2 = re.sub(r"\s+", " ", cand2).strip()
                if is_probable_person_name(cand2):
                    persons.append({"text": cand2, "label": "PER_REGEX"})
    except Exception:
        pass

    # 2) "<AD SOYAD> 'e devretmiştir"
    for m in re.finditer(rf"{name_pat}[ \t]*'?e[ \t]+devretmi[sş]tir", text, flags=re.IGNORECASE):
        nm = m.group(1).strip()
        if nm and is_probable_person_name(nm):
            persons.append({"text": nm, "label": "PER_REGEX"})

    # 3) "ikamet eden <AD SOYAD>"
    for m in re.finditer(rf"ikamet[ \t]+eden[ \t]+{name_pat}", text, flags=re.IGNORECASE):
        nm = m.group(1).strip()
        if nm and is_probable_person_name(nm):
            persons.append({"text": nm, "label": "PER_REGEX"})

    # 4) "adına hareket (eden) <AD SOYAD>" veya "<AD SOYAD> adına hareket"
    for m in re.finditer(rf"ad[ıi]na[ \t]+hareket(?:[ \t]+eden)?[ \t]+{name_pat}", text, flags=re.IGNORECASE):
        nm = m.group(1).strip()
        if nm and is_probable_person_name(nm):
            persons.append({"text": nm, "label": "PER_REGEX"})
    for m in re.finditer(rf"{name_pat}[ \t]+ad[ıi]na[ \t]+hareket", text, flags=re.IGNORECASE):
        nm = m.group(1).strip()
        if nm and is_probable_person_name(nm):
            persons.append({"text": nm, "label": "PER_REGEX"})

    # 4b) "Adi ve Soyadi : <AD SOYAD>" / "Adı Soyadı : <AD SOYAD>" / "Adi Soyadi : <AD SOYAD>"
    for m in re.finditer(rf"^\s*Ad[ıi](?:\s*ve\s*Soyad[ıi]|\s*Soyad[ıi])\s*[:：]\s*{name_pat}\s*$", text, flags=re.IGNORECASE | re.MULTILINE):
        nm = m.group(1).strip()
        if nm and is_probable_person_name(nm):
            persons.append({"text": nm, "label": "PER_REGEX"})

    # 5) Temsil/Yetki/YK rolleri çevresinde isim
    role_keys = [
        r"\bY[öo]netim\s+Kurulu(?:\s+Üyesi)?\b",
        r"\bGenel\s+M[üu]d[üu]r\b",
        r"\bM[üu]d[üu]r\b",  # 'Müdür olarak' vb. durumlar için düz Müdür
        r"\bYetkili(?:si)?\b",
        r"\bTemsilci(?:si)?\b",
        r"\bMurahhas\b",
        r"\bY[öo]netim\s+Kurulu\s+Ba[sş]kan[ıi]\b",
    ]
    role_re = re.compile(r"(?:" + "|".join(role_keys) + r")", re.IGNORECASE)
    # Rol + isim
    for m in re.finditer(rf"(?:{role_re.pattern})[ \t]*[:\-]?[ \t]*{name_pat}", text, flags=re.IGNORECASE):
        nm = m.group(m.lastindex).strip() if m.lastindex else None
        if not nm:
            # fallback: son grup name_pat
            nm = re.search(name_pat, m.group(0))
            nm = nm.group(1).strip() if nm else None
        if nm and is_probable_person_name(nm):
            persons.append({"text": nm, "label": "PER_REGEX"})
    # İsim + rol
    for m in re.finditer(rf"{name_pat}[^\n]{0,30}(?:{role_re.pattern})", text, flags=re.IGNORECASE):
        nm = m.group(1).strip()
        if nm and is_probable_person_name(nm):
            persons.append({"text": nm, "label": "PER_REGEX"})

    # Dedup
    return _dedup_entity_dicts(persons)

def extract_persons_near_masked_ids(text: str) -> List[dict]:
    """
    Maskeli kimlik (örn. 1***34, 179******34) içeren satırların yakınından kişi ismi çıkarır.
    Kurallar:
      - Aynı satırda: "(T.C.) Kimlik Numaralı <AD SOYAD>" veya satır sonunda yalın isim
      - Takip eden 1-3 satır: "ikamet eden <AD SOYAD>" veya yalın isim satırı
    Gürültü azaltmak için adres benzeri satırlar ve sayılı içerikler elenir.
    """
    persons: List[dict] = []
    assigned_by_name: Dict[str, str] = {}
    used_ids: Set[str] = set()

    # İsim kalıbı (2-4 kelime), büyük harf yoğunluklu
    name_pat = r"([A-ZÇĞİÖŞÜ'][A-ZÇĞİÖŞÜ']+(?:[ \t]+[A-ZÇĞİÖŞÜ'][A-ZÇĞİÖŞÜ']+){1,3})"

    STOP_TOKENS = {
        "BILGILER", "BİLGİLER", "BILGILERI", "MADDE", "SERMAYE", "MERKEZI", "MERKEZ",
        "SIRKET", "SIRKETIN", "SIRKETI", "UNVAN", "UNVANI", "ISLETME", "HUSUSLAR",
        "ADRES", "KONUSU", "SAHIBI", "SAHIBINE", "TEMSiLCiLERINE", "TEMSILCILERINE",
        "GOREV", "YERLESIM", "VATANDASLIGI", "KAPSAMI", "YONETIM", "KURULU",
        "LERINE", "AIT", "AİT",
        # Ek gürültü/bağlam sözcükleri
        "TURKIYE", "TÜRKİYE", "UYRUK", "UYRUKLU",
        # Eklenen bağlam kelimeleri
        "ISLETMENIN", "İSLETMENİN", "DENETCILER", "DENETÇİLER",
        # Adres/ikamet bağlam kelimeleri
        "ADRESINDE", "ADRESİNDE", "ADRESINDEKI", "ADRESİNDEKİ", "IKAMET", "IKAMETEN",
        # Başlık/paragraf sızıntılarını kesmek için
        "ICERIGI", "DEGISEN", "MADDELERIN", "YENI", "HALI",
        # Firma/unvan tipik kelimeleri (kişiyi elemek için)
        "SANAYI", "SANAYİ", "TICARET", "TİCARET", "LIMITED", "LİMİTED", "LTD", "ŞTİ", "SIRKET", "ŞİRKET",
        "ANONIM", "ANONİM", "AŞ", "A.Ş", "A.Ş.", "OTOMOTIV", "OTOMOTİV", "GIDA", "INSAAT", "İNŞAAT",
        "TURIZM", "TURİZM", "YAPI", "TEKSTIL", "TEKSTİL", "BANK", "BANKASI", "PAZARLAMA", "DIŞ", "DIS",
        # İşlem/idarî kelimeler
        "TESCIL", "TESCİL", "TARIHINDEN", "ITIBAREN", "ATANMISTIR", "ATANMIŞTIR", "MEMURU", "TASFIYE", "TASFİYE",
        # Gelişmiş gürültüler
        "İDARESİ", "İDARE", "TEKİRDAĞ", "TEKIRDAG", "ÇERKEZKÖY", "CERKEZKOY", "BAHÇELİEVLER", 
        "BAHÇELİ", "BAHCE", "BAHCE LIEVLER", "ÜSKÜDAR", "USKUDAR", "GÜNGÖREN", "GUNGOREN", 
        "EYÜPSULTAN", "EYUPSULLAN", "ESENYURT", "STANBUL", "ISTANBULT", "YOLU", "SOKAĞI", "SK", 
        "CAD", "KAPI", "MAHALLESİ", "MAH", "RESMİ", "ILAN", "PORTALI", "BASIN", "KURUMU", 
        "İLAN.GOV.TR", "KADIKOY", "ŞİŞL", "ŞİŞLİ", "İÇERİĞİ", "DEĞİŞEN", "MADDELERİN", "HALİ", 
        "AMAÇ", "KONU", "EĞİTİM", "DANIŞMANLIK", "REKLAM", "ORGANİZASYON", "ORGANİZAS", "MÜZİK", 
        "SİGORTA", "GENEL", "KURUL", "TASFİYE", "MADDESİ", "TÜRKİYE", "URKIYH", "CUMHUKITE", "SAYFA", "GAZETESİ",
        "CUMHURİYET", "CUMHURİYETİ", "CUMHUR", "EYUPSULLAN", "ISTANBULT",
        # ASCII ve OCR varyantları
        "GAZETESI", "SICILI", "TICARET", "TURKIYE", "MUDURLUGU", "MUDUR", "MUDURLER", "SECILENLER", 
        "UDURLUGE", "MUDURLUGE", "SEÇİLENLER", "SECILENLER", "TICARETI", "TİCARETİ", "LIMITED", "LİMİTED", 
        "SIRKETI", "ŞİRKETİ", "ANONIM", "ANONİM", "INSAAT", "İNŞAAT", "SANAYI", "SANAYİ", "PAZARLAMA", 
        "ITHALAT", "IHRACAT", "TURIZM", "TURİZM", "YETKILILER", "YETKİLİLER", "BİLGİLER", "SECILEN",
        "DEĞİŞİKLİK", "DEĞİŞİKLİĞİ", "GÖREV", "GOREV", "DAĞILIMINDAKİ", "DAGILIMINDAKI", "ORTAKLIK", 
        "BİLGİSİ", "BİLGİ", "BİLGİLERİ", "BİLGİLER", "TEK"
        # Bölüm başlıkları/bağlam sözcükleri (isim gövdesine sızmasın)
        "KISIYE", "KİŞİYE",
    }

    def _clean_person_name(nm: str) -> str:
        # Uçtaki ekler ve noktalama: "ACAR'e", "ACAR’a", son tek tırnak, nokta/virgül
        nm = re.sub(r"[’'](?:[eEaAiİI])$", "", nm.strip())
        nm = re.sub(r"[’']+$", "", nm)
        nm = re.sub(r"[,.;:]+$", "", nm)
        # İsimden sonra gelen "'e", "'a" ve devamını tamamen kes (örn. "YILDIRIM'e devretmistir")
        nm = re.sub(r"[’']\s*[eEaAiİI]\b.*$", "", nm, flags=re.IGNORECASE).strip()
        # Başta yanlışlıkla kalan kalıp sözcükleri temizle (Numaralı, Kimlik Numaralı)
        nm = re.sub(r"^(?:Numaral[ıi]|Kimlik\s*Numara(?:l[ıi])?)\s+", "", nm, flags=re.IGNORECASE)
        # Sonda rol/bağlaç kırpması: 'Müdür (olarak)', '... olarak' vb.
        nm = re.sub(r"\bM[üu]d[üu]r\b(?:\s+olarak)?\.?$", "", nm, flags=re.IGNORECASE).strip()
        nm = re.sub(r"\bolarak\b\.?$", "", nm, flags=re.IGNORECASE).strip()
        # Sonda rol/pozisyon ibareleri ve devamını kes: 'Yönetim Kurulu Üyesi', 'Başkan', 'Temsile Yetkili', 'Yetki Şekli', 'Görev Dağılımı' vb.
        nm = re.sub(r"\b(Y[öo]netim\s+Kurulu(?:\s+Ba[sş]kan[ıi])?|Y[öo]netim|Kurulu|[ÜU]yesi|Ba[sş]kan[ıi]|Temsile\s+Yetkili(?:dir)?|Yetki\s+S[eé]kli|G[öo]rev\s+Da[gğ]il[ıi]m[ıi])\b.*$", "", nm, flags=re.IGNORECASE).strip()
        # Sonda idarî/işlem kelimeleri ve devamını kes: 'tescil', 'tarihinden', 'itibaren', 'atanmistir', 'memuru', 'tasfiye' vb.
        nm = re.sub(r"\b(tescil(?:den)?|tarihinden|itibaren|atanm[ıi]ş(?:tır)?|atanan|memuru|tasfiye)\b.*$", "", nm, flags=re.IGNORECASE).strip()
        # Sonda bölüm başlığına taşma durumlarını kes: 'KISIYE', 'BILGILER' vb.
        nm = re.sub(r"\b(K[İI]S[İI]YE|KISIYE|B[İI]LG[İI]LER)\b.*$", "", nm, flags=re.IGNORECASE).strip()
        # Çift/mültiple boşlukları sadeleştir
        nm = re.sub(r"\s+", " ", nm).strip()
        return nm

    def _merge_split_upper_tokens(nm: str) -> str:
        toks = [t for t in re.split(r"\s+", nm.strip()) if t]
        out: List[str] = []
        j = 0
        while j < len(toks):
            cur = toks[j]
            if j + 1 < len(toks):
                nxt = toks[j + 1]
                if (len(cur) <= 2 and
                    re.fullmatch(r"[A-ZÇĞİÖŞÜ'’\-]{1,}", cur) and
                    re.fullmatch(r"[A-ZÇĞİÖŞÜ'’\-]{2,}", nxt)):
                    merged = (cur + nxt).replace(" ", "")
                    if re.fullmatch(r"[A-ZÇĞİÖŞÜ'’\-]{3,}", merged):
                        out.append(merged)
                        j += 2
                        continue
            out.append(cur)
            j += 1
        return " ".join(out)

    def is_probable_person_name(nm: str) -> bool:
        if "\n" in nm or "\r" in nm:
            return False
        nm = _clean_person_name(nm)
        nm = _merge_split_upper_tokens(nm)
        toks = [t for t in re.split(r"\s+", nm) if t]
        # 2–4 kelimeyi kabul et (kullanıcı isteği)
        if not (2 <= len(toks) <= 4):
            return False
        # Soyad en az 2 harf olmalı (örn. ÖZ gibi 2 harfli soyadlar için izin ver)
        if len(toks[-1]) < 2:
            return False
        # Her token yalnızca harf/tek tırnak/bağlaç içermeli
        for t in toks:
            if t.upper() in STOP_TOKENS:
                return False
            if t.upper() in NOISE_TOKENS:
                return False
            if not (2 <= len(t) <= 20):
                return False
            if not re.fullmatch(r"[A-Za-zÇĞİÖŞÜçğıöşü'\-]+", t):
                return False
        # Yer adı filtresi: tüm tokenler yer adı benzeri ise reddet; son token yer adı ise reddet
        if all(_is_location_like(t) for t in toks):
            return False
        if _is_location_like(toks[-1]):
            return False
        # Türkçe ünlü denetimi (tamamen ünlüsüz olmasın)
        vowels = set("AEIİOÖUÜaeıioöuü")
        for t in toks:
            if len(set(t) & vowels) == 0:
                return False
        return True

    # Not: '5' karakteri OCR'de '$' olarak gelebilir; \b yerine lookaround kullan
    # Yabancı kimlik/OCR varyantları için: başında tek harf (örn. 'N********9') opsiyonel olsun.
    # Kurallar:
    #  - Eğer prefix varsa: yıldızlardan önce 0-4 hane kabul et (OCR'de ön hanenin düşmesi olası)
    #  - Prefix yoksa: yıldızlardan önce en az 1 hane olmalı (false positive azaltır)
    mask_re = re.compile(
        r"(?<!\w)(?:"
        r"(?P<prefix>[A-Za-z])(?P<id1>(?:\d|\$){0,4}\*{2,8}(?:\d|\$){1,3})"
        r"|(?P<id2>(?:\d|\$){1,4}\*{2,8}(?:\d|\$){1,3})"
        r")(?<!\w)?(?!\w)"
    )
    # OCR toleranslı: 'Kimlik Numaral' varyantını da yakala (sondaki ı/i düşmüş olabilir)
    kimlik_re = re.compile(r"(?:T\.?\s*C\.?\s*)?Kimlik\s*(?:Numara(?:l[ıi]?)?|No'?lu|No)\b", re.IGNORECASE)
    # Virgül/iki nokta toleransı: "ikamet eden, <AD>" veya "ikamet eden: <AD>"
    ikamet_re = re.compile(rf"ikamet\s+eden\s*[,:]?\s+{name_pat}", re.IGNORECASE)
    # Adres benzeri içerik ayıracı
    addressish = re.compile(r"\b(MAH\.?|MAHALLES[İI]|CAD\.?|CADDES[İI]|CD\.?|SOK\.?|SOKA[ĞG][ıi]|SK\.?|BLV\.?|BULVAR[ıi]?|NO\b|KAT\b|DA[İI]RE\b|APT\.?|S[İI]TE|OSB|\d)\b", re.IGNORECASE)
    # Aynı satır kuyruğunda yalın isim tespitinde, tek başına rakam varlığı (ör. maskeli kimlik) adres sayılmasın
    addressish_nodigit = re.compile(r"\b(MAH\.?|MAHALLES[İI]|CAD\.?|CADDES[İI]|CD\.?|SOK\.?|SOKA[ĞG][ıi]|SK\.?|BLV\.?|BULVAR[ıi]?|NO\b|KAT\b|DA[İI]RE\b|APT\.?|S[İI]TE|OSB)\b", re.IGNORECASE)

    lines = text.splitlines()
    for i, raw in enumerate(lines):
        ln = raw.strip()
        if not ln:
            continue
        # Satırdaki tüm maskeli kimlikleri yakala; yoksa devam et
        mid_matches = list(mask_re.finditer(ln))
        if not mid_matches:
            continue

        # Her maskeli kimlik için aynı yakalama mantığını uygula
        for mk in mid_matches:
            # Opsiyonel harf ön-ek (örn. 'N********9')
            pfx = mk.groupdict().get("prefix") or ""
            # Sadece maskeli ID gövdesi (yıldızlı kısım + uç haneler)
            core = mk.groupdict().get("id1") or mk.groupdict().get("id2") or (mk.group(0)[1:] if pfx else mk.group(0))
            # Kural 4: '$' -> '5' normalizasyonu (ID gövdesi için)
            mid = core.replace("$", "5")
            # Çıktıda maskeyi parçalama: varsa harf öneki ile birlikte göster
            mid_out = (pfx + mid) if pfx else mid
            if mid in used_ids:
                continue

            # Bağlam: tablo benzeri mi? (Kurucu tablosu gibi)
            ctx_lines = lines[max(0, i-3): min(len(lines), i+4)]
            ctx_block = "\n".join(ctx_lines)
            tableish = re.search(r"^(Sira\s*No|Kurucu|Uyruk|Kimlik\s*No\s*/?\s*MERS[İI]S\s*No)\b", ctx_block, flags=re.IGNORECASE | re.MULTILINE) is not None

            # (Öncelik) Geriye yakın satırlarda 'Adı ve Soyadı: <AD SOYAD>' başlığı ile ad yakalama
            try:
                for k in range(1, 7):
                    if i - k < 0 or mid in used_ids:
                        break
                    prev = lines[i - k].strip()
                    if not prev:
                        continue
                    m_prev_name = re.search(r"Ad[ıi]\s*ve\s*Soyad[ıi]\s*[:：]\s*([A-ZÇĞİÖŞÜ'’\-]+(?:\s+[A-ZÇĞİÖŞÜ'’\-]+){1,3})", prev, flags=re.IGNORECASE)
                    if m_prev_name:
                        nm0 = m_prev_name.group(1).strip()
                        nm0 = _merge_split_upper_tokens(_clean_person_name(nm0))
                        toks0 = [t for t in re.split(r"\s+", nm0) if t]
                        while toks0 and _is_location_like(toks0[0]):
                            toks0.pop(0)
                        nm = " ".join(toks0) if toks0 else nm0
                        if nm and is_probable_person_name(nm):
                            rec = {"text": nm, "label": "PER_MASKED", "masked_ids": mid_out}
                            if pfx:
                                rec["masked_id_prefix"] = pfx
                            persons.append(rec)
                            used_ids.add(mid)
                            # Bu maskeyi eşledik, diğer taramalara geçmeyelim
                            break
            except Exception:
                pass
            if mid in used_ids:
                continue

            # 0.0) Markdown Tablo Satırı: "Maskeli ID bir tablo satırındaysa (|), satırdaki BÜYÜK HARFLİ hücreyi kişi, diğerini adres olarak ata"
            if "|" in ln:
                cells = [c.strip() for c in ln.split("|") if c.strip()]
                cand_name = None
                cand_addr = None
                for cell in cells:
                    if cell == mid_out or cell == mid:
                        continue
                    # Look for name (Uppercase, 2-4 words)
                    toks = cell.split()
                    if 2 <= len(toks) <= 4 and all(re.fullmatch(r"[A-ZÇĞİÖŞÜ'’\-]+", t) for t in toks) and any(len(t) >= 3 for t in toks):
                        if not _is_location_like(cell):
                            cand_name = " ".join(toks)
                    
                    # Look for address (has addressish keywords)
                    if addressish_nodigit.search(cell) or (len(cell) > 5 and _is_location_like(cell)):
                         if cell != mid_out and cell != mid:
                             cand_addr = cell

                if cand_name and is_probable_person_name(cand_name):
                    key = cand_name.upper().strip()
                    if key not in assigned_by_name or assigned_by_name.get(key) == mid:
                        rec = {
                            "text": cand_name, 
                            "label": "PER_MASKED", 
                            "masked_ids": mid_out,
                            "address": cand_addr
                        }
                        if pfx: rec["masked_id_prefix"] = pfx
                        persons.append(rec)
                        assigned_by_name.setdefault(key, mid)
                        used_ids.add(mid)
                        break
            
            if mid in used_ids:
                continue

            # 1) Aynı satır: "Kimlik Numaralı <AD SOYAD>" (OCR toleranslı: I-acute -> İ)
            ln_norm = unicodedata.normalize('NFC', ln)
            ln_norm = ln_norm.replace("Í", "İ").replace("Í", "İ").replace("Ì", "İ")
            m_same = re.search(rf"{kimlik_re.pattern}.*?{name_pat}", ln_norm, flags=re.IGNORECASE)
            if m_same:
                nm0 = m_same.group(m_same.lastindex).strip() if m_same.lastindex else m_same.group(1).strip()
                nm0 = _merge_split_upper_tokens(_clean_person_name(nm0))
                # Baştaki yer adı benzeri tokenları kırp (örn. IZMIT ADNAN UÇAR -> ADNAN UÇAR)
                toks0 = [t for t in re.split(r"\s+", nm0) if t]
                trimmed = False
                while toks0 and _is_location_like(toks0[0]):
                    toks0.pop(0)
                    trimmed = True
                nm = " ".join(toks0) if trimmed else nm0
                if nm and is_probable_person_name(nm):
                    key = nm.upper().strip()
                    if key not in assigned_by_name or assigned_by_name.get(key) == mid:
                        rec = {"text": nm, "label": "PER_MASKED", "masked_ids": mid_out}
                        if pfx:
                            rec["masked_id_prefix"] = pfx
                        persons.append(rec)
                        assigned_by_name.setdefault(key, mid)
                        used_ids.add(mid)
                    continue

            # 1b) Aynı satırın sonunda yalın isim (daha muhafazakâr, adres anahtarları yoksa)
            # Not: maskeli rakamlar nedeniyle adresmiş gibi elenmesin diye digitsiz sürümü kullan
            if not addressish_nodigit.search(ln):
                m_tail = re.search(rf"{name_pat}\s*$", ln)
                if m_tail and mid not in used_ids:
                    nm = _merge_split_upper_tokens(_clean_person_name(m_tail.group(1).strip()))
                    if nm and is_probable_person_name(nm):
                        key = nm.upper().strip()
                        if key not in assigned_by_name or assigned_by_name.get(key) == mid:
                            rec = {"text": nm, "label": "PER_MASKED", "masked_ids": mid_out}
                            if pfx:
                                rec["masked_id_prefix"] = pfx
                            persons.append(rec)
                            assigned_by_name.setdefault(key, mid)
                            used_ids.add(mid)
                        continue

            # 1c) Müsterek/müştereken kalıpları: "... (AD SOYAD) ile birlikte müştereken ..."
            try:
                ctx = ln
                # Aynı satırda değilse takip eden 1-2 satırı da bağlama ekle
                if i + 1 < len(lines):
                    ctx += " " + lines[i + 1]
                if i + 2 < len(lines):
                    ctx += " " + lines[i + 2]
                if re.search(r"m[üu][şs]terek(?:en)?", ctx, flags=re.IGNORECASE) and mid not in used_ids:
                    for pm in re.finditer(r"\(([^)]+)\)", ctx):
                        inner = (pm.group(1) or "").strip()
                        if not inner:
                            continue
                        # '... <NAME> için müşterek olduğu yetkililer ( ... )' bağlamında
                        # parantez içindeki isimlere maskeyi atamamalıyız; bu durumda maske 'için' öncesindeki kişiye aittir.
                        try:
                            s_pm, _e_pm = pm.span()
                            pre_ctx = ctx[max(0, s_pm - 48): s_pm]
                            if re.search(r"\b(?:için|icin)\b", pre_ctx, flags=re.IGNORECASE):
                                continue
                        except Exception:
                            pass
                        split_names = re.split(r"\s*(?:,|\s+ve\s+)\s*", inner)
                        for cand in split_names:
                            cand = cand.strip()
                            # Büyük harf ağırlıklı kişi adı filtresi
                            if not cand or len(cand) < 3:
                                continue
                            # Harf setini sınırlı tut, sayıları ayıkla
                            cand2 = re.sub(r"[^A-ZÇĞİÖŞÜ'’\-\s]", " ", cand)
                            cand2 = re.sub(r"\s+", " ", cand2).strip()
                            if is_probable_person_name(cand2):
                                rec = {"text": cand2, "label": "PER_MASKED", "masked_ids": mid_out}
                                if pfx:
                                    rec["masked_id_prefix"] = pfx
                                persons.append(rec)
                                used_ids.add(mid)
                                # aynı id için tekrar tekrar eklemeyi sınırlama; ama diğer isimler de eklenebilsin
            except Exception:
                pass

            # 1d) Basit ileri tarama: maskeden sonra 2-4 BÜYÜK harfli kelimeyi ad-soyad olarak yakala
            # Not: Tablo benzeri bağlamdaysak (Sira No, Kurucu, Uyruk ...), genel token taramasını PAS geç
            try:
                if tableish:
                    # Yine de 'ikamet eden <AD>' penceresini tarayalım (bir satır aşağı yukarı bağlamda)
                    tail_ctx = ln[mk.end():]
                    if i + 1 < len(lines):
                        tail_ctx += " " + lines[i + 1]
                    if i + 2 < len(lines):
                        tail_ctx += " " + lines[i + 2]
                    if i + 3 < len(lines):
                        tail_ctx += " " + lines[i + 3]
                    m_same_ik2 = re.search(rf"ikamet\s+eden\s*[:,]?\s*{name_pat}", tail_ctx, flags=re.IGNORECASE)
                    if m_same_ik2 and mid not in used_ids:
                        nm = m_same_ik2.group(m_same_ik2.lastindex).strip() if m_same_ik2.lastindex else m_same_ik2.group(1).strip()
                        nm = _merge_split_upper_tokens(_clean_person_name(nm))
                        if nm and is_probable_person_name(nm):
                            key = nm.upper().strip()
                            if key not in assigned_by_name or assigned_by_name.get(key) == mid:
                                rec = {"text": nm, "label": "PER_MASKED", "masked_ids": mid_out}
                                if pfx:
                                    rec["masked_id_prefix"] = pfx
                                persons.append(rec)
                                assigned_by_name.setdefault(key, mid)
                                used_ids.add(mid)
                        continue
                    # Tablo bağlamında fallback token taraması yapmayalım
                    continue
                tail_ctx = ln[mk.end():]
                # Aynı satır yetersizse takip eden 1-3 satırı da bağlama ekle (basit)
                if i + 1 < len(lines):
                    tail_ctx += " " + lines[i + 1]
                if i + 2 < len(lines):
                    tail_ctx += " " + lines[i + 2]
                if i + 3 < len(lines):
                    tail_ctx += " " + lines[i + 3]
                # Öncelik: aynı satır/kısa bağlam içinde 'ikamet eden, <AD SOYAD>' kalıbını yakala
                m_same_ik = re.search(rf"ikamet\s+eden\s*[,:]?\s*{name_pat}", tail_ctx, flags=re.IGNORECASE)
                if m_same_ik and mid not in used_ids:
                    nm = m_same_ik.group(m_same_ik.lastindex).strip() if m_same_ik.lastindex else m_same_ik.group(1).strip()
                    nm = _merge_split_upper_tokens(_clean_person_name(nm))
                    if nm and is_probable_person_name(nm):
                        key = nm.upper().strip()
                        if key not in assigned_by_name or assigned_by_name.get(key) == mid:
                            persons.append({"text": nm, "label": "PER_MASKED", "masked_ids": mid_out})
                            assigned_by_name.setdefault(key, mid)
                            used_ids.add(mid)
                        break
                # Öncelik 2: Önceki 1-6 satırda 'Adı ve Soyadı: <AD SOYAD>' başlığı
                try:
                    for k in range(1, 7):
                        if i - k < 0 or mid in used_ids:
                            break
                        prev = lines[i - k].strip()
                        if not prev:
                            continue
                        m_prev_name = re.search(rf"Ad[ıi]\s*ve\s*Soyad[ıi]\s*[:：]\s*{name_pat}", prev, flags=re.IGNORECASE)
                        if m_prev_name:
                            nm0 = m_prev_name.group(m_prev_name.lastindex).strip() if m_prev_name.lastindex else m_prev_name.group(1).strip()
                            nm0 = _merge_split_upper_tokens(_clean_person_name(nm0))
                            # Baştaki yer adı benzeri tokenları kırp
                            toks0 = [t for t in re.split(r"\s+", nm0) if t]
                            while toks0 and _is_location_like(toks0[0]):
                                toks0.pop(0)
                            nm = " ".join(toks0) if toks0 else nm0
                            if nm and is_probable_person_name(nm):
                                rec = {"text": nm, "label": "PER_MASKED", "masked_ids": mid_out}
                                if pfx:
                                    rec["masked_id_prefix"] = pfx
                                persons.append(rec)
                                used_ids.add(mid)
                                break
                except Exception:
                    pass
                # Eğer kısa bağlamda 'Şirketin unvanı' başlığı geçiyorsa, genel büyük harf taramasını atla.
                if re.search(r"\bS[ıi]rketin\s+unvan[ıiİI]\b", tail_ctx, flags=re.IGNORECASE) or re.search(r"\bUnvan[ıiİI]\b", tail_ctx[:80], flags=re.IGNORECASE):
                    continue
                slash_near = "/" in tail_ctx[:120]
                # Tokenlere böl (boşluk ve yaygın ayırıcılar)
                raw_toks = re.split(r"[\s,;:()\[\]{}<>|\/\\\-]+", tail_ctx.strip())
                name_toks: List[str] = []
                found = False
                started = False
                seen_lower_after_slash = False
                def _is_upper_token(t: str) -> bool:
                    if not t:
                        return False
                    t2 = t.replace("'", "").replace("’", "").replace("-", "")
                    if not (len(t2) >= 2 and t2.isalpha()):
                        return False
                    # Tamamen büyük harfse kabul
                    if t2.upper() == t2:
                        return True
                    # OCR toleransı: yalnızca son karakteri küçük olan tokenı kabul et (örn. ESKt)
                    if len(t2) >= 2 and (t2[:-1].upper() == t2[:-1]) and t2[-1].islower():
                        return True
                    return False

                for tok in raw_toks:
                    if not tok:
                        continue
                    # Token normalize et (OCR): birleşim işaretlerini birleştir
                    tok = unicodedata.normalize('NFC', tok)
                    # OCR diakritik normalizasyonu: I-acute/kombine -> İ
                    tok = tok.replace("Í", "İ").replace("Í", "İ").replace("Ì", "İ")
                    # Tokeni temizle: apostrof + iyelik/genitif eklerini uçtan kaldır
                    # Örn: ÇELIK'in / ÇELİK’İN / ÇELIK'nun / ÇELİK’nün
                    tok_clean = re.sub(r"[’'](?:nin|nın|nun|nün|in|ın|un|ün)$", "", tok, flags=re.IGNORECASE)
                    # Tek harfli ek (örn. BAYRAM'e) için de emniyet şeridi
                    tok_clean = re.sub(r"[’'][aAeEiİIıuUüÜ]$", "", tok_clean)
                    # Küçük harf içeriyorsa ve toplama başlamışsa;
                    # özel tolerans: tamamen büyük + sonda tek küçük harf ise (örn. BOSTANCIe) son harfi atıp finalize et
                    if re.search(r"[a-zçğıöşü]", tok) and tok_clean == tok:
                        if started and re.fullmatch(r"[A-ZÇĞİÖŞÜ'’\-]{2,}[a-zçğıöşü]", tok):
                            name_toks.append(tok[:-1])
                            if 2 <= len(name_toks) <= 4:
                                found = True
                                break
                        if slash_near and not started:
                            # '/' bağlamında küçük harf segmenti görüldü; bundan sonrası ilk büyük harfli blok isim olabilir
                            seen_lower_after_slash = True
                            continue
                        if started and 2 <= len(name_toks) <= 4:
                            found = True
                            break
                        else:
                            continue
                    # Yalnızca büyük harfli (Unicode) tokenleri kabul et (diakritik dostu)
                    if not _is_upper_token(tok_clean):
                        if started and 2 <= len(name_toks) <= 4:
                            found = True
                            break
                        else:
                            continue
                    # Gürültü tokenları (OCR/başlık) ise finalize et veya atla
                    if tok_clean.upper() in NOISE_TOKENS:
                        if started and 2 <= len(name_toks) <= 4:
                            found = True
                            break
                        else:
                            continue
                    # Yer adı benzeri ise: eğer en az 2 aday toplandıysa finalize et, değilse atla
                    if _is_location_like(tok_clean):
                        # Slash bağlamında (örn. ISTANBUL / ZEYTINBURNU ...) baştaki yer adlarını yut, isim başlayınca topla
                        if slash_near and not started and not seen_lower_after_slash:
                            continue
                        if started and 2 <= len(name_toks) <= 4:
                            found = True
                            break
                        else:
                            continue
                    # Gürültü/başlık sözcüklerini atla (TOKENS)
                    if tok_clean.upper() in STOP_TOKENS:
                        if started and 2 <= len(name_toks) <= 4:
                            found = True
                            break
                        else:
                            continue
                    # Uygun büyük harfli token: toplamayı başlat/ekle
                    # '/' bağlamında küçük harf segmentini görmeden başlamayız
                    if slash_near and not seen_lower_after_slash and not started:
                        continue
                    started = True
                    # Eğer mevcut token çok kısa (<=2) ise bir önceki token ile yapıştır (örn. 'BEYTEK' + 'İN')
                    if name_toks and len(tok_clean) <= 2 and re.fullmatch(r"[A-ZÇĞİÖŞÜ'’\-]{1,2}", tok_clean):
                        name_toks[-1] = (name_toks[-1] + tok_clean)
                    else:
                        name_toks.append(tok_clean)
                    if len(name_toks) == 4:
                        found = True
                        break
                if not found and 2 <= len(name_toks) <= 4:
                    found = True
                if found and 2 <= len(name_toks) <= 4 and mid not in used_ids:
                    nm0 = _clean_person_name(" ".join(name_toks))
                    # Baştaki yer adı benzeri tokenları kırp
                    toks0 = [t for t in re.split(r"\s+", nm0) if t]
                    trimmed = False
                    while toks0 and _is_location_like(toks0[0]):
                        toks0.pop(0)
                        trimmed = True
                    nm = " ".join(toks0) if trimmed else nm0
                    if nm and is_probable_person_name(nm):
                        rec = {"text": nm, "label": "PER_MASKED", "masked_ids": mid_out}
                        if pfx:
                            rec["masked_id_prefix"] = pfx
                        persons.append(rec)
                        used_ids.add(mid)
                        continue
            except Exception:
                pass

            # 1d.1) Geriye yakın satırlarda 'Adı ve Soyadı: <AD SOYAD>' başlığı ile ad yakalama (en fazla 5 satır geriye)
            try:
                for k in range(1, 6):
                    if i - k < 0:
                        break
                    prev = lines[i - k].strip()
                    if not prev:
                        continue
                    m_prev_name = re.search(rf"Ad[ıi]\s*ve\s*Soyad[ıi]\s*[:：]\s*([A-ZÇĞİÖŞÜ'’\-]+(?:\s+[A-ZÇĞİÖŞÜ'’\-]+){1,3})", prev, flags=re.IGNORECASE)
                    if m_prev_name and mid not in used_ids:
                        nm0 = m_prev_name.group(1).strip()
                        nm0 = _merge_split_upper_tokens(_clean_person_name(nm0))
                        # Baştaki yer adı benzeri tokenları kırp
                        toks0 = [t for t in re.split(r"\s+", nm0) if t]
                        trimmed = False
                        while toks0 and _is_location_like(toks0[0]):
                            toks0.pop(0)
                            trimmed = True
                        nm = " ".join(toks0) if trimmed else nm0
                        if nm and is_probable_person_name(nm):
                            persons.append({"text": nm, "label": "PER_MASKED", "masked_ids": mid_out})
                            used_ids.add(mid)
                            break
            except Exception:
                pass

            # 1e) Geri tarama: önceki 1-12 satırda 2-4 büyük harfli kelime dizisi
            try:
                back_candidates: List[Tuple[int,str]] = []
                for k in range(1, 13):
                    if i - k < 0:
                        break
                    prev = lines[i - k].strip()
                    if not prev or addressish.search(prev):
                        continue
                    slash_line = "/" in prev
                    toks = re.split(r"[\s,;:()\[\]{}<>|\/\\\-]+", prev)
                    cur: List[str] = []
                    best: List[str] = []
                    for tok in toks:
                        if not tok:
                            continue
                        if re.search(r"[a-zçğıöşü]", tok):
                            if len(cur) > len(best):
                                best = cur
                            cur = []
                            continue
                        if not re.fullmatch(r"[A-ZÇĞİÖŞÜ'’\-]{2,}", tok):
                            if len(cur) > len(best):
                                best = cur
                            cur = []
                            continue
                        if tok.upper() in NOISE_TOKENS:
                            if len(cur) > len(best):
                                best = cur
                            cur = []
                            continue
                        if _is_location_like(tok):
                            # Slash bulunan satırda baştaki yer adlarını yut
                            if slash_line and not cur:
                                continue
                            if len(cur) > len(best):
                                best = cur
                            cur = []
                            continue
                        if tok.upper() in STOP_TOKENS:
                            if len(cur) > len(best):
                                best = cur
                            cur = []
                            continue
                        cur.append(tok)
                    if len(cur) > len(best):
                        best = cur
                    if 2 <= len(best) <= 4 and mid not in used_ids:
                        cand0 = _clean_person_name(" ".join(best))
                        # Başta yer adı benzeri tokenları kırp
                        toks0 = [t for t in re.split(r"\s+", cand0) if t]
                        trimmed = False
                        while toks0 and _is_location_like(toks0[0]):
                            toks0.pop(0)
                            trimmed = True
                        cand = " ".join(toks0) if trimmed else cand0
                        if cand and is_probable_person_name(cand):
                            back_candidates.append((k, cand))
                if back_candidates and mid not in used_ids:
                    # En yakın satırı seç
                    back_candidates.sort(key=lambda x: x[0])
                    nm = back_candidates[0][1]
                    rec = {"text": nm, "label": "PER_MASKED", "masked_ids": mid_out}
                    if pfx:
                        rec["masked_id_prefix"] = pfx
                    persons.append(rec)
                    used_ids.add(mid)
                    continue
            except Exception:
                pass

            # 2) Takip eden 1-3 satır
            j = i + 1
            steps = 0
            while j < len(lines) and steps < 3:
                nxt = lines[j].strip(" -*–·•\t").strip()
                if not nxt:
                    break  # boş satırda dur
                # 1) Adres benzeri satırları yakala ama atlama (Kişi için sakla)
                p_addr = None
                if addressish.search(nxt):
                    # Eğer bu satırda 'ikamet eden' yoksa, bir sonraki satır için adres olarak sakla
                    if not re.search(r"ikamet\s+eden", nxt, re.IGNORECASE):
                        p_addr = nxt
                        j += 1
                        steps += 1
                        # Bir sonraki satırda ikamet eden var mı bak
                        if j < len(lines):
                            nxt_next = lines[j].strip()
                            m_ik_next = re.search(rf"ikamet\s+eden\s*[,:]?\s+{name_pat}", nxt_next, re.IGNORECASE)
                            if m_ik_next and mid not in used_ids:
                                nm = _clean_person_name(m_ik_next.group(1).strip())
                                if nm and is_probable_person_name(nm):
                                    rec = {"text": nm, "label": "PER_MASKED", "masked_ids": mid_out, "address": p_addr}
                                    if pfx: rec["masked_id_prefix"] = pfx
                                    persons.append(rec)
                                    used_ids.add(mid)
                                    break
                        continue

                # 2) "ikamet eden <AD SOYAD>" (AYNI SATIRDA ADRES)
                # Regex'i adres yakalayacak şekilde genişlet:
                m_ik = re.search(r"([A-ZÇĞİÖŞÜ0-9\.\s,/\-#]{5,150})\s+adresinde\s+ikamet\s+eden[,:]?\s+([A-ZÇĞİÖŞÜ$'’\-\s]{3,})", nxt, flags=re.IGNORECASE)
                if m_ik and mid not in used_ids:
                    p_addr = m_ik.group(1).strip()
                    nm = _clean_person_name(m_ik.group(2).strip())
                    if nm and is_probable_person_name(nm):
                        rec = {"text": nm, "label": "PER_MASKED", "masked_ids": mid_out, "address": p_addr}
                        if pfx:
                            rec["masked_id_prefix"] = pfx
                        persons.append(rec)
                        used_ids.add(mid)
                        break
                
                # Fallback: Eski ikamet regex'i (eğer adres önünde yakalanamazsa)
                m_ik_fallback = ikamet_re.search(nxt)
                if m_ik_fallback and mid not in used_ids:
                    nm = _clean_person_name(m_ik_fallback.group(1).strip())
                    if nm and is_probable_person_name(nm):
                        rec = {"text": nm, "label": "PER_MASKED", "masked_ids": mid_out}
                        if pfx:
                            rec["masked_id_prefix"] = pfx
                        persons.append(rec)
                        used_ids.add(mid)
                        break
                # Yalın isim satırı veya Adı Soyadı başlıklı satır
                m_name_line = re.search(rf"^(?:Ad[ıi](?:\s*ve\s*Soyad[ıi]|\s*Soyad[ıi])\s*[:：]\s*)?{name_pat}\s*$", nxt, flags=re.IGNORECASE)
                if m_name_line:
                    nm = m_name_line.group(m_name_line.lastindex).strip() if m_name_line.lastindex else m_name_line.group(1).strip()
                    # Satırda '/' varsa veya başta yer adı gibi parçalar varsa, öndeki lokasyon benzeri tokenları kırp
                    toks0 = [t for t in re.split(r"\s+", nm) if t]
                    trimmed = False
                    while toks0 and _is_location_like(toks0[0]):
                        toks0.pop(0)
                        trimmed = True
                    nm2 = " ".join(toks0) if trimmed else nm
                    nm2 = _clean_person_name(nm2)
                    if nm2 and is_probable_person_name(nm2) and mid not in used_ids:
                        rec = {"text": nm2, "label": "PER_MASKED", "masked_ids": mid_out}
                        if pfx:
                            rec["masked_id_prefix"] = pfx
                        persons.append(rec)
                        used_ids.add(mid)
                        break
                j += 1
                steps += 1

    return _dedup_entity_dicts(persons)

def extract_actions(text: str) -> List[dict]:
    """
    İlan metninden temel aksiyonları tespit eder.
    Şu kalıplar desteklenir:
      - Pay Devri
      - Amaç ve Konu (değişikliği)
      - Birleşme/İnfisah (devrolunan/devralan)
    """
    actions: List[dict] = []

    norm = text
    # PAY DEVRI
    if re.search(r"\bPay\s+Devri\b", norm, flags=re.IGNORECASE) or re.search(r"Tescil\s*Harici\s*Ilan\s*:.*Pay\s+Devri", norm, flags=re.IGNORECASE):
        details_lines: List[str] = []
        # İlgili bölümden kısa bir özet almak için 6-8 satıra kadar bağlam al
        lines = [ln.strip() for ln in norm.splitlines()]
        for i, ln in enumerate(lines):
            if re.search(r"Pay\s+Devri", ln, flags=re.IGNORECASE):
                ctx = " ".join([l for l in lines[i:i+12] if l])
                details_lines.append(ctx[:800])
                break
        parties: List[str] = []
        # Kimlik Numaralı <AD SOYAD>
        for m in re.finditer(r"Kimlik\s*Numara(?:l[ıi])?\s*([A-ZÇĞİÖŞÜ'][A-ZÇĞİÖŞÜ']+(?:\s+[A-ZÇĞİÖŞÜ'][A-ZÇĞİÖŞÜ']+){1,3})", norm, flags=re.IGNORECASE):
            parties.append(m.group(1).strip())
        # Mersis Numaralı <UNVAN> (alıcı kurum olabilir)
        for m in re.finditer(r"Mersis\s*Numara(?:l[ıi])?\s*([A-Z0-9ÇĞİÖŞÜ' .,&/-]{3,})", norm, flags=re.IGNORECASE):
            cand = m.group(1).strip()
            cand = re.sub(r"\s+(LIMITED|L[İI]M[İI]TED|ANON[İI]M|S[İI]RKET[İI]).*", r" \1", cand, flags=re.IGNORECASE)
            parties.append(cand.strip())
        parties = list(dict.fromkeys([p for p in parties if p]))  # benzersiz sırayla
        amounts = extract_money_spans(norm)
        actions.append({
            "type": "PAY_DEVRI",
            "details": details_lines[0] if details_lines else "Pay devri tespit edildi",
            "parties": parties,
            "amounts": amounts,
        })

    # AMAC VE KONU (DEĞİŞİKLİĞİ)
    if re.search(r"Ama[cç]\s*ve\s*Konu", norm, flags=re.IGNORECASE):
        eff_date = (
            find_first(rf"\b\d{{1,2}}\s+(?:{TURKISH_MONTHS})\s+\d{{4}}\b", norm, flags=re.IGNORECASE)
            or find_first(r"\b\d{1,2}\.\d{1,2}\.\d{4}\b", norm)
        )
        actions.append({
            "type": "AMAC_VE_KONU",
            "details": "Amaç ve Konu başlığı tespit edildi",
            "effective_date": eff_date,
        })

    # BİRLEŞME/İNFİSAH
    if re.search(r"Birlesme|Birleşme|[İI]nfisah", norm, flags=re.IGNORECASE):
        # Devralan unvanını yakalamaya çalış
        devralan = find_first(r"^\s*Unvan\s*[:.]\s*(.+)$", norm, flags=re.IGNORECASE | re.MULTILINE) or find_first(r"^\s*Devralan\s*[:.]\s*(.+)$", norm, flags=re.IGNORECASE | re.MULTILINE)
        actions.append({
            "type": "BIRLESME_INFISAH",
            "details": "Birleşme/İnfisah ifadesi tespit edildi",
            "devralan": devralan,
        })

    return actions


# --- Tescil Bölümleri Çıkarımı ---
def extract_tescil_sections(text: str) -> Tuple[List[str], Optional[str]]:
    """
    "Tescil Edilen Hususlar:" satırını ve onu izleyen "Tescile Delil Olan Belgeler:" satırını ayrıştırır.

    Döndürür: (hususlar_listesi, belgeler_metni)
      - hususlar_listesi: Virgül, "/" vb. ile ayrılmış hususların listesi
      - belgeler_metni: "Tescile Delil Olan Belgeler" içeriği (jenerik kesmelerle birleştirilmiş)
    """
    if not text:
        return ([], None)

    # Etiket desenleri (OCR toleranslı, inline flag yok)
    husus_label = re.compile(
        r"^\s*Tescil(?:e)?\s+Edilen\s+Husus(?:lar[ıi]?|lar)\s*[:：]?\s*(.*)$",
        re.IGNORECASE | re.MULTILINE,
    )
    belgeler_label = re.compile(
        r"^\s*(?:Tescile?\s+)?Delil\s+Olan\s+Belge(?:ler[ıi]?|ler)\s*[:：]?\s*(.*)$",
        re.IGNORECASE | re.MULTILINE,
    )

    m_h = husus_label.search(text)
    if not m_h:
        return ([], None)

    # Hususlar: etiket satırının sonundan, öncelikle ilk boş satıra; yoksa "Belgeler" etiketine kadar
    h_start = m_h.end()
    m_b = belgeler_label.search(text, h_start)
    h_end = m_b.start() if m_b else len(text)

    # İlk tercih: boş satır (section break) gördüğümüz yerde kes
    slice_after = text[h_start:h_end]
    m_blank = re.search(r"\n\s*\n", slice_after)
    if m_blank:
        h_end = h_start + m_blank.start()

    # Alternatif durdurucular: başlık/iletişim/adres vb. satırlar veya TAM BÜYÜK başlıklar
    stop_line_pat = re.compile(
        r"^\s*(?:[\-\u2022\u2027•·–—\*\.]*\s*)?(?:Adres|Eski\s*Adres|Yeni\s*Adres|Yu(?:ka(?:r|rn|n)?[ıi]?da)|Yukarıda|Yukarida|Tescil|Tescile|MERS[İI]S|Ticaret\s*Sicil|Telefon|Tel\.?|GSM|Faks|Fax|İlan\s*Sira\s*No|Ilan\s*Sira\s*No|Sira\s*No|Madde\b)",
        re.IGNORECASE | re.MULTILINE,
    )
    m_stop1 = stop_line_pat.search(text, h_start)
    upper_heading_pat = re.compile(r"^\s*(?:[^a-zçğıöşüà-öø-ÿ]{4,})$", re.MULTILINE)
    m_stop2 = upper_heading_pat.search(text, h_start)
    for m in (m_stop1, m_stop2):
        if m and m.start() < h_end:
            h_end = m.start()

    first_line_remainder = (m_h.group(1) or "").strip()
    between = text[h_start:h_end]
    # Sonraki satırlarda başlık tekrarları veya madde işareti gürültülerini sadeleştir
    between = re.sub(r"^[\s•·•\-–]+", "", between, flags=re.MULTILINE)
    # Kural: Eğer etiket ile aynı satırda içerik varsa (ör. "Tescil Edilen Hususlar: Kuruluş"), yalnızca o içeriği al.
    # Yoksa, aşağıdaki satırlardan (boş satır/başlıkta kesilmiş) içeriği kullan.
    if first_line_remainder:
        hususlar_raw = first_line_remainder
    else:
        hususlar_raw = (between or "").strip()
    # İlk boş satır kuralı sebebiyle çok satırlı blok zaten kırpıldı; tek satıra indir ve ayraçlara göre böl
    hususlar_raw = re.sub(r"\s+", " ", hususlar_raw)
    if hususlar_raw:
        parts = re.split(r"\s*(?:,|/|\\|\||;|\s+-\s+)\s*", hususlar_raw)
        hususlar = [p.strip(" .-–·•\t").strip() for p in parts if p and len(p.strip()) >= 2]
    else:
        hususlar = []

    # Hususlar için basit OCR normalizasyonları (ör. Artinmi -> Artırımı, Degisimi -> Değişimi)
    if hususlar:
        normed: List[str] = []
        for h in hususlar:
            t = h
            # 'Sermaye' OCR düzeltmesi (sermave -> Sermaye)
            t = re.sub(r"\bsermave\b", "Sermaye", t, flags=re.IGNORECASE)
            # Artırımı varyantları:
            #  - 'artirmi'/'artirmi' (eksik noktalama)
            t = re.sub(r"\bart[ıi]r[ıi]?m[ıi]\b", "Artırımı", t, flags=re.IGNORECASE)
            #  - 'artinmi' (r -> n OCR hatası; n opsiyonel, arada fazladan sesli olmayabilir)
            t = re.sub(r"\bart[ıi]n?m[ıi]\b", "Artırımı", t, flags=re.IGNORECASE)
            #  - 'arurmi' (t -> u OCR hatası; arurmi/arvrmi gibi varyantlar, eksik sesli olasılığı)
            t = re.sub(r"\bar[uv]r[ıi]?m[ıi]\b", "Artırımı", t, flags=re.IGNORECASE)
            #  - 'sermaye art...' birleşik düzeltme (bağlama duyarlı)
            t = re.sub(r"\bsermaye\s+art[ıi](?:r[ıi]?|n?)m[ıi]\b", "Sermaye Artırımı", t, flags=re.IGNORECASE)
            #  - 'sermaye arurmi/arvrmi' bağlamsal düzeltme (eksik sesli olasılığı)
            t = re.sub(r"\bsermaye\s+ar[uv]r[ıi]?m[ıi]\b", "Sermaye Artırımı", t, flags=re.IGNORECASE)
            # Değişimi varyantları (degisimi vb.)
            t = re.sub(r"\bdeg[ıi]s[ıi]m[ıi]\b", "Değişimi", t, flags=re.IGNORECASE)
            normed.append(t)
        hususlar = normed

    # Belgeler: etiketten sonra, bir sonraki genel başlık/durdurucuya kadar
    belgeler_text: Optional[str] = None
    if m_b:
        b_first = (m_b.group(1) or "").strip()
        b_start = m_b.end()
        # Genel durdurucular (adres/ilan/diger başlıklar): Adres başlıklarını da kapsa
        stop_line_pat = re.compile(
            r"^\s*(?:[\-\u2022\u2027•·–—\*\.]*\s*)?(?:Adres|Eski\s*Adres|Yeni\s*Adres|Yu(?:ka(?:r|rn|n)?[ıi]?da)|Yukarıda|Yukarida|Tescil|Tescile|MERS[İI]S|Ticaret\s*Sicil|Telefon|Tel\.?|GSM|Faks|Fax|İlan\s*Sira\s*No|Ilan\s*Sira\s*No|Sira\s*No|Madde\b)",
            re.IGNORECASE | re.MULTILINE,
        )
        # Tamamen BÜYÜK HARF (ve/veya sayı/punktuasyon) satırlar için de kes.
        # Mantık: küçük harf içermeyen, en az 4 karakterlik satır (örn. 'İÇERİĞİ DEĞİŞEN ...', 'SERMAYE ARTIRIMI').
        upper_heading_pat = re.compile(
            r"^\s*(?:[^a-zçğıöşüà-öø-ÿ]{4,})$",
            re.MULTILINE,
        )
        # Numaralı başlıklar (ör. "1. Kurulus", "2) ...", "(3) ...")
        enum_heading_pat = re.compile(
            r"^\s*(?:\d{1,3}\s*[\.)]|\(\s*\d{1,3}\s*\))\s+\S+",
            re.MULTILINE,
        )
        m_stop1 = stop_line_pat.search(text, b_start)
        m_stop2 = upper_heading_pat.search(text, b_start)
        m_stop3 = enum_heading_pat.search(text, b_start)
        candidates = [m for m in (m_stop1, m_stop2, m_stop3) if m]
        b_end = min(m.start() for m in candidates) if candidates else len(text)

        # İlk boş satır (section break) görürsek orada kes
        slice_after = text[b_start:b_end]
        m_blank = re.search(r"\n\s*\n", slice_after)
        if m_blank:
            b_end = b_start + m_blank.start()
        b_between = text[b_start:b_end]
        b_between = re.sub(r"^[\s•·•\-–]+", "", b_between, flags=re.MULTILINE)
        # Çok satırlı içeriği önce birleştir, sonra adres/iletişim başlıklarını satır bazında filtrele
        raw_combined = (b_first + ("\n" + b_between if b_between else "")).strip()
        drop_line_pat = re.compile(r"^\s*(Adres|Eski\s*Adres|Yeni\s*Adres|Telefon|Tel\.?|GSM|Faks|Fax)\b", re.IGNORECASE)
        filtered_lines = [ln for ln in raw_combined.splitlines() if not drop_line_pat.search(ln)]
        combined = " ".join(ln.strip(" -•—·") for ln in filtered_lines if ln.strip())
        combined = re.sub(r"\s+", " ", combined).strip()
        if combined:
            # Çok uzunlukları makulleştir
            if len(combined) > 500:
                combined = combined[:500].rstrip()
            belgeler_text = combined

    return (hususlar, belgeler_text)

def _dedup_entity_dicts(items: List[dict]) -> List[dict]:
    """'text' anahtarına göre küçük harf ve overlap kontrolüyle deduplikasyon yapar."""
    out: List[dict] = []
    import unicodedata
    
    def norm_val(s: str) -> str:
        s = unicodedata.normalize('NFD', s)
        s = "".join([c for c in s if not unicodedata.combining(c)])
        return re.sub(r"[^A-Z]", "", s.upper())
        
    for it in items:
        name = (it.get("text") or "").strip()
        if not name or len(name) < 4:
            continue
            
        norm_name = norm_val(name)
        is_dup = False
        
        for i, existing in enumerate(out):
            exist_name = existing.get("text") or ""
            norm_exist = norm_val(exist_name)
            
            # Eğer isimler birbirinin alt kümesiyse veya ilk 5 karakteri aynıysa
            if norm_name in norm_exist or norm_exist in norm_name or norm_name[:5] == norm_exist[:5]:
                # Türkçe karakter zenginliği ve uzunluk bazlı daha doğru varyantı koru
                tr_chars = set("ÇĞİÖŞÜçğiöşü")
                count_new = sum(1 for c in name if c in tr_chars)
                count_exist = sum(1 for c in exist_name if c in tr_chars)
                
                if len(name) > len(exist_name) or (count_new > count_exist and len(name) >= len(exist_name) - 2):
                    out[i] = it
                is_dup = True
                break
                
        if not is_dup:
            out.append(it)
            
    return out

def _dedup_persons_pref_masked(items: List[dict]) -> List[dict]:
    """Aynı kişiyi (text) tekilleştirirken PER_MASKED etiketi varsa onu tercih eder.
    Aksi halde ilk görüleni korur.
    """
    # Önce genel zeki overlap/benzerlik tekilleştirmesini çalıştır
    items = _dedup_entity_dicts(items or [])
    
    chosen: Dict[str, dict] = {}
    order: List[str] = []
    for it in items:
        key = (it.get("text") or "").strip().lower()
        if not key:
            continue
        if key not in chosen:
            chosen[key] = it
            order.append(key)
        else:
            cur = chosen[key]
            # PER_MASKED mevcutsa onu koru; yoksa mevcut kalır
            if (cur.get("label") != "PER_MASKED") and (it.get("label") == "PER_MASKED"):
                chosen[key] = it
    return [chosen[k] for k in order]

def _http_post_json(url: str, payload: dict, headers: Optional[dict] = None, timeout: float = 30.0) -> Optional[dict]:
    """Basit HTTP POST JSON. httpx/requests mevcutsa onları, değilse urllib kullanır."""
    hdrs = {"Content-Type": "application/json"}
    if headers:
        hdrs.update(headers)
    data = json.dumps(payload).encode("utf-8")
    # Tercihen httpx
    if httpx is not None:
        try:
            resp = httpx.post(url, headers=hdrs, content=data, timeout=timeout)
            if 200 <= resp.status_code < 300:
                return resp.json()
            logger.warning("LLM HTTP %s: %s", resp.status_code, resp.text[:200])
            return None
        except Exception as e:
            logger.warning("LLM httpx post hatası: %s", e)
    # requests fallback
    if requests is not None:
        try:
            resp = requests.post(url, headers=hdrs, data=data, timeout=timeout)  # type: ignore
            if 200 <= resp.status_code < 300:  # type: ignore[attr-defined]
                return resp.json()  # type: ignore[no-any-return]
            logger.warning("LLM HTTP %s: %s", getattr(resp, 'status_code', '?'), getattr(resp, 'text', '')[:200])
            return None
        except Exception as e:
            logger.warning("LLM requests post hatası: %s", e)
    # urllib son çare
    try:
        import urllib.request as urlreq
        req = urlreq.Request(url, data=data, headers=hdrs, method="POST")
        with urlreq.urlopen(req, timeout=timeout) as r:  # type: ignore[attr-defined]
            txt = r.read().decode("utf-8")
            return json.loads(txt)
    except Exception as e:
        logger.warning("LLM urllib post hatası: %s", e)
        return None

def _llm_extract_entities(text: str) -> Optional[Dict[str, Any]]:
    """
    LM Studio/OpenAI uyumlu chat.completions ile varlık çıkarımı.
    Beklenen anahtarlar: persons[str[]], organizations[str[]], addresses[str[]],
    trade_name[str?], registration_number[str?], sicil_dosya_no[str?], mersis_no[str?]
    """
    if not LLM_ENABLED:
        return None
    try:
        url = LLM_BASE_URL.rstrip("/") + "/chat/completions"
        headers = {}
        if LLM_API_KEY:
            headers["Authorization"] = f"Bearer {LLM_API_KEY}"
        system = (
            "Türkçe ticaret sicil ilanı/duyurusu OCR metninden varlık çıkar. "
            "Sadece geçerli kişi ad-soyadlarını (ör. 'Atakan Yüklü') tespit et; "
            "kurum/unvan, adres, MERSIS, Sicil/Dosya No alanlarını ayıkla. "
            "Sıkı JSON döndür. Ek açıklama yok."
        )
        user = (
            "Metin:\n" + text + "\n\n"
            "Yalnızca şu JSON'u döndür:\n"
            "{\n"
            "  \"persons\": [\"Ad Soyad\"...],\n"
            "  \"organizations\": [\"...\"],\n"
            "  \"addresses\": [\"...\"],\n"
            "  \"trade_name\": \"...\" | null,\n"
            "  \"registration_number\": \"...\" | null,\n"
            "  \"sicil_dosya_no\": \"...\" | null,\n"
            "  \"mersis_no\": \"...\" | null\n"
            "}"
        )
        payload = {
            "model": LLM_MODEL,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "temperature": 0,
            "max_tokens": 800,
            "response_format": {"type": "json_object"},
        }
        resp = _http_post_json(url, payload, headers=headers, timeout=LLM_TIMEOUT)
        if not resp:
            return None
        # OpenAI uyumlu çıktı
        content = None
        try:
            content = (
                resp.get("choices", [{}])[0]
                .get("message", {})
                .get("content")
            )
        except Exception:
            content = None
        if not content:
            return None
        data = None
        try:
            data = json.loads(content)
        except Exception:
            # Güvenli ayrıştırma için olası codeblock içini çekmeye çalış
            m = re.search(r"\{[\s\S]*\}\s*$", content)
            if m:
                try:
                    data = json.loads(m.group(0))
                except Exception:
                    data = None
        if isinstance(data, dict):
            return data
    except Exception as e:
        logger.warning("LLM extract hatası: %s", e)
    return None


def parse_announcement_text(text: str) -> dict:
    """
    Parses the announcement text using spaCy to extract named entities and other info.
    
    Args:
        text: The raw text from the OCR process.
        
    Returns:
        A dictionary with extracted entities.
    """
    t_start = time.perf_counter() if DEBUG_NLP else 0.0
    if DEBUG_NLP:
        try:
            prev = (text[:120] or "").replace("\n", " ")
        except Exception:
            prev = ""
        logger.info("DEBUG_NLP parse_announcement_text start len=%d preview=%r", len(text or ""), prev)
    if not text:
        if DEBUG_NLP:
            logger.warning("DEBUG_NLP parse_announcement_text empty input")
        return {"error": "Input text cannot be empty."}

    # Normalize et
    norm = normalize_text(text)
    if DEBUG_NLP:
        try:
            print(f"DEBUG_NLP norm start: {norm[:500]!r}")
        except: pass

    # HF NER (varsa) sonuçlarını topla; yoksa spaCy ile devam
    ner = load_hf_ner()
    entities = {
        "persons": [],
        "organizations": [],
        "locations": [],
        "dates": [],
        "money": [],
        "misc": [],
    }

    if ner is not None:
        # Uzun metinleri parçalayıp çalıştır (yaklaşık 800-1200 karakter bloklar)
        def chunk_lines(txt: str, max_len: int = 1000):
            buf, acc = [], 0
            for ln in txt.splitlines():
                ln2 = ln.strip()
                if not ln2:
                    # boş satırları blok sınırı gibi kullan
                    if buf:
                        yield "\n".join(buf)
                        buf, acc = [], 0
                    continue
                if acc + len(ln2) + 1 > max_len and buf:
                    yield "\n".join(buf)
                    buf, acc = [ln2], len(ln2)
                else:
                    buf.append(ln2)
                    acc += len(ln2) + 1
            if buf:
                yield "\n".join(buf)

        hf_results = []
        block_count = 0
        total_chars = 0
        t_all = time.perf_counter()
        for block in chunk_lines(norm):
            block_count += 1
            total_chars += len(block)
            try:
                t0 = time.perf_counter()
                res = ner(block)
                took = time.perf_counter() - t0
                logger.debug("HF NER block %d len=%d took=%.3fs", block_count, len(block), took)
                # bazı pipeline sürümleri tek öğe yerine dict dönebilir
                if isinstance(res, dict):
                    hf_results.append(res)
                else:
                    hf_results.extend(res)
            except Exception as e:
                logger.warning(f"HF NER blok hatası: {e}")
        logger.info("HF NER inference summary: blocks=%d chars=%d elapsed=%.3fs", block_count, total_chars, time.perf_counter() - t_all)

        # Sonuçları kategori listelerine aktar
        for r in hf_results:
            text_val = r.get("word") or r.get("text") or ""
            label = (r.get("entity_group") or r.get("entity") or "").upper()
            item = {"text": text_val, "label": label}
            if label.startswith("PER"):
                entities["persons"].append(item)
            elif label.startswith("ORG"):
                entities["organizations"].append(item)
            elif label.startswith("LOC"):
                entities["locations"].append(item)
            elif label.startswith("DATE"):
                entities["dates"].append(item)
            elif label.startswith("MONEY"):
                entities["money"].append(item)
            else:
                entities["misc"].append(item)
    else:
        # spaCy NER (yalnızca model varsa; aksi halde blank('tr') ile ents boş olur)
        doc = nlp_model(norm)
        for ent in getattr(doc, "ents", []):
            label = ent.label_.upper()
            entity_data = {"text": ent.text, "label": label}
            if label in ("PERSON", "PER"):
                entities["persons"].append(entity_data)
            elif label in ("ORG", "ORGANIZATION"):
                entities["organizations"].append(entity_data)
            elif label in ("GPE", "LOC", "LOCATION"):
                entities["locations"].append(entity_data)
            elif label in ("DATE",):
                entities["dates"].append(entity_data)
            elif label in ("MONEY",):
                entities["money"].append(entity_data)
            else:
                entities["misc"].append(entity_data)

    # Basit yanlış-pozitif kişi filtrelemesi (sıkılaştırılmış)
    def is_false_person(t: str) -> bool:
        t_norm = re.sub(r"[’']+$", "", t.strip())
        t_norm = re.sub(r"[,.;:]+$", "", t_norm)
        t_low = t_norm.lower()
        bad_keys = (
            "tl",
            "türk lira",
            "hisse",
            "madde",
            "sayfa",
            "tutanak",
            "genel kurul",
            "sicil",
            "gazete",
            "kimlik",
            "numara",
            "numaral",
        )
        if any(k in t_low for k in bad_keys):
            return True
        # Sayı içerenleri ele
        if re.search(r"\d", t_norm):
            return True
        toks = [x for x in re.split(r"\s+", t_norm) if x]
        # 2–4 kelime dışında kalanları ele (örn. üçlü adlar ve mürekkep soyadlar için)
        if not (2 <= len(toks) <= 4):
            return True
        # Soyad en az 2 harf (örn. ÖZ gibi iki harfli soyadlara izin ver)
        if len(toks[-1]) < 2:
            return True
        # Her token harf/tek tırnak/bağ ile sınırlı olmalı
        for tok in toks:
            if not re.fullmatch(r"[A-Za-zÇĞİÖŞÜçğıöşü'\-]+", tok):
                return True
        return False

    entities["persons"] = [e for e in entities["persons"] if not is_false_person(e["text"]) ]

    # --- Regex Tabanlı Ek Çıkarımlar ---
    # 1) MERSIS No (genelde 16 hane)
    mersis = find_first(r"MERS[İI]S\s*No\s*[:.]?\s*([0-9]{10,20})", norm)
    if mersis:
        entities["mersis_no"] = mersis

    # 2) Ticaret Sicil/Dosya No veya Sicil No
    sicil_dosya = find_first(r"Ticaret\s*Sicil(?:/Dosya)?\s*No\s*[:.]?\s*([A-ZÇĞİÖŞÜ0-9/\-]+)", norm)
    if sicil_dosya:
        entities["sicil_dosya_no"] = sicil_dosya

    # 3) Registration number (eski alan) – daha geniş kalıp
    registration = find_first(r"(Ticaret\s*Sicil(?:/Dosya)?\s*No|Sicil\s*No|Ticaret\s*Sicili\s*Numaras[ıi])\s*[:.]?\s*([A-ZÇĞİÖŞÜ0-9/\-]+)", norm)
    if registration:
        # find_first ikinci grup dönmüyor; bu yüzden manuel alalım
        m = re.search(r"(Ticaret\s*Sicil(?:/Dosya)?\s*No|Sicil\s*No|Ticaret\s*Sicili\s*Numaras[ıi])\s*[:.]?\s*([A-ZÇĞİÖŞÜ0-9/\-]+)", norm, re.IGNORECASE)
        if m:
            entities["registration_number"] = m.group(2).strip()

    # --- 4) Ticaret Unvanı ---
    trade_name = None
    used_block_inference = False
    old_trade_name_block: Optional[str] = None

    # Helper: Swift-style multiline extraction until next header
    def _nlp_extract_multiline_unvan(base_text: str, is_old: bool = False) -> Optional[str]:
        # Swift logic pattern: Capture until next known header (Adres, Tescil, Yukarida, Mudurler, etc.)
        hdr_prefix = r"Eski\s*" if is_old else r"(?![ \t#]*Eski\b)"
        # Regex matches 'Ticaret Unvani' (or variants) and stops at the next logical section
        # Refined: Added optional leading noise ([ \t#*|]*) to handle Markdown headers in extraction.
        pattern = (
            r"(?i)" + hdr_prefix + r"[ \t#*|]*(?:Yeni\s*)?(?:Ticaret\s*)?Unva[nm](?:[ıiİI])?(?:t)?\s*[:.：]*\s*"
            r"([\s\S]+?)"
            r"(?=\bAdres\b|\bTescil\b|\bYuka[r|rn][ıi]da\b|\bM[üu]d[üu]rler\b|\bY[öo]netim\b|\bİşletme\s+Konusu\b|\bMERS[İI]S\b|\bTicaret\s*Sicil\b|\bIlan\s*Sira\b|$)"
        )
        m = re.search(pattern, base_text)
        if m and m.group(1).strip():
            val = m.group(1).strip()
            # Clean noise from the block (Markdown markers, excessive spaces, stuck symbols)
            val = re.sub(r"\s+", " ", val)
            val = val.strip(" -*–·•\t|#")
            # Emergency cleanup for OCR segmentation errors (if headers were stuck to the name)
            surgical_tail = re.compile(r"\s*(?:##\s*)?(?:Adres|MERS[İI]S|Ticaret\s*Sicil|Ilan\s*Sira|Tescil).*$", re.IGNORECASE)
            val = surgical_tail.sub("", val).strip()
            return val if len(val) > 3 else None
        return None

    # 4.1) Swift-Style Block Extraction (Primary)
    # First, try identifying the trade name within the Docling-extracted segment
    tn_block = extract_trade_name_block_segment(text)
    if tn_block:
        val = _nlp_extract_multiline_unvan(tn_block)
        if val:
            if DEBUG_NLP: print(f"DEBUG_NLP SWIFT BLOCK found: {val!r}")
            trade_name = val
            used_block_inference = True
        
        old_val = _nlp_extract_multiline_unvan(tn_block, is_old=True)
        if old_val:
            old_trade_name_block = old_val

    # 4.2) Fallback to full text if block extraction didn't yield a result
    if not trade_name:
        val = _nlp_extract_multiline_unvan(norm)
        if val:
            if DEBUG_NLP: print(f"DEBUG_NLP SWIFT FULLTEXT found: {val!r}")
            trade_name = val
            used_block_inference = True

    # 4.4) ULTRA FALLBACK: Header Block Search (if no 'Ticaret Unvani' header found)
    # This catches "Continued" announcements or those where the name is at the top but unlabeled.
    # 4.4) ULTRA FALLBACK: Header Block Search (if no 'Ticaret Unvani' header found)
    # This catches "Continued" announcements or those where the name is at the top but unlabeled.
    if not trade_name:
        lines_all = [ln.strip() for ln in norm.splitlines()]
        # Scan first 15 lines for a string that looks like a company
        lines_top = [ln for ln in lines_all if ln][:15]
        # Common suffixes: LTD, STI, AS, ANONIM, LIMITED, SIRKETI, ISLETMESI, TASFIYE HALINDE
        comp_marker_re = re.compile(r"(?i)\b(?:LTD|ŞTİ|ŞTİ|A\.?Ş\.?|A\.?S\.?|ANON[İI]M|L[İI]M[İI]TED|S[İI]RKET[İI]?|[İŞ]LETMES[İI]|TASF[İI]YE(?:\s+HAL[İI]NDE)?)\b", re.IGNORECASE)
        # Avoid lines that are headers (TC, MERSIS, SICIL, etc.)
        header_noise_re = re.compile(r"(?i)^(T\.?C\.|MERS[İI]S|SICIL|ADRES|TESCIL|ILAN|SIRA|NO[:.]|ALACAKL[İI]LAR)", re.IGNORECASE)
        
        for ln in lines_top:
            # We want lines that have a company marker OR are clearly uppercase names
            is_company = bool(comp_marker_re.search(ln))
            is_noise = bool(header_noise_re.match(ln))
            # Sole proprietorship check: fully uppercase, at least 2 words, no excessive numbers
            is_sole = (ln.isupper() and len(ln.split()) >= 2 and not any(c.isdigit() for c in ln))
            
            if (is_company or is_sole) and not is_noise and len(ln) > 8:
                if DEBUG_NLP: print(f"DEBUG_NLP HEADER FALLBACK found: {ln!r} (sole={is_sole})")
                # Surgical cleanup: remove leading artifacts and trailing headers stuck on the same line
                ln = re.sub(r"^(?:#*\s*|-*\s*|\.\s*)", "", ln)
                ln = re.sub(r"^(?:T\.?C\.\s*)", "", ln, flags=re.IGNORECASE)
                ln = re.sub(r"\s*(?:MERS[İI]S|SICIL|ADRES|TESCIL|ILAN|SIRA).*$", "", ln, flags=re.IGNORECASE)
                trade_name = ln.strip()
                break
                if DEBUG_NLP: print(f"DEBUG_NLP scan line: {t!r} | is_stop={is_stop}")
                has_noise = bool(re.search(r"(\||\b(Uyruk|Kurucu|Dosya\s*No|ibraz\s+edilen|tasdikli|karar[ıi]|M[uü]d[uü]rl[uü]g[uü]nden|G[uü]ndemi)\b)", t, re.IGNORECASE))
                is_uh = is_upper_heavy(t)
                has_comp = bool(comp_pat.search(t))
                if DEBUG_NLP:
                    print(f"DEBUG_NLP last_resort check line='{t[:40]}...' is_stop={is_stop} has_noise={has_noise} is_uh={is_uh} has_comp={has_comp}")
                if is_stop or has_noise:
                    continue
                # Şirket eki var mı veya tamamen büyük harf mi?
                if (has_comp or is_uh) and len(t.split()) >= 2:
                    trade_name = t
                    break

    # --- 4.5) Inline / Phrasal Fallback ---
    # Sirketin unvanı ... SIRKETidir pattern'ı çok güçlüdür, başlık eşleşmesini bile ezebilir.
    # MODIFIED: Handling 'SIRKETidir' (no space) and case variations
    m_inline = re.search(r"S[ıiİI]rketin\s+unvan[ıiİI]?\s+(.*?)\s*[Ss][İIıi]RKET[İIıi]\s*dir[\s.:]*", norm, flags=re.IGNORECASE)
    if m_inline and m_inline.group(1).strip():
        val = m_inline.group(1).strip() + " ŞİRKETİ"
        if DEBUG_NLP: print(f"DEBUG_NLP INLINE OVERRIDE found: {val!r}")
        trade_name = val
    
    if not trade_name:
        # Match company suffix (ANONIM SIRKETI, LIMITED SIRKETI etc.) to find the end of the name
        # Allow standalone LIMITED/ANONIM/SIRKETI for embedded text
        comp_suffix = r"(?:ANON[Iİ]M(?:\s*S[İI]RKET[Iİ])?|L[Iİ]M[Iİ]TED(?:\s*S[İI]RKET[Iİ])?|[AL]\s*\.?\s*[ŞS]\s*\.?\s*[TİI])"
        m_yetki = re.search(rf"YETK[Iİ]L[Iİ]D[Iİ]R\s+([A-ZÇĞİÖŞÜ\s]{5,150}?{comp_suffix})", norm)
        if m_yetki:
            val = m_yetki.group(1).strip()
            if DEBUG_NLP: print(f"DEBUG_NLP YETKILIDIR found: {val!r}")
            trade_name = val

    # --- 4.6) Deep Scan Fallback (Final Surgical Effort) ---
    if not trade_name:
        # Search for first line that contains a confident company pattern
        # Allow standalone LIMITED/ANONIM/A.S for shorter names
        strict_comp = re.compile(r"(.*?)\b(A\s*\.?\s*[ŞS]\s*\.?|LTD\.?\s*[ŞS]T[İI]|L[İI]M[İI]TED(?:\s*[ŞS][İI]RKET[İI])?|ANON[İI]M(?:\s*[ŞS][İI]RKET[İI])?|ANONYME|S\s*\.?\s*A\s*\.?)\b", re.IGNORECASE)
        for ln in lines_all:
            t = ln.strip(" -*–·•\t|#").strip()
            if len(t) < 10: continue
            m = strict_comp.search(t)
            if m:
                extracted = m.group(0).strip()
                # Check for stop words inside the EXTRACTED part, not the whole line
                if not bool(re.search(r"(?i)\b(MERS[IIi1]S|Ticaret\s+Sicil|Sira\s*No|Adres|Tescil|Vekaletname)\b", extracted, re.IGNORECASE)):
                   # Clean up left garbage (e.g. 'tescil edilmistir . TASFIYE...')
                   cleanup = re.search(r"^.*?\s*([A-ZÇĞİÖŞÜ\d].*)$", extracted)
                   trade_name = cleanup.group(1) if cleanup else extracted
                   if DEBUG_NLP: print(f"DEBUG_NLP DEEP_SCAN_SURGICAL found: {trade_name!r}")
                   break

    if not trade_name:
        m_inline_old = re.search(r"[SŞ]irketin\s+unvanı?\s+(.*?)(?:dir|dır|dur|dür)\.?", norm, flags=re.IGNORECASE)
        if m_inline_old and m_inline_old.group(1).strip():
            trade_name = m_inline_old.group(1).strip()
    
    if DEBUG_NLP:
        try:
            print(f"DEBUG_NLP trade_name_result: {trade_name!r} (used_block={used_block_inference})")
        except Exception:
            pass

    if trade_name:
        # İdari Gürültü ve Belge Başlıklarını Temizle (VEKALETNAME, ASLI GIBIDIR vb.)
        noise_patterns = [
            r"^\s*#*\s*T\.?C\.?\b",
            r"^\s*#*\s*[İI]STANBUL\s+T[İI]CARET\s+S[İI]C[İI]L[İI]\s+M[ÜU]D[ÜU]RL[ÜU]G[ÜU]['’]NDEN\.?",
            r"^\s*#*\s*M[ÜU]D[ÜU]RL[ÜU]G[ÜU]\b",
            r"^\s*#*\s*S[OÖ]ZLE[SŞ]ME\s+YAPMA\s+YETK[Iİ].*?\b",
            r"^\s*#*\s*VEKALETNAME\b",
            r"^\s*#*\s*ASLI\s+G[Iİ]B[Iİ]D[Iİ]R\b",
            r"\b\d+\s*\.?\s*[İI]LAN\b\.?\s*$",
            r"##\s*Adres.*$", # Stuck headers
            r"##\s*[İI]lan\s*S[ıi]ra.*$",
            r"##\s*MERS[İI]S.*$"
        ]
        for pat in noise_patterns:
            trade_name = re.sub(pat, "", trade_name, flags=re.IGNORECASE).strip()

        # Unvan sonuna eklemlenmiş gürültüyü kes (Adres, Tescil, MERSIS vb.)
        stop_pat = re.compile(r"\b(?:Adres|(?:Yu(?:ka(?:r|rn|n)?[ıi]?da)|Yukarıda|Yukarida)|Tescil|Tescile|MERS[İI]S|Ticaret\s*Sicil|Eski\s+Adres|Telefon|İlan\s*Sira\s*No|Ilan\s*Sira\s*No|Sira\s*No|ad[ıi]na\s+hareket|ikamet\s+eden|temsilci|Y[öo]netim\s+Kurulu|Genel\s+M[üu]d[üu]r|M[üu]d[üu]rl[üu]g[üu](?:nden|ne)?|Karar[ıi]|Hususlar|G[üu]ndem)\b", re.IGNORECASE)
        mstop = stop_pat.search(trade_name)
        if mstop:
            trade_name = trade_name[: mstop.start()].strip()
        # Adres-benzeri içerik varsa soldan kes (unvanı kirleten adres parçacıklarını at)
        addressish_final = re.compile(r"\b(MAH\.?|MAHALLES[İI]|CAD\.?|CADDES[İI]|CD\.?|SOK\.?|SOKA[ĞG][ıi]|SK\.?|BLV\.?|BULVAR[ıi]?|NO\b|KAT\b|DA[İI]RE\b|APT\.?|S[İI]TE|OSB|İÇ\s*KAP[İI]|DIŞ\s*KAP[İI]|BLOK)\b|[A-ZÇĞİÖŞÜ]{2,}\s*/\s*[A-ZÇĞİÖŞÜ]{2,}", re.IGNORECASE)
        maddr = addressish_final.search(trade_name)
        if maddr and maddr.start() > 0:
            left = trade_name[: maddr.start()].strip()
            # Sadece makul bir unvan kaldıysa uygula (en az 3 harf, çok kısa değil)
            if len(re.sub(r"[^A-Za-zÇĞİÖŞÜçğıöşü]", "", left)) >= 3:
                trade_name = left
        # Makul uzunluk sınırı ve sadeleştirme
        trade_name = re.sub(r"\s+", " ", trade_name).strip(" -*–·•\t|#")
        if len(trade_name) > 150:
            cuts = re.split(r"(?:\s{2,}|,|;)", trade_name, maxsplit=1)
            trade_name = cuts[0].strip()

        # --- UNIVERSAL RECURSIVE REFINER ---
        # This solves 'TC.', '##', 'Müdürlüğü'nden', etc. universally
        refine_pat = re.compile(
            r"^([#\*\s\-\:：.,;]+|"
            r"T\.?C\.?(\s|(?=[A-ZÇĞİÖŞÜ]))|"
            r"TiCARET\s+SiCiL[İI](\s+MÜDÜRLÜĞÜ)?\s*[:：.\-]*|"
            r"MERS[İI]S\s*No.*?\:|"
            r"[İI]lan\s*S[ıi]ra\s*No.*?\:|"
            r"S[ıi]ra\s*No.*?\:)"
            r"|([#\*\s\-\:：.,;]+|"
            r"MÜDÜRLÜĞÜ['’]NDEN\.?|"
            r"MÜDÜRLÜĞÜNE\.?|"
            r"MÜDÜRLÜĞÜ\.?)$",
            re.IGNORECASE
        )
        
        iteration = 0
        while iteration < 5:
            prev = trade_name
            trade_name = refine_pat.sub("", trade_name).strip()
            # Special case: if it starts with 'ISTANBUL', 'ANKARA' etc followed by stuff we want to keep, leave it.
            # But if it's 'TC. ISTANBUL TICARET SICILI MUDURLUGU', the whole thing is noise.
            if trade_name == prev: break
            iteration += 1

        trade_name = trade_name.strip(":,.- ")

        # PREAMBLE CLEANING: 'Istanbul da Maslak mukim;' vs.
        # Allow room for City/District names in the preamble
        preamble_pat = re.compile(r"^.*?\b(?:da|de|ta|te)\b.*?\b(?:mukim|bulunan|ikamet\s+eden)\b\s*[:;]?", re.IGNORECASE)
        trade_name = preamble_pat.sub("", trade_name).strip()
        # 'Merkezi ... olan' temizle
        merkezi_pat = re.compile(r"^Merkezi\s+.*?\s+olan\s+", re.IGNORECASE)
        trade_name = merkezi_pat.sub("", trade_name).strip()

        # Sonda içindekiler/ilan işaretçilerinden "1.İLAN/1.ILAN" benzeri sonekleri kaldır
        trade_name = re.sub(r"\s*\b\d+\s*\.?\s*[İI]LAN\b\.?\s*$", "", trade_name, flags=re.IGNORECASE).strip()

        # --- Doğrulama/Kabul Kriterleri (precision artırımı) ---
        def _digit_ratio(s: str) -> float:
            if not s:
                return 0.0
            digits = sum(ch.isdigit() for ch in s)
            alnum = sum(ch.isalnum() for ch in s)
            return (digits / max(alnum, 1))

        comp_pat_v = re.compile(
            r"\b("
            r"A\s*\.?\s*Ş\s*\.?|"                                  # AŞ, A.Ş.
            r"LTD\.?\s*ŞT[İIıi]\.?.?|"                          # LTD. ŞTİ. (tüm i varyantları)
            r"L[İIıi]M[İIıi]TED(?:\s+(?:Ş|S)[İIıi]RKET[İIıi])?|"      # LİMİTED (ŞİRKETİ)
            r"ANON[İIıi]M(?:\s+(?:Ş|S)[İIıi]RKET[İIıi])?|"            # ANONİM (ŞİRKETİ)
            r"SAN(?:\.?|AY[İIıi])?\s*VE\s*T[İIıi]C(?:\.?|ARET)?|" # SAN... VE TİC(ARET)
            r"KOLEKT[İIıi]F|KOMAND[İIıi]T|KOOP(?:ERAT[İIıi]F)?|"
            r"VAKFI|VAKF[İIıi]|DERNE[GĞ][İIıi]|"
            r"INSAAT|T[İI]CARET|TUR[İI]ZM|SANAY[İI]|GIDA|TEKST[İI]L|H[İI]ZMETLER[İI]|" # Professional indicators for Sole Props
            r"[İIıi]KT[İIıi]SAD[İIıi]\s+[İIıi]ŞLETME[SŞ][İIıi]"
            r")\b",
            re.IGNORECASE,
        )

        bad_start_v = re.compile(r"(\b(Adres|(?:Yu(?:ka(?:r|rn|n)?[ıi]?da)|Yukarıda|Yukarida)|Tescil|Tescile|MERS[İI]S|Ticaret\s*Sicil|Eski\s+Adres|Telefon|İlan\s*Sira\s*No|Ilan\s*Sira\s*No|Sira\s*No|Dosya|ibraz\s+edilen|Kurucu|Uyruk|tasdikli|\|)\b)", re.IGNORECASE)

        tn = trade_name.strip()
        valid = True
        # Reddetme kuralları
        if len(tn) < 6:
            valid = False
        if bad_start_v.search(tn):
            valid = False
        if _digit_ratio(tn) > 0.3:
            valid = False
            
        # 4) Sürreal gürültü kelimeleri: İlan, Tasfiyeden, Çağrı vb. (Tek başına unvan olamazlar)
        if valid and re.search(r"(?i)\b(\d*\.?\s*[İI]LAN|TASF[İI]YEDEN|[ÇC]A[GĞSŠ]R[Iİ1])\b", tn):
             # Eğer yanında LTD/AS gibi güçlü bir ibare yoksa reddet
             if not comp_pat_v.search(tn):
                 valid = False

        # Kabul sinyalleri: şirket soneki ya da başlığa/numara alanlarına yakınlık
        if valid and not comp_pat_v.search(tn):
            # Başlık yakınlığı: ilk ~700 karakter veya ilk 20 satıra denk gelmesi
            lines_all_v = norm.splitlines()
            # Unvanın metin içinde konumunu yaklaşık eşleştir (boşluk toleranslı)
            esc = re.escape(tn)
            esc = esc.replace(r"\ ", r"\s+")
            mpos = re.search(rf"{esc}", norm, re.IGNORECASE)
            char_idx = mpos.start() if mpos else len(norm)
            # Satır indeksi hesapla
            if mpos:
                line_idx = norm[:char_idx].count("\n")
            else:
                line_idx = 10**6
            header_close = (char_idx <= 700) or (line_idx <= 20)

            # MERSIS/Sicil yakınlığı (±10 satır)
            mersis_sicil_idxs = []
            for i, l in enumerate(lines_all_v):
                if re.search(r"MERS[İI]S\s*No", l, flags=re.IGNORECASE) or re.search(r"Ticaret\s*Sicil(?:/Dosya)?\s*No", l, flags=re.IGNORECASE):
                    mersis_sicil_idxs.append(i)
            near_nums = False
            if mpos and mersis_sicil_idxs:
                near_nums = any(abs(line_idx - k) <= 10 for k in mersis_sicil_idxs)

            if DEBUG_NLP:
                print(f"DEBUG_NLP validation tn='{tn[:30]}' head_close={header_close} near_nums={near_nums} used_block={used_block_inference}")

            if not (header_close or near_nums or used_block_inference):
                valid = False

        if valid:
            if DEBUG_NLP:
                print(f"DEBUG_NLP ACCEPTED tn='{tn}'")
            entities["trade_name"] = tn
            entities["organizations"].append({"text": tn, "label": "ORG"})
            if old_trade_name_block:
                entities["old_trade_name"] = re.sub(r"\s+", " ", old_trade_name_block).strip()
        # Geçersizse unvanı düşür (precision lehine)
    
    # 5) Adres(ler) – önce kesin blok: "Adres:" -> "Yukarıdaki Bilgiler"
    # Not: Eğer metinde "Eski/Önceki Adres(i)" başlığı varsa, anlatım paragrafından ("... adresinden ... adresine ...")
    # eski/yeni adres çekmeye çalışmayacağız; başlık zaten esas kaynaktır.
    has_old_address_header = bool(re.search(r"^\s*(?:Eski\s*Adres|Eski\s*Adresi|Önceki\s*Adres|Önceki\s*Adresi)\b", norm, flags=re.IGNORECASE | re.MULTILINE))
    addr_block = extract_address_block_segment(text)
    if addr_block:
        # Adres bloğunu tüketim için tek satıra indir (tire ile bölünmüş satırları birleştir)
        base_addr = _dehyphenate_lines(addr_block)
        # İlk kaba temizlik: adres satırına yapışmış başlıkları kes
        stop_pat_inline = re.compile(r"\b(?:Yu(?:ka(?:r|rn|n)?[ıi]?da)|Yukarıda|Yukarida|Tescil|Tescile|MERS[İI]S|Ticaret\s*Sicil|Telefon|Tel|GSM|Faks|İlan\s*Sira\s*No|Ilan\s*Sira\s*No|Sira\s*No|Madde|Gündem|Gundem|Genel\s+Kurul|Vekaletname\b|Yeni\s*Ticaret\s*Sicil[iı]\s*M[üu]d[üu]rl[üu]g[üu][üu]?|Yeni\s*Sicil\s*No|Yeni\s*Adres|Merkezin\s+Kay\w*\s+Oldu\w*\s+M[üu]d[üu]rl[üu](?:g[üu]|k)|Eski\s*Ticaret\s*Sicil[iı]\s*M[üu]d[üu]rl[üu]g[üu][üu]?|Eski\s*Sicil\s*No|Eski\s*Adres|bir\s+veya\s+birka[çc]\s+m[üu]d[üu]r|Kimlik\s+No|T[üu]rkiye\s+Cumhuriyeti)\b", re.IGNORECASE)
        a2 = re.sub(r"\s+", " ", base_addr or "").strip()
        mstop = stop_pat_inline.search(a2)
        if mstop:
            a2 = a2[: mstop.start()].strip()
        # Çok kısa ya da boşsa yazma; değilse listeye koy
        entities["addresses"] = [a2] if (a2 and len(a2) >= 8) else []
        # Eski Adres(ler) için bağımsız tarama (başlık tabanlı ve tek satırlı)
        old_addresses: List[str] = []
        lines_list = norm.splitlines()
        stop_line_pat = re.compile(r"^(?:Yu(?:ka(?:r|rn|n)?[ıi]?da)|Yukarıda|Yukarida|Tescil|Tescile|MERS[İI]S|Ticaret\s*Sicil|Telefon|İlan\s*Sira\s*No|Ilan\s*Sira\s*No|Sira\s*No|Gündem|Gundem|Genel\s+Kurul|Vekaletname)\b", re.IGNORECASE)
        # Başlık yeniden başlıyorsa (Yeni Adres, Adres vb.) da durdur
        header_break_pat = re.compile(r"^(?:Yeni\s*Adres|Adres|Merkez(?:i)?\s*:|Şube\s*Adresi|İkametg[aâ]h\s*Adresi|Şirket\s*Merkezi|İşletmenin\s*Merkezi|Önceki\s*Adres|Önceki\s*Adresi|Eski\s*Adresi)\b", re.IGNORECASE)
        negative_in_line = re.compile(r"\bikamet\s+eden\b", re.IGNORECASE)
        addressish = re.compile(r"\b(Mah\.?|Mahallesi|Cad\.?|Caddesi|Cd\.?|Sok\.?|Sokağı|Sk\.?|Bulvar[ıi]?|Blv\.?|Blok|No\b|Kat\b|Daire\b|Apt\.?|Apartman|Sit\.?|Site|OSB|Organize\s*Sanayi|İl\b|İlçe\b|/)\b", re.IGNORECASE)
        i = 0
        while i < len(lines_list):
            raw = lines_list[i].strip()
            if not raw:
                i += 1
                continue
            # "Eski/Önceki Adres(i)" başlıkları için çok satırlı yakalama
            if re.match(r"^\s*(?:Eski\s*Adres|Eski\s*Adresi|Önceki\s*Adres|Önceki\s*Adresi)\b", raw, flags=re.IGNORECASE):
                m = re.match(r"^\s*(?:Eski\s*Adres|Eski\s*Adresi|Önceki\s*Adres|Önceki\s*Adresi)\s*[:.]?\s*(.*)$", raw, flags=re.IGNORECASE)
                first = (m.group(1).strip() if m else "")
                if negative_in_line.search(raw):
                    i += 1
                    continue
                buf = [first] if first else []
                j = i + 1
                join_count = 0
                while j < len(lines_list) and join_count < 4:
                    nxt = lines_list[j].strip(" -*–·•\t").strip()
                    if not nxt:
                        break
                    if stop_line_pat.match(nxt) or header_break_pat.match(nxt):
                        break
                    if negative_in_line.search(nxt):
                        j += 1
                        continue
                    if addressish.search(nxt) or (len(nxt) >= 12 and re.search(r"\d", nxt)):
                        buf.append(nxt)
                        join_count += 1
                        j += 1
                        continue
                    else:
                        break
                cand = _dehyphenate_lines("\n".join(buf))
                if cand:
                    mstop = re.search(r"\b(?:Yu(?:ka(?:r|rn|n)?[ıi]?da)|Yukarıda|Yukarida|Tescil|Tescile|MERS[İI]S|Ticaret\s*Sicil|Telefon|Tel|GSM|Faks|İlan\s*Sira\s*No|Ilan\s*Sira\s*No|Sira\s*No|Madde|Gündem|Gundem|Genel\s+Kurul|Vekaletname\b|Yeni\s*Ticaret\s*Sicil[iı]\s*M[üu]d[üu]rl[üu]g[üu][üu]?|Yeni\s*Sicil\s*No|Yeni\s*Adres)" , cand, flags=re.IGNORECASE)
                    if mstop:
                        cand = cand[: mstop.start()].strip()
                if cand and not negative_in_line.search(cand):
                    if len(cand) > 300:
                        cand = cand[:300].rstrip()
                    old_addresses.append(cand)
                i = j
                continue
            i += 1
        # Basit tek satır "Eski/Önceki Adres(i)" yakalama — eğer başlık zaten varsa tekrar arama yapma
        if not has_old_address_header:
            for m in re.finditer(r"^\s*(?:Eski\s*Adres|Eski\s*Adresi|Önceki\s*Adres|Önceki\s*Adresi)\s*[:.]?\s*(.+)$", norm, flags=re.IGNORECASE | re.MULTILINE):
                val = (m.group(1) or "").strip()
                if val:
                    old_addresses.append(val)
            # Parantez içi eski/önceki ibaresi barındıran adres benzer tek satırlar
            for m in re.finditer(r"\((?:\s*(?:Eski|Önceki)[^)]*)\)\s*[:\-–]?\s*(.+)$", norm, flags=re.IGNORECASE | re.MULTILINE):
                val = (m.group(1) or "").strip()
                if val:
                    old_addresses.append(val)
        if old_addresses:
            # Temizle ve dedup et
            cleaned_old: List[str] = []
            stop_pat_addr = re.compile(r"\b(?:Yu(?:ka(?:r|rn|n)?[ıi]?da)|Yukarıda|Yukarida|Tescil|Tescile|MERS[İI]S|Ticaret\s*Sicil|Telefon|Tel|GSM|Faks|İlan\s*Sira\s*No|Ilan\s*Sira\s*No|Sira\s*No|Madde|Gündem|Gundem|Genel\s+Kurul|Vekaletname\b|Yeni\s*Ticaret\s*Sicil[iı]\s*M[üu]d[üu]rl[üu]g[üu][üu]?|Yeni\s*Sicil\s*No|Yeni\s*Adres)\b", re.IGNORECASE)
            for a in old_addresses:
                a = re.sub(r"\s+", " ", a).strip()
                if not a or negative_in_line.search(a):
                    continue
                mstop = stop_pat_addr.search(a)
                if mstop:
                    a = a[: mstop.start()].strip()
                if a and len(a) >= 8:
                    cleaned_old.append(a if len(a) <= 300 else a[:300].rstrip())
            if cleaned_old:
                # substring bazlı deduplikasyon: kısa (alt string) olanı at, daha kapsamlı olanı koru
                dedup_old: List[str] = []
                for i, ai in enumerate(cleaned_old):
                    ai_l = ai.lower()
                    keep = True
                    for j, aj in enumerate(cleaned_old):
                        if i == j:
                            continue
                        aj_l = aj.lower()
                        if aj_l in ai_l and aj_l != ai_l:
                            # ai daha uzun ve aj'yi kapsıyor -> aj kalsın, ai'yi at
                            # Ancak burada kısa olanı (aj) atmak istiyoruz; bu nedenle ters koşulu kullanalım
                            pass
                        if ai_l in aj_l and ai_l != aj_l:
                            # ai kısa ve aj tarafından kapsanıyor -> ai'yi at
                            keep = False
                            break
                    if keep:
                        dedup_old.append(ai)
                entities["old_addresses"] = unique_list(dedup_old if dedup_old else cleaned_old)
    else:
        # Fallback: başlık tespiti + çok satır birleştirme + gürültü filtresi
        addresses: List[str] = []
        old_addresses: List[str] = []
        lines_list = norm.splitlines()
        header_pat = re.compile(r"^(?:Adres|Eski\s*Adres|Eski\s*Adresi|Önceki\s*Adres|Önceki\s*Adresi|Yeni\s*Adres|Merkez(?:i)?\s*:|Şube\s*Adresi|İkametg[aâ]h\s*Adresi|Şirket\s*Merkezi|İşletmenin\s*Merkezi)\s*[:.]?\s*(.*)$", re.IGNORECASE)
        stop_line_pat = re.compile(r"^(?:Yu(?:ka(?:r|rn|n)?[ıi]?da)|Yukarıda|Yukarida|Tescil|Tescile|MERS[İI]S|Ticaret\s*Sicil|Telefon|Tel|GSM|Faks|İlan\s*Sira\s*No|Ilan\s*Sira\s*No|Sira\s*No|Madde|Gündem|Gundem|Genel\s+Kurul|Vekaletname\b)", re.IGNORECASE)
        negative_in_line = re.compile(r"\bikamet\s+eden\b", re.IGNORECASE)
        addressish = re.compile(r"\b(Mah\.?|Mahallesi|Cad\.?|Caddesi|Cd\.?|Sok\.?|Sokağı|Sk\.?|Bulvar[ıi]?|Blv\.?|Blok|No\b|Kat\b|Daire\b|Apt\.?|Apartman|Sit\.?|Site|OSB|Organize\s*Sanayi|İl\b|İlçe\b|/)\b", re.IGNORECASE)
        i = 0
        while i < len(lines_list):
            raw = lines_list[i].strip()
            if not raw:
                i += 1
                continue
            m = header_pat.match(raw)
            if m:
                first = m.group(1).strip()
                if negative_in_line.search(raw):
                    i += 1
                    continue
                buf = [first] if first else []
                j = i + 1
                join_count = 0
                while j < len(lines_list) and join_count < 4:
                    nxt = lines_list[j].strip(" -*–·•\t").strip()
                    if not nxt:
                        break
                    if stop_line_pat.match(nxt):
                        break
                    if negative_in_line.search(nxt):
                        j += 1
                        continue
                    # devam satırı adres benzer ise ekle
                    if addressish.search(nxt) or (len(nxt) >= 12 and re.search(r"\d", nxt)):
                        buf.append(nxt)
                        join_count += 1
                        j += 1
                        continue
                    else:
                        break
                # Çok satırlı adres adayını tire birleştirme ile tek satıra indir
                cand = _dehyphenate_lines("\n".join(buf))
                if cand:
                    mstop = re.search(r"\b(?:Yu(?:ka(?:r|rn|n)?[ıi]?da)|Yukarıda|Yukarida|Tescil|Tescile|MERS[İI]S|Ticaret\s*Sicil|Telefon|Tel|GSM|Faks|İlan\s*Sira\s*No|Ilan\s*Sira\s*No|Sira\s*No|Madde\b|Yeni\s*Ticaret\s*Sicil[iı]\s*M[üu]d[üu]rl[üu]g[üu][üu]?|Yeni\s*Sicil\s*No|Yeni\s*Adres)" , cand, flags=re.IGNORECASE)
                    if mstop:
                        cand = cand[: mstop.start()].strip()
                if cand and not negative_in_line.search(cand):
                    if len(cand) > 300:
                        cand = cand[:300].rstrip()
                    # Başlık "Eski/Önceki Adres(i)" ise sadece old_addresses'e ekle (addresses'e ekleme)
                    if re.match(r"^\s*(?:Eski\s*Adres|Eski\s*Adresi|Önceki\s*Adres|Önceki\s*Adresi)\b", raw, flags=re.IGNORECASE):
                        old_addresses.append(cand)
                    else:
                        addresses.append(cand)
                i = j
                continue
            i += 1
        # Basit yakalamaları da ekle (kaçan tek satırlılar)
        for m in re.finditer(r"^\s*Adres\s*[:.]?\s*(.+)$", norm, flags=re.IGNORECASE | re.MULTILINE):
            addresses.append(m.group(1).strip())
        if not has_old_address_header:
            for m in re.finditer(r"^\s*(?:Eski\s*Adres|Eski\s*Adresi|Önceki\s*Adres|Önceki\s*Adresi)\s*[:.]?\s*(.+)$", norm, flags=re.IGNORECASE | re.MULTILINE):
                val = m.group(1).strip()
                # Eski adresi yalnızca old_addresses'e ekle
                old_addresses.append(val)
            # Parantez içi eski/önceki ibaresi barındıran tek satırlar
            for m in re.finditer(r"\((?:\s*(?:Eski|Önceki)[^)]*)\)\s*[:\-–]?\s*(.+)$", norm, flags=re.IGNORECASE | re.MULTILINE):
                val = (m.group(1) or "").strip()
                if val:
                    old_addresses.append(val)
        for m in re.finditer(r"^\s*Yeni\s*Adres\s*[:.]?\s*(.+)$", norm, flags=re.IGNORECASE | re.MULTILINE):
            addresses.append(("Yeni: " + m.group(1).strip()))
        if addresses:
            cleaned = []
            stop_pat_addr = re.compile(r"\b(?:Yu(?:ka(?:r|rn|n)?[ıi]?da)|Yukarıda|Yukarida|Tescil|Tescile|MERS[İI]S|Ticaret\s*Sicil|Telefon|Tel|GSM|Faks|İlan\s*Sira\s*No|Ilan\s*Sira\s*No|Sira\s*No|Madde|Gündem|Gundem|Genel\s+Kurul|Vekaletname\b|Merkezin\s+Kay\w*\s+Oldu\w*\s+M[üu]d[üu]rl[üu](?:g[üu]|k))\b", re.IGNORECASE)
            noise_fragments = re.compile(r"\b(ini\s+süresi\s+içinde|tebligat\s+sirkete\s+yapilmis\s+sayilir|fesih\s+sebebi\s+sayilir)\b", re.IGNORECASE)
            for a in addresses:
                a = re.sub(r"\s+", " ", a).strip()
                if not a or negative_in_line.search(a):
                    continue
                if a.upper().startswith("NAKLI"):
                    continue
                if noise_fragments.search(a):
                    continue
                mstop = stop_pat_addr.search(a)
                if mstop:
                    a = a[: mstop.start()].strip()
                if a and len(a) >= 8:
                    cleaned.append(a if len(a) <= 300 else a[:300].rstrip())
            # substring bazlı deduplikasyon: kısa adresi koru (min-cover)
            dedup = []
            for i, ai in enumerate(cleaned):
                ai_l = ai.lower()
                keep = True
                for j, aj in enumerate(cleaned):
                    if i == j:
                        continue
                    aj_l = aj.lower()
                    # Eğer ai, aj'yi kapsıyorsa (ai daha uzun süperstring), ai'yi at
                    if aj_l in ai_l and aj_l != ai_l:
                        keep = False
                        break
                if keep:
                    dedup.append(ai)
            if dedup:
                entities["addresses"] = unique_list(dedup)
        # 5c) "... adresi <OLD> adresinden, <NEW> adresine ..." kalıbından SADECE eski adres çıkarımı
        # Eğer metinde 'Eski/Önceki Adres' başlığı varsa, bu anlatım kalıplarını kullanma (çiftleme/bozulma olmasın)
        if not has_old_address_header:
            try:
                # Tek satırda yakalayabilmek için satır sonlarını yumuşatılmış boşlukla eşleştir
                # Çok açgözlü olmamak için adres parçalarını 12-220 karakter arası kısıtla
                # Öncelik: büyük harf ağırlıklı adres bloklarını tercih eden kalıp
                pat_uc = re.compile(
                    r"[sş]irketin\s+adresi\s+([A-ZÇĞİÖŞÜ0-9\s\./:-]{8,240}?)\s+adresinden\s*,?\s*([A-ZÇĞİÖŞÜ0-9\s\./:-]{8,240}?)\s+adresine",
                    re.IGNORECASE | re.DOTALL,
                )
                def _clean_addr(x: str) -> str:
                    x2 = _dehyphenate_lines(x)
                    x2 = re.sub(r"\s+", " ", x2).strip()
                    return x2[:300].rstrip()

                for m in pat_uc.finditer(norm):
                    old_raw = (m.group(1) or '').strip()
                    new_raw = (m.group(2) or '').strip()
                    old_c = _clean_addr(old_raw)
                    new_c = _clean_addr(new_raw)
                    if old_c:
                        entities.setdefault('old_addresses', [])
                        if old_c not in entities['old_addresses']:
                            entities['old_addresses'].append(old_c)
                # Genel kalıp (her ihtimale karşı)
                pat = re.compile(
                    r"adresi\s+(?P<old>.{12,220}?)\s+adresinden\s*,?\s*(?P<new>.{12,220}?)\s+adresine",
                    re.IGNORECASE | re.DOTALL,
                )
                for m in pat.finditer(norm):
                    old_raw = (m.group('old') or '').strip()
                    new_raw = (m.group('new') or '').strip()
                    old_c = _clean_addr(old_raw)
                    new_c = _clean_addr(new_raw)
                    if old_c:
                        entities.setdefault('old_addresses', [])
                        if old_c not in entities['old_addresses']:
                            entities['old_addresses'].append(old_c)
                # Yeni varyant: "... şirketin adresi <OLD> olan adresi <NEW> ..."
                pat_olan_uc = re.compile(
                    r"[sş]irketin\s+adresi\s+(?P<old>[A-ZÇĞİÖŞÜ0-9\s\./:-]{8,240}?)\s+olan\s+adresi\s+(?P<new>[A-ZÇĞİÖŞÜ0-9\s\./:-]{8,240}?)(?:\s+olarak|\s+g[üu]ncell|\s+deg[iı]şt|\s+değ[iı]şt|\s*/|\s*$)",
                    re.IGNORECASE | re.DOTALL,
                )
                for m in pat_olan_uc.finditer(norm):
                    old_raw = (m.group('old') or '').strip()
                    new_raw = (m.group('new') or '').strip()
                    old_c = _clean_addr(old_raw)
                    if old_c:
                        entities.setdefault('old_addresses', [])
                        if old_c not in entities['old_addresses']:
                            entities['old_addresses'].append(old_c)
            except Exception as e:
                print(f"An error occurred: {e}")
        # 5b) Toplantı davet metinlerinde geçen '"<ADRES>" adresinde/ adresindeki' kalıbından adres çıkarımı
        #     (ör. "Macun Mahallesi, 177.Cadde No.15/202 ..." adresinde/ adresindeki ...)
        try:
            meet_addrs: List[str] = []
            # Öncelik: tırnak içindeki adres + 'adresinde/ adresindeki'
            patt = re.compile(r'["“](?P<addr>[^"”]{8,220})["”]\s+adresind(?:e|eki)\b', re.IGNORECASE)
            for m in patt.finditer(norm):
                cand = (m.group('addr') or '').strip().strip('"“”')
                cand = re.sub(r"\s+", " ", cand).strip()
                if not cand:
                    continue
                # Adres benzer sinyaller ve olumsuz bağlam kontrolü
                if addressish.search(cand) and not negative_in_line.search(cand):
                    meet_addrs.append(cand[:300].rstrip())
            # İkinci öncelik: tırnaksız ama doğrudan '... Ankara adresinde' gibi yapılar
            if not meet_addrs:
                patt2 = re.compile(r"(?P<addr>(?:[A-Z0-9ÇĞİÖŞÜ][^\n]{6,220}?))\s+adresind(?:e|eki)\b", re.IGNORECASE)
                for m in patt2.finditer(norm):
                    cand = (m.group('addr') or '').strip()
                    cand = re.sub(r"\s+", " ", cand).strip()
                    if not cand:
                        continue
                    if addressish.search(cand) and not negative_in_line.search(cand):
                        meet_addrs.append(cand[:300].rstrip())
            if meet_addrs:
                # Mevcut adreslerle birleştir ve yeniden temizle; ancak öncelik toplantı-adresi kalıbında
                base = entities.get("addresses") or []
                merged = unique_list(meet_addrs + base)
                stop_pat_inline = re.compile(r"\b(?:Yu(?:ka(?:r|rn|n)?[ıi]?da)|Yukarıda|Yukarida|Tescil|Tescile|MERS[İI]S|Ticaret\s*Sicil|Telefon|Tel|GSM|Faks|İlan\s*Sira\s*No|Ilan\s*Sira\s*No|Sira\s*No|Madde|Gündem|Gundem|Genel\s+Kurul|Vekaletname\b)\b", re.IGNORECASE)
                cleaned2: List[str] = []
                for a in merged:
                    a2 = re.sub(r"\s+", " ", (a or "")).strip()
                    if not a2 or negative_in_line.search(a2):
                        continue
                    # Eğer uzun bir paragraf ise ve içinde '"..." adresinde/ adresindeki' geçiyorsa, tırnak içindeki bölümü adres olarak al
                    mqa = re.search(r'["“]([^"”]{8,220})["”]\s+adresind(?:e|eki)\b', a2, re.IGNORECASE)
                    if mqa:
                        a2 = mqa.group(1).strip()
                    else:
                        # Tırnaksız varyant için sınırlı bir geri dönüşüm (çok agresif olmadan)
                        mqa2 = re.search(r'([A-Z0-9ÇĞİÖŞÜ][^\n]{8,220}?)\s+adresind(?:e|eki)\b', a2, re.IGNORECASE)
                        if mqa2 and addressish.search(mqa2.group(1)):
                            a2 = mqa2.group(1).strip()
                    mstop = stop_pat_inline.search(a2)
                    if mstop:
                        a2 = a2[: mstop.start()].strip()
                    if a2 and len(a2) >= 8 and addressish.search(a2):
                        cleaned2.append(a2 if len(a2) <= 300 else a2[:300].rstrip())
                if cleaned2:
                    entities["addresses"] = unique_list(cleaned2)
                else:
                    entities["addresses"] = unique_list(meet_addrs)
        except Exception:
            pass
        # Eski adresler için ayrı temizleme ve deduplikasyon
        if old_addresses:
            cleaned_old = []
            stop_pat_addr = re.compile(r"\b(?:Yu(?:ka(?:r|rn|n)?[ıi]?da)|Yukarıda|Yukarida|Tescil|Tescile|MERS[İI]S|Ticaret\s*Sicil|Telefon|Tel|GSM|Faks|İlan\s*Sira\s*No|Ilan\s*Sira\s*No|Sira\s*No|Madde\b|Yeni\s*Ticaret\s*Sicil[iı]\s*M[üu]d[üu]rl[üu]g[üu][üu]?|Yeni\s*Sicil\s*No|Yeni\s*Adres)\b", re.IGNORECASE)
            for a in old_addresses:
                a = re.sub(r"\s+", " ", a).strip()
                if not a or negative_in_line.search(a):
                    continue
                mstop = stop_pat_addr.search(a)
                if mstop:
                    a = a[: mstop.start()].strip()
                if a and len(a) >= 8:
                    cleaned_old.append(a if len(a) <= 300 else a[:300].rstrip())
            if cleaned_old:
                entities["old_addresses"] = unique_list(cleaned_old)

    # --- Tescil Edilen Hususlar / Tescile Delil Olan Belgeler ---
    hususlar_list, belgeler_text = extract_tescil_sections(norm)
    if hususlar_list:
        entities["hususlar"] = hususlar_list
    if belgeler_text:
        entities["belgeler"] = belgeler_text

    # 5d) (global) "... adresi <OLD> adresinden, <NEW> adresine ..." kalıbı (adres bloğu bulunsa da çalışsın)
    # Ancak metinde 'Eski/Önceki Adres' başlığı varsa, bu global çıkarımı atla (esas veri başlıktan alınır)
    if not has_old_address_header:
        try:
            # Önce büyük harf ağırlıklı kalıp
            pat_global_uc = re.compile(
                r"[sş]irketin\s+adresi\s+([A-ZÇĞİÖŞÜ0-9\s\./:-]{8,240}?)\s+adresinden\s*,?\s*([A-ZÇĞİÖŞÜ0-9\s\./:-]{8,240}?)\s+adresine",
                re.IGNORECASE | re.DOTALL,
            )
            def _clean_addr(x: str) -> str:
                x2 = _dehyphenate_lines(x)
                x2 = re.sub(r"\s+", " ", x2).strip()
                return x2[:300].rstrip()

            matched_any = False
            for m in pat_global_uc.finditer(norm):
                old_raw = (m.group(1) or '').strip()
                new_raw = (m.group(2) or '').strip()
                old_c = _clean_addr(old_raw)
                new_c = _clean_addr(new_raw)
                if old_c:
                    entities.setdefault('old_addresses', [])
                    if old_c not in entities['old_addresses']:
                        entities['old_addresses'].append(old_c)
                        matched_any = True
        # Genel kalıp
            pat_global = re.compile(
                r"adresi\s+(?P<old>.{12,220}?)\s+adresinden\s*,?\s*(?P<new>.{12,220}?)\s+adresine",
                re.IGNORECASE | re.DOTALL,
            )
            for m in pat_global.finditer(norm):
                old_raw = (m.group('old') or '').strip()
                new_raw = (m.group('new') or '').strip()
                old_c = _clean_addr(old_raw)
                new_c = _clean_addr(new_raw)
                if old_c:
                    entities.setdefault('old_addresses', [])
                    if old_c not in entities['old_addresses']:
                        entities['old_addresses'].append(old_c)
                # Yeni adres adreslerine EKLENMEYECEK (sadece adres bloğu kullanılır)
        # Tescil bölümü varyantı: "... şirketin adresi <OLD> olan adresi <NEW> ..."
            pat_tescil_olan = re.compile(
                r"[sş]irketin\s+adresi\s+(?P<old>.{8,240}?)\s+olan\s+adresi\s+(?P<new>.{8,240}?)(?:\s+olarak|\s+g[üu]ncell|\s+deg[iı]şt|\s+değ[iı]şt|\s*/|\s*$)",
                re.IGNORECASE | re.DOTALL,
            )
            for m in pat_tescil_olan.finditer(norm):
                old_raw = (m.group('old') or '').strip()
                old_c = _clean_addr(old_raw)
                if old_c:
                    entities.setdefault('old_addresses', [])
                    if old_c not in entities['old_addresses']:
                        entities['old_addresses'].append(old_c)
        except Exception:
            pass

    # 6) Telefon(lar)
    phones = find_all(r"^\s*(?:Telefon|Tel|GSM)\s*[:.]?\s*([+0-9 ()-]{8,})\s*$", norm, flags=re.IGNORECASE | re.MULTILINE)
    if phones:
        entities["phones"] = unique_list(phones)

    # 7) Maskeli Kimlik No’lar (örn: 4*****9, 179******34)
    # Not: OCR'de '5' karakteri '$' olarak gelebilir; \b yerine lookaround kullan
    masked_ids = find_all(r"(?<!\w)(?:\d|\$){1,4}\*{2,8}(?:\d|\$){1,3}(?!\w)", norm)
    if masked_ids:
        entities["masked_ids"] = unique_list(masked_ids)

    # 8) TL Tutarları (genişletilmiş: TL., TRY, ₺)
    amounts = find_all(r"\b\d{1,3}(?:\.\d{3})*(?:,\d{2})?\s*(?:TL\.?|Türk Lirasi|Türk Lirası|TRY|₺)\b", norm)
    if amounts:
        for a in unique_list(amounts):
            entities["money"].append({"text": a, "label": "MONEY"})

    # 9) Tarihler (dd.mm.yyyy, 24 MAYIS 2023, dd/mm/yyyy, yyyy-mm-dd)
    regex_dates = find_all(r"\b\d{1,2}\.\d{1,2}\.\d{4}\b", norm)
    regex_dates += find_all(rf"\b\d{{1,2}}\s+(?:{TURKISH_MONTHS})\s+\d{{4}}\b", norm, flags=re.IGNORECASE)
    regex_dates += find_all(r"\b\d{1,2}/\d{1,2}/\d{4}\b", norm)
    regex_dates += find_all(r"\b\d{4}-\d{2}-\d{2}\b", norm)
    if regex_dates:
        for d in unique_list(regex_dates):
            entities["dates"].append({"text": d, "label": "DATE"})

    # 10) IBAN
    ibans = find_all(r"\bTR\d{2}(?:\s*\d{4}){5}\s*\d{2}\b", norm)
    if ibans:
        entities["ibans"] = unique_list(ibans)

    # 11) Vergi Dairesi ve Vergi/T.C. Kimlik No
    tax_offices = find_all(r"^\s*Vergi\s*Daires[ıi]\s*[:.]?\s*(.+)$", norm, flags=re.IGNORECASE | re.MULTILINE)
    if tax_offices:
        entities["tax_offices"] = unique_list([re.sub(r"\s+", " ", t) for t in tax_offices])
    vkns = find_all(r"\b(?:Vergi\s*No|Vergi\s*Kimlik\s*No|VKN)\s*[:.]?\s*([0-9]{10})\b", norm, flags=re.IGNORECASE | re.MULTILINE)
    if vkns:
        entities["vkns"] = unique_list(vkns)
    tckns = find_all(r"\b(?:T\.?C\.?\s*Kimlik\s*No|TC\s*Kimlik\s*No|TCKN)\s*[:.]?\s*([0-9]{11})\b", norm, flags=re.IGNORECASE | re.MULTILINE)
    if tckns:
        entities["tckns"] = unique_list(tckns)

    # 12) Faks
    faxes = find_all(r"^\s*Faks\s*[:.]?\s*([+0-9 ()-]{8,})\s*$", norm, flags=re.IGNORECASE | re.MULTILINE)
    if faxes:
        entities["faxes"] = unique_list(faxes)

    # 13) E-posta
    emails = find_all(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b", norm)
    if emails:
        entities["emails"] = unique_list(emails)

    # 14) Web adresleri
    websites = find_all(r"\bhttps?://[^\s]+\b|\bwww\.[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b", norm)
    if websites:
        entities["websites"] = unique_list(websites)

    # 15) İlan Sıra No (OCR toleranslı: Ilan/ilan/llan/Ilan/Han, Sira/Slra, No/N0)
    ilan_sira = find_all(r"\b(?:[İI1l][lIıi]an|ilan|llan|han)\s*S[ıiI1]ra\s*N[O0]\s*[:.]?\s*([A-Z0-9/\-]+)\b", norm, flags=re.IGNORECASE | re.MULTILINE)
    if not ilan_sira:
        # Başlık satırı + bir sonraki satırda değer fallback'i
        lines2 = norm.splitlines()
        header_only = re.compile(r"^\s*(?:[İI1l][lIıi]an|ilan|llan|han)\s*S[ıiI1]ra\s*N[O0]\s*[:.]*\s$", re.IGNORECASE | re.MULTILINE)
        for i, ln in enumerate(lines2):
            if header_only.match(ln.strip()):
                if i + 1 < len(lines2):
                    nxt = lines2[i + 1].strip()
                    mval = re.search(r"([A-Z0-9/\-]{3,})", nxt)
                    if mval:
                        ilan_sira.append(mval.group(1))
    if ilan_sira:
        entities["ilan_sira_no"] = unique_list(ilan_sira)

    # 16) Sermaye satırları (özet bilgi yakalama)
    capital_lines = find_all(r"^\s*(?:[ÖO]denmi[sş]\s+)?Sermaye\s*[:.]?\s*(.+)$", norm, flags=re.IGNORECASE | re.MULTILINE)
    if capital_lines:
        entities["capital_lines"] = unique_list([re.sub(r"\s+", " ", c) for c in capital_lines])

    # --- LLM Destekli Ek Çıkarım (opsiyonel) ---
    if LLM_ENABLED:
        llm_out = _llm_extract_entities(norm)
        if isinstance(llm_out, dict):
            # persons
            for p in llm_out.get("persons", []) or []:
                if isinstance(p, str) and p.strip():
                    entities["persons"].append({"text": p.strip(), "label": "PER_LLM"})
            # organizations
            for o in llm_out.get("organizations", []) or []:
                if isinstance(o, str) and o.strip():
                    entities["organizations"].append({"text": o.strip(), "label": "ORG_LLM"})
            # addresses
            addrs = []
            for a in llm_out.get("addresses", []) or []:
                if isinstance(a, str) and a.strip():
                    addrs.append(a.strip())
            if addrs:
                # Adres bloğu ile zaten birincil adres bulunduysa LLM adresleri ekleme
                if not (entities.get("addresses") or []):
                    entities["addresses"] = unique_list(addrs)
            # trade_name / registration_number / mersis / sicil_dosya_no
            if not entities.get("trade_name") and isinstance(llm_out.get("trade_name"), str):
                tn = llm_out.get("trade_name", "").strip()
                if tn:
                    entities["trade_name"] = tn
                    entities["organizations"].append({"text": tn, "label": "ORG"})
            if not entities.get("registration_number") and isinstance(llm_out.get("registration_number"), str):
                rn = llm_out.get("registration_number", "").strip()
                if rn:
                    entities["registration_number"] = rn
            if not entities.get("sicil_dosya_no") and isinstance(llm_out.get("sicil_dosya_no"), str):
                sd = llm_out.get("sicil_dosya_no", "").strip()
                if sd:
                    entities["sicil_dosya_no"] = sd
            if not entities.get("mersis_no") and isinstance(llm_out.get("mersis_no"), str):
                mn = llm_out.get("mersis_no", "").strip()
                if mn:
                    entities["mersis_no"] = mn

    # Anahtar kelime kalıplarından kişi ekle
    extra_persons = extract_persons_from_keywords(norm)
    if extra_persons:
        entities["persons"].extend(extra_persons)

    # Maskeli kimlik yakınından kişi ekle
    masked_persons = extract_persons_near_masked_ids(norm)
    if masked_persons:
        entities["persons"].extend(masked_persons)

    # Aksiyon çıkarımı
    actions = extract_actions(norm)
    if actions:
        entities["actions"] = actions

    # Deduplikasyon ve filtreler
    # 1) Sahte kişi filtrelemesi (rol/başlık yanlış pozitifleri)
    entities["persons"] = [e for e in entities["persons"] if not is_false_person(e["text"]) ]

    # 2) Parçalı/fragment token temizliği ve whitespace normalize + deduplikasyon
    def _is_fragment_token(s: str) -> bool:
        # WordPiece benzeri parçalar: '##' içerenleri at
        return bool(s) and ("##" in s)

    def _clean_list_dicts(lst: List[dict]) -> List[dict]:
        cleaned: List[dict] = []
        for it in lst or []:
            t = (it.get("text") or "").strip()
            if not t:
                continue
            if _is_fragment_token(t):
                continue
            # Boşluk sadeleştir
            t_norm = re.sub(r"\s+", " ", t)
            it["text"] = t_norm
            cleaned.append(it)
        return _dedup_entity_dicts(cleaned)

    # Kişiler: önce temizle (dedup yapmadan), ardından PER_MASKED'i tercih eden dedup uygula
    def _clean_list_dicts_no_dedup(lst: List[dict]) -> List[dict]:
        cleaned: List[dict] = []
        for it in lst or []:
            t = (it.get("text") or "").strip()
            if not t:
                continue
            if _is_fragment_token(t):
                continue
            t_norm = re.sub(r"\s+", " ", t)
            it["text"] = t_norm
            cleaned.append(it)
        return cleaned

    entities["persons"] = _dedup_persons_pref_masked(_clean_list_dicts_no_dedup(entities.get("persons") or []))

    # 2b) Aynı isim için birden çok PER_MASKED atanmasını engelle (bir isme tek maske)
    def _one_mask_per_name(persons: List[dict]) -> List[dict]:
        seen: Dict[str, dict] = {}
        out: List[dict] = []
        for p in persons:
            name_key = (p.get("text") or "").strip().upper()
            if not name_key:
                continue
            if p.get("label") == "PER_MASKED":
                if name_key in seen and (seen[name_key] or {}).get("label") == "PER_MASKED":
                    # zaten bir PER_MASKED var, yenisini atla
                    continue
                else:
                    seen[name_key] = p
                    out.append(p)
            else:
                # PER veya diğerleri: daha önce hiç görmediysek ekle
                if name_key not in seen:
                    seen[name_key] = p
                    out.append(p)
        return out

    entities["persons"] = _one_mask_per_name(entities["persons"])

    entities["organizations"] = _clean_list_dicts(entities.get("organizations") or [])
    entities["locations"] = _clean_list_dicts(entities.get("locations") or [])
    entities["dates"] = _clean_list_dicts(entities.get("dates") or [])
    entities["money"] = _clean_list_dicts(entities.get("money") or [])
    entities["misc"] = _clean_list_dicts(entities.get("misc") or [])

    # 3) Adres(ler) mevcutsa, LOC öğelerini tekrarlayıcı olduklarından bastır
    if entities.get("addresses"):
        entities["locations"] = []

    # 4) Organizations: başlık benzeri ve gürültüleri temizle + güçlü deduplikasyon
    def _is_headerish_org(s: str) -> bool:
        k = (s or "").upper()
        # Ticaret Sicili Müdür/Memurluğu başlık izleri ve 'NDEN/NDAN'
        if re.search(r"TICARET\s*SICIL[Iİ]|MEMURLU?G|MÜDÜRLÜ", k):
            return True
        if re.search(r"\bN'?D[EA]N\b", k):
            return True
        return False

    def _is_noise_org(s: str) -> bool:
        t = (s or "").strip()
        if len(t) <= 2:
            return True
        ku = t.upper()
        # Kanun adları kurum değildir; ayrıca çok kısa parçaları at
        if "KANUNU" in ku:
            return True
        if re.fullmatch(r"[A-Za-zÇĞİÖŞÜ0-9\-./ ]{1,3}", t):
            return True
        return False

    def _is_judiciary_org(s: str) -> bool:
        k = (s or "").upper()
        # Mahkeme adları (Asliye Ticaret vb.) kurum listesinde istenmeyebilir
        if re.search(r"MAHKEME", k):
            return True
        # Cumhuriyet + Mahkeme birlikte geçtiğinde de gürültü kabul et
        if re.search(r"CUMHURIYET[Iİ]", k) and re.search(r"MAHKEME", k):
            return True
        return False

    def _norm_for_org(s: str) -> str:
        t = unicodedata.normalize("NFKD", s or "")
        t = "".join(ch for ch in t if not unicodedata.category(ch).startswith("M"))
        t = t.upper()
        t = re.sub(r"[^A-Z0-9 ]+", " ", t)
        t = re.sub(r"\s+", " ", t).strip()
        return t

    orgs0 = entities.get("organizations") or []
    tname_key = _norm_for_org(entities.get("trade_name", "") or "")
    orgs1: List[dict] = []
    for o in orgs0:
        txt = o.get("text", "")
        key = _norm_for_org(txt)
        # Ticaret unvanını her durumda koru
        if tname_key and key == tname_key:
            orgs1.append(o)
            continue
        if _is_headerish_org(txt) or _is_noise_org(txt) or _is_judiciary_org(txt):
            continue
        orgs1.append(o)
    # Substring bazlı güçlü dedup: önce uzunları koru
    orgs_sorted = sorted(orgs1, key=lambda o: len(_norm_for_org(o.get("text", ""))), reverse=True)
    kept: List[dict] = []
    keys: List[str] = []
    for o in orgs_sorted:
        key = _norm_for_org(o.get("text", ""))
        if not key:
            continue
        if any(key in k or k in key for k in keys):
            continue
        kept.append(o)
        keys.append(key)
    entities["organizations"] = kept

    if DEBUG_NLP:
        try:
            tn = entities.get("trade_name")
            mn = entities.get("mersis_no")
            rn = entities.get("registration_number")
            addr_cnt = len(entities.get("addresses") or [])
            persons_cnt = len(entities.get("persons") or [])
            actions_cnt = len(entities.get("actions") or [])
        except Exception:
            tn = mn = rn = None
            addr_cnt = persons_cnt = actions_cnt = 0
        elapsed = (time.perf_counter() - t_start) if DEBUG_NLP else 0.0
        logger.info(
            "DEBUG_NLP parse_announcement_text done took=%.3fs tn=%r mersis=%r reg=%r addr=%d persons=%d actions=%d",
            elapsed, tn, mn, rn, addr_cnt, persons_cnt, actions_cnt,
        )
    return entities

def _normalize_tr_for_header(s: str) -> str:
    """Başlık tespiti için sadeleştirilmiş normalize: diakritik ve sık OCR hataları
    kaldırılır, büyük harfe çevrilir ve fazla boşluklar sıkılaştırılır.
    (Sadece başlık araması için kullanılır; metin ofsetlerini olduğu gibi korur.)"""
    if not s:
        return ""
    out = s
    # Apostrof ve benzeri işaretleri tek tipe indir
    out = (out
        .replace("’", "'")
        .replace("`", "'")
        .replace("ʼ", "'")
        .replace("ʹ", "'")
        .replace("′", "'")
        .replace("‘", "'")
        .replace("´", "'")
    )
    # Unicode normalizasyonu: diakritikleri ayır ve birleştirici işaretleri kaldır
    out = unicodedata.normalize("NFKD", out)
    out = "".join(ch for ch in out if not unicodedata.category(ch).startswith("M"))

    # Türkçe ve OCR karışıklıkları için harf eşlemeleri
    repl = (
        ("İ", "I"), ("I", "I"), ("ı", "I"), ("i", "I"),
        ("Ş", "S"), ("ş", "S"), ("Ç", "C"), ("ç", "C"),
        ("Ğ", "G"), ("ğ", "G"), ("Ü", "U"), ("ü", "U"),
        ("Ö", "O"), ("ö", "O"),
        # I varyantları
        ("Ì", "I"), ("Í", "I"), ("Î", "I"), ("Ï", "I"),
        ("ì", "I"), ("í", "I"), ("î", "I"), ("ï", "I"),
    )
    for a, b in repl:
        out = out.replace(a, b)

    # Sık OCR karışıklıkları: 1->I, 0->O vb. (aşırı agresif olmadan)
    out = re.sub(r"\bT1CARET\b", "TICARET", out)
    out = re.sub(r"S1CIL", "SICIL", out)
    out = re.sub(r"MUD0R", "MUDUR", out)
    out = re.sub(r"MUDUR LUGU", "MUDURLUGU", out)
    # Harfleri aralıklı yazılmış çekirdek kelimeleri birleştir (OCR boşluk bozulmaları)
    out = re.sub(r"T\s*[I1]\s*C\s*[AA]\s*R\s*[EE]\s*T", "TICARET", out, flags=re.IGNORECASE)
    out = re.sub(r"S\s*[I1]\s*C\s*[I1]\s*L(?:\s*[I1])?", "SICIL", out, flags=re.IGNORECASE)
    out = re.sub(r"M\s*[ÜU]\s*D\s*[ÜU]\s*R", "MUDUR", out, flags=re.IGNORECASE)
    out = re.sub(r"M\s*E\s*M\s*U\s*R\s*L\s*U", "MEMURLU", out, flags=re.IGNORECASE)
    out = re.sub(r"MUDUR\s*LUGU", "MUDURLUGU", out, flags=re.IGNORECASE)
    out = re.sub(r"MEMURLU\s*GUNDEN", "MEMURLUGUNDEN", out, flags=re.IGNORECASE)
    out = re.sub(r"MUDURLU\s*GUNDEN", "MUDURLUGUNDEN", out, flags=re.IGNORECASE)
    # Sonekleri ve ayrık harfleri birleştir: LUGU ve 'NDEN/'NDAN varyantları (OCR boşlukları)
    # "MUDUR L U G U" -> "MUDURLUGU"
    out = re.sub(r"(MUDUR)\s*L\s*U\s*G\s*U", r"\1LUGU", out, flags=re.IGNORECASE)
    # "MEMURLU G U" -> "MEMURLUGU" (\u011E -> G normalizasyonundan sonra)
    out = re.sub(r"(MEMURLU)\s*G\s*U", r"\1GU", out, flags=re.IGNORECASE)
    # Genel olarak L U G U ayrık yazımı
    out = re.sub(r"L\s*U\s*G\s*U", "LUGU", out, flags=re.IGNORECASE)
    # "' N D E N" / "' N D A N" ya da aralıklı N D E/A N sonu -> NDEN/NDAN
    out = re.sub(
        r"(?:['’]?\s*)N\s*D\s*(E|A)\s*N\b",
        lambda m: "NDEN" if m.group(1).upper() == "E" else "NDAN",
        out,
        flags=re.IGNORECASE,
    )

    # Boşlukları sıkılaştır
    out = re.sub(r"\s+", " ", out)
    return out.upper().strip()

def _find_header_matches_robust(text: str) -> List[re.Match]:
    """
    Başlıkları yakalamak için daha toleranslı kalıplar:
      1) 'loose' regex: T(I)CARET ... SICIL ... MUDUR/MEMURL ... N?DEN/NDAN satır sonu
      2) Token bazlı tarama: normalize edilmiş satırda TICARET & SICIL ve MUDUR/MEMURLU
         ve sonda NDEN/NDAN görünen satırları başlık kabul et.
    Dönüş: re.Match benzeri nesneler listesi (span'ları satır başlangıcına oturur).
    """
    matches: List[re.Match] = []

    # 1) Loose regex doğrudan ham metin üzerinde (diakritik varyasyonları kapsar)
    # Harf aralarına boşlukların girdiği (T I C A R E T vb.) OCR bozulmalarını da destekle
    spaced_TICARET = r"T\s*[İI1]\s*C\s*[AA]\s*R\s*[EE]\s*T"
    spaced_SICIL   = r"S\s*[İI1]\s*C\s*[İI1]\s*L(?:\s*[İI])?"
    spaced_MUDUR   = r"M\s*[ÜU]\s*D\s*[ÜU]\s*R"
    spaced_MEMURL  = r"M\s*E\s*M\s*U\s*R\s*L"
    # Apostrofun N'den ÖNCE geldiği gerçek varyantı da destekle ('NDEN/'NDAN)
    spaced_NDEN    = r"(?:['’]?\s*)N\s*D\s*[EA]\s*N"

    loose_re = re.compile(
        r"^[ \t]*(?!Eski\b).{0,160}?"  # satırın başından 160 karaktere kadar tolerans
        r"(?:T[İI1]C[AA]R[EE]T|" + spaced_TICARET + r")"
        r"[^\r\n]{0,160}?"                 # satır içi ilerleme, satır sonunu aşma
        r"(?:S[İI1]C[İI1]L[İI]?|" + spaced_SICIL + r")"
        r"[^\r\n]{0,160}?"
        r"(?:M[ÜU]D[ÜU]R|MEMURL|" + spaced_MUDUR + r"|" + spaced_MEMURL + r")"
        r"[^\r\n]{0,120}?"
        # NDEN/NDAN sonu: apostrof N'den önce olabilir
        r"(?:['’]?\s*N'?D[EA]N|" + spaced_NDEN + r")\s*$"
    , re.IGNORECASE | re.MULTILINE)
    matches = list(loose_re.finditer(text))

    # 2) Token bazlı: satır satır gez, normalize edip anahtarları ara (LOOSE'a ek)
    #    Bulunan satırın başlangıç konumu üzerinden sahte Match üret; mevcut başlangıçları atla.
    existing_starts: Set[int] = set()
    try:
        existing_starts = {m.start() for m in matches}
    except Exception:
        existing_starts = set()
    line_start = 0
    for ln in text.splitlines(True):  # keepends=True
        raw = ln.rstrip("\n\r")
        norm = _normalize_tr_for_header(raw)
        if norm:
            has_core = ("TICARET" in norm and "SICIL" in norm and
                        ("MUDUR" in norm or "MEMURLU" in norm))
            has_suffix = norm.endswith("NDEN") or norm.endswith("NDAN")
            # NDEN/NDAN eki olmayan ama 'T.C' ile başlayan ve çekirdek kalıbı taşıyan
            # başlıkları da aday olarak kabul et (örn. 'T.C. ISTANBUL TICARET SICILI MÜDÜRLÜĞÜ')
            has_tc = bool(re.search(r"^(?:T\s*\.?\s*C\s*\.?|TC\b|T\.C\.)", raw, flags=re.IGNORECASE))
            # Token bazlı adayları daha geniş al: çekirdek varsa ekle; nihai seçim _detect_headers içinde yapılacak.
            if has_core:
                # Satır başından satır sonuna kadar aralık
                s_idx = line_start
                if s_idx not in existing_starts:
                    class _FakeMatch:
                        def __init__(self, s: int, e: int):
                            self._span = (s, e)
                        def start(self):
                            return self._span[0]
                        def end(self):
                            return self._span[1]
                    e_idx = line_start + len(ln)
                    matches.append(_FakeMatch(s_idx, e_idx))
                    existing_starts.add(s_idx)
        line_start += len(ln)

    return matches  # boş olabilir

def _find_court_header_matches(text: str) -> List[re.Match]:
    """
    Mahkeme başlıklarını yakalamak için toleranslı tarama.
    Heuristik: Satır normalize edildiğinde 'MAHKEME' içeriyorsa ve
    - satır 'NDEN/NDAN' ile bitiyorsa veya
    - satır içinde 'BAŞKAN' (BASKAN) izi varsa veya
    - satır başında T.C. izi varsa
    başlık adayı kabul edilir.

    Dönüş: re.Match benzeri nesneler listesi (span'ları satır başlangıcına oturur).
    """
    matches: List[re.Match] = []
    line_start = 0
    for ln in text.splitlines(True):  # keepends=True
        raw = ln.rstrip("\n\r")
        norm = _normalize_tr_for_header(raw)
        if not norm:
            line_start += len(ln)
            continue
        has_ct = ("MAHKEME" in norm)
        ends_nden = norm.endswith("NDEN") or norm.endswith("NDAN")
        has_baskan = ("BASKAN" in norm)
        has_tc = bool(re.search(r"^(?:T\s*\.??\s*C\s*\.??|TC\b|T\.C\.)", raw, flags=re.IGNORECASE))
        if has_ct and (ends_nden or has_baskan or has_tc):
            s_idx = line_start
            class _FakeMatch:
                def __init__(self, s: int, e: int):
                    self._span = (s, e)
                def start(self):
                    return self._span[0]
                def end(self):
                    return self._span[1]
            e_idx = line_start + len(ln)
            matches.append(_FakeMatch(s_idx, e_idx))
        line_start += len(ln)
    return matches

def _detect_headers(text: str) -> List[int]:
    """
    Başlık başlangıçlarını (karakter ofseti) tespit eder.
    Kaynaklar: sıkı regex, fallback regex ve _find_header_matches_robust birleştirilir.
    Yakın (<= HEADER_CLUSTER_DIST karakter) ofsetler puanlanarak tek temsilci seçilir.

    Puanlama sezgileri:
      +2 aynı satırda "T.C" izi (T.?C.?)
      +2 sonraki ~HEADER_LOOKAHEAD_CHARS karakterde "ILAN SIRA NO" (OCR varyantı) geçmesi
      +1 sonraki ~HEADER_LOOKAHEAD_CHARS karakterde "MERSIS NO" geçmesi
      +1 aynı satır "NDEN/NDAN" ile bitiş
    """
    if not text:
        return []

    strict_re = re.compile(
        r"^\s*(?!Eski\b)(?:T\.?\s*C\.?\s*)?.{0,80}?"
        r"TICARET(?:\s+|\r?\n){0,3}SICIL[Iİ]"
        r"(?:\s+|\r?\n){0,3}(?:M[ÜU]D[ÜU]R[^\n\r]{0,30}|MEMURL[^\n\r]{0,30})"
        r"(?:['’]?\s*N'?D[EA]N)\s*$"
    , re.IGNORECASE | re.MULTILINE)
    # Fallback: müdürlüğü'nden / memurluğu'ndan (apostrof opsiyonel) ve NDEN/NDAN iki varyantı
    fallback_re = re.compile(
        r"^\s*(?!Eski\b).{0,160}?((?:m[üu]d[üu]rl[üu][ğg]?[üu]?|memurlu[ğg]?[üu]?)['’]?n[dt]an)\s$",
        re.IGNORECASE | re.MULTILINE,
    )

    cands: List[Tuple[int, int]] = []
    strict_ms = list(strict_re.finditer(text))
    fallback_ms = list(fallback_re.finditer(text))
    robust_ms = list(_find_header_matches_robust(text))
    court_ms = list(_find_court_header_matches(text))
    for m in strict_ms:
        cands.append((m.start(), m.end()))
    for m in fallback_ms:
        cands.append((m.start(), m.end()))
    for m in robust_ms:
        try:
            cands.append((m.start(), m.end()))
        except Exception:
            continue
    # Mahkeme başlık adaylarını da ekle
    for m in court_ms:
        try:
            cands.append((m.start(), m.end()))
        except Exception:
            continue
    if DEBUG_NLP:
        try:
            logger.info("DEBUG_NLP headers: strict=%d fallback=%d robust=%d total_cands=%d", len(strict_ms), len(fallback_ms), len(robust_ms), len(cands))
            print("DEBUG_NLP headers counts:", len(strict_ms), len(fallback_ms), len(robust_ms), len(cands))
            # Eşleşen satırları yazdır
            def _line_span(pos: int) -> Tuple[int, int]:
                ls = text.rfind("\n", 0, pos)
                ls = 0 if ls < 0 else ls + 1
                le = text.find("\n", pos)
                le = len(text) if le < 0 else le
                return ls, le
            for tag, ms in (("strict", strict_ms), ("fallback", fallback_ms), ("robust", robust_ms)):
                for m in ms[:10]:
                    ls, le = _line_span(m.start())
                    logger.info("DEBUG_NLP %s line: %r", tag, text[ls:le])
        except Exception:
            pass

    # Refined Splitters: Only split on MERSIS/ILAN SIRA if they are at the START of a line
    # or preceded by a newline, to avoid splitting multi-company single-line headers.
    fallback_split_re = re.compile(r"(?m)^\s*(?:#*\s*)?(?:[İIıi1l]lan\s*S[mt]?r[ıi]?a\s*No|MERS[İI]S\s*No)\s*[:.]", re.IGNORECASE)
    for m in fallback_split_re.finditer(text):
        ls = text.rfind("\n", 0, m.start())
        ls = 0 if ls < 0 else ls + 1
        # Only add as candidate if it's the start of the match or preceded by a cleanup.
        cands.append((ls, m.end()))

    if not cands:
        return []

    def line_bounds(pos: int) -> Tuple[int, int]:
        ls = text.rfind("\n", 0, pos)
        ls = 0 if ls < 0 else ls + 1
        le = text.find("\n", pos)
        le = len(text) if le < 0 else le
        return ls, le

    def score_span(s: int, e: int) -> Tuple[int, bool]:
        ls, le = line_bounds(s)
        line = text[ls:le]
        look = text[le: min(len(text), le + HEADER_LOOKAHEAD_CHARS)]
        # Normalize edilmiş lookahead penceresi: OCR varyantlarına dayanıklı anahtar kelime araması
        look_norm = _normalize_tr_for_header(look)
        norm_line_here = _normalize_tr_for_header(line)
        sc = 0
        # T.C izi (noktalı/noktasız, araya boşluk girmiş olabilir)
        if re.search(r"T\s*\.?\s*C\s*\.?", line, flags=re.IGNORECASE):
            sc += 2
        # OCR toleranslı 'ILAN SIRA NO' varyantları (kendi satırı veya lookahead)
        # SIRA/STRA/SMRA/SRRA varyantları
        ilan_sira_re = r"\b[IH1L][IL1]AN\s*S[MT]?RA\s*N[O0]\b"
        if re.search(ilan_sira_re, norm_line_here) or re.search(ilan_sira_re, look_norm):
            sc += 2
        # OCR toleranslı 'MERSIS NO' varyantları (kendi satırı veya lookahead)
        if re.search(r"\bMERS[IL1]S\s*N[O0]\b", norm_line_here) or re.search(r"\bMERS[IL1]S\s*N[O0]\b", look_norm):
            sc += 2
        # Şehir adı benzeri bir kelime grubu + 'TICARET SICIL' çekirdeği (örn. ISTANBUL TICARET SICIL)
        if re.search(r"\b[A-ZÇĞİÖŞÜ]{3,}(?:\s+[A-ZÇĞİÖŞÜ]{3,})?\s+TICARET\s+SICIL", norm_line_here):
            sc += 1
        if re.search(r"N'?D[EA]N\s$", line, flags=re.IGNORECASE) or re.search(r"N'?D[EA]N\s*$", line, flags=re.IGNORECASE):
            sc += 1
        # Mahkeme başlıkları için ek puanlama: satır 'MAHKEME' içeriyorsa puan ver
        if "MAHKEME" in norm_line_here:
            sc += 2
        has_ilan = bool(re.search(r"\b[IH1L][IL1]AN\s*SIRA\s*N[O0]\b", look_norm))
        return sc, has_ilan

    # Adayları satır başlangıcına göre grupla; aynı satırdaki alternatif match'ler tek başlıktır
    cands_sorted = sorted(cands, key=lambda x: x[0])
    by_line: Dict[int, List[Tuple[int, int, int, bool]]] = {}
    for s, e in cands_sorted:
        sc, has_ilan = score_span(s, e)
        ls, le = line_bounds(s)
        by_line.setdefault(ls, []).append((s, e, sc, has_ilan))

    picks: List[int] = []
    for ls in sorted(by_line.keys()):
        grp = by_line[ls]
        # en yüksek puanı seç; eşitlikte ILAN içereni, yine eşitlikte daha ileri başlangıcı seç
        best = sorted(grp, key=lambda t: (t[2], t[3], t[0]))[-1]
        s, e, sc, has_ilan = best
        le = line_bounds(s)[1]
        # Eşik: en az HEADER_MIN_SCORE puan (T.C veya ILAN/MERSIS bağlamsal ipucu) ya da doğrudan ILAN yakınlığı
        # Ek kural: normalize satır çekirdek kalıbı taşımalı ve (NDEN/NDAN ile bitmeli ya da T.C izi olmalı)
        norm_line = _normalize_tr_for_header(text[ls:le])
        has_core = ("TICARET" in norm_line and "SICIL" in norm_line and ("MUDUR" in norm_line or "MEMURLU" in norm_line))
        ends_nden = norm_line.endswith("NDEN") or norm_line.endswith("NDAN")
        has_tc = bool(re.search(r"^(?:T\s*\.?\s*C\s*\.?|TC\b|T\.C\.)", text[ls:le], flags=re.IGNORECASE))
        if norm_line.startswith("KAYITLI OLDUGU TICARET SICILI MUDURLUGU"):
            continue
        if ("KAYITLI OLDUGU TICARET SICILI" in norm_line and "MUDURLUGU" in norm_line):
            continue
        # Kabul ölçütü:
        #  A) Ticaret Sicil başlığı:
        #    - Çekirdek (TICARET & SICIL & MUDUR/MEMURLU) ZORUNLU
        #    - Sonek koşulu: NDEN/NDAN veya T.C. izi varsa kabul
        #    - Alternatif olarak, lookahead penceresinde 'İlan Sıra No' varsa (has_ilan), sonek şartını gevşet
        #  B) Mahkeme başlığı:
        #    - Satırda 'MAHKEME' geçiyorsa ve (NDEN/NDAN ile bitiyor ya da T.C./BAŞKAN izi var)
        #  - EK: Metin içinde 'MÜDÜRLÜĞÜNCE' / 'MEMURLUĞUNCA' (normalize: MUDURLUGUNCE / MEMURLUGUNCE) geçiyorsa
        #    bu bir başlık DEĞİLDİR; orta paragraf ifadesidir. Bu nedenle dışla.
        if re.search(r"\b(MUDURLUGUNCE|MEMURLUGUNCE)\b", norm_line):
            continue
        is_court = ("MAHKEME" in norm_line) and (ends_nden or has_tc or ("BASKAN" in norm_line))
        # Allow splits if it has core header parts OR if it's a strong fallback (MERSIS/ILAN)
        if (has_core and ((ends_nden or has_tc) or has_ilan) and (sc >= 0)) or is_court or (sc >= 2):
            # sc >= 2 implies it has MERSIS or ILAN SIRA NO in it/near it
            # Başlığı satır başına hizala
            picks.append(ls)

    res = sorted(picks)
    return res

def split_announcements(text: str) -> List[str]:
    """
    OCR metnini ilân segmentlerine böler.
    Bölme ölçütü: "Ticaret Sicili Müdürlüğü'nden" veya "Ticaret Sicili Memurluğu'ndan"
    benzeri başlıkları içeren satırlar. (Yeni 2 sütunlu ve eski 5 sütunlu tipler)

    Dönüş: Normalized metin parçaları listesi (başlık satırı dahil).
    """
    if not text:
        return []
    t0 = time.perf_counter() if DEBUG_NLP else 0.0
    if DEBUG_NLP:
        logger.info("DEBUG_NLP split_announcements start len=%d", len(text))

    # Başlık kalıbı (ham metin üzerinde):
    #  - "Eski Ticaret Sicili Müdürlügü:" ile başlayan sahte başlıkları dışla
    #  - satır sonu "NDEN/NDAN" varyantları ile bitmeli (apostrof olabilir)
    # 5 sütunlu eski gazete OCR'larında başlık kelimeleri satırlara bölünebilir.
    # Bu nedenle 'TİCARET' 'SİCİLİ' ve 'MÜDÜRLÜĞÜNDEN/MEMURLUĞUNDAN' arasında
    # satır sonlarına izin veren daha toleranslı bir regex kullanıyoruz.
    header_re = re.compile(
        r"^\s*(?!Eski\b)(?:T\.?C\.?\s*)?.{0,80}?"
        r"TICARET(?:\s+|\r?\n){0,3}SICIL[Iİ]"
        r"(?:\s+|\r?\n){0,3}(?:M[ÜU]D[ÜU]R[^\n\r]{0,30}|MEMURL[^\n\r]{0,30})"
        r"N'?D[EA]N\s*$"
    , re.IGNORECASE | re.MULTILINE)

    # Aşırı gürültü sayfa/aktarma satırlarını temizleyerek bölme sonrası metni sadeleştir
    def clean_lines(seg: str) -> str:
        lines = []
        for ln in seg.splitlines():
            l2 = ln.strip()
            if not l2:
                lines.append(ln)
                continue
            # Önceki/sonraki sayfa ve sayfa numarası satırlarını at
            if re.search(r"devam[iı1]|bastarafi|^\s*sayfa\s*[:\-]", l2, flags=re.IGNORECASE):
                continue
            # Gazete/URL başlığı gibi gürültü satırları
            if re.search(r"turkiye\s+ticaret\s+sicil\s+gazetesi|ticaretsicil\.gov\.tr", l2, flags=re.IGNORECASE):
                continue
            # Resmi İlan Portalı / Basın İlan Kurumu / ilan.gov.tr gürültüsü
            if re.search(r"resm[iı]\s+ilan\s+portal[ıi]|bas[ıi]n\s+ilan\s+kurumu|ilan\.gov\.tr", l2, flags=re.IGNORECASE):
                continue
            # OCR varyantları: 'ICILI GAZETESI' veya 'SAYI:' içeren tarih/sayı satırlarını temizle
            if ("ICILI GAZETESI" in l2.upper() or re.search(r"\bSAYI\s*:\s*\d+", l2, flags=re.IGNORECASE)):
                continue
            # Kısa parantezli kod/yevmiye/sayfa referanslarını temizle (örn. (3/A)(30/554466), (19842027))
            if (len(l2) <= 40 and
                re.fullmatch(r"[()0-9A-ZÇĞİÖŞÜ/\.\-\s]+", l2) is not None and
                l2.count("(") >= 1 and l2.count(")") >= 1):
                continue
            lines.append(ln)
        # Çoklu boş satırları azalt
        out = "\n".join(lines)
        out = re.sub(r"\n{3,}", "\n\n", out)
        return out.strip()

    starts = _detect_headers(text)
    if not starts:
        # Hiç başlık yoksa tüm metni tek ilân varsay
        segs = [clean_lines(text)] if text.strip() else []
        if DEBUG_NLP:
            logger.info("DEBUG_NLP split_announcements no headers segments=%d", len(segs))
        return segs

    segments: List[str] = []
    for i, start in enumerate(starts):
        end = starts[i + 1] if i + 1 < len(starts) else len(text)
        seg = text[start:end].strip()
        seg = clean_lines(seg)
        if seg:
            segments.append(seg)
    # Kısa ama GEÇERLİ başlık taşıyan segmentleri birleştirme: header-like kontrolü
    def _is_header_like(s: str) -> bool:
        for ln in s.splitlines():
            t = ln.strip()
            if not t:
                continue
            norm = _normalize_tr_for_header(t)
            has_core = ("TICARET" in norm and "SICIL" in norm and ("MUDUR" in norm or "MEMURLU" in norm))
            ends_nden = norm.endswith("NDEN") or norm.endswith("NDAN")
            has_tc = bool(re.search(r"^(?:T\s*\.?\s*C\s*\.?|TC\b|T\.C\.)", t, flags=re.IGNORECASE))
            if has_core and (ends_nden or has_tc):
                return True
            break
        return False
    if len(segments) >= 2 and MIN_SPLIT_SEG_LEN > 0:
        merged: List[str] = []
        i = 0
        while i < len(segments):
            cur = segments[i]
            if len(cur) < MIN_SPLIT_SEG_LEN and not _is_header_like(cur) and (i + 1) < len(segments):
                nxt = segments[i + 1]
                new_seg = (cur.rstrip() + "\n\n" + nxt.lstrip()).strip()
                merged.append(new_seg)
                i += 2
                continue
            if len(cur) < MIN_SPLIT_SEG_LEN and not _is_header_like(cur) and merged:
                merged[-1] = (merged[-1].rstrip() + "\n\n" + cur.lstrip()).strip()
                i += 1
                continue
            merged.append(cur)
            i += 1
        segments = merged
    if DEBUG_NLP:
        logger.info(
            "DEBUG_NLP split_announcements done headers=%d segments=%d took=%.3fs",
            len(starts), len(segments), (time.perf_counter() - t0) if DEBUG_NLP else 0.0,
        )
    return segments

def split_announcements_with_offsets(text: str) -> List[dict]:
    """
    OCR metnini ilân segmentlerine böler ve her segment için orijinal metin
    üzerindeki başlangıç/bitiş karakter ofsetlerini de döner.

    Dönüş: { start, end, text, raw_text } sözlüklerinden oluşan liste.
    - start/end: orijinal 'text' içinde [start:end) aralığı
    - text: temizlenmiş segment (clean_lines uygulanmış)
    - raw_text: orijinal metnin aynen kesiti (temizlenmemiş, normalize edilmemiş)
    """
    if not text:
        return []
    t0 = time.perf_counter() if DEBUG_NLP else 0.0
    if DEBUG_NLP:
        logger.info("DEBUG_NLP split_announcements_with_offsets start len=%d", len(text))

    header_re = re.compile(
        r"^\s*(?!Eski\b)(?:T\.?C\.?\s*)?.{0,80}?"
        r"TICARET(?:\s+|\r?\n){0,3}SICIL[Iİ]"
        r"(?:\s+|\r?\n){0,3}(?:M[ÜU]D[ÜU]R[^\n\r]{0,30}|MEMURL[^\n\r]{0,30})"
        r"N'?D[EA]N\s*$"
    , re.IGNORECASE | re.MULTILINE)

    def clean_lines(seg: str) -> str:
        lines = []
        for ln in seg.splitlines():
            l2 = ln.strip()
            if not l2:
                lines.append(ln)
                continue
            if re.search(r"devam[iı1]|bastarafi|^\s*sayfa\s*[:\-]", l2, flags=re.IGNORECASE):
                continue
            if re.search(r"turkiye\s+ticaret\s+sicil\s+gazetesi|ticaretsicil\.gov\.tr", l2, flags=re.IGNORECASE):
                continue
            if re.search(r"resm[iı]\s+ilan\s+portal[ıi]|bas[ıi]n\s+ilan\s+kurumu|ilan\.gov\.tr", l2, flags=re.IGNORECASE):
                continue
            if ("ICILI GAZETESI" in l2.upper() or re.search(r"\bSAYI\s*:\s*\d+", l2, flags=re.IGNORECASE)):
                continue
            if (len(l2) <= 40 and
                re.fullmatch(r"[()0-9A-ZÇĞİÖŞÜ/\.\-\s]+", l2) is not None and
                l2.count("(") >= 1 and l2.count(")") >= 1):
                continue
            lines.append(ln)
        out = "\n".join(lines)
        out = re.sub(r"\n{3,}", "\n\n", out)
        return out.strip()

    def _trim_trailing_artifacts(raw: str) -> Tuple[str, int]:
        """
        Segment sonundaki sayfa/artifact satırlarını kırpar ve kaç karakter
        çıkarıldığını döner. Ofset uyumu için end ofseti bu miktarda azaltılmalıdır.

        Kırpılan örnekler:
        - "(18142741)" gibi yalnız sayı parantez satırları
        - "Devami 973.Sayfada" / "Bastarafi 969.Sayfada" / "Sayfa : 970" benzeri satırlar
        """
        s = raw
        removed = 0
        # Sondaki boş satır sonu karakterlerini (\n/\r) kaldır ki son gerçek
        # satırı inceleyebilelim ve kaldırılan karakterleri sayalım.
        while s.endswith("\n") or s.endswith("\r"):
            s = s[:-1]
            removed += 1

        def _pop_last_line(buf: str) -> Tuple[str, str, int]:
            # Son satırı (öncesindeki \n ile birlikte) güvenli biçimde ayır.
            if not buf:
                return "", "", 0
            i = buf.rfind("\n")
            if i == -1:
                return "", buf, len(buf)
            # Windows CRLF durumunda sondaki satırda \r olabilir; analiz için strip kullanacağız.
            last = buf[i+1:]
            prefix = buf[:i]
            # Kaldırılacak uzunluk: sondaki satır + onu ayıran \n
            return prefix, last, len(buf) - len(prefix)

        artifact_re_list = [
            re.compile(r"^\s*\([0-9\s]{6,}\)\s*$"),  # (18142741), (19266851) vb.
            re.compile(r"devam[iı1]", re.IGNORECASE),
            re.compile(r"bastarafi", re.IGNORECASE),
            re.compile(r"^\s*sayfa\s*[:\-]?", re.IGNORECASE),
        ]

        while s:
            prefix, last, cut = _pop_last_line(s)
            if not last:
                break
            last_stripped = last.strip()
            is_artifact = False
            for are in artifact_re_list:
                if are.search(last_stripped):
                    is_artifact = True
                    break
            # Çok kısa ve sadece parantez/rakam/ayraç içeren satırlar (ek güvenlik)
            if not is_artifact:
                if (len(last_stripped) <= 40 and
                    re.fullmatch(r"[()0-9A-ZÇĞİÖŞÜ/\.\-\s]+", last_stripped) is not None and
                    last_stripped.count("(") >= 1 and last_stripped.count(")") >= 1):
                    is_artifact = True

            if is_artifact:
                s = prefix
                removed += cut
                continue
            break

        return s, removed

    starts = _detect_headers(text)
    if not starts:
        res = ([{"start": 0, "end": len(text), "text": clean_lines(text), "raw_text": text}]
                if text.strip() else [])
        if DEBUG_NLP:
            logger.info("DEBUG_NLP split_announcements_with_offsets no headers segments=%d", len(res))
        return res

    out: List[dict] = []
    for i, start in enumerate(starts):
        end = starts[i + 1] if i + 1 < len(starts) else len(text)
        # Orijinal metni aynen al, fakat segment SONUNDAKİ sayfa/artifact satırlarını kırp
        raw = text[start:end]
        trimmed_raw, removed_chars = _trim_trailing_artifacts(raw)
        if removed_chars:
            end -= removed_chars
            raw = trimmed_raw
        seg = clean_lines(raw)
        if seg:
            out.append({"start": start, "end": end, "text": seg, "raw_text": raw})
    # Kısa segmentleri birleştir (ör. kırpılmış artıkları); fakat başlık benzeri segmentleri KORU
    def _is_header_like_obj(o: dict) -> bool:
        s = o.get("text") or ""
        for ln in s.splitlines():
            t = ln.strip()
            if not t:
                continue
            norm = _normalize_tr_for_header(t)
            has_core = ("TICARET" in norm and "SICIL" in norm and ("MUDUR" in norm or "MEMURLU" in norm))
            ends_nden = norm.endswith("NDEN") or norm.endswith("NDAN")
            has_tc = bool(re.search(r"^(?:T\s*\.?\s*C\s*\.?|TC\b|T\.C\.)", t, flags=re.IGNORECASE))
            if has_core and (ends_nden or has_tc):
                return True
            break
        return False
    if len(out) >= 2 and MIN_SPLIT_SEG_LEN > 0:
        merged: List[dict] = []
        i = 0
        while i < len(out):
            cur = out[i]
            cur_len = len(cur.get("text", ""))
            # Eğer ilk segment çok kısaysa ve bir sonrakisi varsa, sonrakine ekle
            if cur_len < MIN_SPLIT_SEG_LEN and not _is_header_like_obj(cur) and (i + 1) < len(out):
                nxt = out[i + 1]
                new_text = (cur["text"].rstrip() + "\n\n" + nxt["text"].lstrip()).strip()
                new_raw = (cur.get("raw_text", "") + nxt.get("raw_text", ""))
                cur = {"start": cur["start"], "end": nxt["end"], "text": new_text, "raw_text": new_raw}
                i += 2
                merged.append(cur)
                continue
            # Sondaki kısa parçayı öncekiyle birleştir
            if cur_len < MIN_SPLIT_SEG_LEN and not _is_header_like_obj(cur) and merged:
                prev = merged[-1]
                prev["end"] = cur["end"]
                prev["text"] = (prev["text"].rstrip() + "\n\n" + cur["text"].lstrip()).strip()
                prev["raw_text"] = prev.get("raw_text", "") + cur.get("raw_text", "")
                i += 1
                continue
            merged.append(cur)
            i += 1
        out = merged

    # --- Sayfa Taşması/Devamı Birleştirme Mantığı ---
    # Eğer bir segmentin başında yeni bir ilana ait kimlikleyici alanlar (Unvan, Mersis, Sıra No, Sicil No) 
    # geçmiyorsa, bu segment bir önceki ilanın sayfa sınırında bölünmüş devamıdır!
    if len(out) >= 2:
        merged_pages: List[dict] = []
        for seg in out:
            seg_text = seg["text"]
            has_id = False
            # Kimlikleyici alanları ara (büyük/küçük harf duyarsız)
            if re.search(r"(?i)(?:ticaret\s+)?[üu]nvan[ıit]?\s*[:\s]", seg_text):
                has_id = True
            elif re.search(r"(?i)MERS[İI]S\s*(?:No)?\s*[:\s]", seg_text):
                has_id = True
            elif re.search(r"(?i)[İi]lan\s+S[ıi]ra\s+No\s*[:\s]", seg_text):
                has_id = True
            elif re.search(r"(?i)sicil(?:/Dosya)?\s*No\s*[:\s]", seg_text):
                has_id = True
                
            if not has_id and merged_pages:
                # Önceki ilanın devamı olarak birleştir
                prev = merged_pages[-1]
                prev["end"] = seg["end"]
                prev["text"] = (prev["text"].rstrip() + "\n\n" + seg_text.lstrip()).strip()
                prev["raw_text"] = prev.get("raw_text", "") + seg.get("raw_text", "")
            else:
                merged_pages.append(seg)
        out = merged_pages

    return out

def _autosave_results_to_ocr_ciktilari(results: List[dict], original_text: Optional[str] = None) -> Optional[str]:
    """
    'sicilius/ocr_ciktilari/' klasörüne JSON çıktısı olarak kaydeder.
    Dosya adı: parsed_ocr_{YYYYMMDD_HHMMSS_mmmmmm}_{sha1[:10]}.json
    """
    try:
        base_dir = os.path.dirname(__file__)
        # .../sicilius/backend/app/services -> .../sicilius
        sicilius_dir = os.path.abspath(os.path.join(base_dir, "..", "..", ".."))
        out_dir = os.path.join(sicilius_dir, "ocr_ciktilari")
        os.makedirs(out_dir, exist_ok=True)

        ts = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        src = original_text or ""
        sha1_full = hashlib.sha1(src.encode("utf-8")).hexdigest() if src else "0" * 40
        short = sha1_full[:10]

        # Idempotency: Aynı original_text (sha1) için zaten oluşturulmuş bir dosya varsa tekrar yazma
        existing_path: Optional[str] = None
        if original_text:
            try:
                # 1) Hızlı yol: kısa sha1 soneki adı içeren dosyaları kontrol et
                suffix = f"_{short}.json"
                for fn in os.listdir(out_dir):
                    if not fn.endswith(".json"):
                        continue
                    if suffix in fn:
                        f0 = os.path.join(out_dir, fn)
                        try:
                            with open(f0, "r", encoding="utf-8") as rf:
                                meta = json.load(rf)
                            if isinstance(meta, dict) and meta.get("source_sha1") == sha1_full:
                                existing_path = f0
                                break
                        except Exception:
                            # Bozuk dosya vs. durumunda devam et
                            continue
                # 2) Fallback: Tüm json dosyalarını tarayıp içerikten doğrula
                if existing_path is None:
                    for fn in os.listdir(out_dir):
                        if not fn.endswith(".json"):
                            continue
                        f1 = os.path.join(out_dir, fn)
                        try:
                            with open(f1, "r", encoding="utf-8") as rf:
                                meta = json.load(rf)
                            if isinstance(meta, dict) and meta.get("source_sha1") == sha1_full:
                                existing_path = f1
                                break
                        except Exception:
                            continue
            except Exception as e:
                logger.warning("AUTO_SAVE_OCR idempotency check failed: %s", e)
        if existing_path:
            logger.info(
                "AUTO_SAVE_OCR: Aynı kaynak (sha1=%s) için mevcut dosya bulundu, yeniden yazılmadı: %s",
                short,
                existing_path,
            )
            return existing_path

        # Autosave için sonuçlarda tepe seviye 'masked_ids' alanını çıkart
        save_results: List[dict] = []
        for r in results:
            if isinstance(r, dict):
                r2 = {k: v for k, v in r.items() if k != "masked_ids"}
                save_results.append(r2)
            else:
                save_results.append(r)

        payload: Dict[str, Any] = {
            "created_at": datetime.now().isoformat(),
            "auto_save_ocr": True,
            "item_count": len(results),
            "results": save_results,
        }
        if original_text is not None:
            payload["original_text_full"] = original_text
            payload["source_sha1"] = sha1_full

        fname = f"parsed_ocr_{ts}_{short}.json"
        fpath = os.path.join(out_dir, fname)
        with open(fpath, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
        logger.info("AUTO_SAVE_OCR: Sonuçlar kaydedildi: %s", fpath)
        return fpath
    except Exception as e:
        logger.warning("AUTO_SAVE_OCR kaydetme hatası: %s", e)
        return None

def parse_multiple_announcements(text: str) -> List[dict]:
    """
    Metni ilânlara böler ve her ilânı `parse_announcement_text` ile işler.
    ÇIKTIYI SADELEŞTİRİR (minimal):
      - index, sicil_office_header, original_text,
        start_offset, end_offset,
        sicil_dosya_no, mersis_no, trade_name, addresses,
        tescil alanları (hususlar, belgeler)
      - Diğer tüm ayrıntı listeleri ve entities_full KALDIRILMIŞTIR.
    """
    t_all = time.perf_counter() if DEBUG_NLP else 0.0
    if DEBUG_NLP:
        logger.info("DEBUG_NLP parse_multiple_announcements start len=%d", len(text or ""))
        
    # --- MODİFİYE: Docling Markdown Etiketlerini KORU (Strip yapma ki regexler çalışsın) ---
    if text:
        # text = re.sub(r"^(?:#+\s+|\*\s+|-\s+|>+\s+)", "", text, flags=re.MULTILINE)
        # Kalın ve Eğik sembollerini temizle (Sadece görsel gürültü oldukları için)
        text = re.sub(r"(?<!\*)\*\*([^\*]+)\*\*(?!\*)", r"\1", text)
        text = re.sub(r"(?<!_)__([^_]+)__(?!_)", r"\1", text)
    # ---------------------------------------------------

    out: List[dict] = []
    segments = split_announcements_with_offsets(text)
    if DEBUG_NLP:
        logger.info("DEBUG_NLP parse_multiple_announcements segmented count=%d", len(segments))
    # Mahkeme segmenti mi? Basit sezgi: ilk ~8 satırda 'MAHKEME' geçiyorsa
    def _segment_is_court(seg: str) -> bool:
        top = [ln.strip() for ln in (seg or "").splitlines() if ln.strip()][:8]
        norm_top = [ _normalize_tr_for_header(ln) for ln in top ]
        # More restrictive: Look for standalone MAHKEME/BASKAN/HUKUK keywords or specific phrase
        court_keywords = re.compile(r"\b(MAHKEME|HUKUK\s*MAHKEMES[Iİ]|ASL[Iİ]YE\s*HUKUK|SULH\s*HUKUK|BASKANLIG[Iİ])\b", re.IGNORECASE)
        # Also ensure it's not a false positive like 'mahkemelerinde' inside a long sentence
        return any(bool(court_keywords.search(nt)) for nt in norm_top if nt and len(nt) < 150)

    def _pick_court_header_line(preferred_text: str, alt_text: str) -> str:
        def _scan(lines: List[str]) -> str:
            cand_lines = [ln.strip() for ln in lines if ln.strip()]
            top = cand_lines[:8]
            for ln in top:
                norm = _normalize_tr_for_header(ln)
                if not norm:
                    continue
                if ("MAHKEME" in norm) and (norm.endswith("NDEN") or norm.endswith("NDAN") or "BASKAN" in norm or re.search(r"^(?:T\s*\.?\s*C\s*\.?|TC\b|T\.C\.)", ln, flags=re.IGNORECASE)):
                    return ln
            for ln in cand_lines:
                if re.search(r"Mahkemesi", ln, re.IGNORECASE):
                    return ln
            return cand_lines[0] if cand_lines else ""
        res = _scan(preferred_text.splitlines())
        if res:
            return res
        if alt_text and alt_text != preferred_text:
            return _scan(alt_text.splitlines())
        return ""

    for idx, segobj in enumerate(segments, start=1):
        seg = segobj["text"]
        raw = segobj.get("raw_text") or seg
        t0 = time.perf_counter() if DEBUG_NLP else 0.0
        if DEBUG_NLP:
            logger.info(
                "DEBUG_NLP parse_multiple_announcements item start index=%d len=%d start=%s end=%s",
                idx, len(seg), str(segobj.get("start")), str(segobj.get("end")),
            )
        if _segment_is_court(seg):
            # Mahkeme ilânı için yalın çıktı
            court_header = _pick_court_header_line(seg, raw)
            # Esas No
            m_esas = re.search(r"Esas\s*No\s*[:：]?\s*([0-9]{4}\s*/\s*[0-9]+(?:\s*Esas)?)", raw, flags=re.IGNORECASE)
            esas_no = None
            if m_esas:
                esas_no = re.sub(r"\s+", " ", (m_esas.group(1) or "").strip())
            else:
                # Fallback: "Esas :" veya sadece "Esas" başlığıyla yazılmış olabilir
                m_esas2 = re.search(r"^\s*Esas\s*[:：]?\s*([0-9]{4}\s*/\s*[0-9]+(?:\s*Esas)?)\s*$", raw, flags=re.IGNORECASE | re.MULTILINE)
                if m_esas2:
                    esas_no = re.sub(r"\s+", " ", (m_esas2.group(1) or "").strip())
            # Davacı
            davaci = None
            # 1) Tek satır varyantı: "Davacı: <AD>"
            m_dav_inline = re.search(r"^\s*Davac[ıi]\s*[:：]\s*(.+)$", raw, flags=re.IGNORECASE | re.MULTILINE)
            if m_dav_inline and (m_dav_inline.group(1) or "").strip():
                davaci = re.sub(r"\s+", " ", m_dav_inline.group(1).strip())
            else:
                # 2) Başlık satırı: "Davacı" ve takip eden satırda isim
                lines = raw.splitlines()
                for i, ln in enumerate(lines):
                    if re.fullmatch(r"\s*Davac[ıi]\s*", ln, flags=re.IGNORECASE):
                        # sonraki dolu satırı al
                        for j in range(i+1, min(i+4, len(lines))):
                            nxt = (lines[j] or "").strip()
                            if nxt:
                                davaci = re.sub(r"\s+", " ", nxt)
                                break
                        if davaci:
                            break
            # 3) Alternatif başlık: "Talep Eden" (Davacı yerine)
            if not davaci:
                m_te_inline = re.search(r"^\s*Talep\s+Eden\s*[:：]?\s*(.+)$", raw, flags=re.IGNORECASE | re.MULTILINE)
                if m_te_inline and (m_te_inline.group(1) or "").strip():
                    davaci = re.sub(r"\s+", " ", (m_te_inline.group(1) or "").strip())
                else:
                    for i, ln in enumerate(lines):
                        if re.fullmatch(r"\s*Talep\s+Eden\s*", ln, flags=re.IGNORECASE):
                            for j in range(i+1, min(i+4, len(lines))):
                                nxt = (lines[j] or "").strip()
                                if nxt:
                                    davaci = re.sub(r"\s+", " ", nxt)
                                    break
                            if davaci:
                                break
            # 4) Davacı metninden bağlamsal kuyrukları buda ("tarafından", "hasımsız", "olarak", "açılan" vb.)
            if davaci:
                davaci = re.sub(r"\s+\b(taraf[ıi]ndan|has[ıi]ms[ıi]z|olarak|aç[ıi]lan|acilan|mahkememizde|mahkememizce)\b.*$", "", davaci, flags=re.IGNORECASE).strip()
            minimal = {
                "index": idx,
                "type": "mahkeme",
                "court_name": court_header,
                "esas_no": esas_no,
                "davaci": davaci,
                "original_text": raw,
                "start_offset": segobj.get("start"),
                "end_offset": segobj.get("end"),
            }
            out.append(minimal)
            continue

        parsed = parse_announcement_text(seg)
        if parsed is None:
            print(f"DEBUG_ERROR: parse_announcement_text returned None for segment: {seg[:60]!r}")
        # Başlığı TEK satır olarak al: güçlü heuristikler ile seç
        def _pick_header_line(preferred_text: str, alt_text: str) -> str:
            """
            Başlık satırını seçmek için güçlü heuristikler:
            1) Çekirdek kalıp: 'TICARET SICIL' + ('MUDUR'|'MEMURLU') ve satır sonu NDEN/NDAN
            2) Çekirdek + T.C. izi (satır başında)
            3) Üst kısımdaki (ilk ~6 satır) upper-heavy ve çekirdek geçen satır
            4) Güvenli fallback: Adres/Unvan/Tescil/MERSIS/İlan Sıra No gibi içerik başlıkları ile
               başlamayan ilk dolu satır

            Önce preferred_text (temizlenmiş seg), sonra alt_text (raw_text) üzerinde dener.
            """
            def _scan(lines: List[str]) -> str:
                # Ortak ön koşullar
                core_re = re.compile(r"TICARET.*SICIL.*(M[ÜU]D[ÜU]R|MEMURL)", re.IGNORECASE)
                nden_re = re.compile(r"N'?D[EA]N\s*$", re.IGNORECASE)
                tc_re = re.compile(r"^(?:T\s*\.?\s*C\s*\.?|TC\b|T\.C\.)", re.IGNORECASE)
                bad_start = re.compile(r"^(Adres|(?:Yu(?:ka(?:r|rn|n)?[ıi]?da)|Yukarıda|Yukarida)|Tescil|Tescile|MERS[İI]S|Ticaret\s*Sicil|Eski\s+Adres|Telefon|İlan\s*Sira\s*No|Ilan\s*Sira\s*No|Sira\s*No|Madde|Unvan[ıiİI]|Ticaret\s*Unvan[ıiİI])\b", re.IGNORECASE)

                cand_lines = [ln.strip() for ln in lines if ln.strip()]
                top = cand_lines[:8]
                # 1) core + NDEN/NDAN
                for ln in top:
                    norm = _normalize_tr_for_header(ln)
                    if ("TICARET" in norm and "SICIL" in norm and ("MUDUR" in norm or "MEMURLU" in norm)) and (norm.endswith("NDEN") or norm.endswith("NDAN")):
                        return ln
                    if core_re.search(ln) and nden_re.search(ln):
                        return ln
                # 2) core + T.C.
                for ln in top:
                    norm = _normalize_tr_for_header(ln)
                    if ("TICARET" in norm and "SICIL" in norm and ("MUDUR" in norm or "MEMURLU" in norm)) and tc_re.search(ln):
                        return ln
                    if core_re.search(ln) and tc_re.search(ln):
                        return ln
                # 3) upper-heavy + core (başlığa benzer)
                def is_upper_heavy(s: str) -> bool:
                    letters = [ch for ch in s if ch.isalpha()]
                    uppers = [ch for ch in letters if ch.upper() == ch]
                    return (len(letters) >= 6 and len(uppers) / max(len(letters), 1) >= 0.6)

                for ln in top:
                    norm = _normalize_tr_for_header(ln)
                    if ("TICARET" in norm and "SICIL" in norm) and is_upper_heavy(ln):
                        return ln
                # 4) güvenli fallback: kötü başlangıçları ele
                for ln in cand_lines:
                    if not bad_start.search(ln):
                        return ln
                return cand_lines[0] if cand_lines else ""

            # Önce seg (temizlenmiş), sonra raw (temizlenmemiş) üzerinde dene
            res = _scan(preferred_text.splitlines())
            if res:
                return res
            if alt_text and alt_text != preferred_text:
                return _scan(alt_text.splitlines())
            return ""

        header = _pick_header_line(seg, raw)

        # Kişiler zaten maskeli kimlikleri ile birlikte çıkarıldı; doğrudan minimal temizliğe tabi tut
        minimal_persons = _clean_persons_for_minimal(parsed.get("persons") or [])

        minimal = {
            "index": idx,
            "type": "ilan",
            "sicil_office_header": header,
            "original_text": raw,  # orijinal segment (temizlenmemiş)
            "start_offset": segobj.get("start"),
            "end_offset": segobj.get("end"),
            # Kimlik/sicil alanları
            "sicil_dosya_no": parsed.get("sicil_dosya_no"),
            "mersis_no": parsed.get("mersis_no"),
            "trade_name": parsed.get("trade_name"),
            "old_trade_name": parsed.get("old_trade_name"),
            # Adresler (liste yoksa boş liste)
            "addresses": parsed.get("addresses") or [],
            "old_addresses": parsed.get("old_addresses") or [],
            # Kişiler ve maskeli kimlikler (opsiyonel; yoksa boş liste)
            "persons": minimal_persons,
            "masked_ids": parsed.get("masked_ids") or [],
            # Tescil alanları
            "hususlar": parsed.get("hususlar") or [],
            "belgeler": parsed.get("belgeler"),
        }

        out.append(minimal)
        # --- Merkez Nakli: Türetilmiş ilanlar ---
        try:
            txt = raw or seg
            # A) Kaynak metinde açıkça 'Merkez Nakli Sonucu Silinme' varsa: Yeni ofis başlıklarıyla türet
            if re.search(r"merkez\s+nakl[ıi]\s+sonucu\s+silinme", txt, re.IGNORECASE):
                # Yeni Ticaret Sicili Müdürlüğü
                m_office = re.search(
                    r"Yeni\s+Ticaret\s+Sicil[iı]\s+M[üu]d[üu]rl[üu]g[üu][üu]?\s*[:：]?\s*(.+)$",
                    txt,
                    re.IGNORECASE | re.MULTILINE,
                )
                # Yeni Sicil No
                m_sicil = re.search(r"Yeni\s+Sicil\s+No\s*[:：]?\s*([0-9A-Za-z\-_/]+)", txt, re.IGNORECASE)
                # Yeni Adres (çok satır olabilir, tipik başlıklar gelene kadar devamı ekle)
                m_addr_line = re.search(r"Yeni\s+Adres\s*[:：]?\s*(.+)$", txt, re.IGNORECASE | re.MULTILINE)
                new_addr = None
                if m_addr_line:
                    start_pos = m_addr_line.end()
                    line1 = (m_addr_line.group(1) or "").strip()
                    rest = txt[start_pos:]
                    cont = []
                    for ln in rest.splitlines():
                        s = (ln or "").strip()
                        if not s:
                            # İlk satır boş olabilir; içerik yokken boş satırı atla, içerik geldikten sonra boş satırda dur
                            if cont:
                                break
                            else:
                                continue
                        if re.search(r"^(Yukar[ıi]da|ibraz\s+edilen|resen\s+tescil|Tescil\s+Edilen\s+Hususlar|Tescile\s+Delil|Yeni\s+(Ticaret|Sicil|Adres))\b", s, re.IGNORECASE):
                            break
                        cont.append(s)
                        if len(" ".join(cont)) > 220:
                            break
                    new_addr = (line1 + (" " + " ".join(cont) if cont else "")).strip()
                new_office = (m_office.group(1).strip() if m_office else None)
                new_sicil = (m_sicil.group(1).strip() if m_sicil else None)
                if any([new_office, new_sicil, new_addr]):
                    derived = {
                        "type": "ilan",
                        "index": len(out) + 1,
                        "sicil_office_header": new_office or "",
                        "original_text": raw,
                        "start_offset": None,
                        "end_offset": None,
                        "sicil_dosya_no": new_sicil,
                        "mersis_no": parsed.get("mersis_no"),
                        "trade_name": parsed.get("trade_name"),
                        "old_trade_name": parsed.get("old_trade_name"),
                        "addresses": [new_addr] if new_addr else [],
                        "old_addresses": [],
                        "persons": [],
                        "masked_ids": [],
                        "hususlar": ["Merkez Nakli - Yeni Kayit"],
                        "belgeler": None,
                        "is_derived": True,
                        "derived_from_index": idx,
                    }
                    out.append(derived)
            # B) Farklı sicil müdürlüğüne taşınma (Merkez Nakli) ama 'sonucu silinme' yazmıyor:
            #    'Eski Ticaret Sicili Müdürlüğü / Eski Sicil No / Eski Adres' başlıklarına bakıp
            #    'Eski Kayit (Silinme)' için türetilmiş bir kayıt oluştur.
            if re.search(r"Tescil\s+Edilen\s+Hususlar\s*[:：]?\s*.*Merkez\s+Nakl\S{0,2}", txt, re.IGNORECASE) or re.search(r"\bMERKEZ\s+NAKL\S{0,2}\b", txt, re.IGNORECASE):
                m_old_office = re.search(
                    r"Eski\s+Ticaret\s+Sicil[iı]\s*M[üu]d[üu]rl[üu]g[üu][üu]?\s*[:：]?\s*(.+)$",
                    txt,
                    re.IGNORECASE | re.MULTILINE,
                )
                m_old_sicil = re.search(r"Eski\s+Sicil\s+No\s*[:：]?\s*([0-9A-Za-z\-_/]+)", txt, re.IGNORECASE)
                m_old_addr_line = re.search(r"Eski\s+Adres\s*[:：]?\s*(.+)$", txt, re.IGNORECASE | re.MULTILINE)
                old_addr = None
                if m_old_addr_line:
                    start_pos = m_old_addr_line.end()
                    line1 = (m_old_addr_line.group(1) or "").strip()
                    rest = txt[start_pos:]
                    cont2: List[str] = []
                    for ln2 in rest.splitlines():
                        s = (ln2 or "").strip()
                        if not s:
                            # İlk satır boş olabilir; içerik yokken boş satırı atla, içerik geldikten sonra boş satırda dur
                            if cont2:
                                break
                            else:
                                continue
                        # Eski başlık alanını aşma koşulları
                        if re.search(r"^(Yukar[ıi]da|ibraz\s+edilen|resen\s+tescil|Tescil\s+Edilen\s+Hususlar|Tescile\s+Delil|Yeni\s+(Ticaret|Sicil|Adres))\b", s, re.IGNORECASE):
                            break
                        if re.search(r"^(Eski\s+(Ticaret|Sicil|Adres))\b", s, re.IGNORECASE):
                            break
                        cont2.append(s)
                        if len(" ".join(cont2)) > 220:
                            break
                    old_addr = (line1 + (" " + " ".join(cont2) if cont2 else "")).strip()
                old_office = (m_old_office.group(1).strip() if m_old_office else None)
                old_sicil = (m_old_sicil.group(1).strip() if m_old_sicil else None)
                # Tetik: en azından ofis veya sicil ya da adres bilgisinden biri bulunmalı
                if any([old_office, old_sicil, old_addr]):
                    derived_old = {
                        "type": "ilan",
                        "index": len(out) + 1,
                        "sicil_office_header": old_office or "",
                        "original_text": raw,
                        "start_offset": None,
                        "end_offset": None,
                        "sicil_dosya_no": old_sicil,
                        "mersis_no": parsed.get("mersis_no"),
                        "trade_name": parsed.get("trade_name"),
                        "old_trade_name": parsed.get("old_trade_name"),
                        "addresses": [old_addr] if old_addr else [],
                        "old_addresses": [],
                        "persons": [],
                        "masked_ids": [],
                        "hususlar": ["Merkez Nakli - Eski Kayit (Silinme)"],
                        "belgeler": None,
                        "is_derived": True,
                        "derived_from_index": idx,
                    }
                    out.append(derived_old)
        except Exception:
            pass
        if DEBUG_NLP:
            logger.info(
                "DEBUG_NLP parse_multiple_announcements item done index=%d took=%.3fs tn=%r old_tn=%r mersis=%r sicil=%r addr=%d persons=%d",
                idx,
                (time.perf_counter() - t0) if DEBUG_NLP else 0.0,
                minimal.get("trade_name"),
                minimal.get("old_trade_name"),
                minimal.get("mersis_no"),
                minimal.get("sicil_dosya_no"),
                len(minimal.get("addresses") or []),
                len(minimal.get("persons") or []),
            )
        # Son eleman işlendiğinde otomatik kaydet
        if idx == len(segments) and AUTO_SAVE_OCR:
            try:
                _autosave_results_to_ocr_ciktilari(out, original_text=text)
            except Exception as e:
                logger.warning("AUTO_SAVE_OCR hata: %s", e)
    if DEBUG_NLP:
        logger.info(
            "DEBUG_NLP parse_multiple_announcements done total_items=%d took=%.3fs",
            len(out), (time.perf_counter() - t_all) if DEBUG_NLP else 0.0,
        )
    return out
