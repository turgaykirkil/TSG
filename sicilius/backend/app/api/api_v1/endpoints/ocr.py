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

router = APIRouter()
logger = logging.getLogger(__name__)

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

