from sqlalchemy import Column, String, Float, Boolean, DateTime, Index
from sqlalchemy.sql import func
from app.db.base import Base

class GeocodingCache(Base):
    __tablename__ = "geocoding_cache"

    # We use a hash of the normalized address as the primary key or a unique index for fast lookups
    address_hash = Column(String(64), primary_key=True, index=True)
    
    # Store the original cleaned text for debugging
    address_text = Column(String(1000), nullable=False)
    
    # The resulting coordinates (if successful)
    lat = Column(Float, nullable=True)
    lon = Column(Float, nullable=True)
    
    # Whether the geocoding attempt was successful
    # (We also cache failures so we don't retry bad addresses forever)
    success = Column(Boolean, default=False, nullable=False)
    
    # Optional: We could store which API succeeded (e.g. 'nominatim', 'locationiq')
    provider = Column(String(50), nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
