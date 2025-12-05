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
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    """
    List all incoming emails. Admin only.
    """
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=403, detail="Admin access required")

    query = db.query(models.IncomingEmail)
    
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
