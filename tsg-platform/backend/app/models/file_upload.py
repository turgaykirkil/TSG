from sqlalchemy import Column, String, Integer, ForeignKey, Enum, Text, DateTime, Boolean, JSON
from sqlalchemy.orm import relationship

from app.models.base import Base
import enum

class FileUploadStatus(str, enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class FileUploadType(str, enum.Enum):
    GAZETTE_PDF = "gazette_pdf"
    COMPANY_DATA = "company_data"
    PERSON_DATA = "person_data"
    OTHER = "other"

class FileUpload(Base):
    __tablename__ = "file_uploads"
    
    # File Information
    file_name = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_size = Column(Integer)  # in bytes
    file_type = Column(String(50))
    mime_type = Column(String(100))
    
    # Upload Information
    upload_type = Column(Enum(FileUploadType), nullable=False, default=FileUploadType.OTHER)
    status = Column(Enum(FileUploadStatus), default=FileUploadStatus.PENDING, index=True)
    
    # Processing Information
    processed_at = Column(DateTime)
    processed_records = Column(Integer, default=0)
    failed_records = Column(Integer, default=0)
    error_message = Column(Text)
    
    # File Metadata
    file_metadata = Column(JSON)  # For storing any additional metadata
    
    # Relationships
    uploaded_by_id = Column(Integer, ForeignKey("users.id"), index=True)
    uploaded_by = relationship("User", back_populates="file_uploads")
    
    # Job History
    job_histories = relationship("JobHistory", back_populates="file_upload")
    
    def __repr__(self):
        return f"<FileUpload {self.file_name} ({self.status})>"
    
    @property
    def is_completed(self):
        return self.status == FileUploadStatus.COMPLETED
    
    @property
    def is_failed(self):
        return self.status == FileUploadStatus.FAILED
    
    def to_dict(self):
        result = super().to_dict()
        # Convert datetime to string for JSON serialization
        if 'processed_at' in result and result['processed_at']:
            result['processed_at'] = result['processed_at'].isoformat()
        return result
