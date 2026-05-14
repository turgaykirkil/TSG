from sqlalchemy import Column, String, DateTime, Text, func, Date, Integer, Boolean, ForeignKey, UniqueConstraint, Computed
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry
import uuid
from app.db.base import Base

from .announcement import Announcement

class Company(Base):
    __tablename__ = "companies"
    __table_args__ = (
        UniqueConstraint('sicil_no', 'sicil_office_code', name='ux_companies_sicil_no_office'),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    unvan = Column(String(500), index=True)
    unvan_unaccent = Column(Text, Computed("tr_normalize(unvan)"), index=True)
    mersis_number = Column(String(50), unique=True, index=True, nullable=True)
    sicil_no = Column(String(50), index=True)
    sicil_mudurluk = Column(String(255), nullable=True)
    sicil_office_code = Column(String(64), nullable=True, index=True)
    nace_code = Column(String(255), nullable=True)

    # Contact Information
    phone = Column(String(20), nullable=True)
    email = Column(String(255), nullable=True)
    website = Column(String(255), nullable=True)

    # Address Information
    address = Column(Text, nullable=True)
    district = Column(String(100), nullable=True)
    city = Column(String(100), nullable=True)
    country = Column(String(100), default="Türkiye")
    koordinat = Column(Geometry('POINT', srid=4326), nullable=True)

    # Status and Timestamps
    is_active = Column(Boolean, default=True)
    establishment_date = Column(Date, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    scraped_at = Column(DateTime, nullable=True)

    # PDF Info
    pdf_name = Column(String, nullable=True)
    pdf_path = Column(String, nullable=True)

    # Relationships
    announcements = relationship("Announcement", back_populates="company", cascade="all, delete-orphan")
    ocr_results = relationship("OcrResult", back_populates="company", cascade="all, delete-orphan")
    gazette_entries = relationship("GazetteEntry", back_populates="company")
    persons = relationship("CompanyPersonRelation", back_populates="company")

    def __repr__(self):
        return f"<Company(id={self.id}, unvan='{self.unvan}')>"
