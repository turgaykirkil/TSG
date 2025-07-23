from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base

class OcrResult(Base):
    __tablename__ = "ocr_results"

    id = Column(Integer, primary_key=True, index=True)
    announcement_id = Column(UUID(as_uuid=True), ForeignKey("announcements.id"), unique=True, nullable=False, index=True)
    
    raw_text = Column(Text, nullable=True)
    structured_data = Column(JSON, nullable=True) # To store words, bounding boxes, confidence, etc.
    status = Column(String, nullable=False, default='pending') # pending, processing, completed, failed

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    announcement = relationship("Announcement", back_populates="ocr_result")
