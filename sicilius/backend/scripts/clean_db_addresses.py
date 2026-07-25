#!/usr/bin/env python3
import re
import sys
from pathlib import Path

# Add backend directory to sys.path
backend_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_dir))

from app.db.session import SessionLocal
from app.models.ocr_result import OcrResult

def clean_address(raw_addr: str) -> str:
    if not raw_addr:
        return ""
    addr = str(raw_addr).strip()
    match = re.search(r"(?i)\badresi\s*[:\s]?", addr)
    if match:
        addr = addr[match.end():].strip()
    addr = re.sub(r"^\s*[:\-\.]+", "", addr).strip()
    return addr

def main():
    db = SessionLocal()
    try:
        ocr_rows = db.query(OcrResult).filter(OcrResult.old_addresses.isnot(None)).all()
        updated_count = 0
        for row in ocr_rows:
            if not row.old_addresses:
                continue
            new_list = []
            changed = False
            for item in row.old_addresses:
                raw = item.get("address") if isinstance(item, dict) else str(item)
                cleaned = clean_address(raw)
                if cleaned:
                    if isinstance(item, dict):
                        new_list.append({"address": cleaned})
                    else:
                        new_list.append(cleaned)
                    if cleaned != raw:
                        changed = True
            if changed:
                row.old_addresses = new_list
                db.add(row)
                updated_count += 1
        db.commit()
        print(f"✅ Successfully cleaned old addresses for {updated_count} OCR records in PostgreSQL database!")
    finally:
        db.close()

if __name__ == "__main__":
    main()
