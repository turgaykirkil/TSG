from fastapi import APIRouter, File, UploadFile, HTTPException, status
from fastapi.responses import JSONResponse
import os
import uuid
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

from app.services.file_service import save_uploaded_file, validate_file_type

router = APIRouter()

class FileUploadResponse(BaseModel):
    filename: str
    size: int
    content_type: str
    saved_path: str

@router.post("/", response_model=FileUploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_file(
    file: UploadFile = File(...),
    upload_type: str = "document"
):
    """
    Upload a file to the server.
    
    Accepts PDF and Excel files. Saves the file to the uploads directory
    and returns file metadata.
    """
    # Validate file type
    if not validate_file_type(file.filename, file.content_type):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF and Excel files are allowed"
        )
    
    try:
        # Save the file
        saved_path = save_uploaded_file(file)
        
        # Get file stats
        file_size = os.path.getsize(saved_path)
        
        return {
            "filename": file.filename,
            "size": file_size,
            "content_type": file.content_type or "application/octet-stream",
            "saved_path": saved_path
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error uploading file: {str(e)}"
        )
