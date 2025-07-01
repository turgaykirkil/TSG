from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
from app.models.job_history import JobType, JobStatus

# Shared properties
class JobHistoryBase(BaseModel):
    job_type: Optional[JobType] = None
    job_name: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    status: Optional[JobStatus] = JobStatus.PENDING
    progress: Optional[int] = Field(0, ge=0, le=100)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    result_summary: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    stack_trace: Optional[str] = None
    user_id: Optional[int] = None
    file_upload_id: Optional[int] = None
    parameters: Optional[Dict[str, Any]] = None

# Properties to receive on job history creation
class JobHistoryCreate(JobHistoryBase):
    job_type: JobType
    job_name: str = Field(..., max_length=255)

# Properties to receive on job history update
class JobHistoryUpdate(JobHistoryBase):
    pass

# Properties shared by models stored in DB
class JobHistoryInDBBase(JobHistoryBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": 1,
                "job_type": "import",
                "job_name": "Excel Import",
                "description": "Firma verileri içe aktarılıyor",
                "status": "completed",
                "progress": 100,
                "started_at": "2023-01-01T00:00:00",
                "completed_at": "2023-01-01T00:05:00",
                "result_summary": {"imported": 10, "failed": 0},
                "user_id": 1,
                "file_upload_id": 1,
                "created_at": "2023-01-01T00:00:00",
                "updated_at": "2023-01-01T00:05:00"
            }
        }
    }

# Properties to return to client
class JobHistory(JobHistoryInDBBase):
    pass

# Properties stored in DB
class JobHistoryInDB(JobHistoryInDBBase):
    pass
