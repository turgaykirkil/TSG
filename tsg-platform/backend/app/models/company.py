from sqlalchemy import Column, String, Text, ForeignKey, Integer, DateTime, Boolean, Index
from sqlalchemy.orm import relationship

from app.models.base import Base

class Company(Base):
    __tablename__ = "companies"
    
    # Basic Information
    title = Column(String(500), nullable=False, index=True)
    trade_name = Column(String(500))
    tax_number = Column(String(50), unique=True, index=True)
    mersis_number = Column(String(50), unique=True, index=True)
    trade_registry_number = Column(String(50), index=True)
    
    # Contact Information
    phone = Column(String(20))
    email = Column(String(255))
    website = Column(String(255))
    
    # Address Information
    address = Column(Text)
    district = Column(String(100))
    city = Column(String(100))
    country = Column(String(100), default="Türkiye")
    postal_code = Column(String(20))
    
    # Status
    is_active = Column(Boolean, default=True)
    establishment_date = Column(DateTime)
    
    # Relationships
    gazette_entries = relationship("GazetteEntry", back_populates="company")
    persons = relationship("CompanyPersonRelation", back_populates="company")
    
    # Indexes
    __table_args__ = (
        Index('idx_company_title_trgm', 'title', postgresql_using='gin', postgresql_ops={'title': 'gin_trgm_ops'}),
    )
    
    def __repr__(self):
        return f"<Company {self.title}>"
    
    def to_dict(self):
        result = super().to_dict()
        # Convert datetime to string for JSON serialization
        if 'establishment_date' in result and result['establishment_date']:
            result['establishment_date'] = result['establishment_date'].isoformat()
        return result
