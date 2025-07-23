from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, status
from sqlalchemy.orm import Session
from uuid import UUID

from app import crud, schemas, services
from app.api import deps

router = APIRouter()

@router.post("/process/{announcement_id}", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.OcrResult)
def start_ocr_processing(
    announcement_id: UUID,
    db: Session = Depends(deps.get_db),
    background_tasks: BackgroundTasks = BackgroundTasks()
):
    """
    Start OCR processing for a given announcement.
    """
    announcement = crud.announcement.get(db, id=announcement_id)
    if not announcement:
        raise HTTPException(status_code=404, detail="Announcement not found")

    if announcement.ocr_result:
        raise HTTPException(
            status_code=400,
            detail=f"OCR process already exists for this announcement with status: {announcement.ocr_result.status}"
        )

    # Create an initial OCR result entry
    ocr_result_in = schemas.OcrResultCreate(announcement_id=announcement_id)
    ocr_result = crud.ocr_result.create(db=db, obj_in=ocr_result_in)

    # Add the heavy processing to the background
    background_tasks.add_task(services.ocr_service.process_pdf_for_ocr, db=db, announcement_id=announcement_id)

    return ocr_result

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
