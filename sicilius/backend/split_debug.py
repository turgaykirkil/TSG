import json, re, os

FILE_PATH = '/Users/turgaykirkil/Apps/TSG_Platform/sicilius/backend/test_ocr_vizualisation/debug_ocr.json'

try:
    with open(FILE_PATH, 'r', encoding='utf-8') as f:
        d = json.load(f)
    
    txt = d['raw_text']
    # Project-native regex for segmentation
    regex = r"(?mi)^\s*(?:T\.?C\.?\s*)?.{0,100}?(?:T[İIÌ]CARET(?:\s+|[\r\n]){0,3}S[İIÌ]C[İIÌ]L[İIÌ](?:\s+|[\r\n]){0,3}(?:M[ÜU]D[ÜU]RL[ÜU][ĞG][ÜU][’\']?N[DT][EA]N|MEMURLU[ĞG][UÜ][’\']?N[DT][EA]N)|MAHKEMES[İIÌ][NNDD][’\']?EN)\s*$"
    
    matches = list(re.finditer(regex, txt))
    chunks = []
    
    if not matches:
        chunks = [txt]
    else:
        for i in range(len(matches)):
            start = matches[i].start()
            end = matches[i+1].start() if i+1 < len(matches) else len(txt)
            chunk = txt[start:end].strip()
            if chunk:
                chunks.append(chunk)
                
    d['chunks'] = chunks
    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
        
    print(f"✅ Parçalama Tamamlandı. Toplam {len(chunks)} adet ilan bulundu.")
except Exception as e:
    print(f"❌ Hata: {e}")
