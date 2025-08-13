import os
import spacy
import logging
import re
from spacy.cli.download import download as spacy_download
from spacy.util import is_package
try:
    from transformers import pipeline as hf_pipeline  # type: ignore
except Exception:  # transformers yoksa da çalışabilsin
    hf_pipeline = None  # type: ignore

# Configure logging
logger = logging.getLogger(__name__)

MODEL_NAME = "tr_core_news_sm"
nlp_model = None
hf_ner = None  # Hugging Face NER pipeline (opsiyonel)

# --- OCR Normalizasyonu ve Yardımcı Regex Fonksiyonları ---
TURKISH_MONTHS = (
    "OCAK|SUBAT|MART|NISAN|MAYIS|HAZIRAN|TEMMUZ|AGUSTOS|EYLUL|EKIM|KASIM|ARALIK"
)

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
    # $ -> Ş gibi çok sık görülen OCR hatası (metinler çoğunlukla büyük harf)
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
    return m.group(1).strip() if m else None

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

    use_hf = os.getenv("USE_HF_NER", "0").strip() in ("1", "true", "True")
    if not use_hf:
        return None

    if hf_pipeline is None:
        logger.warning("transformers bulunamadı; HF NER devre dışı.")
        return None

    # Model kimliğini ortam değişkeninden oku; yoksa makul bir varsayılan dene
    candidates: list[str] = []
    env_model = os.getenv("HF_NER_MODEL", "").strip()
    if env_model:
        candidates.append(env_model)
    # Yaygın ve bakımlı bir Türkçe NER modeli
    candidates.append("savasy/bert-base-turkish-ner-cased")

    # CPU kullanımını zorla (device=-1) ve birden fazla adayı sırayla dene
    for model_id in candidates:
        try:
            logger.info("HF NER modeli yükleniyor: %s", model_id)
            ner = hf_pipeline(
                "token-classification",
                model=model_id,
                aggregation_strategy="simple",
                framework="pt",
                device=-1,
            )
            logger.info("HF NER '%s' yüklendi.", model_id)
            return ner
        except Exception as e:
            logger.warning("HF NER modeli '%s' yüklenemedi: %s", model_id, e)

    logger.warning("HF NER modelleri yüklenemedi; SpaCy/regex ile devam edilecek.")
    return None

def parse_announcement_text(text: str) -> dict:
    """
    Parses the announcement text using spaCy to extract named entities and other info.
    
    Args:
        text: The raw text from the OCR process.
        
    Returns:
        A dictionary with extracted entities.
    """
    if not text:
        return {"error": "Input text cannot be empty."}

    # Normalize et
    norm = normalize_text(text)

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
        for block in chunk_lines(norm):
            try:
                res = ner(block)
                # bazı pipeline sürümleri tek öğe yerine dict dönebilir
                if isinstance(res, dict):
                    hf_results.append(res)
                else:
                    hf_results.extend(res)
            except Exception as e:
                logger.warning(f"HF NER blok hatası: {e}")

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

    # Basit yanlış-pozitif kişi filtrelemesi: para/anahtar kelimeler içerenleri at
    def is_false_person(t: str) -> bool:
        t_low = t.lower()
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
        )
        if any(k in t_low for k in bad_keys):
            return True
        # Çok uzun tek kelime ya da içinde çokça rakam
        if re.search(r"\d", t):
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

    # 4) Ticaret Unvanı – satır bazlı yakala ve durdurucu anahtarlarla temizle
    trade_name = None
    m_unvan = re.search(r"Ticaret\s*Unvan[ıi]\s*[:.]?\s*(.*)", norm, re.IGNORECASE)
    if m_unvan:
        after = m_unvan.group(1).strip()
        if after:
            trade_name = after
        else:
            # Sonraki satırı al (ilk boş olmayan satır)
            lines = norm.splitlines()
            idx = 0
            for i, ln in enumerate(lines):
                if re.search(r"Ticaret\s*Unvan[ıi]\s*:?\s*$", ln, re.IGNORECASE):
                    idx = i
                    break
            for j in range(idx + 1, min(idx + 5, len(lines))):
                cand = lines[j].strip()
                if cand:
                    trade_name = cand
                    break
    if trade_name:
        # Unvan sonuna eklemlenmiş gürültüyü kes (Adres, Tescil, MERSIS vb.)
        stop_pat = re.compile(r"\b(Adres|Yukarıda|Yukarida|Tescil|Tescile|MERS[İI]S|Ticaret\s*Sicil|Eski\s+Adres|Telefon|İlan\s*Sira\s*No|Ilan\s*Sira\s*No|Sira\s*No)\b", re.IGNORECASE)
        mstop = stop_pat.search(trade_name)
        if mstop:
            trade_name = trade_name[: mstop.start()].strip()
        # Makul uzunluk sınırı ve sadeleştirme
        trade_name = re.sub(r"\s+", " ", trade_name).strip()
        if len(trade_name) > 150:
            cuts = re.split(r"(?:\s{2,}|,|;)", trade_name, maxsplit=1)
            trade_name = cuts[0].strip()
        entities["trade_name"] = trade_name
        # ORG listesine de ek olarak itilebilir
        entities["organizations"].append({"text": trade_name, "label": "ORG"})

    # 5) Adres(ler) – satır bazlı, anahtarlarla kes ve uzunluk sınırı uygula
    addresses: list[str] = []
    # "Adres:" satırları
    for m in re.finditer(r"(?mi)^\s*Adres\s*[:.]?\s*(.+)$", norm):
        addresses.append(m.group(1).strip())
    # Eski/Yeni adres varyantları
    for m in re.finditer(r"(?mi)^\s*Eski\s*Adres\s*[:.]?\s*(.+)$", norm):
        addresses.append(("Eski: " + m.group(1).strip()))
    for m in re.finditer(r"(?mi)^\s*Yeni\s*Adres\s*[:.]?\s*(.+)$", norm):
        addresses.append(("Yeni: " + m.group(1).strip()))
    if addresses:
        stop_pat_addr = re.compile(r"\b(Yukarıda|Yukarida|Tescil|Tescile|MERS[İI]S|Ticaret\s*Sicil|Telefon|İlan\s*Sira\s*No|Ilan\s*Sira\s*No|Sira\s*No)\b", re.IGNORECASE)
        cleaned = []
        for a in addresses:
            a = re.sub(r"\s+", " ", a).strip()
            mstop = stop_pat_addr.search(a)
            if mstop:
                a = a[: mstop.start()].strip()
            if len(a) > 220:
                a = a[:220].rstrip()
            if a:
                cleaned.append(a)
        if cleaned:
            entities["addresses"] = unique_list(cleaned)

    # 6) Telefon(lar)
    phones = find_all(r"Telefon\s*[:.]?\s*([+0-9 ()-]{8,})", norm)
    if phones:
        entities["phones"] = unique_list(phones)

    # 7) Maskeli Kimlik No’lar (örn: 179******34)
    masked_ids = find_all(r"\b\d{3}\*{2,6}\d{2,3}\b", norm)
    if masked_ids:
        entities["masked_ids"] = unique_list(masked_ids)

    # 8) TL Tutarları
    amounts = find_all(r"\b\d{1,3}(?:\.\d{3})*(?:,\d{2})?\s*(?:TL|Türk Lirasi|Türk Lirası)\b", norm)
    if amounts:
        for a in unique_list(amounts):
            entities["money"].append({"text": a, "label": "MONEY"})

    # 9) Tarihler (dd.mm.yyyy veya ‘24 MAYIS 2023’)
    regex_dates = find_all(r"\b\d{1,2}\.\d{1,2}\.\d{4}\b", norm)
    regex_dates += find_all(rf"\b\d{{1,2}}\s+(?:{TURKISH_MONTHS})\s+\d{{4}}\b", norm, flags=re.IGNORECASE)
    if regex_dates:
        for d in unique_list(regex_dates):
            entities["dates"].append({"text": d, "label": "DATE"})
            
    return entities

def split_announcements(text: str) -> list[str]:
    """
    OCR metnini ilân segmentlerine böler.
    Bölme ölçütü: "Ticaret Sicili Müdürlüğü'nden" veya "Ticaret Sicili Memurluğu'ndan"
    benzeri başlıkları içeren satırlar. (Yeni 2 sütunlu ve eski 5 sütunlu tipler)

    Dönüş: Normalized metin parçaları listesi (başlık satırı dahil).
    """
    if not text:
        return []

    # Başlık kalıbı (ham metin üzerinde):
    #  - "Eski Ticaret Sicili Müdürlügü:" ile başlayan sahte başlıkları dışla
    #  - satır sonu "NDEN/NDAN" varyantları ile bitmeli (apostrof olabilir)
    # 5 sütunlu eski gazete OCR'larında başlık kelimeleri satırlara bölünebilir.
    # Bu nedenle 'TİCARET' 'SİCİLİ' ve 'MÜDÜRLÜĞÜNDEN/MEMURLUĞUNDAN' arasında
    # satır sonlarına izin veren daha toleranslı bir regex kullanıyoruz.
    header_re = re.compile(
        r"(?mi)^\s*(?!Eski\b)(?:T\.?C\.?\s*)?.{0,80}?"
        r"TICARET(?:\s+|\r?\n){0,2}SICIL[Iİ]"
        r"(?:\s+|\r?\n){0,2}(?:M[ÜU]D[ÜU]R[^\n\r]{0,20}|MEMURL[^\n\r]{0,20})"
        r"N'?D[EA]N\s*$"
    )

    # Aşırı gürültü sayfa/aktarma satırlarını temizleyerek bölme sonrası metni sadeleştir
    def clean_lines(seg: str) -> str:
        lines = []
        for ln in seg.splitlines():
            l2 = ln.strip()
            if not l2:
                lines.append(ln)
                continue
            # Önceki/sonraki sayfa ve sayfa numarası satırlarını at
            if re.search(r"(?i)devam[iı]|bastarafi|^\s*sayfa\s*[:\-]", l2):
                continue
            lines.append(ln)
        # Çoklu boş satırları azalt
        out = "\n".join(lines)
        out = re.sub(r"\n{3,}", "\n\n", out)
        return out.strip()

    matches = list(header_re.finditer(text))
    # Fallback: 5 sütunlu OCR'da araya gürültü girerse, yalnızca
    # '...Müdürlüğünden'/'...Memurluğundan' ile biten satırları ankraj al.
    if len(matches) <= 1:
        fallback_re = re.compile(r"(?mi)^\s*(?!Eski\b).{0,160}?(m[üu]d[üu]rl[üu][ğg]?[üu]?nden|memurlu[ğg]?[üu]?ndan)\s*$")
        fb = list(fallback_re.finditer(text))
        if len(fb) > len(matches):
            matches = fb
    if not matches:
        # Hiç başlık yoksa tüm metni tek ilân varsay
        return [clean_lines(text)] if text.strip() else []

    segments: list[str] = []
    for i, m in enumerate(matches):
        start = m.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        seg = text[start:end].strip()
        seg = clean_lines(seg)
        if seg:
            segments.append(seg)
    return segments

def split_announcements_with_offsets(text: str) -> list[dict]:
    """
    OCR metnini ilân segmentlerine böler ve her segment için orijinal metin
    üzerindeki başlangıç/bitiş karakter ofsetlerini de döner.

    Dönüş: { start, end, text } sözlüklerinden oluşan liste.
    - start/end: orijinal 'text' içinde [start:end) aralığı
    - text: 'split_announcements' ile aynı temizleme kuralları uygulanmış segment
    """
    if not text:
        return []

    header_re = re.compile(
        r"(?mi)^\s*(?!Eski\b)(?:T\.?C\.?\s*)?.{0,80}?"
        r"TICARET(?:\s+|\r?\n){0,2}SICIL[Iİ]"
        r"(?:\s+|\r?\n){0,2}(?:M[ÜU]D[ÜU]R[^\n\r]{0,20}|MEMURL[^\n\r]{0,20})"
        r"N'?D[EA]N\s*$"
    )

    def clean_lines(seg: str) -> str:
        lines = []
        for ln in seg.splitlines():
            l2 = ln.strip()
            if not l2:
                lines.append(ln)
                continue
            if re.search(r"(?i)devam[iı]|bastarafi|^\s*sayfa\s*[:\-]", l2):
                continue
            lines.append(ln)
        out = "\n".join(lines)
        out = re.sub(r"\n{3,}", "\n\n", out)
        return out.strip()

    matches = list(header_re.finditer(text))
    if len(matches) <= 1:
        fallback_re = re.compile(r"(?mi)^\s*(?!Eski\b).{0,160}?(m[üu]d[üu]rl[üu][ğg]?[üu]?nden|memurlu[ğg]?[üu]?ndan)\s*$")
        fb = list(fallback_re.finditer(text))
        if len(fb) > len(matches):
            matches = fb
    if not matches:
        return ([{"start": 0, "end": len(text), "text": clean_lines(text)}]
                if text.strip() else [])

    out: list[dict] = []
    for i, m in enumerate(matches):
        start = m.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        raw = text[start:end].strip()
        seg = clean_lines(raw)
        if seg:
            out.append({"start": start, "end": end, "text": seg})
    return out

def parse_multiple_announcements(text: str) -> list[dict]:
    """
    Metni ilânlara böler ve her ilânı `parse_announcement_text` ile işler.
    ÇIKTIYI SADELEŞTİRİR:
      - Sadece şu alanları döner: index, sicil_office_header, original_text,
        registration_number, sicil_dosya_no, mersis_no, trade_name, addresses
      - Tüm diğer varlık listelerini (organizations, locations, persons, dates, money, misc)
        Swift Codable kırılmaması için boş liste olarak set eder.
    """
    out: list[dict] = []
    for idx, segobj in enumerate(split_announcements_with_offsets(text), start=1):
        seg = segobj["text"]
        parsed = parse_announcement_text(seg)
        # Başlık satır(lar)ını daha sağlıklı oluştur: ilk dolu satırdan başlayıp
        # '...nden' (Müdürlüğünden/Memurluğundan) içeren satıra kadar 1-4 satırı birleştir.
        header_lines: list[str] = []
        for ln in seg.splitlines():
            s = ln.strip()
            if not s:
                continue
            header_lines.append(s)
            if re.search(r"(?i)m[üu]d[üu]rl[üu][ğg]?[üu]?nden|memurlu[ğg]?[üu]?ndan|m[üu]d[üu]rl[üu]g[üu]nden", s):
                break
            if len(header_lines) >= 4:
                break
        header = " ".join(header_lines).strip()

        minimal = {
            "index": idx,
            "sicil_office_header": header,
            "original_text": seg,  # ham segment (normalize edilmemiş)
            "start_offset": segobj.get("start"),
            "end_offset": segobj.get("end"),
            # Kimlik/sicil alanları
            "registration_number": parsed.get("registration_number"),
            "sicil_dosya_no": parsed.get("sicil_dosya_no"),
            "mersis_no": parsed.get("mersis_no"),
            "trade_name": parsed.get("trade_name"),
            # Adresler (liste yoksa boş liste)
            "addresses": parsed.get("addresses") or [],
            # Diğer varlık listeleri boş dönsün (UI opsiyonel alanları güvenle decode etsin)
            "organizations": [],
            "locations": [],
            "persons": [],
            "dates": [],
            "money": [],
            "misc": [],
        }

        out.append(minimal)
    return out
