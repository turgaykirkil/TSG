import logging
from typing import List
from uuid import UUID

from fastapi import APIRouter, BackgroundTasks, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.core.config import settings
from app.core.storage import list_objects
from app.services import ocr_service
from app.tasks.ocr_tasks import run_historical_ocr_backfill
from sqlalchemy import text
from pydantic import BaseModel

class OcrStats(BaseModel):
    total_pdfs: int
    pending: int
    completed: int
    failed: int

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/migrate/")
def migrate_ocr_schema(db: Session = Depends(deps.get_db)):
    """
    One-time DDL migration: adds the AI OCR columns to app.ocr_results.
    Safe to call multiple times (uses IF NOT EXISTS).
    """
    ddl_statements = [
        "ALTER TABLE app.ocr_results ADD COLUMN IF NOT EXISTS message TEXT",
        "ALTER TABLE app.ocr_results ADD COLUMN IF NOT EXISTS markdown_content TEXT",
        "ALTER TABLE app.ocr_results ADD COLUMN IF NOT EXISTS json_payload JSONB",
        "ALTER TABLE app.ocr_results ADD COLUMN IF NOT EXISTS processing_time FLOAT",
    ]
    applied = []
    for stmt in ddl_statements:
        try:
            db.execute(text(stmt))
            applied.append(stmt)
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Migration failed on: {stmt}\nError: {e}")
    db.commit()
    return {"status": "ok", "applied": len(applied), "statements": applied}

@router.post("/process/{announcement_id}", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.OcrResult)
def start_ocr_processing(
    announcement_id: UUID,
    db: Session = Depends(deps.get_db),
    background_tasks: BackgroundTasks = BackgroundTasks()
):
    """
    Start OCR processing for a given announcement.
    """
    # This endpoint is temporarily disabled to focus on the preview/verification flow.
    # It will be re-enabled with the correct logic later.
    return {"message": "OCR processing endpoint is temporarily disabled. Use the preview endpoint for testing."}

@router.get("/status/{announcement_id}", response_model=schemas.OcrResult)
def get_ocr_status(
    announcement_id: UUID,
    db: Session = Depends(deps.get_db)
):
    """
    Get the status of an OCR processing task.
    """
    announcement = crud.announcement.get(db, id=announcement_id)
    if not announcement or not announcement.ocr_result:
        raise HTTPException(status_code=404, detail="No OCR task found for this announcement.")
    
    return announcement.ocr_result

@router.get("/results/{announcement_id}", response_model=schemas.OcrResult)
def get_ocr_results(
    announcement_id: UUID,
    db: Session = Depends(deps.get_db)
):
    """
    Get the results of a completed OCR task.
    """
    announcement = crud.announcement.get(db, id=announcement_id)
    if not announcement or not announcement.ocr_result:
        raise HTTPException(status_code=404, detail="No OCR result found for this announcement.")

    if announcement.ocr_result.status != 'completed':
        raise HTTPException(
            status_code=400,
            detail=f"OCR process is not complete. Current status: {announcement.ocr_result.status}"
        )

    return announcement.ocr_result

@router.post("/technical-preview", response_model=schemas.OcrPreviewResponse)
async def get_ocr_technical_preview(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_superuser),
    file: UploadFile = File(...)
):
    """
    Process a PDF with Surya OCR and return a detailed preview for technical review.
    This does not save anything to the database.
    """
    try:
        pdf_content = await file.read()
        logger.info(
            "OCR technical-preview requested file=%s size=%s",
            getattr(file, 'filename', 'unknown'), len(pdf_content) if pdf_content else 0
        )
        # Note: We are using the new Surya-based service function
        preview = ocr_service.get_surya_ocr_preview(
            pdf_content=pdf_content, file_name=file.filename
        )
        logger.info("OCR technical-preview generated pages=%s", len(getattr(preview, 'pages', []) or []))
        return preview
    except Exception as e:
        logger.error("OCR technical-preview failed: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate OCR technical preview: {str(e)}"
        )


# The list-pdfs endpoint is temporarily disabled as we are switching to local file upload
@router.get("/list-pdfs", response_model=List[schemas.FileNameRequest], include_in_schema=False)
def list_available_pdfs():
    """MinIO üzerindeki gazete PDF dosyalarını listeler."""
    try:
        objects = list_objects(settings.minio_bucket_gazette_pdfs)
    except Exception as exc:  # pragma: no cover - ağ/erişim hatası
        logger.error("MinIO list_objects failed: %s", exc, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Could not list files from storage: {exc}"
        )
    pdf_files = []
    for obj in objects:
        name = obj.get("object_name", "")
        if name.lower().endswith(".pdf") and not obj.get("is_dir"):
            pdf_files.append(schemas.FileNameRequest(file_name=name))
    return pdf_files

@router.get("/stats/", response_model=OcrStats)
def get_ocr_stats(db: Session = Depends(deps.get_db)):
    """
    Get the overall statistics for the OCR pipeline.
    """
    # Force schema just in case
    db.execute(text("SET search_path TO app, public"))
    
    # 1. Total pdfs
    total_pdfs = db.execute(text("SELECT COUNT(*) FROM app.announcements WHERE pdf_url IS NOT NULL")).scalar() or 0
    
    # 2. Completed
    completed = db.execute(text("SELECT COUNT(*) FROM app.ocr_results WHERE status = 'completed'")).scalar() or 0
    
    # 3. Failed
    failed = db.execute(text("SELECT COUNT(*) FROM app.ocr_results WHERE status = 'failed'")).scalar() or 0
    
    # 4. Pending (waiting to be scraped)
    # Total PDFs minus the ones that have an ocr_result entry
    ocr_result_count = db.execute(text("SELECT COUNT(DISTINCT announcement_id) FROM app.ocr_results")).scalar() or 0
    pending = total_pdfs - ocr_result_count
    
    return OcrStats(
        total_pdfs=total_pdfs,
        pending=max(0, pending),
        completed=completed,
        failed=failed
    )

@router.post("/start/")
def start_ocr_backfill(limit: int = 100, db: Session = Depends(deps.get_db)):
    """
    Manually triggers the Celery worker to start an OCR backfill process.
    """
    task = run_historical_ocr_backfill.delay(limit=limit)
    return {"message": f"OCR background processing started. Batch size: {limit}", "task_id": task.id}

@router.get("/recent/")
def get_recent_ocr_results(limit: int = 20, db: Session = Depends(deps.get_db)):
    """
    Get the most recently processed OCR results to display in the task queue table.
    """
    db.execute(text("SET search_path TO app, public"))
    results = db.query(models.OcrResult).order_by(models.OcrResult.created_at.desc()).limit(limit).all()
    out = []
    for r in results:
        out.append({
            "id": str(r.id),
            "announcement_id": str(r.announcement_id),
            "status": r.status,
            "message": r.message,
            "pages": r.pdf_page_count,
            "time": r.processing_time,
            "created_at": r.created_at.isoformat() if r.created_at else None,
            "pdf_url": r.announcement.pdf_url if getattr(r, 'announcement', None) else None,
            "markdown_content": r.markdown_content
        })
    return out

@router.get("/debug/")
def debug_ocr_pipeline(db: Session = Depends(deps.get_db)):
    """Debug: shows sample pdf_url values from DB and actual MinIO object names."""
    from app.core.storage import get_minio_client, list_objects
    from urllib.parse import urlparse

    # Sample 10 announcements exactly as the backfill task would pick them
    db.execute(text("SET search_path TO app, public"))
    rows = db.execute(text("""
        SELECT a.id, a.company_id, a.pdf_url, a.publication_date
        FROM app.announcements a
        LEFT JOIN app.ocr_results o ON a.id = o.announcement_id
        WHERE a.pdf_url IS NOT NULL
          AND (o.id IS NULL OR o.status = 'failed')
        ORDER BY a.publication_date DESC NULLS LAST
        LIMIT 10
    """)).mappings().all()

    query_results = []
    for r in rows:
        url = r["pdf_url"]
        
        # Resolve object name using task logic
        obj_name = "N/A"
        try:
            if url.startswith("http"):
                parsed = urlparse(url)
                path = parsed.path
                prefix = f"/{settings.minio_bucket_gazette_pdfs}/"
                if path.startswith(prefix):
                    obj_name = path[len(prefix):]
                else:
                    obj_name = path.lstrip("/")
                    if obj_name.startswith(f"{settings.minio_bucket_gazette_pdfs}/"):
                        obj_name = obj_name[len(settings.minio_bucket_gazette_pdfs)+1:]
            else:
                obj_name = url
        except:
            pass

        query_results.append({
            "id": str(r["id"]),
            "pub_date": str(r["publication_date"]),
            "pdf_url_truncated": url[:80] + "..." if url and len(url) > 80 else url,
            "resolved_object_name": obj_name
        })

    # List MinIO objects
    minio_objects = list_objects(settings.minio_bucket_gazette_pdfs, limit=50)

    return {
        "bucket": settings.minio_bucket_gazette_pdfs,
        "minio_object_count": len(minio_objects),
        "actual_minio_objects": [o["object_name"] for o in minio_objects],
        "top_query_targets": query_results,
    }



