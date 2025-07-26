from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, status, File, UploadFile
from sqlalchemy.orm import Session
from uuid import UUID

from app import crud, models, schemas
from app.services import ocr_service
from app.api import deps
from supabase.client import Client
from typing import List
from supabase.client import Client
from typing import List

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
        # Note: We are using the new Surya-based service function
        return ocr_service.get_surya_ocr_preview(
            pdf_content=pdf_content, file_name=file.filename
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate OCR technical preview: {str(e)}"
        )


# The list-pdfs endpoint is temporarily disabled as we are switching to local file upload
@router.get("/list-pdfs", response_model=List[schemas.FileNameRequest], include_in_schema=False)
def list_available_pdfs(
    supabase: Client = Depends(deps.get_supabase_client)
):
    """
    List all available PDFs in the 'gazette-pdfs' storage bucket.
    """
    try:
        files = supabase.storage.from_("gazette-pdfs").list()
        # Filter out any non-PDF files or system files like .emptyFolderPlaceholder
        pdf_files = [schemas.FileNameRequest(file_name=file['name']) for file in files if file['name'].lower().endswith('.pdf')]
        return pdf_files
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Could not list files from Supabase Storage: {e}"
        )

