from typing import Optional
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel
from app.models.company_error import ErrorStatus

class CompanyErrorBase(BaseModel):
    description: str

class CompanyErrorCreate(CompanyErrorBase):
    company_id: UUID

class CompanyErrorUpdate(BaseModel):
    status: Optional[ErrorStatus] = None
    resolved_at: Optional[datetime] = None

class CompanyErrorInDB(CompanyErrorBase):
    id: UUID
    company_id: UUID
    user_id: UUID
    status: str
    created_at: datetime
    resolved_at: Optional[datetime] = None

    class Config:
        from_attributes = True  # Pydantic V2

class CompanyError(CompanyErrorInDB):
    company_name: Optional[str] = None

