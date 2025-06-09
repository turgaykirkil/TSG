import os
import uuid
from typing import Optional
from fastapi import UploadFile

def save_uploaded_file(file: UploadFile, upload_dir: str = "/app/data/uploads") -> str:
    """
    Save uploaded file to the specified directory with a unique filename.
    
    Args:
        file: The uploaded file object
        upload_dir: Directory to save the file (default: /app/data/uploads)
        
    Returns:
        str: Path to the saved file
    """
    os.makedirs(upload_dir, exist_ok=True)
    
    # Generate a unique filename
    file_ext = os.path.splitext(file.filename)[1] if file.filename else ''
    file_name = f"{uuid.uuid4()}{file_ext}"
    file_path = os.path.join(upload_dir, file_name)
    
    # Save the file
    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())
    
    return file_path

def validate_file_type(filename: Optional[str], content_type: Optional[str]) -> bool:
    """
    Validate if the file type is allowed.
    
    Args:
        filename: Name of the file
        content_type: MIME type of the file
        
    Returns:
        bool: True if file type is allowed, False otherwise
    """
    if not filename:
        return False
        
    allowed_extensions = {'.pdf', '.xlsx', '.xls'}
    allowed_mime_types = {
        'application/pdf',
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'application/vnd.ms-excel'
    }
    
    _, ext = os.path.splitext(filename.lower())
    return ext in allowed_extensions and (not content_type or content_type in allowed_mime_types)
