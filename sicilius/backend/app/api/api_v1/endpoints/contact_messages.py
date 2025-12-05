from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.api import deps
from app.schemas.contact_message import ContactMessage, ContactMessageCreate
from app.crud import crud_contact_message
from app.services.email_service import send_contact_notification
from app.core.config import settings

router = APIRouter()


@router.post("/", response_model=ContactMessage, status_code=201)
def submit_contact_form(
    *,
    db: Session = Depends(deps.get_db),
    message_in: ContactMessageCreate,
) -> ContactMessage:
    """
    Submit a contact form message.
    Saves to database and sends email notification to info@sicilius.com.tr
    """
    # Save to database
    message = crud_contact_message.create_contact_message(db, message_in)
    
    # Send email notification
    try:
        send_contact_notification(
            db=db,
            to_email=settings.CONTACT_EMAIL or "info@sicilius.com.tr",
            first_name=message_in.first_name,
            last_name=message_in.last_name,
            email=message_in.email,
            subject=message_in.subject,
            message=message_in.message,
        )
    except Exception as e:
        # Log error but don't fail the request
        print(f"Failed to send contact email: {e}")
    
    return message


@router.get("/", response_model=List[ContactMessage])
def get_contact_messages(
    *,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_active_superuser),
    skip: int = 0,
    limit: int = 100,
    unread_only: bool = False,
) -> List[ContactMessage]:
    """
    Get all contact messages (admin only).
    """
    return crud_contact_message.get_contact_messages(db, skip=skip, limit=limit, unread_only=unread_only)


@router.patch("/{message_id}/read", response_model=ContactMessage)
def mark_message_as_read(
    *,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_active_superuser),
    message_id: str,
) -> ContactMessage:
    """
    Mark a contact message as read (admin only).
    """
    message = crud_contact_message.mark_as_read(db, message_id)
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    return message
