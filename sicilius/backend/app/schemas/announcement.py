from pydantic import BaseModel
from typing import Optional
from datetime import date
import uuid

# Shared properties
class AnnouncementBase(BaseModel):
    trade_registry_name: Optional[str] = None
    trade_registry_number: Optional[str] = None
    title: Optional[str] = None
    publication_date: Optional[date] = None
    issue_number: Optional[int] = None
    page_number: Optional[int] = None
    announcement_type: Optional[str] = None
    pdf_url: Optional[str] = None
    company_id: uuid.UUID

# Properties to receive on item creation
class AnnouncementCreate(AnnouncementBase):
    pass

# Properties to receive on item update
class AnnouncementUpdate(AnnouncementBase):
    pass

# Properties shared by models stored in DB
class AnnouncementInDBBase(AnnouncementBase):
    id: uuid.UUID

    class Config:
        orm_mode = True

# Properties to return to client
class Announcement(AnnouncementInDBBase):
    pass

# Properties stored in DB
class AnnouncementInDB(AnnouncementInDBBase):
    pass
