"""
File handling utilities
"""
import os
import shutil
import uuid
import mimetypes
try:
    import magic  # type: ignore
except ImportError:  # pragma: no cover - optional dependency may be missing
    magic = None
from pathlib import Path
from typing import Optional, List, Tuple
from fastapi import UploadFile, HTTPException

from app.core.config import settings

def get_file_extension(filename: str) -> str:
    """Get file extension from filename."""
    return Path(filename).suffix.lower()

def validate_file_type(filename: str, allowed_extensions: List[str]) -> bool:
    """Check if file has an allowed extension."""
    return get_file_extension(filename) in allowed_extensions

async def save_upload_file(upload_file: UploadFile, sub_dir: str = "") -> str:
    """
    Save an uploaded file to the uploads directory.
    
    Args:
        upload_file: The uploaded file
        sub_dir: Subdirectory under UPLOAD_FOLDER to save the file
        
    Returns:
        str: Relative path to the saved file
    """
    # Create a unique filename to prevent overwriting
    file_ext = get_file_extension(upload_file.filename)
    unique_filename = f"{uuid.uuid4().hex}{file_ext}"
    
    # Create the directory if it doesn't exist
    upload_dir = Path(settings.UPLOAD_FOLDER) / sub_dir
    upload_dir.mkdir(parents=True, exist_ok=True)
    
    # Save the file
    file_path = upload_dir / unique_filename
    
    # Read the file in chunks to handle large files
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)
    
    # Return the relative path from the upload folder
    return str(Path(sub_dir) / unique_filename)

def delete_file(file_path: str) -> bool:
    """
    Delete a file if it exists.
    
    Args:
        file_path: Path to the file to delete (relative to UPLOAD_FOLDER)
        
    Returns:
        bool: True if file was deleted, False if it didn't exist
    """
    full_path = Path(settings.UPLOAD_FOLDER) / file_path
    try:
        full_path.unlink()
        return True
    except FileNotFoundError:
        return False

def get_file_mime_type(file_path: str) -> str:
    """
    Get the MIME type of a file.

    Args:
        file_path: Path to the file

    Returns:
        str: MIME type
    """
    if magic is None:
        guess, _ = mimetypes.guess_type(str(file_path))
        return guess or ""

    mime = magic.Magic(mime=True)
    return mime.from_file(str(file_path))

def get_file_size(file_path: str) -> int:
    """
    Get the size of a file in bytes.
    
    Args:
        file_path: Path to the file
        
    Returns:
        int: File size in bytes
    """
    return Path(file_path).stat().st_size

def ensure_directory_exists(directory: str) -> None:
    """
    Ensure that a directory exists, create it if it doesn't.
    
    Args:
        directory: Path to the directory
    """
    Path(directory).mkdir(parents=True, exist_ok=True)

def get_relative_path(full_path: str) -> str:
    """
    Convert an absolute path to a path relative to UPLOAD_FOLDER.
    
    Args:
        full_path: Absolute path to the file
        
    Returns:
        str: Relative path from UPLOAD_FOLDER
    """
    full_path = Path(full_path).resolve()
    upload_path = Path(settings.UPLOAD_FOLDER).resolve()
    
    try:
        return str(full_path.relative_to(upload_path))
    except ValueError:
        # If the path is not under UPLOAD_FOLDER, return it as is
        return str(full_path)

async def validate_upload_file(
    file: UploadFile, 
    allowed_extensions: List[str], 
    max_size_mb: int = 10
) -> Tuple[str, str]:
    """
    Validate an uploaded file.
    
    Args:
        file: The uploaded file
        allowed_extensions: List of allowed file extensions (e.g., ['.pdf', '.jpg'])
        max_size_mb: Maximum file size in MB
        
    Returns:
        Tuple of (file_extension, mime_type)
        
    Raises:
        HTTPException: If validation fails
    """
    # Check file extension
    file_ext = get_file_extension(file.filename)
    if not validate_file_type(file.filename, allowed_extensions):
        raise HTTPException(
            status_code=400,
            detail=f"File type not allowed. Allowed types: {', '.join(allowed_extensions)}"
        )
    
    # Check file size
    max_size = max_size_mb * 1024 * 1024  # Convert MB to bytes
    
    # Read first chunk to check MIME type
    chunk = await file.read(1024)
    if not chunk:
        raise HTTPException(status_code=400, detail="Empty file")
    
    # Check MIME type
    if magic is not None:
        mime = magic.Magic(mime=True)
        mime_type = mime.from_buffer(chunk)
    else:
        guess, _ = mimetypes.guess_type(file.filename)
        mime_type = guess or ""
    
    # Reset file pointer
    await file.seek(0)
    
    # Check file size by reading the whole file (for async uploads)
    file_size = 0
    while chunk := await file.read(8192):  # 8KB chunks
        file_size += len(chunk)
        if file_size > max_size:
            raise HTTPException(
                status_code=400,
                detail=f"File too large. Maximum size is {max_size_mb}MB"
            )
    
    # Reset file pointer again
    await file.seek(0)
    
    return file_ext, mime_type
