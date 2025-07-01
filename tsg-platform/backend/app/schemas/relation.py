from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from app.models.relation import RelationType

# Shared properties
class CompanyPersonRelationBase(BaseModel):
    company_id: int
    person_id: int
    relation_type: RelationType
    position: Optional[str] = Field(None, max_length=200)
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    share_percentage: Optional[str] = Field(None, max_length=20)
    share_amount: Optional[str] = Field(None, max_length=50)
    description: Optional[str] = None
    is_current: Optional[bool] = True
    source: Optional[str] = Field(None, max_length=100)
    source_reference: Optional[str] = Field(None, max_length=255)

# Properties to receive on relation creation
class CompanyPersonRelationCreate(CompanyPersonRelationBase):
    pass

# Properties to receive on relation update
class CompanyPersonRelationUpdate(CompanyPersonRelationBase):
    pass

# Properties shared by models stored in DB
class CompanyPersonRelationInDBBase(CompanyPersonRelationBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": 1,
                "company_id": 1,
                "person_id": 1,
                "relation_type": "shareholder",
                "position": "Ortak",
                "start_date": "2023-01-01T00:00:00",
                "end_date": None,
                "share_percentage": "50%",
                "share_amount": "50.000 TL",
                "is_current": True,
                "source": "Ticaret Sicil Gazetesi",
                "source_reference": "2023/12345",
                "created_at": "2023-01-01T00:00:00",
                "updated_at": "2023-01-01T01:00:00"
            }
        }
    }

# Properties to return to client
class CompanyPersonRelation(CompanyPersonRelationInDBBase):
    pass

# Properties stored in DB
class CompanyPersonRelationInDB(CompanyPersonRelationInDBBase):
    pass
