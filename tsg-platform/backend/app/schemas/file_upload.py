from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
from app.models.file_upload import FileUploadStatus, FileUploadType

# Shared properties
class FileUploadBase(BaseModel):
    file_name: Optional[str] = Field(None, max_length=255)
    file_path: Optional[str] = Field(None, max_length=500)
    file_size: Optional[int] = None
    file_type: Optional[str] = Field(None, max_length=50)
    mime_type: Optional[str] = Field(None, max_length=100)
    upload_type: Optional[FileUploadType] = FileUploadType.OTHER
    status: Optional[FileUploadStatus] = FileUploadStatus.PENDING
    processed_at: Optional[datetime] = None
    processed_records: Optional[int] = 0
    failed_records: Optional[int] = 0
    error_message: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    uploaded_by_id: Optional[int] = None

# Properties to receive on file upload creation
class FileUploadCreate(FileUploadBase):
    file_name: str = Field(..., max_length=255)
    file_path: str = Field(..., max_length=500)
    file_size: int
    mime_type: str = Field(..., max_length=100)
    upload_type: FileUploadType = FileUploadType.OTHER

# Properties to receive on file upload update
class FileUploadUpdate(FileUploadBase):
    pass

# Properties shared by models stored in DB
class FileUploadInDBBase(FileUploadBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": 1,
                "file_name": "example.pdf",
                "file_path": "/uploads/example.pdf",
                "file_size": 1024,
                "file_type": "pdf",
                "mime_type": "application/pdf",
                "upload_type": "document",
                "status": "completed",
                "processed_at": "2023-01-01T01:00:00",
                "processed_records": 10,
                "failed_records": 0,
                "uploaded_by_id": 1,
                "created_at": "2023-01-01T00:00:00",
                "updated_at": "2023-01-01T01:00:00"
            }
        }
    }

# Properties to return to client
class FileUpload(FileUploadInDBBase):
    pass

# Properties stored in DB
class FileUploadInDB(FileUploadInDBBase):
    pass
