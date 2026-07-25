import logging
import time
import asyncio
from typing import Dict, Any, List
from fastapi import APIRouter, Depends, BackgroundTasks, status, HTTPException
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

is_enrichment_active = False
should_stop_enrichment = False

class OperationStatus(BaseModel):
    stats: OperationStats
    logs: List[str]
    is_scraping_active: bool
    is_enrichment_active: bool

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
        "is_scraping_active": is_scraping_active,
        "is_enrichment_active": is_enrichment_active
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
    global is_enrichment_active, should_stop_enrichment
    is_enrichment_active = True
    should_stop_enrichment = False

    # Since we're in a background task, we need a fresh session
    db = next(db_gen)
    try:
        pending = db.query(models.OcrResult).filter(
            models.OcrResult.status == "pending_llm"
        ).order_by(models.OcrResult.created_at.desc()).limit(limit).all()
        
        if not pending:
            # Fallback: Process recent completed or un-enriched OCR rows if none marked as pending_llm
            pending = db.query(models.OcrResult).order_by(models.OcrResult.created_at.desc()).limit(limit).all()
        
        if not pending:
            logger.info("Background enrichment: No tasks found.")
            scraping_state.add_log("🤖 [AI Enrichment] İşlenecek OCR kaydı bulunamadı.")
            return

        logger.info(f"Background enrichment: Processing {len(pending)} items.")
        scraping_state.add_log(f"🤖 [AI Enrichment] Yapay zeka analizi (Llama 3.2:3b) başladı! Toplam {len(pending)} kayıt işleniyor...")
        
        for idx, ocr in enumerate(pending, 1):
            if should_stop_enrichment:
                scraping_state.add_log("🛑 [AI Enrichment] Yapay zeka analizi kullanıcı tarafından durduruldu.")
                break

            try:
                # Capture BEFORE state
                before_persons = ocr.persons or []
                before_old_addrs = ocr.old_addresses or []
                before_p_cnt = len(before_persons) if isinstance(before_persons, list) else 0
                before_oa_cnt = len(before_old_addrs) if isinstance(before_old_addrs, list) else 0
                title = (ocr.trade_name or f"Sicil No: {ocr.sicil_dosya_no}" or f"OCR #{ocr.id}")[:30]

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
                if enriched:
                    ocr.trade_name = enriched.get("trade_name") or ocr.trade_name
                    ocr.old_trade_name = enriched.get("old_trade_name") or ocr.old_trade_name
                    ocr.sicil_dosya_no = enriched.get("sicil_dosya_no") or ocr.sicil_dosya_no
                    ocr.mersis_no = enriched.get("mersis_no") or ocr.mersis_no
                    ocr.addresses = enriched.get("addresses") or ocr.addresses
                    ocr.old_addresses = enriched.get("old_addresses") or ocr.old_addresses
                    ocr.persons = enriched.get("persons") or ocr.persons
                    ocr.hususlar = enriched.get("hususlar") or ocr.hususlar
                    ocr.belgeler = enriched.get("belgeler") or ocr.belgeler
                    ocr.ilan_sira_no = enriched.get("ilan_sira_no") or ocr.ilan_sira_no
                
                ocr.status = "completed"
                ocr.processing_time = (ocr.processing_time or 0) + duration
                
                if ocr.company_id and enriched:
                    try:
                        from app.services.ingest_service import sync_relational_data_from_nlp
                        sync_relational_data_from_nlp(db, ocr.company_id, enriched)
                    except Exception as ex_sync:
                        logger.warning(f"Relational sync failed after enrichment for company_id={ocr.company_id}: {ex_sync}")
                        
                db.commit()
                
                # Format AFTER state
                p_names = []
                if isinstance(ocr.persons, list):
                    for p in ocr.persons:
                        if isinstance(p, dict) and p.get("name"):
                            tc_str = f" ({p.get('tckn')})" if p.get("tckn") else ""
                            p_names.append(f"{p.get('name')}{tc_str}")
                        elif isinstance(p, str):
                            p_names.append(p)

                p_cnt = len(ocr.persons) if isinstance(ocr.persons, list) else 0
                oa_cnt = len(ocr.old_addresses) if isinstance(ocr.old_addresses, list) else 0
                p_detail = f" -> Kişiler: {', '.join(p_names)}" if p_names else ""
                oa_detail = f" -> Eski Adres: {ocr.old_addresses[0].get('address') if isinstance(ocr.old_addresses[0], dict) else ocr.old_addresses[0]}" if (isinstance(ocr.old_addresses, list) and ocr.old_addresses) else ""
                
                # Log BEFORE vs AFTER Comparison
                scraping_state.add_log(f"🔴 [AI Enrichment NEYDİ {idx}/{len(pending)}] #{ocr.id} {title} -> {before_p_cnt} kişi, {before_oa_cnt} eski adres")
                scraping_state.add_log(f"🟢 [AI Enrichment NE OLDU {idx}/{len(pending)}] #{ocr.id} {title} -> {p_cnt} kişi, {oa_cnt} eski adres{p_detail}{oa_detail} ({duration:.2f}s)")
                
                # If scraping is running concurrently, pause slightly to share CPU resources
                if scraping_state.get_status().get("running"):
                    await asyncio.sleep(0.5)
                
            except Exception as e:
                logger.error(f"Error enriching OCR result {ocr.id}: {e}")
                ocr.status = "failed_llm"
                ocr.message = str(e)
                db.commit()
                scraping_state.add_log(f"❌ [AI Enrichment] OCR #{ocr.id} analizi başarısız: {e}")
                
        if not should_stop_enrichment:
            scraping_state.add_log(f"✅ [AI Enrichment] Toplam {len(pending)} adet kayıt Llama 3.2:3b ile başarıyla zenginleştirildi!")
    finally:
        is_enrichment_active = False
        should_stop_enrichment = False
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
    global is_enrichment_active, should_stop_enrichment
    if is_enrichment_active:
        raise HTTPException(status_code=400, detail="AI Enrichment is already running.")

    background_tasks.add_task(run_enrichment_task, deps.get_db(), limit)
    return {"message": f"AI enrichment started for up to {limit} items."}

@router.post("/enrich/stop")
def stop_enrichment(
    current_user: models.User = Depends(deps.get_current_active_superuser)
):
    """
    Stop active AI enrichment task.
    """
    global should_stop_enrichment
    should_stop_enrichment = True
    scraping_state.add_log("🛑 [AI Enrichment] Yapay zeka analizini durdurma isteği gönderildi...")
    return {"message": "Enrichment stop signal sent."}
