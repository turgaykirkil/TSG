from sqlalchemy import Column, Float, Integer, String, Text, ForeignKey, DateTime, JSON, Boolean
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base

class OcrResult(Base):
    __tablename__ = "ocr_results"

    id = Column(Integer, primary_key=True, index=True)
    # Optional link to an announcement (legacy flow)
    announcement_id = Column(
        UUID(as_uuid=True),
        ForeignKey("announcements.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    # New required link to company (canonical owner of OCR result)
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"), nullable=False, index=True)
    
    original_text = Column(Text, nullable=True)
    # Flattened columns from DB schema
    publication_date = Column(DateTime(timezone=True), nullable=True)
    issue_number = Column(Integer, nullable=True)
    page_number = Column(Integer, nullable=True)
    pdf_url = Column(Text, nullable=True)
    pdf_page_count = Column(Integer, nullable=True)
    sicil_office_header = Column(Text, nullable=True)
    sicil_dosya_no = Column(Text, nullable=True)
    mersis_no = Column(Text, nullable=True)
    trade_name = Column(Text, nullable=True)
    old_trade_name = Column(Text, nullable=True)
    addresses = Column(JSON, nullable=True)
    old_addresses = Column(JSON, nullable=True)
    persons = Column(JSON, nullable=True)
    masked_ids = Column(JSON, nullable=True)
    hususlar = Column(JSON, nullable=True)
    belgeler = Column(Text, nullable=True)
    type = Column(Text, nullable=True)
    item_index = Column(Integer, nullable=True)
    start_offset = Column(Integer, nullable=True)
    end_offset = Column(Integer, nullable=True)
    is_derived = Column(Boolean, nullable=True)
    derived_from_index = Column(Integer, nullable=True)
    ilan_sira_no = Column(JSON, nullable=True)
    content_sha256 = Column(Text, nullable=True)
    
    status = Column(String, nullable=False, default='pending') # pending, processing, completed, failed
    message = Column(Text, nullable=True)          # error or info message
    markdown_content = Column(Text, nullable=True) # AI-extracted markdown from docling
    json_payload = Column(JSONB, nullable=True)    # raw docling JSON output
    processing_time = Column(Float, nullable=True) # seconds taken by docling

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    announcement = relationship("Announcement", back_populates="ocr_result", passive_deletes=True)
    company = relationship("Company", back_populates="ocr_results")
