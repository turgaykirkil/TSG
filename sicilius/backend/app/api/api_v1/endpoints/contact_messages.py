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
    # Save to database (ContactMessage table)
    message = crud_contact_message.create_contact_message(db, message_in)
    
    # Save to Mailbox (incoming_emails table) so it appears in Mailbox Inbox
    from app import models
    incoming_email = models.IncomingEmail(
        from_address=f"{message_in.first_name} {message_in.last_name} <{message_in.email}>",
        to_address="iletisim@sicilius.com.tr",
        subject=f"İletişim Formu: {message_in.subject or 'Konu Belirtilmemiş'}",
        body_text=message_in.message,
        is_outbound=False,
        is_read=False
    )
    db.add(incoming_email)
    db.commit()
    db.refresh(incoming_email)
    
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


from pydantic import BaseModel, Field

class ReplyRequest(BaseModel):
    message: str = Field(..., description="Reply message body")


@router.post("/{message_id}/reply", status_code=200)
def reply_to_contact_message(
    *,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_active_superuser),
    message_id: str,
    reply_in: ReplyRequest,
) -> dict:
    """
    Reply to a contact message.
    Sends an email using the email service and marks the message as read.
    """
    from app.services.email_service import send_email
    from app.models.contact_message import ContactMessage as ContactMessageModel
    from app import models
    
    # Retrieve the contact message
    message = db.query(ContactMessageModel).filter(ContactMessageModel.id == message_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
        
    subject = f"Re: {message.subject}" if message.subject else "Sicilius İletişim Yanıtı"
    
    # Send email
    try:
        send_email(
            db=db,
            to=message.email,
            subject=subject,
            body_text=reply_in.message,
            body_html=f"<div style='font-family: sans-serif; line-height: 1.6;'>{reply_in.message.replace(chr(10), '<br>')}</div>",
            from_email="iletisim@sicilius.com.tr"
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"E-posta gönderilemedi: {e}")
        
    # Mark as read and save reply in contact message table
    from datetime import datetime
    message.read = "READ"
    message.reply_text = reply_in.message
    message.replied_at = datetime.utcnow()
    db.add(message)
    
    # Save to Mailbox (incoming_emails table) as an outbound record so it appears in Mailbox Sent folder
    outbound_email = models.IncomingEmail(
        from_address="iletisim@sicilius.com.tr",
        to_address=message.email,
        subject=subject,
        body_text=reply_in.message,
        body_html=f"<div style='font-family: sans-serif; line-height: 1.6;'>{reply_in.message.replace(chr(10), '<br>')}</div>",
        is_read=True,
        is_outbound=True
    )
    db.add(outbound_email)
    db.commit()
    
    return {"msg": "Reply sent successfully"}
