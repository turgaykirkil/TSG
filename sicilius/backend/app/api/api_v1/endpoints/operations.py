import logging
import time
from typing import Dict, Any, List
from fastapi import APIRouter, Depends, BackgroundTasks, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import text

from app import crud, models, schemas
from app.api import deps
from app.scraping_state import scraping_state
from process_pdfs import enrich_ocr_with_llama

router = APIRouter()
logger = logging.getLogger(__name__)

class OperationStats(BaseModel):
    total_announcements: int
    scraped_pdfs: int
    pending_llm: int
    completed_ocr: int
    failed_llm: int
    success_rate: float

class OperationStatus(BaseModel):
    stats: OperationStats
    logs: List[str]
    is_scraping_active: bool

@router.get("/status", response_model=OperationStatus)
def get_unified_status(db: Session = Depends(deps.get_db)):
    """
    Get combined statistics and logs in a single request.
    """
    # Get stats logic
    db.execute(text("SET search_path TO app, public"))
    total_announcements = db.execute(text("SELECT COUNT(*) FROM app.announcements")).scalar() or 0
    scraped_pdfs = db.execute(text("SELECT COUNT(*) FROM app.announcements WHERE pdf_url IS NOT NULL")).scalar() or 0
    pending_llm = db.execute(text("SELECT COUNT(*) FROM app.ocr_results WHERE status = 'pending_llm'")).scalar() or 0
    completed_ocr = db.execute(text("SELECT COUNT(*) FROM app.ocr_results WHERE status = 'completed'")).scalar() or 0
    failed_llm = db.execute(text("SELECT COUNT(*) FROM app.ocr_results WHERE status = 'failed_llm'")).scalar() or 0
    
    success_rate = 0.0
    if completed_ocr + failed_llm > 0:
        success_rate = (completed_ocr / (completed_ocr + failed_llm)) * 100
        
    stats = {
        "total_announcements": total_announcements,
        "scraped_pdfs": scraped_pdfs,
        "pending_llm": pending_llm,
        "completed_ocr": completed_ocr,
        "failed_llm": failed_llm,
        "success_rate": round(success_rate, 2)
    }

    # Get logs and status
    scraping_info = scraping_state.get_status()
    logs = scraping_info.get("logs", [])
    is_scraping_active = scraping_info.get("running", False)

    return {
        "stats": stats,
        "logs": logs,
        "is_scraping_active": is_scraping_active
    }

@router.get("/stats", response_model=OperationStats)
def get_operations_stats(db: Session = Depends(deps.get_db)):
    """
    Get the latest system activity logs from the scraping state.
    """
    return scraping_state.get_status().get("logs", [])

async def run_enrichment_task(db_gen, limit: int):
    """
    Background task to process pending LLM enrichments.
    """
    # Since we're in a background task, we need a fresh session
    db = next(db_gen)
    try:
        pending = db.query(models.OcrResult).filter(
            models.OcrResult.status == "pending_llm"
        ).order_by(models.OcrResult.created_at.desc()).limit(limit).all()
        
        if not pending:
            logger.info("Background enrichment: No pending tasks.")
            return

        logger.info(f"Background enrichment: Processing {len(pending)} items.")
        
        for ocr in pending:
            try:
                # Extract context
                text_content = ocr.original_text
                regex_entities = (ocr.json_payload or {}).get("regex_entities", {})
                index = ocr.item_index or 0
                header = ocr.sicil_office_header or ""
                
                # Call Llama Enhancement
                start_time = time.time()
                enriched = enrich_ocr_with_llama(text_content, regex_entities, index, header)
                duration = time.time() - start_time
                
                # Update fields
                ocr.trade_name = enriched.get("trade_name")
                ocr.old_trade_name = enriched.get("old_trade_name")
                ocr.sicil_dosya_no = enriched.get("sicil_dosya_no")
                ocr.mersis_no = enriched.get("mersis_no")
                ocr.addresses = enriched.get("addresses")
                ocr.old_addresses = enriched.get("old_addresses")
                ocr.persons = enriched.get("persons")
                ocr.hususlar = enriched.get("hususlar")
                ocr.belgeler = enriched.get("belgeler")
                ocr.ilan_sira_no = enriched.get("ilan_sira_no")
                
                ocr.status = "completed"
                ocr.processing_time = (ocr.processing_time or 0) + duration
                db.commit()
                
            except Exception as e:
                logger.error(f"Error enriching OCR result {ocr.id}: {e}")
                ocr.status = "failed_llm"
                ocr.message = str(e)
                db.commit()
    finally:
        db.close()

@router.post("/enrich", status_code=status.HTTP_202_ACCEPTED)
async def trigger_enrichment(
    background_tasks: BackgroundTasks,
    limit: int = 50,
    current_user: models.User = Depends(deps.get_current_active_superuser)
):
    """
    Trigger AI enrichment for pending results in the background.
    """
    background_tasks.add_task(run_enrichment_task, deps.get_db(), limit)
    return {"message": f"AI enrichment started for up to {limit} items."}
