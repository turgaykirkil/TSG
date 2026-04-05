from sqlalchemy import Column, String, Date, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.db.base import Base

class Announcement(Base):
    __tablename__ = "announcements"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)

    # Scraped Information from the table
    trade_registry_name = Column(String(255), index=True, nullable=True) # Müdürlük
    trade_registry_number = Column(String(50), index=True, nullable=True) # Sicil No
    title = Column(String(500), index=True, nullable=True) # Unvan
    publication_date = Column(Date, index=True, nullable=True) # Yayın Tarihi
    issue_number = Column(Integer, nullable=True) # Sayı
    page_number = Column(Integer, nullable=True) # Sayfa
    announcement_type = Column(String(255), nullable=True) # İlan Türü
    newspaper_name = Column(String(255), nullable=True) # Gazete adı veya pre-2021 işareti
    pdf_url = Column(String(1024), nullable=True) # Gazete
    content = Column(Text, nullable=True) # Full announcement text (failsafe)

    # Relationship to Company
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"), nullable=False)
    company = relationship("Company", back_populates="announcements")

    # Relationship to OcrResult (one-to-one)
    ocr_result = relationship("OcrResult", back_populates="announcement", uselist=False)

    def __repr__(self):
        return f"<Announcement {self.id} - {self.title}>"
