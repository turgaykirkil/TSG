import os
import uuid
from typing import Optional
from fastapi import UploadFile
from app.core.config import settings

def save_uploaded_file(file: UploadFile) -> str:
    """
    Save uploaded file to the directory specified in settings.
    
    Args:
        file: The uploaded file object
        
    Returns:
        str: Path to the saved file
    """
    upload_dir = settings.UPLOAD_FOLDER
    os.makedirs(upload_dir, exist_ok=True)
    
    # Generate a unique filename
    file_ext = os.path.splitext(file.filename)[1] if file.filename else ''
    file_name = f"{uuid.uuid4()}{file_ext}"
    file_path = os.path.join(upload_dir, file_name)
    
    # Save the file
    with open(file_path, "wb") as buffer:
        content = file.file.read()
        buffer.write(content)
    
    return file_path

def validate_file_type(filename: Optional[str], content_type: Optional[str]) -> bool:
    """
    Validate if the file type is allowed based on settings.
    
    Args:
        filename: Name of the file
        content_type: MIME type of the file (currently not used for validation)
        
    Returns:
        bool: True if file type is allowed, False otherwise
    """
    if not filename:
        return False
        
    # Parse allowed extensions from settings string (e.g., "pdf,jpg,png")
    # and format them with a leading dot (e.g., {'.pdf', '.jpg', '.png'})
    allowed_extensions = {f".{ext.strip().lower()}" for ext in settings.ALLOWED_EXTENSIONS.split(',')}
    
    _, ext = os.path.splitext(filename.lower())
    
    return ext in allowed_extensions
