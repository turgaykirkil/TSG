from sqlalchemy import Column, Date, Integer, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.db.base import Base

class DailyUsage(Base):
    __tablename__ = "daily_usages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    day = Column(Date, nullable=False, index=True)
    count = Column(Integer, nullable=False, default=0)

    __table_args__ = (
        UniqueConstraint('user_id', 'day', name='uq_daily_usage_user_day'),
    )
