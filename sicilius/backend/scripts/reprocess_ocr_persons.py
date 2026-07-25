#!/usr/bin/env python3
import sys
from pathlib import Path

# Add backend directory to sys.path
backend_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_dir))

from app.db.session import SessionLocal
from app.models.ocr_result import OcrResult
from process_pdfs import extract_entities_regex
from app.services.ingest_service import sync_relational_data_from_nlp

def main():
    db = SessionLocal()
    try:
        ocr_rows = db.query(OcrResult).filter(OcrResult.original_text.isnot(None)).all()
        total = len(ocr_rows)
        print(f"🔄 Processing {total} OCR records with real-time feedback...")
        
        for idx, row in enumerate(ocr_rows, 1):
            re_ent = extract_entities_regex(row.original_text)
            row.addresses = re_ent.get("addresses")
            row.old_addresses = re_ent.get("old_addresses")
            row.persons = re_ent.get("persons")
            db.add(row)
            if row.company_id:
                sync_relational_data_from_nlp(db, row.company_id, re_ent)
            
            if idx % 10 == 0 or idx == total:
                db.commit()
                print(f"   [{idx}/{total}] Processed and saved...")
                
        print(f"✅ FINISHED! Successfully re-extracted clean persons and addresses for {total} OCR records!")
    except Exception as e:
        db.rollback()
        print(f"❌ Error during reprocess: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    main()
