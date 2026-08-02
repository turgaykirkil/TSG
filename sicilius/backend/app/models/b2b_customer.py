import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.session import Base

class B2BCustomer(Base):
    __tablename__ = "b2b_customers"
    __table_args__ = {"schema": "app"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False)
    tax_number = Column(String(20), nullable=False, unique=True)
    contact_email = Column(String(255), nullable=False)
    package_name = Column(String(50), nullable=False, default="Pro")
    monthly_quota = Column(Integer, nullable=False, default=15000)
    used_quota = Column(Integer, nullable=False, default=0)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    api_keys = relationship("APIKey", back_populates="customer", cascade="all, delete-orphan")


class APIKey(Base):
    __tablename__ = "api_keys"
    __table_args__ = {"schema": "app"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("app.b2b_customers.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(100), nullable=False, default="Live Key")
    key_prefix = Column(String(50), nullable=False)
    hashed_key = Column(String(255), nullable=False)
    key_type = Column(String(20), nullable=False, default="live")
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    expires_at = Column(DateTime(timezone=True), nullable=True)

    customer = relationship("B2BCustomer", back_populates="api_keys")
