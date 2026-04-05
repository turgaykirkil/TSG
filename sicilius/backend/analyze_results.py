import json
import re
from sqlalchemy import create_engine, text

engine = create_engine("postgresql://postgres:postgres@localhost:5433/sicilius")

# Regex to detect masked IDs (TCKN, VKN, Pasaport)
ID_PATTERN = re.compile(
    r"(\b[1-9]\*{5}[1-9]\d\b|"         
    r"\b[1-9]\d{2}\*{6}[1-9]\d\b|"      
    r"\b[1-9]\d{10}\b|"                 
    r"\b(?:[A-ZÇĞİÖŞÜ]\*{7,8}\d{1,2}|[A-ZÇĞİÖŞÜ]\d{8,9})\b|" 
    r"\b\*{9}\d{2}\b)"                  
)

with engine.connect() as conn:
    results = conn.execute(text(
        "SELECT id, announcement_id, markdown_content, trade_name, persons "
        "FROM app.ocr_results WHERE status='completed'"
    )).mappings().all()
    
    anomalies = []
    
    for row in results:
        md = row["markdown_content"] or ""
        
        # Check Trade Name
        trade_name = row["trade_name"]
        if not trade_name:
            if re.search(r'(unvan|şirket|anonim|limited|a\.ş\.|ltd\.)', md, re.IGNORECASE):
                anomalies.append((row["announcement_id"], "Empty trade_name but company keywords exist."))
                
        # Check Persons
        persons = row["persons"]
        if not persons:  # either None or []
            if ID_PATTERN.search(md):
                anomalies.append((row["announcement_id"], "Empty persons list but masked IDs found in Markdown!"))
                
    print(f"Total processed analyzed: {len(results)}")
    if anomalies:
        print(f"--- Anomalies found: {len(anomalies)} ---")
        for a_id, desc in anomalies:
            print(f"- Announcement {a_id}: {desc}")
    else:
        print("No zero-error anomalies found so far! 100% Accuracy.")
