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
    markdown_content: Optional[str] = None
    json_payload: Optional[Any] = None
    processing_time: Optional[float] = None
    pdf_page_count: Optional[int] = None
    status: str
    
    # Matching OcrResult model columns
    publication_date: Optional[datetime] = None
    issue_number: Optional[int] = None
    page_number: Optional[int] = None
    pdf_url: Optional[str] = None
    sicil_office_header: Optional[str] = None
    sicil_dosya_no: Optional[str] = None
    mersis_no: Optional[str] = None
    trade_name: Optional[str] = None
    old_trade_name: Optional[str] = None
    addresses: Optional[Any] = None
    old_addresses: Optional[Any] = None
    persons: Optional[Any] = None
    masked_ids: Optional[Any] = None
    hususlar: Optional[Any] = None
    belgeler: Optional[str] = None
    type: Optional[str] = None
    ilan_sira_no: Optional[Any] = None
    
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
