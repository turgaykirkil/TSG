from sqlalchemy import Column, String, Text, Integer, ForeignKey, DateTime, Boolean, Enum, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

from app.db.base import Base
import enum

class GazetteType(str, enum.Enum):
    TRADE = "trade"
    ANNOUNCEMENT = "announcement"
    OTHER = "other"

class Gazette(Base):
    __tablename__ = "gazettes"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    
    # Basic Information
    gazette_number = Column(String(100), index=True)
    gazette_date = Column(DateTime, nullable=False, index=True)
    gazette_type = Column(Enum(GazetteType), default=GazetteType.TRADE, nullable=False)
    
    # File Information
    file_path = Column(String(500))
    file_name = Column(String(255))
    file_size = Column(Integer)  # in bytes
    page_count = Column(Integer)
    
    # Processing Status
    is_processed = Column(Boolean, default=False, index=True)
    processed_at = Column(DateTime)
    
    # Relationships
    entries = relationship("GazetteEntry", back_populates="gazette")
    
    # Indexes
    __table_args__ = (
        Index('idx_gazette_date_type', 'gazette_date', 'gazette_type'),
    )
    
    def __repr__(self):
        return f"<Gazette {self.gazette_number} - {self.gazette_date}>"


class GazetteEntry(Base):
    __tablename__ = "gazette_entries"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    
    # Relationships
    gazette_id = Column(UUID(as_uuid=True), ForeignKey("gazettes.id"), nullable=False, index=True)
    gazette = relationship("Gazette", back_populates="entries")
    
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"), index=True)
    company = relationship("Company", back_populates="gazette_entries")
    
    # Content
    entry_type = Column(String(100))  # Örn: "Yönetim Kurulu Değişikliği", "Ortaklık Yapısı Değişikliği"
    entry_date = Column(DateTime, index=True)
    page_number = Column(Integer)
    
    # Extracted Text
    raw_text = Column(Text)
    processed_text = Column(Text)
    
    # Status
    is_processed = Column(Boolean, default=False, index=True)
    has_errors = Column(Boolean, default=False)
    error_message = Column(Text)
    
    # Indexes
    __table_args__ = (
        Index('idx_entry_type_date', 'entry_type', 'entry_date'),
    )
    
    def __repr__(self):
        return f"<GazetteEntry {self.id} - {self.entry_type}>"
