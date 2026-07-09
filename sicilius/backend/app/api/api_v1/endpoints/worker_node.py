import logging
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from datetime import datetime

from app.api import deps
from app import crud, models


router = APIRouter()

# Authentication (Simple static key for workers)
# In production, use DB-backed API keys or tokens.
WORKER_API_KEY = "temp-worker-key"

def verify_worker_key(api_key: str = "") -> bool:
    if not api_key or api_key != WORKER_API_KEY:
        raise HTTPException(status_code=403, detail="Invalid Worker API Key")
    return True

class WorkerCandidateRequest(BaseModel):
    api_key: str
    city: str
    year: int
    start_from: Optional[int] = None
    count: int = 1
    strategy: Optional[str] = "gap_fill"


from app.schemas import AnnouncementCreate

class WorkerAnnouncement(BaseModel):
    publication_date_str: str
    title: str
    trade_registry_name: str
    trade_registry_number: str
    issue_number: int
    page_number_val: int
    announcement_type: str
    newspaper_name: str
    pdf_url: Optional[str] = None
    ocr_results: List[Dict[str, Any]] = []

class WorkerSubmitRequest(BaseModel):
    api_key: str
    office_label: str
    sicil_no: str
    announcements: List[WorkerAnnouncement] = []

@router.post("/candidates", response_model=Dict[str, Any])
def get_candidates(
    payload: WorkerCandidateRequest,
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    Returns candidate sicil numbers for the worker to scrape.
    """
    verify_worker_key(payload.api_key)
    
    # Use normalized office label and the identical candidate logic as the web scraper
    from app.utils.office_normalization import normalize_office_freeform
    office_label = normalize_office_freeform(payload.city) or payload.city
    
    min_threshold = 100000 if office_label == 'İSTANBUL' else 1
    
    start_from_val = payload.start_from
    if start_from_val is not None and start_from_val <= 0:
        start_from_val = None
    
    from app.scraping_browser import _compute_candidate_sicil_numbers
    candidates = _compute_candidate_sicil_numbers(
        db,
        office_label,
        payload.count,
        min_threshold=min_threshold,
        strategy=payload.strategy or 'gap_fill',
        start_from=start_from_val
    )
    
    return {
        "city": payload.city,
        "candidates": candidates
    }


@router.post("/submit-company", response_model=Dict[str, Any])
def submit_company_data(
    payload: WorkerSubmitRequest,
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    Receives fully scraped and OCR-processed data from a standalone worker and commits it to the database.
    """
    verify_worker_key(payload.api_key)
    
    try:
        company = crud.company.get_or_create_minimal_by_sicil(db, office_label=payload.office_label, sicil_no=str(payload.sicil_no))
        
        saved_announcements_count = 0
        
        for ann in payload.announcements:
            try:
                publication_date = datetime.strptime(ann.publication_date_str.strip(), '%d.%m.%Y').date()
                
                # Deduplication check
                if crud.announcement.get_by_keys(
                    db, 
                    publication_date=publication_date, 
                    issue_number=ann.issue_number, 
                    page_number=ann.page_number_val
                ):
                    continue
                
                # Create Announcement
                announcement_data = AnnouncementCreate(
                    company_id=company.id,
                    trade_registry_name=ann.trade_registry_name,
                    trade_registry_number=ann.trade_registry_number,
                    title=ann.title,
                    publication_date=publication_date,
                    issue_number=ann.issue_number,
                    page_number=ann.page_number_val,
                    announcement_type=ann.announcement_type,
                    newspaper_name=ann.newspaper_name,
                    pdf_url=ann.pdf_url
                )
                announcement = crud.announcement.create(db=db, obj_in=announcement_data)
                saved_announcements_count += 1
                
                # Update basic company info & Save OCR Results
                updated = False
                for ocr_res in ann.ocr_results:
                    regex_entities = ocr_res.get("regex_entities", {})
                    mersis = regex_entities.get("mersis_no") or ocr_res.get("mersis_no")
                    trade = regex_entities.get("trade_name") or ocr_res.get("trade_name")
                    
                    if mersis and not company.mersis_number:
                        company.mersis_number = mersis
                        updated = True
                    if trade and not company.unvan:
                        company.unvan = trade
                        updated = True
                        
                    # Create OcrResult
                    new_ocr = models.OcrResult(
                        announcement_id=announcement.id,
                        company_id=company.id,
                        original_text=ocr_res.get("original_text"),
                        trade_name=regex_entities.get("trade_name"),
                        old_trade_name=regex_entities.get("old_trade_name"),
                        sicil_dosya_no=regex_entities.get("registration_number") or regex_entities.get("sicil_dosya_no"),
                        mersis_no=regex_entities.get("mersis_no"),
                        addresses=regex_entities.get("addresses"),
                        old_addresses=regex_entities.get("old_addresses"),
                        persons=regex_entities.get("persons"),
                        hususlar=regex_entities.get("hususlar"),
                        belgeler=regex_entities.get("belgeler"),
                        ilan_sira_no=regex_entities.get("ilan_sira_no"),
                        sicil_office_header=ocr_res.get("header"),
                        item_index=ocr_res.get("index"),
                        json_payload={"regex_entities": regex_entities},
                        status="pending_llm"
                    )
                    db.add(new_ocr)
                    
                if updated:
                    db.add(company)
                    
                db.commit()
                db.refresh(company)
            except Exception as row_e:
                db.rollback()
                logging.error(f"Error processing row in worker submit: {row_e}")
                continue
            
        return {
            "status": "success",
            "company_id": company.id,
            "announcements_created": saved_announcements_count
        }
    except Exception as e:
        db.rollback()
        logging.error(f"Worker submission error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
