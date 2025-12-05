from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr
from uuid import UUID


class ContactMessageBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    subject: str
    message: str


class ContactMessageCreate(ContactMessageBase):
    pass


class ContactMessage(ContactMessageBase):
    id: UUID
    created_at: datetime
    read: str = "UNREAD"
    
    class Config:
        from_attributes = True
