"""
Cloudflare Email Routing Webhook - Receives incoming emails
"""
import logging
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr, Field

from app import models
from app.api import deps
from app.core.config import settings
from app.core.rate_limit import limiter
import hmac
import hashlib

logger = logging.getLogger(__name__)

router = APIRouter()


class CloudflareEmailPayload(BaseModel):
    """
    Simplified Cloudflare Email Routing webhook payload.
    Actual payload may have more fields - adapt as needed.
    """
    from_: EmailStr = Field(alias='from')
    to: EmailStr
    subject: Optional[str] = None
    text: Optional[str] = None  # Plain text body
    html: Optional[str] = None  # HTML body
    message_id: Optional[str] = None  # Cloudflare message ID

    class Config:
        populate_by_name = True


import email
from email import policy

def extract_clean_content(raw_text: Optional[str]) -> tuple[Optional[str], Optional[str]]:
    """
    Parses raw MIME/RFC822 email text and returns clean (plain_text, html_text).
    Strips away all server headers (Received, DKIM, ARC-Seal, Proofpoint, etc.).
    """
    if not raw_text:
        return None, None

    # If it contains raw email headers
    if any(h in raw_text for h in ["Received:", "DKIM-Signature:", "Content-Type:", "ARC-Seal:"]):
        try:
            msg = email.message_from_string(raw_text, policy=policy.default)
            
            clean_text = None
            clean_html = None

            # Extract plain text body
            body_plain = msg.get_body(preferencelist=('plain',))
            if body_plain:
                clean_text = body_plain.get_content()

            # Extract HTML body
            body_html_part = msg.get_body(preferencelist=('html',))
            if body_html_part:
                clean_html = body_html_part.get_content()

            if clean_text or clean_html:
                return clean_text or clean_html, clean_html
        except Exception as err:
            logger.warning(f"Failed to parse raw MIME email: {err}")

    return raw_text, None


@router.post("/webhooks/cloudflare-email", summary="Cloudflare Email Routing webhook")
@limiter.limit("30/minute")  # Max 30 webhooks per minute per IP
async def cloudflare_email_webhook(
    request: Request,
    db: Session = Depends(deps.get_db),
):
    """
    Receives incoming emails from Cloudflare Email Routing.
    Stores them in the database for admin inbox viewing.
    
    Optional HMAC signature validation via TSG_CLOUDFLARE_WEBHOOK_SECRET env var.
    """
    # Optional: Verify webhook signature if secret is configured
    if settings.CLOUDFLARE_WEBHOOK_SECRET:
        signature = request.headers.get("X-Cloudflare-Signature")
        if not signature:
            logger.warning("Cloudflare webhook: missing signature header")
            raise HTTPException(status_code=403, detail="Missing signature")
        
        # Verify HMAC
        body_bytes = await request.body()
        expected_sig = hmac.new(
            settings.CLOUDFLARE_WEBHOOK_SECRET.encode(),
            body_bytes,
            hashlib.sha256
        ).hexdigest()
        
        if not hmac.compare_digest(signature, expected_sig):
            logger.warning("Cloudflare webhook: invalid signature")
            raise HTTPException(status_code=403, detail="Invalid signature")
    
    try:
        # Parse JSON body
        body = await request.json()
        logger.info(f"Cloudflare webhook received: {body}")

        # Extract fields (Cloudflare format may vary - adjust as needed)
        from_address = body.get("from") or body.get("sender")
        to_address = body.get("to") or body.get("recipient")
        subject = body.get("subject", "")
        raw_text = body.get("text") or body.get("body_text") or body.get("plain_text")
        body_html = body.get("html") or body.get("body_html")
        message_id = body.get("message_id") or body.get("id")

        if not from_address or not to_address:
            raise HTTPException(status_code=400, detail="Missing required fields: from/to")

        # Parse & clean technical headers if raw email was sent
        clean_text, clean_html = extract_clean_content(raw_text)
        if clean_text:
            body_text = clean_text
        else:
            body_text = raw_text

        if clean_html and not body_html:
            body_html = clean_html

        # Create incoming email record
        incoming_email = models.IncomingEmail(
            from_address=str(from_address),
            to_address=str(to_address),
            subject=subject,
            body_text=body_text,
            body_html=body_html,
            cloudflare_message_id=message_id,
            is_read=False,
        )
        
        db.add(incoming_email)
        db.commit()
        db.refresh(incoming_email)

        logger.info(f"Incoming email saved: {incoming_email.id} from={from_address}")

        return {"status": "ok", "email_id": str(incoming_email.id)}

    except Exception as e:
        logger.error(f"Cloudflare webhook error: {e}", exc_info=True)
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to process email: {str(e)}")
