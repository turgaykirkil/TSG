from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Enum, Text, DateTime, Index
from sqlalchemy.orm import relationship

from app.models.base import Base
import enum

class RelationType(str, enum.Enum):
    BOARD_MEMBER = "board_member"
    SHAREHOLDER = "shareholder"
    AUTHORIZED_SIGNATORY = "authorized_signatory"
    AUDITOR = "auditor"
    LIQUIDATOR = "liquidator"
    OTHER = "other"

class CompanyPersonRelation(Base):
    __tablename__ = "company_person_relations"
    
    # Relationships
    company_id = Column(Integer, ForeignKey("companies.id"), primary_key=True)
    person_id = Column(Integer, ForeignKey("persons.id"), primary_key=True)
    
    # Relation Details
    relation_type = Column(Enum(RelationType), nullable=False, index=True)
    position = Column(String(200))  # Örn: "Yönetim Kurulu Başkanı", "Ortak"
    start_date = Column(DateTime, index=True)
    end_date = Column(DateTime, index=True)
    
    # Share Information (for shareholders)
    share_percentage = Column(String(20))  # Yüzde olarak
    share_amount = Column(String(50))      # Hisse miktarı
    
    # Additional Information
    description = Column(Text)
    is_current = Column(Boolean, default=True, index=True)
    
    # Source of this information
    source = Column(String(100))  # Örn: "Ticaret Sicil Gazetesi", "Manuel Giriş"
    source_reference = Column(String(255))  # Kaynak referansı (örn. gazete no)
    
    # Relationships
    company = relationship("Company", back_populates="persons")
    person = relationship("Person", back_populates="companies")
    
    # Indexes
    __table_args__ = (
        Index('idx_relation_company_person', 'company_id', 'person_id', 'relation_type'),
        Index('idx_relation_dates', 'start_date', 'end_date'),
    )
    
    def __repr__(self):
        return f"<CompanyPersonRelation {self.company_id}-{self.person_id} ({self.relation_type})>"
    
    def to_dict(self):
        result = super().to_dict()
        # Convert dates to string for JSON serialization
        if 'start_date' in result and result['start_date']:
            result['start_date'] = result['start_date'].isoformat()
        if 'end_date' in result and result['end_date']:
            result['end_date'] = result['end_date'].isoformat()
        return result
