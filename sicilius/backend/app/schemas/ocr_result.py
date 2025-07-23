from pydantic import BaseModel, Field
from typing import Optional, Any
from datetime import datetime
from uuid import UUID

# Properties to receive on item creation
class OcrResultCreate(BaseModel):
    announcement_id: UUID

# Properties to receive on item update
class OcrResultUpdate(BaseModel):
    raw_text: Optional[str] = None
    structured_data: Optional[Any] = None
    status: Optional[str] = None

# Properties shared by models stored in DB
class OcrResultInDBBase(BaseModel):
    id: int
    announcement_id: UUID
    raw_text: Optional[str] = None
    structured_data: Optional[Any] = None
    status: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True

# Properties to return to client
class OcrResult(OcrResultInDBBase):
    pass


class OcrBatchRequest(BaseModel):
    limit: int = Field(10, gt=0, le=100, description="Number of announcements to process in a batch.")


# Properties stored in DB
class OcrResultInDB(OcrResultInDBBase):
    pass
