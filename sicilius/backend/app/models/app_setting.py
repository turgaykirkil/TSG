from sqlalchemy import Column, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from app.db.base import Base

class AppSetting(Base):
    __tablename__ = "app_settings"
    # Tekil anahtar
    key = Column(String(100), primary_key=True, index=True)
    # Değer JSON saklanır (örn: email ayarları)
    value = Column(JSONB, nullable=False)
