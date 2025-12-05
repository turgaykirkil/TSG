from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.contact_message import ContactMessage
from app.schemas.contact_message import ContactMessageCreate


def create_contact_message(db: Session, message: ContactMessageCreate) -> ContactMessage:
    """Create a new contact message"""
    db_message = ContactMessage(
        first_name=message.first_name,
        last_name=message.last_name,
        email=message.email,
        subject=message.subject,
        message=message.message,
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message


def get_contact_messages(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    unread_only: bool = False
) -> List[ContactMessage]:
    """Get all contact messages"""
    query = db.query(ContactMessage)
    if unread_only:
        query = query.filter(ContactMessage.read == "UNREAD")
    return query.order_by(ContactMessage.created_at.desc()).offset(skip).limit(limit).all()


def mark_as_read(db: Session, message_id: str) -> Optional[ContactMessage]:
    """Mark contact message as read"""
    message = db.query(ContactMessage).filter(ContactMessage.id == message_id).first()
    if message:
        message.read = "READ"
        db.commit()
        db.refresh(message)
    return message
