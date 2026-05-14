import sys
import os
from pathlib import Path
from sqlalchemy import or_
from sqlalchemy.orm import Session

# Add the backend app to Python path
backend_dir = Path(__file__).parent.parent
sys.path.append(str(backend_dir))

from app.db.session import SessionLocal
from app.models.ocr_result import OcrResult
from app.models.company import Company
import unicodedata
import re

def _normalize_tr(text: str) -> str:
    if not text: return ""
    text = text.replace('I', 'ı').replace('İ', 'i').lower()
    return unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('utf-8')

def _get_vkn_from_text(text: str) -> str:
    m = re.search(r'\b(\d{10,16})\b', text)
    if not m: return ""
    val = m.group(1)
    if len(val) == 16 and val.startswith("0"):
        return val[1:11]
    return val[:11]

import uuid

def get_or_create_target_company(db, ocr, original_company, ann_vkn, ann_sicil):
    # Try to find by Mersis if available
    if ann_vkn:
        existing = db.query(Company).filter(
            Company.mersis_number.ilike(f"%{ann_vkn}%")
        ).first()
        if existing: return existing
        
    # Try by Sicil and Unvan loosely
    unvan = (ocr.trade_name or "").strip()
    if ann_sicil and unvan:
        existing = db.query(Company).filter(
            Company.sicil_no == ann_sicil,
            Company.unvan.ilike(f"%{unvan[:10]}%") # Match first 10 chars to avoid small typos
        ).first()
        if existing: return existing

    # Create new company
    new_unvan = unvan if unvan else f"SİSTEM KEŞFİ (Sicil: {ann_sicil or 'BİLİNMİYOR'})"
    new_unvan = new_unvan[:450] # Prevent StringDataRightTruncation (column is VARCHAR 500)
    
    new_company = Company(
        id=uuid.uuid4(),
        unvan=new_unvan,
        sicil_no=ann_sicil or None,
        mersis_number=ann_vkn if ann_vkn else None,
        city=original_company.city, # Assume it's from the same gazette city list
        address=original_company.address # Assume same address if no other clue, but better left blank or generic
    )
    db.add(new_company)
    db.flush() # flush to get the ID without committing the whole transaction yet
    return new_company

def run_cleansing():
    print("Starting OCR Crosslink Cleansing Process (Auto-Discovery Mode)...")
    db: Session = SessionLocal()
    
    try:
        total_ocrs = db.query(OcrResult).count()
        print(f"Total OCR records to scan: {total_ocrs}")
        
        offset = 0
        limit = 1000
        detached_count = 0
        processed_count = 0
        new_company_count = 0
        
        while True:
            # We must load OcrResult and its Company
            results = db.query(OcrResult, Company).join(Company, OcrResult.company_id == Company.id).offset(offset).limit(limit).all()
            if not results:
                break
                
            for ocr, company in results:
                processed_count += 1
                
                target_vkn = _get_vkn_from_text(str(getattr(company, "mersis_number", "") or getattr(company, "mersis_number_ocr", "") or ""))
                company_unvan = company.unvan or ""
                norm_unvan = _normalize_tr(company_unvan).replace("tasfiye halinde", "").strip()
                company_sicil = str(company.sicil_no or "").strip()
                
                ann_text = f"{ocr.trade_name or ''} {ocr.original_text or ''} {ocr.hususlar or ''}"
                
                ann_vkn = _get_vkn_from_text(str(getattr(ocr, "mersis_no", "")))
                if not ann_vkn:
                    ann_vkn = _get_vkn_from_text(ann_text)
                    
                ann_sicil = str(getattr(ocr, "sicil_dosya_no", "")).strip()
                
                is_match = True
                
                # 1. Check Mersis
                if target_vkn and ann_vkn:
                    if ann_vkn != target_vkn:
                        is_match = False
                else:
                    # 2. Check Sicil (if no Mersis)
                    if company_sicil and ann_sicil and ann_sicil != company_sicil:
                        is_match = False
                    else:
                        # 3. Check Name Heuristic
                        parts = [p for p in norm_unvan.split() if len(p) > 3]
                        if parts:
                            search_text = _normalize_tr(ann_text)
                            match_count = sum(1 for p in parts if p in search_text)
                            required_matches = min(2, len(parts))
                            if match_count < required_matches:
                                is_match = False
                
                if not is_match:
                    print(f"Mismatch Detected: OCR {ocr.id} mapped to {company.unvan} (Sicil: {company.sicil_no}). Fixing...")
                    target_company = get_or_create_target_company(db, ocr, company, ann_vkn, ann_sicil)
                    
                    ocr.company_id = target_company.id
                    detached_count += 1
                    if target_company.unvan.startswith("SİSTEM KEŞFİ") or target_company.id not in [comp.id for _, comp in results]:
                         new_company_count += 1
                         print(f" -> Reassigned to auto-discovered company: {target_company.unvan} (ID: {target_company.id})")
            
            db.commit()
            print(f"Processed {processed_count} records. Fixed {detached_count} links so far...")
            offset += limit
            
        print(f"\nCleansing Complete! Fixed {detached_count} incorrectly linked OCR records.")
        print(f"Auto-discovered and created {new_company_count} new companies during the process.")
        
    except Exception as e:
        db.rollback()
        print(f"Error during cleansing: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    run_cleansing()
