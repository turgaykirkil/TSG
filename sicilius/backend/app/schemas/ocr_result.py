from pydantic import BaseModel, Field
from typing import Optional, Any
from datetime import datetime
from uuid import UUID

# Properties to receive on item creation
class OcrResultCreate(BaseModel):
    company_id: UUID
    announcement_id: Optional[UUID] = None
    original_text: Optional[str] = None
    structured_data: Optional[Any] = None
    status: Optional[str] = None

# Properties to receive on item update
class OcrResultUpdate(BaseModel):
    original_text: Optional[str] = None
    structured_data: Optional[Any] = None
    status: Optional[str] = None

# Properties shared by models stored in DB
class OcrResultInDBBase(BaseModel):
    id: int
    company_id: UUID
    announcement_id: Optional[UUID] = None
    original_text: Optional[str] = None
    structured_data: Optional[Any] = None
    status: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Properties to return to client
class OcrResult(OcrResultInDBBase):
    pass


class OcrBatchRequest(BaseModel):
    limit: int = Field(10, gt=0, le=100, description="Number of announcements to process in a batch.")


# Properties stored in DB
class OcrResultInDB(OcrResultInDBBase):
    pass
