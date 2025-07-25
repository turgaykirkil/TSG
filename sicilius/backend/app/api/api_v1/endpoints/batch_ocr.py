import logging
from sqlalchemy.orm import Session

import base64
from io import BytesIO
from PIL import Image
import logging
from typing import List, Any

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from supabase import Client

from app import crud, models, schemas
from app.api import deps
from app.core.dependencies import get_supabase_client
from app.services.ocr_service import process_specific_pdf_preview

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/start-batch-ocr/", status_code=202)
def start_batch_ocr(
    *,
    db: Session = Depends(deps.get_db),
    announcement_ids: List[int],
    background_tasks: BackgroundTasks,
    current_user: models.User = Depends(deps.get_current_active_user),
):
    """
    Starts a background OCR process for a batch of announcements.
    This is a placeholder and does not yet run the full OCR.
    """
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=403, detail="Not enough permissions")

    # 1. Validate that all announcements exist
    for ann_id in announcement_ids:
        announcement = crud.announcement.get(db, id=ann_id)
        if not announcement:
            raise HTTPException(status_code=404, detail=f"Announcement with id {ann_id} not found.")

    # 2. Create initial OCR result entries and add task to background
    for ann_id in announcement_ids:
        existing_ocr_result = crud.ocr_result.get_by_announcement(db, announcement_id=ann_id)
        if not existing_ocr_result:
            ocr_result_in = schemas.OcrResultCreate(announcement_id=ann_id)
            crud.ocr_result.create(db=db, obj_in=ocr_result_in)
            # TODO: Add the actual OCR processing to the background tasks
            # background_tasks.add_task(ocr_service.run_full_ocr, db=db, announcement_id=ann_id)
            logger.info(f"Task for announcement {ann_id} would be added here.")

    return {"message": f"OCR processing tasks initiated for {len(announcement_ids)} announcements."}


@router.post("/process-and-preview/", response_model=schemas.OcrPreviewResponse)
def process_and_preview_single(
    *,
    db: Session = Depends(deps.get_db),
        supabase_client: Client = Depends(get_supabase_client),
    announcement_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Process a single PDF for OCR and return a preview.
    This is an immediate, blocking call, intended for single-file previews.
    """
    announcement = crud.announcement.get(db, id=announcement_id)
    if not announcement:
        raise HTTPException(status_code=404, detail="Announcement not found")

    if not announcement.file_name:
        raise HTTPException(status_code=400, detail="Announcement has no associated file")

    logger.info(f"Starting single preview for announcement ID: {announcement.id}, file: {announcement.file_name}")

    # Call the correct, existing function from ocr_service
    try:
        ocr_preview = process_specific_pdf_preview(db=db, supabase=supabase_client, file_name=announcement.file_name)
        if not ocr_preview:
            raise HTTPException(status_code=404, detail="Could not generate OCR preview.")
        return ocr_preview
    except Exception as e:
        logger.error(f"Error during single preview for file {announcement.file_name}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")
