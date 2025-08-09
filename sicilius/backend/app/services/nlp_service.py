import spacy
import logging
import re
from spacy.cli.download import download as spacy_download
from spacy.util import is_package

# Configure logging
logger = logging.getLogger(__name__)

MODEL_NAME = "tr_core_news_sm"
nlp_model = None

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
    # ‘I’/’l’/’ı’ karışımlarını ellememek daha güvenli; domain-spesifik bilgi gerek.
    # Tekrarlanan boşlukları sadeleştir
    s = re.sub(r"\u00A0", " ", s)  # non-breaking space
    s = re.sub(r"\s+", " ", s)
    # Sayfalar arası ayırıcıları korumadan sadeleştir
    s = re.sub(r"---\s*Sayfa\s*\d+\s*---", "\n", s, flags=re.IGNORECASE)
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

    # Try a list of candidate models in order, then fallback to blank Turkish pipeline
    candidates = ["tr_core_news_sm", "xx_ent_wiki_sm"]

    for model_name in candidates:
        # Ensure installed; attempt download if not
        if not is_package(model_name):
            logger.info(f"spaCy model '{model_name}' not found. Trying to download…")
            try:
                spacy_download(model_name)
                logger.info(f"Model '{model_name}' downloaded successfully.")
            except SystemExit as e:
                if e.code != 0:
                    logger.warning(
                        f"Could not download spaCy model '{model_name}' (exit code {e.code}). Will try next option."
                    )
                    continue
                else:
                    logger.info(f"Model '{model_name}' downloaded successfully (via SystemExit).")

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
    doc = nlp_model(norm)
    
    entities = {
        "organizations": [],
        "locations": [],
        "persons": [],
        "dates": [],
        "money": [],
        "misc": []
    }
    
    for ent in doc.ents:
        entity_data = {"text": ent.text, "label": ent.label_}
        label = ent.label_
        if label == "ORG":
            entities["organizations"].append(entity_data)
        elif label in ("GPE", "LOC"):
            entities["locations"].append(entity_data)
        elif label in ("PERSON", "PER"):
            entities["persons"].append(entity_data)
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

    # 4) Ticaret Unvanı – hemen sonraki boş olmayan satır(lar)
    trade_name = None
    m_unvan = re.search(r"Ticaret\s*Unvan[ıi]\s*[:.]?\s*(.*)", norm, re.IGNORECASE)
    if m_unvan:
        after = m_unvan.group(1).strip()
        if after:
            trade_name = after
        else:
            # Sonraki satırı al
            # Basit yaklaşım: Unvan satırından sonra gelen ilk boş olmayan satır
            lines = norm.splitlines()
            idx = 0
            for i, ln in enumerate(lines):
                if re.search(r"Ticaret\s*Unvan[ıi]\s*:?\s*$", ln, re.IGNORECASE):
                    idx = i
                    break
            for j in range(idx+1, min(idx+5, len(lines))):
                cand = lines[j].strip()
                if cand:
                    trade_name = cand
                    break
    if trade_name:
        entities["trade_name"] = trade_name
        # ORG listesine de ek olarak itilebilir
        entities["organizations"].append({"text": trade_name, "label": "ORG"})

    # 5) Adres(ler)
    addresses = find_all(r"Adres\s*[:.]?\s*([^\n]+)", norm)
    if addresses:
        entities["addresses"] = unique_list(addresses)

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
