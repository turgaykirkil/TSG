# -*- coding: utf-8 -*-
"""
Merkezi Sicil Müdürlüğü normalizasyonu.

Amaç:
- OCR başlıklarından ve serbest metinden, resmi dropdown listesi ile birebir eşleşen
  ofis adını (Türkçe karakterlerle) üretmek.
- Proje genelinde tekrar eden VALID_CITIES listelerini tek bir kaynağa çekmek.

Kullanım:
- normalize_office_from_header(header: str) -> Optional[str]
- normalize_office_freeform(value: str) -> Optional[str]
- VALID_SICIL_OFFICES: List[str]

Notlar:
- EREĞLİ için 'KONYA EREĞLİ' ve 'KARADENİZ EREĞLİ' ayrımı özel durum olarak ele alınır.
- Eşlemede Türkçe/ASCII farkları ve ek/sonekler ("TİCARET SİCİ(L) (İ) MÜDÜRLÜĞÜ") temizlenerek
  en uzun resmi isim eşleşmesi tercih edilir.
"""
from __future__ import annotations

import re
from typing import List, Optional

# Resmi dropdown ile uyumlu ofis isimleri
VALID_SICIL_OFFICES: List[str] = [
    "İSTANBUL", "ANKARA", "İZMİR", "ACIPAYAM", "ADANA", "ADIYAMAN", "AFYONKARAHİSAR",
    "AFŞİN", "AKHİSAR", "AKSARAY", "AKYAZI", "AKÇAKOCA", "AKŞEHİR", "ALACA", "ALANYA",
    "ALAPLI", "ALAŞEHİR", "ALİAĞA", "AMASYA", "ANAMUR", "ANTALYA", "ARDAHAN", "ARDEŞEN",
    "ARHAVİ", "ARTVİN", "AYDIN", "AYVALIK", "AĞRI", "BABADAĞ", "BABAESKİ", "BAFRA",
    "BALIKESİR", "BANDIRMA", "BARTIN", "BATMAN", "BAYBURT", "BAYINDIR", "BERGAMA", "BEYPAZARI",
    "BEYŞEHİR", "BODRUM", "BOLU", "BOLVADİN", "BOR", "BORÇKA", "BOYABAT", "BOZÜYÜK",
    "BOĞAZLIYAN", "BUCAK", "BULANCAK", "BULDAN", "BURDUR", "BURHANİYE", "BURSA", "BÜNYAN",
    "BİGA", "BİLECİK", "BİNGÖL", "BİRECİK", "BİTLİS", "CEYHAN", "CİZRE", "DEMİRCİ",
    "DENİZLİ", "DEVELİ", "DEVREK", "DOĞANHİSAR", "DOĞUBAYAZIT", "DÖRTYOL", "DÜZCE", "DİDİM",
    "DİNAR", "DİYARBAKIR", "EDREMİT", "EDİRNE", "ELAZIĞ", "ELBİSTAN", "EMİRDAĞ", "ERBAA",
    "ERCİŞ", "ERDEK", "ERDEMLİ", "ERZURUM", "ERZİN", "ERZİNCAN", "ESKİŞEHİR", "FATSA",
    "FETHİYE", "GAZİANTEP", "GEBZE", "GEDİZ", "GELİBOLU", "GEMLİK", "GEREDE", "GÖNEN",
    "GÖRDES", "GÜMÜŞHACIKÖY", "GÜMÜŞHANE", "GİRESUN", "HAKKARİ", "HATAY", "HAVZA",
    "HAYMANA", "HAYRABOLU", "HOPA", "ILGIN", "ISPARTA", "IĞDIR", "KAHRAMANMARAŞ", "KADİRLİ",
    "KAMAN", "KARABÜK", "KARACABEY", "KARAHALLI", "KARAMAN", "KARAPINAR", "KARS",
    "KASTAMONU", "KAYSERİ", "KELKİT", "KEŞAN", "KIRIKHAN", "KIRIKKALE", "KIRKLARELİ",
    "KIRŞEHİR", "KIZILTEPE", "KOCAELİ", "KONYA EREĞLİ", "KONYA", "KOZAN", "KUMLUCA",
    "KUŞADASI", "KÖRFEZ", "KÜTAHYA", "KİLİS", "LÜLEBURGAZ", "MALATYA", "MALKARA",
    "MANAVGAT", "MANİSA", "MARDİN", "MARMARİS", "MENEMEN", "MERSİN", "MERZİFON", "MUCUR",
    "MUSTAFAKEMALPAŞA", "MUT", "MUĞLA", "MUŞ", "MİLAS", "NAZİLLİ", "NEVŞEHİR",
    "NUSAYBİN", "NİKSAR", "NİZİP", "NİĞDE", "OLTU", "ORDU", "ORHANGAZİ", "OSMANİYE",
    "PASİNLER", "PAZAR", "POLATLI", "REYHANLI", "RİZE", "SAFRANBOLU", "SAKARYA",
    "SALİHLİ", "SAMSUN", "SANDIKLI", "SARAYKÖY", "SELÇUK", "SEYDİŞEHİR", "SOMA",
    "SULUOVA", "SUNGURLU", "SUSURLUK", "SÖKE", "SİLİFKE", "SİMAV", "SİNOP", "SİVAS",
    "SİVEREK", "SİİRT", "TARSUS", "TATVAN", "TAVAS", "TAVŞANLI", "TAŞKÖPRÜ", "TEKİRDAĞ",
    "TERME", "TOKAT", "TORBALI", "TOSYA", "TRABZON", "TUNCELİ", "TURGUTLU", "TURHAL",
    "TİRE", "UZUNKÖPRÜ", "UŞAK", "VAN", "VEZİRKÖPRÜ", "YAHYALI", "YALOVA", "YALVAÇ",
    "YENİŞEHİR", "YERKÖY", "YOZGAT", "YÜKSEKOVA", "ZONGULDAK", "ZİLE", "ÇANAKKALE",
    "ÇANKIRI", "ÇARŞAMBA", "ÇAY", "ÇAYCUMA", "ÇAYELİ", "ÇERKEZKÖY", "ÇORLU", "ÇORUM",
    "ÇUMRA", "ÖDEMİŞ", "ÜNYE", "ÜRGÜP", "İNEBOLU", "İNEGÖL", "İSKENDERUN", "İSLAHİYE",
    "İZNİK", "ŞANLIURFA", "ŞEREFLİKOÇHİSAR", "ŞIRNAK", "SORGUN", "OF", "ŞEFAATLİ",
    "KARADENİZ EREĞLİ",
]

_SUFFIX_PATTERNS = [
    # Genel gürültü ve bağlaçlar
    r"\bVE\b",
    r"\bVE TİCARET\b",
    r"\bSANAYİ\b",
    r"\bSANAYI\b",
    r"\bODASI\b",
    r"\bODA\b",
    r"\bBORSASI\b",
    # Sicil yapısı ve kurum kelimeleri
    r"\bTİCARET\b",
    r"\bSİCİLİ\b",
    r"\bSİCİL\b",
    r"\bMÜDÜRLÜĞÜ\b",
    r"\bMÜD\.?\b",
    r"\bMÜDÜRLÜĞÜ'NDEN\b",
    r"\bMÜDÜRLÜĞÜNDEN\b",
    # ASCII varyasyonları (OCR hatalarına dayanıklı)
    r"\bTICARET\b",
    r"\bSICILI\b",
    r"\bSICIL\b",
    r"\bMUDURLUGU\b",
    r"\bMUD\.?\b",
    r"\bMUDURLUGU'NDEN\b",
    r"\bMUDURLUGUNDEN\b",
]

# Baş kısımdaki yaygın önekler (T.C., Türkiye Cumhuriyeti vb.)
_PREFIX_PATTERNS = [
    r"^(?:T\s*\.?\s*C\s*\.?\s*)+",  # T.C. / T C / TC. / T. C. vb.
    r"^(?:TÜRKİYE\s+CUMHURİYETİ\s+)",
    r"^(?:TURKIYE\s+CUMHURIYETI\s+)",
]

_TR_TO_ASCII = str.maketrans({
    "İ": "I", "I": "I", "ı": "I", "i": "I",
    "Ğ": "G", "ğ": "G",
    "Ü": "U", "ü": "U",
    "Ş": "S", "ş": "S",
    "Ö": "O", "ö": "O",
    "Ç": "C", "ç": "C",
    "Â": "A", "â": "A", "Î": "I", "î": "I", "Û": "U", "û": "U",
})


def _normalize_key(s: str) -> str:
    if not s:
        return ""
    s = s.upper()
    s = s.translate(_TR_TO_ASCII)
    s = re.sub(r"[^A-Z0-9]+", "", s)
    return s


# Hazırla: resmi isim -> normalized key
_OFFICE_KEYS = [(name, _normalize_key(name)) for name in VALID_SICIL_OFFICES]


def _strip_common_suffixes(s: str) -> str:
    cleaned = s
    # Önce baştaki önekleri kaldır
    for pat in _PREFIX_PATTERNS:
        cleaned = re.sub(pat, "", cleaned, flags=re.IGNORECASE)
    # Sonra gürültü/sonek kelimeleri temizle
    for pat in _SUFFIX_PATTERNS:
        cleaned = re.sub(pat, " ", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned


def _longest_office_match(text_key: str) -> Optional[str]:
    """Normalleştirilmiş metin anahtarında geçen en uzun resmi ofis adını bulur."""
    matches = []
    for official, k in _OFFICE_KEYS:
        if not k:
            continue
        if k in text_key:
            matches.append((len(k), official))
    if not matches:
        return None
    matches.sort(key=lambda x: x[0], reverse=True)
    return matches[0][1]


def _eregli_disambiguation(text_key: str) -> Optional[str]:
    if "EREGLI" in text_key:
        if "KONYA" in text_key:
            return "KONYA EREĞLİ"
        if "KARADENIZ" in text_key:
            return "KARADENİZ EREĞLİ"
    return None


def normalize_office_from_header(header: Optional[str]) -> Optional[str]:
    """
    OCR başlığından resmi sicil müdürlüğü adını üretir.
    Ör: "İZMİR TİCARET SİCİLİ MÜDÜRLÜĞÜ'NDEN" -> "İZMİR"
        "KONYA EREĞLİ TİCARET SİCİL MÜDÜRLÜĞÜ" -> "KONYA EREĞLİ"
    """
    if not header:
        return None
    h = str(header).strip().upper()
    h = _strip_common_suffixes(h)
    key = _normalize_key(h)

    # Özel ayrım
    special = _eregli_disambiguation(key)
    if special:
        return special

    # En uzun eşleşme
    m = _longest_office_match(key)
    if m:
        return m

    # İlk kelime denemesi (resmi listede mevcutsa)
    first = h.split()[0] if h.split() else ""
    if first:
        for official in VALID_SICIL_OFFICES:
            if official == first:
                return official

    return None


def normalize_office_freeform(value: Optional[str]) -> Optional[str]:
    """
    Serbest metinden (örn. frontend formu veya DB) resmi ofis adını bulur.
    Başlıktaki kadar gürültülü değilse de aynı stratejiyi uygular.
    """
    if not value:
        return None
    v = str(value).strip().upper()
    key = _normalize_key(v)

    special = _eregli_disambiguation(key)
    if special:
        return special

    m = _longest_office_match(key)
    if m:
        return m

    # Tam eşitlik
    for official in VALID_SICIL_OFFICES:
        if v == official:
            return official

    return None
