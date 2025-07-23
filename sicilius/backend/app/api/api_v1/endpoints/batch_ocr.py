import logging
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, status
from sqlalchemy.orm import Session

import base64
from io import BytesIO
from PIL import Image
import requests
from tempfile import NamedTemporaryFile

from app import crud, models, schemas, services
from pdf2image import convert_from_bytes
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

@router.post("/process-and-preview", response_model=list[schemas.OcrPreviewResponse])
def process_and_preview_batch(
    *,
    db: Session = Depends(deps.get_db),
    batch_input: schemas.OcrBatchRequest,
    current_user: models.User = Depends(deps.get_current_active_user),
):
    """
    Process a batch of announcements for OCR and return the results for preview without saving.
    """
    announcements_to_process = crud.announcement.get_multi_without_ocr_results(db, limit=batch_input.limit)

    if not announcements_to_process:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No new announcements found to process."
        )

    results = []
    for ann in announcements_to_process:
        if not ann.pdf_url:
            continue

        try:
            logger.info(f"Processing for preview: {ann.id}")
            response = requests.get(ann.pdf_url, stream=True)
            response.raise_for_status()

            with NamedTemporaryFile(delete=True, suffix=".pdf") as temp_pdf:
                temp_pdf.write(response.content)
                temp_pdf.flush()

                # Perform OCR
                ocr_output = services.ocr_service.process_pdf_with_surya(temp_pdf.name)
                raw_text = "\n".join([line['text'] for page in ocr_output for line in page['text_lines']])

                # Convert first page to image
                images = convert_from_bytes(response.content, first_page=1, last_page=1)
                if images:
                    buffered = BytesIO()
                    images[0].save(buffered, format="JPEG")
                    img_str = base64.b64encode(buffered.getvalue()).decode()
                else:
                    img_str = None

            results.append(
                schemas.OcrPreviewResponse(
                    announcement_id=str(ann.id),
                    ocr_text=raw_text,
                    pdf_image_base64=img_str
                )
            )

        except Exception as e:
            logger.error(f"Failed to process announcement {ann.id} for preview: {e}")
            # Optionally, you can add a result with an error message
            results.append(
                schemas.OcrPreviewResponse(
                    announcement_id=str(ann.id),
                    ocr_text=f"Error: {e}",
                    pdf_image_base64=None
                )
            )

    return results
