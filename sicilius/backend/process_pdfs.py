#!/usr/bin/env python3
"""
OCR Pipeline v2.0: "Dual-Brain Guardian"
PDF → Apple Vision OCR (tüm sayfalar) → Regex Segmentasyon → Dual-Model → NlpParsedAnnouncement JSON

Geçmiş hatalardan çıkarılan dersler:
  1. Şema tutarsızlığı → Strict schema validation (şema dışı key silinir)
  2. Trade name halüsinasyonu → Guardian Override (regex → LLM ezer)
  3. OCR typo tolerance → Regex patterns "Unvam/Unvanı/Unvan" toleranslı
  4. Tek sayfa kısıtı → Tüm sayfalar okunur
  5. Adres kesilmesi → Multiline address regex
  6. OCR gürültüsü → Persons: sadece Kimlik No + isim pattern
"""

import os
import sys
import json
import re
import subprocess
import time
import requests
import fitz  # PyMuPDF

# ============================================================================
# CONFIGURATION
# ============================================================================

BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BACKEND_DIR)

BUCKET_NAME = "gazette-pdfs"
LIMIT = 10  # Test aşamasında limitli
OUTPUT_DIR = os.path.join(BACKEND_DIR, "test_ocr_vizualisation")
VISION_TOOL_PATH = os.path.join(BACKEND_DIR, "vision_ocr.swift")
OLLAMA_URL = "http://localhost:11434/api/generate"
DEFAULT_MODEL = "llama3.2:3b"

# Dual-model: Sıralı çalışır, aynı anda yük binmez
MODELS = ["gemma4:e4b", "llama3:8b"]

# ============================================================================
# OCR TEXT NORMALIZATION
# ============================================================================

OCR_FIXES = [
    (r"İ̇", "İ"),        # Çift noktalı İ düzelt
    (r"\u00ad", ""),      # Soft hyphen kaldır
    (r"[ \t](?=\n)", ""), # Satır sonu boşlukları temizle
    (r"\n{3,}", "\n\n"),  # 3+ boş satırı 2'ye indir
]

def normalize_ocr_text(raw: str) -> str:
    """OCR çıktısındaki yaygın hataları düzeltir."""
    txt = raw
    for pat, rep in OCR_FIXES:
        txt = re.sub(pat, rep, txt)
    return txt.strip()

# ============================================================================
# OCR-TOLERANT REGEX PATTERNS (Ders #3: Typo toleransı)
# ============================================================================

# Header segmentasyonu: "T.C. ... TİCARET SİCİLİ MÜDÜRLÜĞÜ'NDEN" veya "MAHKEMES'NDEN"
RE_HEADER_ADVANCED = re.compile(
    r"(?i)(?<!Merkezin Kayıtlı Olduğu\s)"
    r"(?<!Eski\s)"
    r"(?:T\.?C\.?\s*)?"
    r"(?:[A-ZÇĞİÖŞÜa-zçğıöşü\s]*?)"
    r"(?:T[İIÍiı]CARET\s+S[İIÍiı]C[İIÍiı]L[İIÍiı]\s+(?:M[ÜUÚu]D[ÜUÚu]RL[ÜUÚu][ĞGGg][ÜUÚu]|MEMURLU[ĞGGg][UÜÚu])(?:[''\u2019]?[NNDDTt][FEENNDDTt]+)?|"
    r"MAHKEMES[İIÍiı][''\u2019]?[NNDDTt][FEENNDDTt]+)"
)

RE_METADATA_ANCHOR = re.compile(
    r"(?i)(?:"
    r"(?:[İiIı]lan\s+S[ıiİI]ra\s*(?:No)?\s*[:\s]*\d+)|"
    r"(?:MERS[İIÍiı]S\s*(?:No)?\s*[:\s]*\d{14,18})|"
    r"(?:ticaret\s+sicil(?:/dosya)?\s*(?:no)?\s*[:\s]*[0-9/\- ]+)"
    r")"
)

# Ticaret Unvanı (OCR typo toleranslı: Unvam, Unvanı, Unvan, Unvant)
RE_TRADE_NAME = re.compile(
    r"(?i)(?:ticaret\s+)?[üu]nvan[ıit]?\s*[:\s]\s*\n?"
    r"(?P<name>.+?)\s*"
    r"(?=\n\s*(?:Adres\s*[:]|Eski\s+Ticaret|Yukarıda))",
    re.DOTALL
)

# Eski Ticaret Unvanı
RE_OLD_TRADE_NAME = re.compile(
    r"(?i)(?:eski\s+ticaret\s+[üu]nvan[ıit]?)\s*[:\s]\s*\n?"
    r"(?P<name>.+?)(?:\n\s*(?:Adres|Adresi|İsdan|Isdan|Yukarıda|Tescil|İşletme|Isletme)|$)",
    re.DOTALL
)

# MERSIS No: 16 haneli
RE_MERSIS = re.compile(r"\b\d{16}\b")

# Ticaret Sicil/Dosya No
RE_SICIL_NO = re.compile(
    r"(?i)(?:ticaret\s+)?sicil(?:/Dosya)?\s*(?:no|numarası)\s*[:\s]*([0-9/\- ]+)"
)

# İlan Sıra No
RE_ILAN_SIRA = re.compile(
    r"(?i)[İi]lan\s+S[ıi]ra\s+No\s*[:\s]*(\d+)"
)

# Adres (multiline toleranslı - Ders #5, v2: greedy fix)
RE_ADDRESS = re.compile(
    r"(?i)(?:adres|merkez\s+adresi)\s*[:\s]\s*"
    r"(?P<addr>[^\n]+(?:\n[^\n]{1,60})?)"
    r"(?=\nYukarıda|\nTescil|\n[A-ZÖÇŞİĞÜ]{4,}|$)",
    re.DOTALL
)

# Adres değişikliği: "X adresinden, Y adresine taşınmıştır"
RE_ADDRESS_CHANGE = re.compile(
    r"(.{8,250}?)\s+adresinden,?\s+(.{8,250}?)\s+adresine\s+(?:taşınmıştır|nakledilmiştir|taşınmasına|nakline)",
    re.IGNORECASE | re.DOTALL
)

# Kişiler: Kimlik No + İsim (Ders #6: OCR gürültüsü filtresi, v2: sadece BÜYÜK HARF isimler)
RE_PERSON = re.compile(
    r"(\d{3}\*{4,6}\d{2})\s+Kimlik\s+No['’]?lu[,\s]+"
    r"(?:[^,]*?adresinde\s+ikamet\s+eden[,\s]+)?"
    r"([A-ZÖÇŞİĞÜ][A-ZÖÇŞİĞÜa-zöçşığü]+(?:\s+[A-ZÖÇŞİĞÜ][A-ZÖÇŞİĞÜa-zöçşığü]+){1,4})"
    r"(?:\s+Müdür|\s+olarak|\s*;|\s+\d+)",
    re.DOTALL
)

# Kişi tablosu: Satır bazlı isim + masked TC
RE_PERSON_TABLE = re.compile(
    r"(?P<name>[A-ZÖÇŞİĞÜ][A-ZÖÇŞİĞÜ\s]+?)\s+(?P<tc>\d{3}\*{4,6}\d{2})"
)

# Tescil Edilen Hususlar
RE_HUSUSLAR = re.compile(
    r"(?i)Tescil\s+Edilen\s+Hususlar\s*[:\s]*(.+?)(?:\n|$)"
)

# Tescile Delil Olan Belgeler
RE_BELGELER = re.compile(
    r"(?i)Tescile\s+Delil\s+Olan\s+Belgeler\s*[:\s]*(.+?)(?:\n\n|\n[A-ZÖÇŞİĞÜ]|\Z)",
    re.DOTALL
)

# ============================================================================
# REGEX ENTITY EXTRACTION (Guardian Layer)
# ============================================================================

def extract_entities_regex(text: str) -> dict:
    """
    Regex tabanlı deterministik entity çıkarımı.
    LLM'den ÖNCE çalışır ve sonuçları LLM çıktısının ÜZERİNE yazar.
    """
    entities = {
        "trade_name": None,
        "old_trade_name": None,
        "registration_number": None,
        "sicil_dosya_no": None,
        "mersis_no": None,
        "addresses": [],
        "old_addresses": [],
        "persons": [],
        "ilan_sira_no": [],
        "hususlar": [],
        "belgeler": None,
    }

    # Trade name
    m = RE_TRADE_NAME.search(text)
    if m:
        name = m.group("name").strip()
        # Çok satırlı isimleri birleştir, fazla boşlukları temizle
        name = re.sub(r"\s+", " ", name).strip(" .:-\n")
        # "Şirketin unvanı X" veya "Şirketin X" → sadece X'i al (prefix temizliği)
        name = re.sub(r"şirketin\s+(?:unvan[ıi]?\s+)?", "", name, flags=re.IGNORECASE).strip()
        # Sondaki kesik kelimeleri temizle (İN, Adr, Adre gibi)
        name = re.sub(r"\s+(?:İN|IN|Adr(?:es)?)\s*$", "", name).strip()
        if len(name) > 3:
            entities["trade_name"] = name

    # Old trade name
    m = RE_OLD_TRADE_NAME.search(text)
    if m:
        name = re.sub(r"\s+", " ", m.group("name")).strip(" .:-\n")
        if len(name) > 3:
            entities["old_trade_name"] = name

    # Sicil no
    m = RE_SICIL_NO.search(text)
    if m:
        sicil = m.group(1).strip()
        entities["registration_number"] = sicil
        entities["sicil_dosya_no"] = sicil

    persons_list = []
    seen = set()

    def normalize_tckn_typos(tc_raw: str) -> str:
        if not tc_raw:
            return ""
        tc = tc_raw.strip()
        if len(tc) == 11:
            if tc[-1] in "({[OoD":
                tc = tc[:-1] + "0"
            elif tc[-1] in "sS":
                tc = tc[:-1] + "8"
        return tc

    def is_valid_tckn_format(tc_str: str) -> bool:
        if not tc_str:
            return False
        tc_clean = normalize_tckn_typos(tc_str)
        if len(tc_clean) != 11:
            return False
        if tc_clean[0] == '0':
            return False
        if tc_clean[-1] not in "02468":
            return False
        return True

LEGAL_FINANCIAL_WORDS = [
    "sermaye", "tl", "pay", "şube", "sube", "tasfiye", "akçe", "akce", "ayrılması", "ayrilmasi",
    "noter", "noterliği", "noterligi", "kimlik", "numarası", "numarasi", "mersis", "sicil",
    "madde", "fıkra", "fikra", "bent", "sayı", "sayi", "tarih", "tarihi", "tarihine", "yol",
    "cadde", "caddesi", "sokak", "sokağı", "mahalle", "mahallesi", "blok", "daire", "no",
    "telsiz", "temsil", "temsile", "karar", "aksi", "alınıncaya", "alıncaya", "kadar",
    "üyeliğine", "uyeligine", "yönetim", "yonetim", "kurul", "kurulu", "başkana", "başkan",
    "baskan", "müdür", "mudur", "müdürlük", "müdürlüğü", "müdürlüğe", "seçilenler", "secilenler",
    "değişiklik", "degisiklik", "dağılımındaki", "dagilimindaki", "görev", "gorev", "dağılım",
    "dagilim", "yetkililer", "müdürler", "mudurler", "devreden", "devralan", "devri", "bilgisi",
    "ortaklık", "ortaklik", "şirket", "sirket", "unvan", "unvanı", "ticaret", "limited", "anonim",
    "kooperatif", "tüzük", "tuzuk", "gazete", "gazetesi", "ilan", "tescil", "terkin", "hissesi",
    "ikamet", "eden", "adresinde", "adresine", "uyruklu", "uyruğu", "uyrugu", "yerleşim",
    "yerlesim", "yeri", "yerleşim yeri", "kimlik no", "türkiye", "turkiye", "cumhuriyeti"
]

DISTRICT_CITY_PREFIXES = [
    "ISTANBUL", "İSTANBUL", "ANKARA", "İZMİR", "BURSA", "ANTALYA", "ADANA", "KONYA",
    "GAZIOSMAN", "BAŞAKŞEHİR", "BASAKSEHIR", "ESENLER", "ZEYTİNBURNU", "ZEYTINBURNU",
    "BAĞCILAR", "BAGCILAR", "KADIKÖY", "KADIKOY", "ÜSKÜDAR", "USKUDAR", "ŞİŞLİ", "SISLI",
    "BEŞİKTAŞ", "BESIKTAS", "ÜMRANİYE", "UMRANIYE", "PENDİK", "PENDIK", "KARTAL", "MALTEPE",
    "TUZLA", "BEYLİKDÜZÜ", "BEYLIKDUZU", "AVCILAR", "BÜYÜKÇEKMECE", "BUYUKCEKMECE",
    "KÜÇÜKÇEKMECE", "KUCUKCEKMECE", "BAKIRKÖY", "BAKIRKOY", "SARIYER", "BEYOĞLU", "BEYOGLU",
    "FATİH", "FATIH", "EYÜP", "EYUP", "EYÜPSULTAN", "SULTANGAZİ", "SULTANGAZI", "ARNAVUTKÖY",
    "ARNAVUTKOY", "ÇATALCA", "CATALCA", "ŞİLE", "SILE", "SILIVRI", "SİLİVRİ"
]

def is_valid_tckn_format(tc: str) -> bool:
    if not tc:
        return False
    s = str(tc).strip()
    if len(s) == 11 and (s.isdigit() or re.match(r"^[1-9]\d{2}[\*\d]{4,6}\d{2}$", s)):
        return True
    return False

def clean_person_name(name_raw: str) -> str:
    if not name_raw:
        return ""
    name_clean = re.sub(r"(?i)\b(?:TÜRKİYE|CUMHUR[İI]YET[İI]|CUMHUKIIEI|TURK|TÜRK|UYRUK|TC|T\.C\.)\b.*$", "", str(name_raw)).strip()
    name_clean = re.sub(r"[^\w\s\-]", " ", name_clean, flags=re.UNICODE).strip()
    name_clean = re.sub(r"\s+", " ", name_clean).strip()
    
    if re.search(r"\d", name_clean):
        return ""
        
    words = [w for w in name_clean.split()]
    if len(words) < 2 or len(words) > 4:
        return ""
        
    FORBIDDEN_ROOTS = [
        "tasfiy", "alacakl", "cagr", "cagn", "dolay", "noter", "sermay", "tescil", "terkin", 
        "unvan", "sirket", "limited", "anonim", "adres", "mudur", "temsil", "karar", "ilan",
        "turk", "cumhur", "gazet", "sicil", "mersis", "faaliyet", "durum"
    ]
    
    for w in words:
        w_lower = w.lower()
        w_norm = (
            w_lower.replace("ı", "i").replace("g", "g").replace("ğ", "g")
            .replace("ş", "s").replace("ü", "u").replace("ö", "o").replace("ç", "c")
        )
        w_upper = w.upper()
        if w_lower in LEGAL_FINANCIAL_WORDS:
            return ""
        if any(w_norm.startswith(root) for root in FORBIDDEN_ROOTS):
            return ""
        if any(w_upper.startswith(prefix) for prefix in DISTRICT_CITY_PREFIXES):
            return ""
            
    if any(len(w) < 2 for w in words):
        return ""
        
    return " ".join(words)

def extract_entities_regex(text: str) -> dict:
    entities = {
        "trade_name": None,
        "old_trade_name": None,
        "registration_number": None,
        "sicil_dosya_no": None,
        "mersis_no": None,
        "addresses": [],
        "old_addresses": [],
        "persons": [],
        "hususlar": [],
        "belgeler": [],
        "ilan_sira_no": [],
    }
    persons_list = []
    seen = set()

    def add_person(name, tc):
        cleaned_name = clean_person_name(name)
        tc_clean = tc.strip() if tc else None
        
        if not cleaned_name:
            return
            
        if tc_clean and not is_valid_tckn_format(tc_clean):
            return
            
        key = (cleaned_name.upper(), tc_clean)
        if key not in seen:
            seen.add(key)
            persons_list.append({"name": cleaned_name, "tckn": tc_clean})

    # MERSIS
    m = RE_MERSIS.search(text)
    if m:
        entities["mersis_no"] = m.group(0)
        mersis_val = m.group(0)
        if mersis_val[0] in "123456789":
            owner_tckn = mersis_val[:11]
            if is_valid_tckn_format(owner_tckn):
                add_person("İşletme Sahibi", owner_tckn)

    # Address change
    change = RE_ADDRESS_CHANGE.search(text)
    if change:
        old_addr = re.sub(r"\s+", " ", change.group(1)).strip()
        old_addr = re.sub(r"^.*?\badresi\s+", "", old_addr, flags=re.IGNORECASE).strip()
        new_addr = re.sub(r"\s+", " ", change.group(2)).strip()
        entities["addresses"] = [new_addr]
        entities["old_addresses"] = [old_addr]
    else:
        m = RE_ADDRESS.search(text)
        if m:
            entities["addresses"] = [re.sub(r"\s+", " ", m.group("addr")).strip()]

    # Strategy 0: Direct TCKN + Name parser (handles "Kimlik Numaralı NAME", "Kimlik No'lu ... adresinde ikamet eden, NAME")
    direct_tc_pattern = re.compile(
        r"([1-9]\d{2}[\*\d]{4,6}\d{2})\s*(?:Kimlik\s+Numaralı|Kimlik\s+No['’]?lu)[,\s]+"
        r"(?:[^\n]*?adresinde\s+ikamet\s+eden[,\s]+)?"
        r"([A-ZÖÇŞİĞÜIİ][A-ZÖÇŞİĞÜIİa-zöçşığü]+(?:\s+[A-ZÖÇŞİĞÜIİ][A-ZÖÇŞİĞÜIİa-zöçşığü]+){1,3})",
        re.IGNORECASE
    )
    for m in direct_tc_pattern.finditer(text):
        tc_val, name_cand = m.group(1), m.group(2).strip()
        name_cand = re.sub(r"['’](?:e|a|in|ın|un|ün|den|dan)\b", "", name_cand, flags=re.IGNORECASE).strip()
        add_person(name_cand, tc_val)

    # Strategy 1: Appointment Sentence Parser (TCKN -> FORWARD search for ALL CAPS / TitleCase NAME before role title)
    app_pattern = re.compile(
        r"([1-9]\d{2}[\*\d]{4,6}\d{2}).{2,250}?\b"
        r"([A-ZÖÇŞİĞÜIİ][A-ZÖÇŞİĞÜIİa-zöçşığü]+(?:\s+[A-ZÖÇŞİĞÜIİ][A-ZÖÇŞİĞÜIİa-zöçşığü]+){1,3})\s+"
        r"(?:Müdür|Müdürlüğü|Yönetim|Başkan|Başkanı|Temsil|Temsile|olarak|seçilmiştir|seçilmişlerdir|seçilmeleri)",
        re.DOTALL
    )
    for m in app_pattern.finditer(text):
        tc_val, name_cand = m.group(1), m.group(2).strip()
        name_cand = re.sub(r"(?i)\b(?:Müdür|Yönetim|Başkan|Temsile|olarak|seçilmiştir)\b.*$", "", name_cand).strip()
        add_person(name_cand, tc_val)

    # Strategy 2: Founder Table Line Parser (handles multiline wrapped names/surnames like FATMA BEYZA \n ÖZDEMİR)
    CITY_WORDS = ["ISTANBUL", "İSTANBUL", "ANKARA", "İZMİR", "SILIVRI", "SİLİVRİ", "SİLIVRİ", "SILIVRİ", "BURSA", "ANTALYA", "ADANA", "KONYA", "BESIKIAS", "BEŞİKTAŞ"]
    lines = text.split("\n")
    for idx, line in enumerate(lines):
        m_tc = re.search(r"(\d{3}[\*\d]{4,6}\d{2})", line)
        if m_tc and not any(kw in line.lower() for kw in ["mersis", "sicil", "müdürlüğü", "dosya no"]):
            tc_val = m_tc.group(1)
            before = line[:m_tc.start()].strip()
            before = re.sub(r"^\d+\.?\s*", "", before).strip()
            before = re.sub(r"(?i)\b(?:TÜRKİYE|CUMHUR[İI]YET[İI]|CUMHUKIIEI|TURK|TÜRK|UYRUK|TC|T\.C\.|ITÜRKİYE)\b.*$", "", before).strip()
            if "/" in before:
                before = before.split("/")[0].strip()
            words_curr = [w.strip() for w in before.split() if w.strip() and w.upper() not in CITY_WORDS]
            
            # Check UPWARDS (idx-1, idx-2) for first name (e.g. FATMA BEYZA above ÖZDEMİR on TCKN line)
            prev_name = ""
            for offset in [1, 2]:
                if idx - offset >= 0:
                    prev_line = lines[idx - offset].strip()
                    if prev_line and not any(kw in prev_line.lower() for kw in ["şirketin", "unvanı", "mersis", "sicil", "amaç", "konu", "madde", "sura", "sıra", "kurucu", "adres", "uyruk", "kimlik"]):
                        prev_clean = re.sub(r"(?i)\b(?:TÜRKİYE|CUMHUR[İI]YET[İI]|CUMHUKIIEI|TURK|TÜRK|UYRUK|TC|T\.C\.|ITÜRKİYE)\b.*$", "", prev_line).strip()
                        prev_clean = re.sub(r"[^\w\s\-]", " ", prev_clean, flags=re.UNICODE).strip()
                        p_words = [w for w in prev_clean.split() if w.upper() not in CITY_WORDS]
                        if p_words and all(w[0].isupper() for w in p_words if len(w) > 1):
                            prev_name = " ".join(p_words)
                            break
                            
            if prev_name:
                final_name = prev_name + " " + " ".join(words_curr)
            else:
                surname = ""
                if idx + 1 < len(lines):
                    next_line = lines[idx+1].strip()
                    if next_line and not any(kw in next_line.lower() for kw in ["şirketin", "unvanı", "mersis", "sicil", "amaç", "konu", "madde"]):
                        next_words = [w.strip() for w in next_line.split() if w.strip()]
                        if next_words and next_words[0].isupper() and len(next_words[0]) >= 2:
                            first_w = next_words[0]
                            if not any(k in first_w.lower() for k in ["türkiye", "cumhuriyeti", "uyruk", "adres", "kimlik", "sira", "sıra"]):
                                surname = first_w
                if surname:
                    final_name = " ".join(words_curr) + " " + surname
                else:
                    if len(words_curr) >= 3 and words_curr[-1].isupper():
                        final_name = " ".join(words_curr[:2])
                    else:
                        final_name = " ".join(words_curr[:3]) if len(words_curr) > 3 else " ".join(words_curr)
                        
            add_person(final_name, tc_val)

    entities["persons"] = persons_list

    # İlan Sıra No
    for m in RE_ILAN_SIRA.finditer(text):
        entities["ilan_sira_no"].append(m.group(1))

    return entities

# ============================================================================
# TEXT SEGMENTATION (Header-based split)
# ============================================================================

def split_by_headers(raw_text: str) -> list:
    """
    Raw OCR metnini "T.C. ... TİCARET SİCİLİ MÜDÜRLÜĞÜ'NDEN" ve metadata bloklarına göre parçalar.
    Her parça bir ayrı ilan (announcement) ifade eder.
    """
    if not raw_text or not raw_text.strip():
        return []
        
    candidates = []
    
    # 1. Find all potential header matches
    for m in RE_HEADER_ADVANCED.finditer(raw_text):
        start_pos = m.start()
        ahead = raw_text[start_pos:start_pos + 350]
        
        # Exclude body mentions like "tescili için ... müdürlüğüne"
        if re.search(r"(?i)(?:tescili\s+için|müracaat\s+edilmiş|kayıtlı\s+olduğu)", raw_text[max(0, start_pos-40):start_pos]):
            continue
            
        # Must have metadata anchor ahead
        if (re.search(r"(?i)MERS[İIÍiı]S\s*(?:No)?\s*[:\s]", ahead) or
            re.search(r"(?i)sicil(?:/Dosya)?\s*No\s*[:\s]", ahead) or
            re.search(r"(?i)(?:ticaret\s+)?[üu]nvan[ıit]?\s*[:\s]", ahead) or
            re.search(r"(?i)[İiIı]lan\s+S[ıiİI]ra\s*(?:No)?\s*[:\s]", ahead)):
            candidates.append((start_pos, m.group(0).strip()))

    # 2. Find metadata anchors without a header preceding them
    for m in RE_METADATA_ANCHOR.finditer(raw_text):
        start_pos = m.start()
        if any(abs(start_pos - c[0]) < 150 for c in candidates):
            continue
            
        ahead = raw_text[start_pos:start_pos + 300]
        if re.search(r"(?i)(?:ticaret\s+)?[üu]nvan[ıit]?\s*[:\s]", ahead) or re.search(r"(?i)yukarıda\s+bilgileri\s+verilen", ahead):
            candidates.append((start_pos, "T.C. TİCARET SİCİLİ MÜDÜRLÜĞÜ'NDEN"))
            
    candidates.sort(key=lambda x: x[0])
    
    if not candidates:
        return [("T.C. TİCARET SİCİLİ MÜDÜRLÜĞÜ'NDEN", raw_text.strip())]
        
    filtered = []
    for c in candidates:
        if not filtered or (c[0] - filtered[-1][0]) >= 100:
            filtered.append(c)
            
    chunks = []
    for i, (pos, header) in enumerate(filtered):
        next_pos = filtered[i+1][0] if i + 1 < len(filtered) else len(raw_text)
        chunk_txt = raw_text[pos:next_pos].strip()
        if chunk_txt:
            chunks.append((header, chunk_txt))
            
    return chunks

# ============================================================================
# APPLE VISION OCR
# ============================================================================

def perform_vision_ocr(image_path: str) -> str:
    """Apple Vision framework ile OCR. macOS 13+ gerektirir."""
    try:
        result = subprocess.check_output(
            ["swift", VISION_TOOL_PATH, image_path],
            stderr=subprocess.STDOUT,
            timeout=60
        )
        return result.decode("utf-8")
    except subprocess.TimeoutExpired:
        print(f"    [TIMEOUT] Vision OCR timed out for {image_path}")
        return ""
    except Exception as e:
        print(f"    [ERROR] Vision OCR failed: {e}")
        return ""

def ocr_all_pages(doc) -> tuple:
    """
    PDF'in TÜM sayfalarını Apple Vision ile okur (Ders #4).
    Returns: (birleşik_metin, sayfa_görsel_yolları_listesi)
    """
    all_texts = []
    page_images = []

    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        pix = page.get_pixmap(matrix=fitz.Matrix(3.0, 3.0))
        temp_img = os.path.join("/tmp", f"_ocr_page_{page_num}.png")
        pix.save(temp_img)
        page_images.append(temp_img)

        raw = perform_vision_ocr(temp_img)
        if raw:
            all_texts.append(raw)
        print(f"    [OCR] Page {page_num + 1}/{doc.page_count}: {len(raw)} chars")

    combined = "\n".join(all_texts)
    return combined, page_images

# ============================================================================
# LLM STRUCTURED EXTRACTION (Dual-Brain)
# ============================================================================

# Strict NlpParsedAnnouncement şeması - LLM sadece bu keyleri doldurabilir
SCHEMA_PROMPT = """Sen profesyonel bir Türk Ticaret Sicili Gazetesi veri çıkarma asistanısın.
SADECE aşağıdaki JSON şemasına uygun cevap ver. ASLA ek key ekleme.

ZORUNLU JSON ŞEMASI:
{
  "trade_name": "Şirket ticaret unvanı (string veya null)",
  "old_trade_name": "Eski ticaret unvanı (string veya null)",
  "registration_number": "Ticaret sicil numarası (string veya null)",
  "sicil_dosya_no": "Sicil/dosya numarası (string veya null)",
  "mersis_no": "16 haneli MERSIS numarası (string veya null)",
  "addresses": ["Tam adres stringleri listesi"],
  "old_addresses": ["Eski adres stringleri listesi"],
  "persons": [{"text": "Kişi adı", "label": "PERSON", "masked_ids": "TC kimlik (maskeli)"}],
  "ilan_sira_no": ["İlan sıra numaraları"],
  "hususlar": ["Tescil edilen hususlar listesi"],
  "belgeler": "Tescile delil olan belgeler açıklaması (string veya null)"
}

KURALLAR:
1. SADECE yukarıdaki keyleri kullan. shareholders, board_members, city, country gibi keyler YASAK.
2. addresses listesine adresi TEK BİR STRING olarak koy. ASLA street/city/zip gibi alt parçalara BÖLME.
3. persons listesindeki her eleman {"text": "...", "label": "PERSON", "masked_ids": "..."} formatında olmalı.
4. Bulamadığın alanları null veya boş liste [] olarak bırak.
5. Türkçe karakterleri koru. İngilizce'ye çevirme."""


def query_llm(model: str, chunk: str, regex_entities: dict) -> dict | None:
    """
    LLM'e chunk gönderip JSON yapılandırması ister.
    Guardian: Regex bulunan değerler prompt'a enjekte edilir.
    """
    # Regex'in bulduğu kesin verileri prompt'a ekle
    confirmed = []
    if regex_entities.get("trade_name"):
        confirmed.append(f"  trade_name: {regex_entities['trade_name']}")
    if regex_entities.get("old_trade_name"):
        confirmed.append(f"  old_trade_name: {regex_entities['old_trade_name']}")
    if regex_entities.get("registration_number"):
        confirmed.append(f"  registration_number: {regex_entities['registration_number']}")
    if regex_entities.get("mersis_no"):
        confirmed.append(f"  mersis_no: {regex_entities['mersis_no']}")

    confirmed_block = ""
    if confirmed:
        confirmed_block = (
            "\n\nSİSTEMİN ZATEN BULDUĞU KESİN VERİLER (BUNLARI AYNEN KORU, DEĞİŞTİRME):\n"
            + "\n".join(confirmed)
        )

    payload = {
        "model": model,
        "system": SCHEMA_PROMPT + confirmed_block,
        "prompt": f"Aşağıdaki Türk Ticaret Sicili Gazetesi metnini analiz et ve JSON olarak çıkar:\n\n{chunk[:4000]}",
        "stream": False,
        "format": "json",
        "options": {
            "temperature": 0.0,
            "seed": 42,
            "num_thread": 4
        }
    }

    for attempt in range(2):
        try:
            r = requests.post(OLLAMA_URL, json=payload, timeout=120)
            if r.status_code == 200:
                response_text = r.json().get("response", "{}")
                parsed = json.loads(response_text)
                return parsed
            else:
                print(f"    [LLM] HTTP {r.status_code} (deneme {attempt+1})")
        except json.JSONDecodeError as e:
            print(f"    [LLM] JSON parse error: {e}")
            return None
        except requests.exceptions.Timeout:
            print(f"    [LLM] Timeout 120s (deneme {attempt+1})")
            time.sleep(2)
        except Exception as e:
            print(f"    [LLM] Error: {e} (deneme {attempt+1})")
            time.sleep(1)
    return None

# ============================================================================
# GUARDIAN OVERRIDE + SCHEMA VALIDATOR
# ============================================================================

# NlpParsedAnnouncement kesin şeması
REQUIRED_KEYS = {
    "index", "sicil_office_header", "original_text",
    "trade_name", "old_trade_name", "registration_number",
    "sicil_dosya_no", "mersis_no", "addresses", "old_addresses",
    "persons", "ilan_sira_no", "hususlar", "belgeler",
}

def guardian_override(llm_result: dict, regex_entities: dict) -> dict:
    """
    Ders #2: Regex bulduğu her şey LLM çıktısının ÜZERİNE yazılır.
    Bu sayede halüsinasyon (örn: 'Parsel Corporation') imkansız hale gelir.
    """
    result = dict(llm_result)

    # Skalar alanlar: regex varsa ezer
    for key in ["trade_name", "old_trade_name", "registration_number",
                "sicil_dosya_no", "mersis_no", "belgeler"]:
        if regex_entities.get(key):
            result[key] = regex_entities[key]

    # Liste alanlar: Regex varsa birleştirir ve temizler
    for key in ["addresses", "ilan_sira_no", "hususlar"]:
        if regex_entities.get(key):
            result[key] = regex_entities[key]

    # old_addresses: LLM + Regex harmanlama ve ön metin temizliği
    combined_oa = []
    seen_oa = set()
    for oa in (regex_entities.get("old_addresses") or []) + (llm_result.get("old_addresses") or []):
        raw = oa.get("address") if isinstance(oa, dict) else str(oa)
        addr = str(raw).strip()
        match = re.search(r"(?i)\badresi\s*[:\s]?", addr)
        if match:
            addr = addr[match.end():].strip()
        addr = re.sub(r"^\s*[:\-\.]+", "", addr).strip()
        if addr and addr not in seen_oa:
            seen_oa.add(addr)
            combined_oa.append({"address": addr})
    result["old_addresses"] = combined_oa

    # persons: LLM + Regex harmanlama ve clean_person_name doğrulaması
    combined_persons = []
    seen_p = set()
    raw_p_list = (regex_entities.get("persons") or []) + (llm_result.get("persons") or [])
    for p_item in raw_p_list:
        if isinstance(p_item, str):
            p_name = p_item.strip()
            p_tc = None
        elif isinstance(p_item, dict):
            p_name = p_item.get("name") or p_item.get("text") or p_item.get("full_name")
            p_tc = p_item.get("tckn") or p_item.get("masked_ids") or p_item.get("masked_id")
            if isinstance(p_tc, list) and p_tc:
                p_tc = p_tc[0]
        else:
            continue
            
        c_name = clean_person_name(p_name)
        if c_name:
            p_key = (c_name.upper(), str(p_tc).strip() if p_tc else "")
            if p_key not in seen_p:
                seen_p.add(p_key)
                combined_persons.append({"name": c_name, "tckn": p_tc})
    result["persons"] = combined_persons

    return result


def validate_schema(result: dict, index: int, header: str, original_text: str) -> dict:
    """
    Ders #1: Şema dışı keyleri siler, eksik keyleri null/[] olarak ekler.
    NlpParsedAnnouncement şemasına tam uyum sağlar.
    """
    validated = {}
    validated["index"] = index
    validated["sicil_office_header"] = header
    validated["original_text"] = original_text

    # Skalar alanlar
    for key in ["trade_name", "old_trade_name", "registration_number",
                "sicil_dosya_no", "mersis_no", "belgeler"]:
        validated[key] = result.get(key)

    # Liste alanlar
    for key in ["addresses", "old_addresses", "persons",
                "ilan_sira_no", "hususlar"]:
        val = result.get(key)
        validated[key] = val if isinstance(val, list) else []

    return validated

# ============================================================================
# MAIN PIPELINE
# ============================================================================

# Llama 3 setup (Final model choice)
DEFAULT_MODEL = "llama3.2:3b"
MODELS = [DEFAULT_MODEL]

def get_ocr_baseline(pdf_bytes: bytes) -> list:
    """
    FAST PATH: OCR all pages + Regex extraction.
    Returns a list of 'baseline' dicts containing raw text and regex entities.
    """
    try:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    except Exception as e:
        print(f"    [ERROR] Cannot open PDF bytes: {e}")
        return []

    # 1. OCR all pages
    raw_text, page_images = ocr_all_pages(doc)
    doc.close()

    # Clean up temp images
    for img in page_images:
        try: os.remove(img)
        except OSError: pass

    if not raw_text.strip():
        return []

    # 2. Normalize + Segment
    normalized = normalize_ocr_text(raw_text)
    chunks = split_by_headers(normalized)

    # 3. Extract regex entities for each chunk
    baselines = []
    for idx, (header, chunk_text) in enumerate(chunks):
        regex_entities = extract_entities_regex(chunk_text)
        baselines.append({
            "index": idx,
            "header": header,
            "original_text": chunk_text,
            "regex_entities": regex_entities
        })
    return baselines

def enrich_ocr_with_llama(chunk_text: str, regex_entities: dict, index: int, header: str, model: str = DEFAULT_MODEL) -> dict:
    """
    SLOW PATH: LLM structured extraction + Guardian Override.
    Returns a validated NlpParsedAnnouncement dict.
    """
    llm_result = query_llm(model, chunk_text, regex_entities)
    
    if llm_result is None:
        llm_result = {}
        
    merged = guardian_override(llm_result, regex_entities)
    validated = validate_schema(merged, index, header, chunk_text)
    return validated

def process_pdf_content(pdf_bytes: bytes, model: str = DEFAULT_MODEL) -> list:
    """Convenience wrapper that runs both baseline and enrichment sequentially."""
    baselines = get_ocr_baseline(pdf_bytes)
    results = []
    for b in baselines:
        res = enrich_ocr_with_llama(b["original_text"], b["regex_entities"], b["index"], b["header"], model)
        results.append(res)
    return results


def main():
    print("=" * 70)
    print("🛡️ DUAL-BRAIN GUARDIAN v2.0")
    print("   PDF → Vision OCR → Regex → LLM → Guardian → NlpParsedAnnouncement")
    print("=" * 70)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Minio bağlantısı dene
    client = None
    objects = []
    try:
        from minio import Minio
        client = Minio("127.0.0.1:9005", access_key="minioadmin",
                       secret_key="Vj_7pYw2Lr_4nH8cKm_", secure=False)
        objects = [
            obj for obj in client.list_objects(BUCKET_NAME, recursive=True)
            if obj.object_name.lower().endswith(".pdf")
        ][:LIMIT]
        print(f"\n📡 Minio: {len(objects)} PDF bulundu")
    except Exception as e:
        print(f"\n⚠️  Minio erişilemedi: {e}")
        # Yerel fallback
        local_dir = os.path.join(BACKEND_DIR, "downloads")
        if os.path.exists(local_dir):
            local_pdfs = [f for f in os.listdir(local_dir) if f.lower().endswith(".pdf")][:LIMIT]
            print(f"📂 Yerel '{local_dir}': {len(local_pdfs)} PDF bulundu")

            class MockObj:
                def __init__(self, name):
                    self.object_name = os.path.join(local_dir, name)
            objects = [MockObj(f) for f in local_pdfs]
            client = None
        else:
            print("❌ HATA: Ne Minio ne de yerel 'downloads' klasörü bulunamadı!")
            return

    if not objects:
        print("❌ İşlenecek PDF bulunamadı!")
        return

    # İşleme döngüsü: Modeller sırayla dönüşür (Ders: yük binmesin)
    all_results = []
    total_start = time.time()

    for i, obj in enumerate(objects):
        # Model seçimi: sıralı dönüşüm
        model = MODELS[i % len(MODELS)]

        try:
            if client:
                response = client.get_object(BUCKET_NAME, obj.object_name)
                pdf_bytes = response.read()
                response.close()
                response.release_conn()
            else:
                with open(obj.object_name, "rb") as f:
                    pdf_bytes = f.read()

            results = process_single_pdf(obj.object_name, pdf_bytes, i, model)
            all_results.extend(results)

        except Exception as e:
            print(f"\n  [ERROR] PDF {i}: {e}")

    elapsed = time.time() - total_start
    print(f"\n{'=' * 70}")
    print(f"✅ Dual-Brain Guardian Sweep Complete!")
    print(f"   📄 {len(objects)} PDF işlendi")
    print(f"   📋 {len(all_results)} ilan çıkarıldı")
    print(f"   ⏱️  {elapsed:.1f} saniye")
    print(f"   📂 Çıktılar: {OUTPUT_DIR}")
    print(f"{'=' * 70}")


def process_single_pdf(pdf_path: str, pdf_bytes: bytes, pdf_idx: int, model: str) -> list:
    """Legacy wrapper for standalone main()"""
    print(f"\n[{pdf_idx + 1}] 📄 Processing: {pdf_path}")
    return process_pdf_content(pdf_bytes, model)

if __name__ == "__main__":
    main()
