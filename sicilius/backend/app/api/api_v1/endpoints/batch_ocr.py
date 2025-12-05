import logging
from sqlalchemy.orm import Session

import base64
from io import BytesIO
from PIL import Image
import logging
from typing import List, Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
# from app.services.ocr_service import process_specific_pdf_preview

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/start-batch-ocr/", status_code=202)
def start_batch_ocr(
    *,
    db: Session = Depends(deps.get_db),
    announcement_ids: List[UUID],
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
        announcement = crud.announcement.get(db, id=ann_id)
        if not announcement:
            logger.warning("Announcement %s not found during batch creation step; skipping.", ann_id)
            continue
        # Prefer canonical link by company
        existing_ocr_result = crud.ocr_result.get_by_company(db, company_id=announcement.company_id)
        if not existing_ocr_result:
            # Also check legacy link just in case
            existing_ocr_result = crud.ocr_result.get_by_announcement(db, announcement_id=ann_id)

        if not existing_ocr_result:
            ocr_result_in = schemas.OcrResultCreate(
                company_id=announcement.company_id,
                announcement_id=ann_id,
            )
            crud.ocr_result.create(db=db, obj_in=ocr_result_in)
            # TODO: Add the actual OCR processing to the background tasks
            # Clean the URL by removing query parameters
            clean_pdf_url = (announcement.pdf_url or "").split('?')[0] if announcement.pdf_url else None
            # background_tasks.add_task(ocr_service.run_full_ocr, db=db, announcement_id=ann_id)
            logger.info(f"Task for announcement {ann_id} would be added here.")

    return {"message": f"OCR processing tasks initiated for {len(announcement_ids)} announcements."}


# @router.post("/batch-ocr/process-and-preview/", response_model=schemas.OcrPreviewResponse)
# def process_and_preview_single(
#     *,
#     db: Session = Depends(deps.get_db),
#     request_data: schemas.FileNameRequest,
#     current_user: models.User = Depends(deps.get_current_active_user),
# ) -> Any:
#     """
#     Process a single PDF for OCR and return a preview.
#     This is an immediate, blocking call, intended for single-file previews.
#     
#     NOTE: This endpoint is currently disabled as it requires refactoring to work with
#     local storage (MinIO) instead of Supabase storage.
#     """
#     raise HTTPException(status_code=501, detail="OCR preview endpoint is currently disabled")
