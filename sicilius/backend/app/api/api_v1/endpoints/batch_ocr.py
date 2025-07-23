import logging
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, status
from sqlalchemy.orm import Session

from app import crud, models, schemas, services
from app.api import deps

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/process-batch", status_code=status.HTTP_202_ACCEPTED)
def start_batch_ocr_processing(
    *, 
    db: Session = Depends(deps.get_db),
    batch_input: schemas.OcrBatchRequest,
    background_tasks: BackgroundTasks,
    current_user: models.User = Depends(deps.get_current_active_user),
):
    """
    Start OCR processing for a batch of announcements that are pending.
    """
    # 1. Find announcements with pending OCR status
    # We will fetch announcements that do not have an ocr_result entry yet.
    announcements_to_process = crud.announcement.get_multi_without_ocr_results(db, limit=batch_input.limit)
    
    if not announcements_to_process:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No new announcements found to process."
        )

    announcement_ids = [str(ann.id) for ann in announcements_to_process]
    logger.info(f"Found {len(announcement_ids)} announcements for batch OCR processing: {announcement_ids}")

    # 2. Create initial OCR result entries and start background tasks
    for ann_id in announcement_ids:
        # Check if an OCR result already exists, just in case.
        existing_ocr_result = crud.ocr_result.get_by_announcement(db, announcement_id=ann_id)
        if not existing_ocr_result:
            ocr_result_in = schemas.OcrResultCreate(announcement_id=ann_id)
            crud.ocr_result.create(db=db, obj_in=ocr_result_in)
            background_tasks.add_task(services.ocr_service.process_pdf_for_ocr, db=db, announcement_id=ann_id)

    return {"message": f"Started OCR processing for {len(announcement_ids)} announcements."}
