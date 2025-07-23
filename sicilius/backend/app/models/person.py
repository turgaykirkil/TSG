from sqlalchemy import Column, String, Text, Date, Boolean, Index
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.orm import relationship

from app.db.base import Base

class Person(Base):
    __tablename__ = "persons"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    
    # Personal Information
    first_name = Column(String(100), nullable=False, index=True)
    middle_name = Column(String(100))
    last_name = Column(String(100), nullable=False, index=True)
    full_name = Column(String(300), index=True)  # For faster searching
    
    # Identification
    nationality_id = Column(String(20), unique=True, index=True)
    passport_number = Column(String(50), index=True)
    
    # Contact Information
    email = Column(String(255), index=True)
    phone = Column(String(20))
    
    # Additional Information
    birth_date = Column(Date)
    birth_place = Column(String(100))
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Relationships
    companies = relationship("CompanyPersonRelation", back_populates="person")
    
    # Indexes for full-text search
    __table_args__ = (
        Index('idx_person_name_trgm', 'full_name', postgresql_using='gin', postgresql_ops={'full_name': 'gin_trgm_ops'}),
    )
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.update_full_name()
    
    def update_full_name(self):
        """Update the full_name field based on name components"""
        names = [self.first_name or ""]
        if self.middle_name:
            names.append(self.middle_name)
        names.append(self.last_name or "")
        self.full_name = " ".join(filter(None, names))
    
    def __repr__(self):
        return f"<Person {self.full_name}>"
    
    def to_dict(self):
        result = super().to_dict()
        # Convert date to string for JSON serialization
        if 'birth_date' in result and result['birth_date']:
            result['birth_date'] = result['birth_date'].isoformat()
        return result
