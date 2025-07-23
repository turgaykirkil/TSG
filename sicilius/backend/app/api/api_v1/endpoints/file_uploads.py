"""
File Uploads API endpoints
"""
import os
from typing import Any, List

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.core.config import settings
from app.utils.file_utils import save_upload_file, validate_file_type

router = APIRouter()

@router.get("/", response_model=List[schemas.FileUpload])
def read_file_uploads(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve file uploads with pagination.
    """
    file_uploads = crud.file_upload.get_multi(db, skip=skip, limit=limit)
    return file_uploads

@router.post("/", response_model=schemas.FileUpload, status_code=status.HTTP_201_CREATED)
async def create_file_upload(
    *,
    db: Session = Depends(deps.get_db),
    file: UploadFile = File(...),
    upload_type: str = "document",
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Upload a file.
    """
    # Validate file type
    if not validate_file_type(file.filename, file.content_type):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File type not allowed",
        )
    
    # Save file to disk
    file_path = save_upload_file(file)
    
    # Create file upload record
    file_upload_in = schemas.FileUploadCreate(
        file_name=file.filename,
        file_path=file_path,
        file_size=os.path.getsize(file_path),
        mime_type=file.content_type,
        upload_type=upload_type,
        uploaded_by_id=current_user.id,
    )
    
    file_upload = crud.file_upload.create(db, obj_in=file_upload_in)
    return file_upload

@router.get("/{file_upload_id}", response_model=schemas.FileUpload)
def read_file_upload(
    file_upload_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get a file upload by ID.
    """
    file_upload = crud.file_upload.get(db, id=file_upload_id)
    if not file_upload:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File upload not found",
        )
    return file_upload

@router.get("/{file_upload_id}/download")
async def download_file_upload(
    file_upload_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Download a file by file upload ID.
    """
    file_upload = crud.file_upload.get(db, id=file_upload_id)
    if not file_upload:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File upload not found",
        )
    
    if not os.path.exists(file_upload.file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found on disk",
        )
    
    return FileResponse(
        file_upload.file_path,
        filename=file_upload.file_name,
        media_type=file_upload.mime_type,
    )

@router.delete("/{file_upload_id}", response_model=schemas.FileUpload)
def delete_file_upload(
    *,
    db: Session = Depends(deps.get_db),
    file_upload_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete a file upload.
    """
    file_upload = crud.file_upload.get(db, id=file_upload_id)
    if not file_upload:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File upload not found",
        )
    
    # Remove file from disk if it exists
    if os.path.exists(file_upload.file_path):
        try:
            os.remove(file_upload.file_path)
        except OSError:
            pass  # File might be already deleted
    
    file_upload = crud.file_upload.remove(db, id=file_upload_id)
    return file_upload
