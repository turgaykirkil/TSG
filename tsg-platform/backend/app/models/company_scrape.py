from datetime import datetime, timedelta
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from app.db.base import Base

class CompanyScrape(Base):
    __tablename__ = "company_scrapes"

    id = Column(Integer, primary_key=True, index=True)
    sicil_no = Column(String, unique=True, index=True, nullable=False)
    firma_unvani = Column(String, nullable=True)
    is_scraped = Column(Boolean, default=False, nullable=False)
    last_scraped_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    @property
    def needs_scraping(self):
        # Eğer hiç scraping yapılmadıysa veya son scraping üzerinden 3 ay geçtiyse True döner
        if not self.last_scraped_at:
            return True
        return datetime.utcnow() > (self.last_scraped_at + timedelta(days=90))
