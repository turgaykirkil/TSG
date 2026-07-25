import os
from dotenv import load_dotenv
import sys
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(BASE_DIR)
if PARENT_DIR not in sys.path:
    sys.path.insert(0, PARENT_DIR)

# Load environment variables from backend/.env
load_dotenv(os.path.join(PARENT_DIR, ".env"))

import re
import json
import time
import subprocess
import httpx
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

# Initialize FastAPI App
app = FastAPI(title="TSG OCR & NLP Validation Sandbox")

# Allow CORS for local dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

PDFS_DIR = os.path.join(BASE_DIR, "pdfs")
OCR_OUTPUT_DIR = os.path.join(BASE_DIR, "ocr_output")
PROGRESS_PATH = os.path.join(BASE_DIR, "progress.json")
VISION_TOOL_PATH = os.path.join(BASE_DIR, "vision_ocr.swift")

os.makedirs(PDFS_DIR, exist_ok=True)
os.makedirs(OCR_OUTPUT_DIR, exist_ok=True)

if not os.path.exists(PROGRESS_PATH):
    with open(PROGRESS_PATH, "w", encoding="utf-8") as f:
        json.dump({"results": []}, f)

# Local LLM config
LLM_SERVER_URL = "http://localhost:1234/v1/chat/completions"
MODEL_NAME = "default_model"

# ============================================================================
# OCR-TOLERANT REGEX PATTERNS & UTILITIES
# ============================================================================
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

RE_TRADE_NAME = re.compile(
    r"(?i)(?:ticaret\s+)?[üu]nvan[ıit]?\s*[:\s]\s*\n?"
    r"(?P<name>.+?)\s*"
    r"(?=\n\s*(?:Adres\s*[:]|Eski\s+Ticaret|Yukarıda))",
    re.DOTALL
)
RE_OLD_TRADE_NAME = re.compile(
    r"(?i)(?:eski\s+ticaret\s+[üu]nvan[ıit]?)\s*[:\s]\s*\n?"
    r"(?P<name>.+?)(?:\n\s*(?:Adres|Adresi|İsdan|Isdan|Yukarıda|Tescil|İşletme|Isletme)|$)",
    re.DOTALL
)
RE_MERSIS = re.compile(r"\b\d{16}\b")
RE_SICIL_NO = re.compile(
    r"(?i)(?:ticaret\s+)?sicil(?:/Dosya)?\s*(?:no|numarası)\s*[:\s]*([0-9/\- ]+)"
)
RE_ILAN_SIRA = re.compile(
    r"(?i)[İiIı]lan\s+S[ıiİI]ra\s*(?:No)?\s*[:\s]*(\d+)"
)
RE_ADDRESS = re.compile(
    r"(?i)(?:adres|merkez\s+adresi)\s*[:\s]\s*"
    r"(?P<addr>[^\n]+(?:\n[^\n]{1,60})?)"
    r"(?=\nYukarıda|\nTescil|\n[A-ZÖÇŞİĞÜ]{4,}|$)",
    re.DOTALL
)
RE_ADDRESS_CHANGE = re.compile(
    r"(.{8,250}?)\s+adresinden,?\s+(.{8,250}?)\s+adresine\s+(?:taşınmıştır|nakledilmiştir|taşınmasına|nakline)",
    re.IGNORECASE | re.DOTALL
)
RE_PERSON = re.compile(
    r"(\d{3}\*{4,6}\d{2})\s*(?:Kimlik)?\s*(?:No['’]?lu|Numaralı|Numarası)?[,\s]*"
    r"(?:[^,]*?adresinde\s+ikamet\s+eden[,\s]+)?"
    r"([A-ZÖÇŞİĞÜ][A-ZÖÇŞİĞÜa-zöçşığü]+(?:\s+[A-ZÖÇŞİĞÜ][A-ZÖÇŞİĞÜa-zöçşığü]+){1,4})",
    re.DOTALL
)
RE_PERSON_TABLE = re.compile(
    r"(?P<name>[A-ZÖÇŞİĞÜ]+(?:\s+[A-ZÖÇŞİĞÜ]+){1,3})\s+(?:CUMHUR[İI]YET[İI]|CUMHUKIIEI|TURK|TÜRK)?\s*(?P<tc>\d{3}\*{4,6}\d{2})|"
    r"(?P<tc2>\d{3}\*{4,6}\d{2})\s+(?:CUMHUR[İI]YET[İI]|CUMHUKIIEI|TURK|TÜRK)?\s*(?P<name2>[A-ZÖÇŞİĞÜ]+(?:\s+[A-ZÖÇŞİĞÜ]+){1,3})"
)
RE_PERSON_LOOSE = re.compile(
    r"(?P<name>[A-ZÖÇŞİĞÜ][A-ZÖÇŞİĞÜa-zöçşığü]+(?:\s+[A-ZÖÇŞİĞÜ][A-ZÖÇŞİĞÜa-zöçşığü]+){1,3})\s*"
    r"(?:\(|\:\s*|T\.?C\.?\s*)?(?P<tc>\d{3}\*{4,6}\d{2}|\d{11})"
)
RE_HUSUSLAR = re.compile(
    r"(?i)Tescil\s+Edilen\s+Hususlar\s*[:\s]*(.+?)(?:\n|$)"
)
RE_BELGELER = re.compile(
    r"(?i)Tescile\s+Delil\s+Olan\s+Belgeler\s*[:\s]*(.+?)(?:\n\n|\n[A-ZÖÇŞİĞÜ]|\Z)",
    re.DOTALL
)

def normalize_ocr_typos(text: str) -> str:
    replacements = [
        (r"(?i)\b[iIı]res\s*:", "Adres :"),
        (r"(?i)\bdres\s*:", "Adres :"),
        (r"(?i)\bstra\s+no\b", "Sıra No"),
        (r"(?i)\bstra\s+no\s*:", "Sıra No:"),
        (r"(?i)\bstra\s*:", "Sıra :"),
        (r"(?i)\bmersls\b", "Mersis"),
        (r"(?i)\bkimlk\b", "Kimlik"),
        (r"(?i)\bvarur\b", "UYRUK"),
        (r"(?i)\bılgileri\b", "bilgileri"),
        (r"(?i)\[ç\s+Kap[ıi]", "İç Kapı"),
        (r"(?i)\bIg\s+Kap[ıi]", "İç Kapı"),
        (r"(?i)\bIg\s+Kap", "İç Kap"),
        (r"(?i)\bIg\s+", "İç "),
        (r"(?i)\b[iIı]g\s+", "İç "),
        (r"(?i)iç\s+kap[ıi]\s*no\s*[:\s]*(\d+)", r"İç Kapı No: \1"),
        (r"(?i)\b[tT]escll\b", "Tescil"),
        (r"(?i)\b[hH]ususlar[ıi]?\b", "Hususlar"),
        (r"(?i)\b[uU]nvan[ıi]?\b", "Unvanı"),
    ]
    for pattern, repl in replacements:
        text = re.sub(pattern, repl, text)
    return text

def extract_entities_regex(text: str) -> dict:
    text = normalize_ocr_typos(text)
    entities = {
        "trade_name": None,
        "old_trade_name": None,
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
        name = re.sub(r"\s+", " ", name).strip(" .:-\n")
        name = re.sub(r"şirketin\s+(?:unvan[ıi]?\s+)?", "", name, flags=re.IGNORECASE).strip()
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
        entities["sicil_dosya_no"] = m.group(1).strip()

    persons_list = []
    seen = set()

    def normalize_tckn_typos(tc_raw: str) -> str:
        if not tc_raw:
            return ""
        tc = tc_raw.strip()
        if len(tc) == 11:
            # Common OCR typos for final even digits: '(' -> '0', 'O'/'o' -> '0', 's'/'S' -> '8'
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
        "baskan", "müdür", "mudur", "müdürlük", "müdürlüğü", "şirket", "sirket", "unvan", "unvanı",
        "ticaret", "limited", "anonim", "kooperatif", "tüzük", "tuzuk", "gazete", "gazetesi",
        "ilan", "tescil", "terkin", "devri", "hissesi", "kararı", "karari", "önceden", "onceden",
        "ikamet", "eden", "adresinde", "adresine", "uyruklu", "uyruğu", "uyrugu", "yerleşim",
        "yerlesim", "yeri", "yerleşim yeri", "kimlik no", "türkiye", "turkiye", "cumhuriyeti"
    ]

    def clean_person_name(name_raw: str) -> str:
        if not name_raw:
            return ""
        name_clean = re.sub(r"(?i)\b(?:TÜRKİYE|CUMHUR[İI]YET[İI]|CUMHUKIIEI|TURK|TÜRK|UYRUK|TC|T\.C\.)\b.*$", "", name_raw).strip()
        name_clean = re.sub(r"[^\w\s\-]", " ", name_clean, flags=re.UNICODE).strip()
        name_clean = re.sub(r"\s+", " ", name_clean).strip()
        
        if re.search(r"\d", name_clean):
            return ""
            
        words = [w for w in name_clean.split() if w.upper() not in ["ISTANBUL", "İSTANBUL", "ANKARA", "İZMİR", "SILIVRI", "SİLİVRİ", "BURSA", "ANTALYA", "ADANA", "KONYA", "BESIKIAS", "BEŞİKTAŞ"]]
        if len(words) < 2 or len(words) > 4:
            return ""
            
        for w in words:
            if w.lower() in LEGAL_FINANCIAL_WORDS:
                return ""
                
        if any(len(w) < 2 for w in words):
            return ""
            
        return " ".join(words)

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
        new_addr = re.sub(r"\s+", " ", change.group(2)).strip()
        entities["addresses"] = [new_addr]
        entities["old_addresses"] = [old_addr]
    else:
        m = RE_ADDRESS.search(text)
        if m:
            entities["addresses"] = [re.sub(r"\s+", " ", m.group("addr")).strip()]

    # Strategy 1: Appointment Sentence Parser (TCKN -> FORWARD search for ALL CAPS / TitleCase NAME before role title)
    app_pattern = re.compile(
        r"(\d{3}[\*\d]{4,6}\d{2})[^\n]{5,200}?"
        r"([A-ZÖÇŞİĞÜa-zöçşığü]+(?:\s+[A-ZÖÇŞİĞÜa-zöçşığü]+){1,3})\s*"
        r"(?:Müdür|Yönetim|Başkan|olarak|seçilmiştir|tarihine|Temsile|[;:])",
        re.DOTALL
    )
    for m in app_pattern.finditer(text):
        tc_val, name_cand = m.group(1), m.group(2).strip()
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

    # Ilan sira no
    m = RE_ILAN_SIRA.search(text)
    if m:
        entities["ilan_sira_no"] = [m.group(1).strip()]

    # Hususlar
    m = RE_HUSUSLAR.search(text)
    if m:
        entities["hususlar"] = [m.group(1).strip()]

    # Belgeler
    m = RE_BELGELER.search(text)
    if m:
        entities["belgeler"] = re.sub(r"\s+", " ", m.group(1)).strip()

    return entities

def split_by_headers(raw_text: str) -> list:
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
# API ENDPOINTS
# ============================================================================

@app.get("/", response_class=HTMLResponse)
async def serve_index():
    html_path = os.path.join(BASE_DIR, "index.html")
    if not os.path.exists(html_path):
        raise HTTPException(status_code=404, detail="index.html not found")
    with open(html_path, "r", encoding="utf-8") as f:
        return f.read()

@app.get("/api/pdfs")
async def list_pdfs():
    """Lists all locally stored PDF files."""
    files = [f for f in os.listdir(PDFS_DIR) if f.lower().endswith(".pdf")]
    # Also check if OCR output exists for each PDF
    output = []
    for f in files:
        ocr_exists = os.path.exists(os.path.join(OCR_OUTPUT_DIR, f.replace(".pdf", ".txt")))
        output.append({
            "filename": f,
            "ocr_completed": ocr_exists
        })
    return output

@app.get("/api/pdfs/{filename}")
async def get_pdf_file(filename: str):
    """Serves the PDF file directly to display in the viewer iframe."""
    path = os.path.join(PDFS_DIR, filename)
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="PDF not found")
    return FileResponse(path, media_type="application/pdf")

@app.post("/api/run-ocr")
async def run_ocr(payload: dict):
    """Runs Apple Vision OCR page-by-page and saves to ocr_output/."""
    filename = payload.get("filename")
    if not filename:
        raise HTTPException(status_code=400, detail="Filename required")
        
    pdf_path = os.path.join(PDFS_DIR, filename)
    if not os.path.exists(pdf_path):
        raise HTTPException(status_code=404, detail="PDF file not found")
        
    output_path = os.path.join(OCR_OUTPUT_DIR, filename.replace(".pdf", ".tmp"))
    
    # Try importing PyMuPDF (fitz)
    try:
        import fitz
    except ImportError:
        raise HTTPException(status_code=500, detail="PyMuPDF (fitz) library not installed")
        
    try:
        doc = fitz.open(pdf_path)
        all_texts = []
        
        for page_num in range(doc.page_count):
            page = doc.load_page(page_num)
            pix = page.get_pixmap(matrix=fitz.Matrix(3.0, 3.0))
            temp_img = os.path.join("/tmp", f"_ocr_sandbox_{page_num}.png")
            pix.save(temp_img)
            
            # Execute swift tool
            res = subprocess.check_output(
                ["swift", VISION_TOOL_PATH, temp_img],
                stderr=subprocess.STDOUT,
                timeout=60
            )
            page_text = res.decode("utf-8")
            all_texts.append(page_text)
            
            # Clean up temp image
            if os.path.exists(temp_img):
                os.remove(temp_img)
                
        compiled_text = "\n\n--- PAGE BREAK ---\n\n".join(all_texts)
        compiled_text = normalize_ocr_typos(compiled_text)

        txt_path = os.path.join(OCR_OUTPUT_DIR, filename.replace(".pdf", ".txt"))
        tmp_path = os.path.join(OCR_OUTPUT_DIR, filename.replace(".pdf", ".tmp"))
        
        # Save output to both .txt and .tmp so segment endpoint immediately serves the freshly run OCR output
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(compiled_text)
        with open(tmp_path, "w", encoding="utf-8") as f:
            f.write(compiled_text)
            
        return {"status": "success", "message": "OCR completed", "text": compiled_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OCR execution failed: {str(e)}")

class ScrapePayload(BaseModel):
    sicil_no: str
    city: str

@app.post("/api/scrape-download")
async def scrape_download(payload: ScrapePayload):
    """Scrapes and downloads PDFs for a given sicil_no and city directly to pdfs/ folder."""
    try:
        import importlib
        scraping = importlib.import_module("app.scraping_browser_patched")
        office_norm = importlib.import_module("app.utils.office_normalization")
        browser_manager = scraping.browser_manager
        ensure_login = scraping.ensure_login
        open_pdf_in_new_tab = scraping.open_pdf_in_new_tab
        handle_pdf_popup = scraping.handle_pdf_popup
        ensure_captcha = scraping.ensure_captcha
        normalize_office_freeform = office_norm.normalize_office_freeform
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to import scraper modules: {e}")
        
    office_label = normalize_office_freeform(payload.city)
    if not office_label:
        raise HTTPException(status_code=400, detail=f"Invalid city/office name: {payload.city}")
        
    try:
        # Open browser in headless mode or standard mode
        await browser_manager.open_browser(headless=True)
        page = await browser_manager.get_page()
        if not page:
            raise HTTPException(status_code=500, detail="Failed to get browser page")
            
        await ensure_login(page)
        
        await page.goto("https://www.ticaretsicil.gov.tr/view/hizlierisim/ilangoruntuleme.php", wait_until="domcontentloaded")
        
        await page.wait_for_selector('select#SicilMudurluguId', timeout=30000)
        await page.select_option('select#SicilMudurluguId', label=office_label)
        await page.fill('input#TicSicNo', payload.sicil_no)
        await page.click('button[data-message="İlan Ara"]')
        
        # Wait for search results or empty indicator
        try:
            await page.wait_for_selector('table#tblIlanGoruntuleme tbody tr', timeout=15050)
        except Exception:
            await browser_manager.close_browser()
            return {"status": "empty", "message": "No announcements found for this search", "files": []}
            
        # Set page size to 100 to fetch all if multiple
        try:
            size_selector = 'select[name="tblIlanGoruntuleme_length"]'
            await page.wait_for_selector(size_selector, timeout=5000)
            await page.select_option(size_selector, label='100')
            await page.wait_for_load_state('networkidle', timeout=10000)
        except Exception:
            pass
            
        rows = await page.query_selector_all('table#tblIlanGoruntuleme tbody tr')
        downloaded_files = []
        
        for row in rows:
            cells = await row.query_selector_all('td')
            if len(cells) < 8:
                continue
                
            publication_date_str = (await cells[3].inner_text()).strip()
            title = (await cells[2].inner_text()).strip()
            # Clean title for filename usage
            clean_title = re.sub(r'[\\/*?:"<>| ]', '_', title)[:30]
            
            pdf_link_element = await cells[7].query_selector('a')
            if pdf_link_element:
                pdf_href = await pdf_link_element.get_attribute('href')
                if pdf_href:
                    try:
                        await ensure_captcha(page)
                        new_page = await open_pdf_in_new_tab(page, pdf_href)
                        if not new_page:
                            continue
                            
                        content, captcha_solved = await handle_pdf_popup(page, new_page)
                        try:
                            if not new_page.is_closed():
                                await new_page.close()
                        except Exception:
                            pass
                            
                        if content:
                            dest_name = f"{office_label}_{payload.sicil_no}_{publication_date_str}_{clean_title}.pdf"
                            dest_path = os.path.join(PDFS_DIR, dest_name)
                            with open(dest_path, "wb") as f:
                                f.write(content)
                            downloaded_files.append(dest_name)
                    except Exception as e:
                        print(f"Failed download row: {e}")
                        
        await browser_manager.close_browser()
        return {
            "status": "success",
            "message": f"Successfully scraped & downloaded {len(downloaded_files)} PDF files.",
            "files": downloaded_files
        }
    except Exception as e:
        try:
            await browser_manager.close_browser()
        except:
            pass
        raise HTTPException(status_code=500, detail=f"Scraper task failed: {str(e)}")

@app.post("/api/segment")
async def segment_ocr(payload: dict):
    """Segments OCR raw text by headers into drawer announcements."""
    filename = payload.get("filename")
    if not filename:
         raise HTTPException(status_code=400, detail="Filename required")
         
    tmp_path = os.path.join(OCR_OUTPUT_DIR, filename.replace(".pdf", ".tmp"))
    txt_path = os.path.join(OCR_OUTPUT_DIR, filename.replace(".pdf", ".txt"))
    
    if os.path.exists(tmp_path):
        output_path = tmp_path
    elif os.path.exists(txt_path):
        output_path = txt_path
    else:
        raise HTTPException(status_code=404, detail="OCR output not found for this PDF. Run OCR first.")
        
    with open(output_path, "r", encoding="utf-8") as f:
        raw_text = f.read()
        
    raw_text = normalize_ocr_typos(raw_text)
    chunks = split_by_headers(raw_text)
    
    response = []
    for idx, (header, text) in enumerate(chunks):
        is_incomplete = False
        if idx == len(chunks) - 1:
            # Check last 200 chars for continuation keywords
            text_tail = text[-200:].lower()
            if "devamı" in text_tail and ("sayfada" in text_tail or "yanda" in text_tail or re.search(r"sayfa\s*\d+", text_tail)):
                is_incomplete = True
                
        # Check if Ilan Sıra No is missing in this chunk
        sira_no_missing = False
        if not RE_ILAN_SIRA.search(text):
            sira_no_missing = True

        response.append({
            "index": idx,
            "header": header or f"İlan #{idx + 1}",
            "text": text,
            "is_incomplete": is_incomplete,
            "sira_no_missing": sira_no_missing
        })
    return response

class ExtractPayload(BaseModel):
    text: str
    filename: Optional[str] = None

@app.post("/api/extract")
async def extract_nlp(payload: ExtractPayload):
    """Performs Regex, LLM inference (Ollama), and returns the Hybrid output."""
    text = payload.text
    
    # 1. Regex Extract
    regex_data = extract_entities_regex(text)
    
    # Ensure correct lists formats
    for k in ["addresses", "old_addresses", "hususlar", "ilan_sira_no"]:
        if not isinstance(regex_data.get(k), list):
            regex_data[k] = [regex_data[k]] if regex_data.get(k) else []

    # 2. Local LLM (MLX / Llama 3.2:3b)
    FEW_SHOT_SYSTEM_PROMPT = """You are a precise JSON extractor. You parse Turkish Trade Registry (Ticaret Sicil) announcements.
Your output must be a single JSON object matching the exact format. Do not add any extra keys, nested dictionaries, or comments.
Do not invent or guess any keys. Ensure spelling of entities exactly matches the input text to prevent typos.

JSON format to return:
{
  "persons": [{"name": "Ad Soyad", "tckn": "312******42"}],
  "trade_name": "Şirket Unvanı",
  "old_trade_name": "Eski Şirket Unvanı veya null",
  "sicil_dosya_no": "sicil no veya null",
  "mersis_no": "16 haneli no veya null",
  "addresses": ["Mevcut Adres Bilgisi"],
  "old_addresses": ["Eski Adres Bilgisi veya boş liste"],
  "belgeler": "Tescile delil olan noter/karar belgesi bilgileri veya null",
  "hususlar": ["Tescil edilen hususlar"],
  "ilan_sira_no": ["İlan sıra no"]
}

Rules for persons:
1. 'persons' must be a list of objects with 'name' and 'tckn' fields.
2. Extract ONLY real human individuals (e.g. Ahmet Yılmaz, Sümeyra Bilecen). Exclude company titles, MERSIS numbers, or city/district names (e.g. Beşiktaş, Giresun, İstanbul).
3. TCKN MUST NOT start with 0. TCKN last digit MUST BE AN EVEN DIGIT (0, 2, 4, 6, 8). Never accept odd ending TCKNs.
4. If an entity extracted is not a real human person or has invalid TCKN, exclude it immediately."""

    def is_likely_company(name: str) -> bool:
        name_lower = name.lower()
        company_keywords = ["şirket", "ltd", "ştd", "a.ş.", "aş", "ticaret", "sanayi", "holding", "tic.", "san.", "gıda", "turizm"]
        return len(name) > 35 or any(kw in name_lower for kw in company_keywords)

    def clean_address_text(addr: str) -> str:
        if not addr: return ""
        addr = re.sub(r"\s+", " ", addr).strip()
        stop_pat = re.compile(r"\b(?:Tasfiyeden|Yukarıda|Yukarida|Tescil|Tescile|MERS[İI]S|Ticaret|Telefon|Tel|GSM|Faks|İlan|Ilan|Sira|Sıra|Madde|Gündem|Genel)\b", re.IGNORECASE)
        mstop = stop_pat.search(addr)
        if mstop:
            addr = addr[:mstop.start()].strip()
        cities = ["istanbul", "i̇stanbul", "ankara", "izmir", "i̇zmir", "bursa", "kocaeli", "antalya", "adana"]
        addr_lower = addr.lower()
        for city in cities:
            idx = addr_lower.find(city)
            if idx != -1:
                cleaned = addr[:idx + len(city)].strip()
                cleaned = re.sub(r"\s*[/,.-]\s*$", "", cleaned).strip()
                if len(cleaned) > 15:
                    addr = cleaned
                    break
        return addr

    llm_output = {}
    t0 = time.time()
    try:
        mlx_payload = {
            "model": MODEL_NAME,
            "messages": [
                {"role": "system", "content": FEW_SHOT_SYSTEM_PROMPT},
                {"role": "user", "content": f"Document Text:\n{text}\n\nExtract entities:"}
            ],
            "temperature": 0.0,
        }
        async with httpx.AsyncClient() as client:
            resp = await client.post(LLM_SERVER_URL, json=mlx_payload, timeout=30.0)
            if resp.status_code == 200:
                content = resp.json()["choices"][0]["message"]["content"].strip()
                if "```json" in content:
                    content = content.split("```json")[1].split("```")[0].strip()
                elif "```" in content:
                    content = content.split("```")[1].split("```")[0].strip()
                
                parsed_dict = json.loads(content)
                
                # Coerce types
                if "persons" in parsed_dict:
                    if isinstance(parsed_dict["persons"], list):
                        cleaned_persons = []
                        for x in parsed_dict["persons"]:
                            if x is None:
                                continue
                            if isinstance(x, dict):
                                p_name = str(x.get("name") or "").strip()
                                p_tc = str(x.get("tckn") or "").strip() or None
                                if p_name and not is_likely_company(p_name):
                                    cleaned_persons.append({"name": p_name, "tckn": p_tc})
                            else:
                                p_str = str(x).strip()
                                if p_str and not is_likely_company(p_str):
                                    cleaned_persons.append(p_str)
                        parsed_dict["persons"] = cleaned_persons
                
                for k in ["trade_name", "old_trade_name", "sicil_dosya_no", "mersis_no", "belgeler"]:
                    if k in parsed_dict and isinstance(parsed_dict[k], list):
                        parsed_dict[k] = " ".join([str(x) for x in parsed_dict[k] if x is not None]).strip() or None
                
                for k in ["addresses", "old_addresses"]:
                    if k in parsed_dict and isinstance(parsed_dict[k], list):
                        parsed_dict[k] = [clean_address_text(str(x)) for x in parsed_dict[k] if x is not None]
                        
                llm_output = parsed_dict
    except Exception as e:
        llm_output = {"error": str(e)}

    # Ensure keys exist
    for key in ["persons", "addresses", "old_addresses", "hususlar", "ilan_sira_no"]:
        llm_output.setdefault(key, [])
    for key in ["trade_name", "old_trade_name", "sicil_dosya_no", "mersis_no", "belgeler"]:
        llm_output.setdefault(key, None)

    # 3. Hybrid Merge logic
    def clean_str_field(val):
        if val is None: return None
        if isinstance(val, list): val = " ".join(str(x) for x in val if x)
        val_str = str(val).strip()
        return None if val_str.lower() in ["null", "none", ""] else val_str

    regex_tn = clean_str_field(regex_data.get("trade_name"))
    llm_tn = clean_str_field(llm_output.get("trade_name"))
    trade_name = regex_tn if (regex_tn and regex_tn.lower() in text.lower()) else (llm_tn or regex_tn)
    
    old_trade_name = clean_str_field(llm_output.get("old_trade_name")) or clean_str_field(regex_data.get("old_trade_name"))
    
    regex_m = clean_str_field(regex_data.get("mersis_no"))
    llm_m = clean_str_field(llm_output.get("mersis_no"))
    mersis_no = regex_m if (regex_m and re.match(r"^\d{16}$", regex_m)) else (llm_m or regex_m)
    
    sicil = clean_str_field(llm_output.get("sicil_dosya_no")) or clean_str_field(regex_data.get("sicil_dosya_no"))

    # Helper to unpack person entries
    def _parse_p_item(p):
        if isinstance(p, dict):
            return p.get("name"), p.get("tckn")
        if isinstance(p, str):
            s = p.strip()
            if s.startswith("{") and "name" in s:
                try:
                    import ast
                    d = ast.literal_eval(s)
                    if isinstance(d, dict):
                        return d.get("name"), d.get("tckn")
                except Exception:
                    pass
            return s, None
        return None, None

    # Hybrid persons merge
    hybrid_persons = []
    seen_persons = set()

    for p in regex_data.get("persons", []):
        name, tc = _parse_p_item(p)
        if name and not is_likely_company(name):
            key = (name.upper(), tc)
            if key not in seen_persons:
                seen_persons.add(key)
                hybrid_persons.append({"name": name, "tckn": tc})

    for p in llm_output.get("persons", []):
        name, tc = _parse_p_item(p)
        if name and not is_likely_company(name):
            key_name = name.upper()
            if not any(k[0] == key_name for k in seen_persons):
                seen_persons.add((key_name, tc))
                hybrid_persons.append({"name": name, "tckn": tc})

    addresses_set = set()
    for a in regex_data.get("addresses", []) + llm_output.get("addresses", []):
        cleaned = clean_address_text(str(a))
        if cleaned: addresses_set.add(cleaned)

    old_addresses_set = set()
    for a in regex_data.get("old_addresses", []) + llm_output.get("old_addresses", []):
        cleaned = clean_address_text(str(a))
        if cleaned: old_addresses_set.add(cleaned)

    regex_b = clean_str_field(regex_data.get("belgeler"))
    llm_b = clean_str_field(llm_output.get("belgeler"))
    belgeler = llm_b if (regex_b and llm_b and len(llm_b) >= len(regex_b)) else (llm_b or regex_b)

    hususlar_set = set(regex_data.get("hususlar", []) + llm_output.get("hususlar", []))
    ilan_sira_set = set(regex_data.get("ilan_sira_no", []) + llm_output.get("ilan_sira_no", []))

    hybrid_output = {
        "trade_name": trade_name,
        "old_trade_name": old_trade_name,
        "sicil_dosya_no": sicil,
        "mersis_no": mersis_no,
        "addresses": sorted(list(addresses_set)),
        "old_addresses": sorted(list(old_addresses_set)),
        "persons": hybrid_persons,
        "belgeler": belgeler,
        "hususlar": sorted(list(hususlar_set)),
        "ilan_sira_no": sorted(list(ilan_sira_set))
    }

    latency = time.time() - t0
    
    # Finalize OCR file from .tmp to .txt if it exists
    if payload.filename:
        txt_path = os.path.join(OCR_OUTPUT_DIR, payload.filename.replace(".pdf", ".txt"))
        tmp_path = os.path.join(OCR_OUTPUT_DIR, payload.filename.replace(".pdf", ".tmp"))
        if os.path.exists(tmp_path) and not os.path.exists(txt_path):
            import shutil
            shutil.copy(tmp_path, txt_path)
            
    return {
        "ground_truth": regex_data,
        "llm_only": llm_output,
        "hybrid": hybrid_output,
        "latency": latency
    }

@app.get("/api/progress")
async def get_progress():
    with open(PROGRESS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

@app.post("/api/save-progress")
async def save_progress(payload: dict):
    with open(PROGRESS_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    results = data.get("results", [])
    
    # Overwrite if same pdf and announcement index exists
    new_id = f"{payload.get('filename')}_{payload.get('announcement_index')}"
    existing_idx = -1
    for idx, r in enumerate(results):
        if r.get("eval_id") == new_id:
            existing_idx = idx
            break
            
    payload["eval_id"] = new_id
    if existing_idx != -1:
        results[existing_idx] = payload
    else:
        results.append(payload)
        
    data["results"] = results
    with open(PROGRESS_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        
    return {"status": "success"}

@app.post("/api/reset-evaluation")
async def reset_progress():
    import shutil
    if os.path.exists(PROGRESS_PATH):
        shutil.copy(PROGRESS_PATH, PROGRESS_PATH.replace(".json", "_backup.json"))
    with open(PROGRESS_PATH, "w", encoding="utf-8") as f:
        json.dump({"results": []}, f)
    return {"status": "success"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5005)
