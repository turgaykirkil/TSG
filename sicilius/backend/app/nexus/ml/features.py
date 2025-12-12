import re
from typing import Optional

def extract_capital(text: str) -> float:
    """
    Extracts the capital amount from the OCR text.
    Looks for patterns like 'Sermaye... 100.000 TL', '5.000.000 Türk Lirası'.
    Returns the maximum found amount as float (assuming latest capital increase is largest).
    Returns 0.0 if not found.
    """
    if not text:
        return 0.0
    
    # Normalize text
    text_lower = text.lower().replace('\n', ' ')
    
    # Regex to find money amounts near "sermaye"
    # Logic:
    # 1. Look for 'sermaye'
    # 2. Look ahead for digits with optional dots/commas
    # 3. Look for currency marker (TL, Lira, YTL)
    
    # Pattern 1: "Sermaye ... X TL"
    # Matches: "Sermayesi 100.000 TL", "Sermaye artırımı 5.000.000 Türk Lirası"
    # We capture the number group.
    # Regex explanation:
    # sermaye.{0,100}? -> "sermaye" followed by up to 100 chars (lazy)
    # (\d{1,3}(?:[.,]\d{3})*(?:[.,]\d{2})?) -> The number part (e.g. 1.000.000 or 1,000,000.00)
    # \s*(?:tl|türk lirası|ytl) -> Currency suffix
    pattern = r"sermaye.{0,100}?(\d{1,3}(?:[.,]\d{3})*(?:[.,]\d{2})?)\s*(?:tl|türk lirası|ytl)"
    
    matches = re.finditer(pattern, text_lower)
    
    amounts = []
    for match in matches:
        amount_str = match.group(1)
        # Clean string to float
        # Remove dots (thousands separator in TR)
        # Replace comma with dot (decimal separator in TR)
        # Edge case: 1,000,000 (US style)? 
        # TR official style: 1.000.000,00
        
        # Heuristic:
        # If string has both '.' and ',', the last one is decimal.
        # But '1.000.000' has only dots -> these are thousands.
        # '100,00' has only comma -> decimal.
        
        clean_str = amount_str
        
        if '.' in clean_str and ',' in clean_str:
            # 1.000,00 -> remove '.', replace ',' with '.'
            clean_str = clean_str.replace('.', '').replace(',', '.')
        elif '.' in clean_str:
            # 1.000.000 -> remove '.'
            # 1.500 -> remove '.' -> 1500
            # Risk: 1.5 (1 and a half)? No, usually capital is integer or large.
            # Gazette usually uses dots for thousands.
            clean_str = clean_str.replace('.', '')
        elif ',' in clean_str:
            # 1000,00 -> replace ',' with '.'
             clean_str = clean_str.replace(',', '.')
             
        try:
            val = float(clean_str)
            amounts.append(val)
        except ValueError:
            continue
            
    if not amounts:
        return 0.0
        
    # Assumption: The largest amount mentioned is the latest/total capital
    return max(amounts)

def calculate_sector_entropy(titles: list[str]) -> float:
    """
    Calculates the 'Sector Entropy' (Chaos Level) of a group of companies.
    
    Logic:
    - If titles are "Turkis Bank A.S.", "Garanti Bank A.S." -> High Similarity -> Low Entropy (0.1)
    - If titles are "Ahmet Insaat", "Mehmet Yazilim", "Ayse Gida" -> Low Similarity -> High Entropy (0.9)
    
    Returns: Float between 0.0 (Homogeneous) and 1.0 (Chaotic)
    """
    if not titles or len(titles) < 2:
        return 0.0
        
    # 1. Preprocessing (Tokenization)
    stopwords = {
        "ANONİM", "ŞİRKETİ", "LİMİTED", "TİCARET", "SANAYİ", "VE", 
        "A.Ş.", "LTD.", "ŞTİ.", "A.Ş", "LTD", "ŞTİ", "GIDA", "TURİZM", "İNŞAAT", # Generic sectors also noise? No, sector keywords are signal.
        "YATIRIM", "DJ", "DIŞ", "İÇ", "PAZARLAMA", "HİZMETLERİ", "TİC.", "SAN.", "VE", "THE"
    }
    
    tokenized_titles = []
    for t in titles:
        if not t: continue
        # Split, upper, filter, set
        tokens = set(word for word in t.upper().replace('.', ' ').split() 
                     if len(word) > 2 and word not in stopwords)
        if tokens:
            tokenized_titles.append(tokens)

    if len(tokenized_titles) < 2:
        return 0.0

    # 2. Pairwise Jaccard Similarity
    # Compare every title with every other title
    total_score = 0.0
    comparisons = 0
    
    for i in range(len(tokenized_titles)):
        for j in range(i + 1, len(tokenized_titles)):
            set_a = tokenized_titles[i]
            set_b = tokenized_titles[j]
            
            intersection = len(set_a.intersection(set_b))
            union = len(set_a.union(set_b))
            
            if union > 0:
                jaccard = intersection / union
                total_score += jaccard
            comparisons += 1
            
    if comparisons == 0:
        return 0.0
        
    avg_similarity = total_score / comparisons
    
    # Entropy is inverse of similarity
    # Similarity 1.0 -> Entropy 0.0
    # Similarity 0.0 -> Entropy 1.0
    return 1.0 - avg_similarity
