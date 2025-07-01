from sqlalchemy import Column, String, Integer, ForeignKey, Enum, Text, DateTime, JSON, Index
from sqlalchemy.orm import relationship

from app.models.base import Base
import enum

class JobType(str, enum.Enum):
    FILE_UPLOAD = "file_upload"
    OCR_PROCESSING = "ocr_processing"
    DATA_IMPORT = "data_import"
    DATA_EXPORT = "data_export"
    REPORT_GENERATION = "report_generation"
    SYSTEM_MAINTENANCE = "system_maintenance"
    OTHER = "other"

class JobStatus(str, enum.Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class JobHistory(Base):
    __tablename__ = "job_histories"
    
    # Job Information
    job_type = Column(Enum(JobType), nullable=False, index=True)
    job_name = Column(String(255), nullable=False, index=True)
    description = Column(Text)
    
    # Status Information
    status = Column(Enum(JobStatus), default=JobStatus.PENDING, index=True)
    progress = Column(Integer, default=0)  # 0-100
    
    # Timing Information
    started_at = Column(DateTime, index=True)
    completed_at = Column(DateTime)
    
    # Results
    result_summary = Column(JSON)  # Örn: {"processed": 10, "succeeded": 9, "failed": 1}
    error_message = Column(Text)
    stack_trace = Column(Text)
    
    # Relationships
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    user = relationship("User", back_populates="job_histories")
    
    file_upload_id = Column(Integer, ForeignKey("file_uploads.id"), index=True)
    file_upload = relationship("FileUpload", back_populates="job_histories")
    
    # Additional Context
    parameters = Column(JSON)  # Job parametreleri
    
    # Indexes
    __table_args__ = (
        Index('idx_job_type_status', 'job_type', 'status'),
        Index('idx_job_dates', 'started_at', 'completed_at'),
    )
    
    def __repr__(self):
        return f"<JobHistory {self.job_name} ({self.status})>"
    
    @property
    def duration_seconds(self):
        if not self.started_at:
            return None
        end_time = self.completed_at or datetime.utcnow()
        return (end_time - self.started_at).total_seconds()
    
    def to_dict(self):
        result = super().to_dict()
        # Convert datetime to string for JSON serialization
        if 'started_at' in result and result['started_at']:
            result['started_at'] = result['started_at'].isoformat()
        if 'completed_at' in result and result['completed_at']:
            result['completed_at'] = result['completed_at'].isoformat()
        # Add duration if job has started
        if 'started_at' in result and result['started_at']:
            result['duration_seconds'] = self.duration_seconds
        return result
