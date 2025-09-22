from sqlalchemy import Column, String, DateTime, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid

from app.db.base import Base


class UserInvite(Base):
    __tablename__ = "user_invites"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    inviter_user_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    invited_email = Column(String(255), nullable=False, index=True)
    invited_month_key = Column(String(7), nullable=False, index=True)  # YYYY-MM
    token = Column(String(128), nullable=False, unique=True, index=True)
    accepted_at = Column(DateTime(timezone=True), nullable=True)

    __table_args__ = (
        UniqueConstraint('inviter_user_id', 'invited_month_key', name='uq_invite_inviter_month'),
    )
