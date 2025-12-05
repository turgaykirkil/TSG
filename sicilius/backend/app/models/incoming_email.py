from sqlalchemy import Column, String, Text, Boolean, DateTime, UUID
from sqlalchemy.sql import func
import uuid

from app.db.base import Base


class IncomingEmail(Base):
    """
    Model for storing incoming emails received via Cloudflare Email Routing webhook.
    Displayed in admin panel inbox.
    """
    __tablename__ = "incoming_emails"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    from_address = Column(String(255), nullable=False, index=True)
    to_address = Column(String(255), nullable=False, index=True)
    subject = Column(String(500), nullable=True)
    body_text = Column(Text, nullable=True)
    body_html = Column(Text, nullable=True)
    received_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)
    is_read = Column(Boolean, default=False, nullable=False, index=True)
    cloudflare_message_id = Column(String(255), nullable=True, index=True)

    def __repr__(self):
        return f"<IncomingEmail {self.id} from={self.from_address} subject={self.subject[:50]}>"
