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
RE_HEADER = re.compile(
    r"(?mi)^\s*(?:T\.?C\.?\s*)?.*?"
    r"(?:T[İI]CARET\s+S[İI]C[İI]L[İI]\s+(?:M[ÜU]D[ÜU]RL[ÜU][ĞG][ÜU]|MEMURLU[ĞG][UÜ])(?:[''\u2019]?N[DT]EN)?|"
    r"MAHKEMES[İI]['\u2019]?N[DdTt]EN)\s*$"
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
    r"(?P<name>.+?)(?:\n\s*(?:Adres|Yukarıda|Tescil)|$)",
    re.DOTALL
)

# MERSIS No: 16 haneli, 0 ile başlayan
RE_MERSIS = re.compile(r"\b0\d{15}\b")

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
    r"([^.]*?)\s+adresinden,?\s+([^.]*?)\s+adresine\s+(?:taşınmıştır|nakledilmiştir)",
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

    # MERSIS no
    m = RE_MERSIS.search(text)
    if m:
        entities["mersis_no"] = m.group(0)

    # Adres (değişiklik varsa eski/yeni ayır)
    change = RE_ADDRESS_CHANGE.search(text)
    if change:
        old_addr = re.sub(r"\s+", " ", change.group(1)).strip()
        new_addr = re.sub(r"\s+", " ", change.group(2)).strip()
        entities["addresses"] = [new_addr]
        entities["old_addresses"] = [old_addr]
    else:
        m = RE_ADDRESS.search(text)
        if m:
            addr = re.sub(r"\s+", " ", m.group("addr")).strip(" .-\n")
            if len(addr) > 5:
                entities["addresses"] = [addr]

    # İlan Sıra No
    for m in RE_ILAN_SIRA.finditer(text):
        entities["ilan_sira_no"].append(m.group(1))

    # Kişiler (Ders #6: Sadece Kimlik No ile eşleşen isimler)
    seen_persons = set()
    for m in RE_PERSON.finditer(text):
        tc = m.group(1)
        name = re.sub(r"\s+", " ", m.group(2)).strip()
        key = f"{name}_{tc}"
        if key not in seen_persons and len(name) > 2:
            seen_persons.add(key)
            entities["persons"].append({
                "text": name,
                "label": "PERSON",
                "masked_ids": tc
            })

    # Tablo formatındaki kişiler (yedek mekanizma)
    if not entities["persons"]:
        for m in RE_PERSON_TABLE.finditer(text):
            name = m.group("name").strip()
            tc = m.group("tc")
            key = f"{name}_{tc}"
            if key not in seen_persons and len(name) > 2:
                seen_persons.add(key)
                entities["persons"].append({
                    "text": name,
                    "label": "PERSON",
                    "masked_ids": tc
                })

    # Hususlar
    m = RE_HUSUSLAR.search(text)
    if m:
        hususlar_raw = m.group(1).strip()
        entities["hususlar"] = [h.strip() for h in re.split(r"[,;]", hususlar_raw) if h.strip()]

    # Belgeler
    m = RE_BELGELER.search(text)
    if m:
        entities["belgeler"] = re.sub(r"\s+", " ", m.group(1)).strip()

    return entities

# ============================================================================
# TEXT SEGMENTATION (Header-based split)
# ============================================================================

def split_by_headers(raw_text: str) -> list:
    """
    Raw OCR metnini "T.C. ... TİCARET SİCİLİ MÜDÜRLÜĞÜ'NDEN" başlıklarına göre parçalar.
    Her parça bir ayrı ilan (announcement) ifade eder.
    """
    matches = list(RE_HEADER.finditer(raw_text))
    if not matches:
        return [("", raw_text.strip())] if raw_text.strip() else []

    chunks = []
    for i, match in enumerate(matches):
        header = match.group(0).strip()
        start = match.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(raw_text)
        chunk_text = raw_text[start:end].strip()
        if chunk_text:
            chunks.append((header, chunk_text))
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
        pix = page.get_pixmap(matrix=fitz.Matrix(2.0, 2.0))
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
    }

    try:
        r = requests.post(OLLAMA_URL, json=payload, timeout=300)
        if r.status_code != 200:
            print(f"    [LLM] HTTP {r.status_code}")
            return None
        response_text = r.json().get("response", "{}")
        parsed = json.loads(response_text)
        return parsed
    except json.JSONDecodeError as e:
        print(f"    [LLM] JSON parse error: {e}")
        return None
    except requests.exceptions.Timeout:
        print(f"    [LLM] Timeout (300s)")
        return None
    except Exception as e:
        print(f"    [LLM] Error: {e}")
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

    # Liste alanlar: regex varsa ezer
    for key in ["addresses", "old_addresses", "ilan_sira_no", "hususlar"]:
        if regex_entities.get(key):
            result[key] = regex_entities[key]

    # Persons: SIFIR HALÜSİNASYON kuralı
    # Regex Kimlik No pattern ile doğrulanmış kişileri yakalar.
    # Eğer regex kişi bulamadıysa, LLM'in OCR gürültüsünden kişi üretme
    # riski çok yüksek (örn: "Ierkeze AIl Digner"). Bu yüzden:
    #   - Regex buldu → regex sonuçlarını kullan
    #   - Regex bulamadı → BOŞ LISTE (LLM halüsinasyonu engellenir)
    if regex_entities.get("persons"):
        result["persons"] = regex_entities["persons"]
    else:
        result["persons"] = []  # LLM halüsinasyonunu engelle

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
DEFAULT_MODEL = "llama3:8b"
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
