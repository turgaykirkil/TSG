"""
Incoming Emails API - Admin only endpoints for viewing emails received via Cloudflare webhook
"""
import logging
from typing import List, Optional
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr, Field
from uuid import UUID

from app import models
from app.api import deps
from app import crud

logger = logging.getLogger(__name__)

router = APIRouter()


class IncomingEmailOut(BaseModel):
    id: UUID
    from_address: str
    to_address: str
    subject: Optional[str] = None
    body_text: Optional[str] = None
    body_html: Optional[str] = None
    received_at: datetime
    is_read: bool
    cloudflare_message_id: Optional[str] = None
    reply_text: Optional[str] = None
    replied_at: Optional[datetime] = None
    is_outbound: bool

    class Config:
        from_attributes = True


class IncomingEmailList(BaseModel):
    items: List[IncomingEmailOut]
    total: int
    page: int
    per_page: int


@router.get("/incoming-emails", response_model=IncomingEmailList, summary="List incoming emails (admin only)")
def list_incoming_emails(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    unread_only: bool = Query(False),
    mailbox_type: str = Query("inbox"),  # "inbox" or "sent"
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    """
    List all incoming or sent emails. Admin only.
    """
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=403, detail="Admin access required")

    query = db.query(models.IncomingEmail)
    
    if mailbox_type == "sent":
        query = query.filter(models.IncomingEmail.is_outbound == True)
    else:
        query = query.filter(models.IncomingEmail.is_outbound == False)
        if unread_only:
            query = query.filter(models.IncomingEmail.is_read == False)
    
    total = query.count()
    
    items = (
        query
        .order_by(models.IncomingEmail.received_at.desc())
        .offset((page - 1) * per_page)
        .limit(per_page)
        .all()
    )

    return {
        "items": items,
        "total": total,
        "page": page,
        "per_page": per_page,
    }


@router.get("/incoming-emails/{email_id}", response_model=IncomingEmailOut, summary="Get email details")
def get_incoming_email(
    email_id: UUID,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    """
    Get specific email details. Admin only.
    """
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=403, detail="Admin access required")

    email = db.query(models.IncomingEmail).filter(models.IncomingEmail.id == email_id).first()
    
    if not email:
        raise HTTPException(status_code=404, detail="Email not found")
    
    return email


@router.patch("/incoming-emails/{email_id}/mark-read", summary="Mark email as read")
def mark_email_as_read(
    email_id: UUID,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    """
    Mark email as read. Admin only.
    """
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=403, detail="Admin access required")

    email = db.query(models.IncomingEmail).filter(models.IncomingEmail.id == email_id).first()
    
    if not email:
        raise HTTPException(status_code=404, detail="Email not found")
    
    email.is_read = True
    db.commit()
    
    return {"msg": "Email marked as read"}


@router.delete("/incoming-emails/{email_id}", summary="Delete email")
def delete_incoming_email(
    email_id: UUID,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    """
    Delete email. Admin only.
    """
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=403, detail="Admin access required")

    email = db.query(models.IncomingEmail).filter(models.IncomingEmail.id == email_id).first()
    
    if not email:
        raise HTTPException(status_code=404, detail="Email not found")
    
    db.delete(email)
    db.commit()
    
    return {"msg": "Email deleted"}


class EmailReplyRequest(BaseModel):
    message: str = Field(..., description="Reply message body")


@router.post("/incoming-emails/{email_id}/reply", summary="Reply to incoming email")
def reply_to_incoming_email(
    email_id: UUID,
    reply_in: EmailReplyRequest,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    """
    Reply to incoming email. Admin only.
    """
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=403, detail="Admin access required")

    email = db.query(models.IncomingEmail).filter(models.IncomingEmail.id == email_id).first()
    if not email:
        raise HTTPException(status_code=404, detail="Email not found")

    from app.services.email_service import send_email
    
    subject = f"Re: {email.subject}" if email.subject else "Sicilius Yanıtı"
    
    try:
        send_email(
            db=db,
            to=email.from_address,
            subject=subject,
            body_text=reply_in.message,
            body_html=f"<div style='font-family: sans-serif; line-height: 1.6;'>{reply_in.message.replace(chr(10), '<br>')}</div>",
            from_email=email.to_address
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"E-posta gönderilemedi: {e}")

    email.is_read = True
    email.reply_text = reply_in.message
    email.replied_at = datetime.utcnow()
    
    # Save the reply as a separate outbound email record so it appears in the Sent box
    reply_email = models.IncomingEmail(
        from_address=email.to_address,
        to_address=email.from_address,
        subject=subject,
        body_text=reply_in.message,
        body_html=f"<div style='font-family: sans-serif; line-height: 1.6;'>{reply_in.message.replace(chr(10), '<br>')}</div>",
        is_read=True,
        is_outbound=True
    )
    db.add(reply_email)
    db.commit()

    return {"msg": "Reply sent successfully"}


class OutboundEmailSendRequest(BaseModel):
    to_address: EmailStr
    subject: str = Field(..., min_length=1)
    body: str = Field(..., min_length=1)
    from_address: Optional[EmailStr] = None


@router.post("/incoming-emails/send", summary="Send outbound email")
def send_outbound_email(
    req: OutboundEmailSendRequest,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    """
    Send outbound email. Admin only.
    Stores the sent email in the database as an outbound mail record.
    """
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=403, detail="Admin access required")

    from app.services.email_service import send_email, _get_email_settings
    
    settings = _get_email_settings(db)
    if not settings:
        raise HTTPException(status_code=400, detail="E-posta ayarları yapılandırılmamış")
        
    from_email = req.from_address or settings.get("from_email")
    if not from_email:
        raise HTTPException(status_code=400, detail="Gönderen e-posta adresi yapılandırılmamış")

    # Send email
    try:
        send_email(
            db=db,
            to=req.to_address,
            subject=req.subject,
            body_text=req.body,
            body_html=f"<div style='font-family: sans-serif; line-height: 1.6;'>{req.body.replace(chr(10), '<br>')}</div>",
            from_email=from_email
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"E-posta gönderilemedi: {e}")

    # Save to DB
    new_email = models.IncomingEmail(
        from_address=from_email,
        to_address=req.to_address,
        subject=req.subject,
        body_text=req.body,
        body_html=f"<div style='font-family: sans-serif; line-height: 1.6;'>{req.body.replace(chr(10), '<br>')}</div>",
        is_read=True,
        is_outbound=True
    )
    db.add(new_email)
    db.commit()

    return {"msg": "Email sent successfully"}
