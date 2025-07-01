from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

# Shared properties
class CompanyBase(BaseModel):
    title: Optional[str] = Field(None, max_length=500)
    trade_name: Optional[str] = Field(None, max_length=500)
    tax_number: Optional[str] = Field(None, max_length=50)
    mersis_number: Optional[str] = Field(None, max_length=50)
    trade_registry_number: Optional[str] = Field(None, max_length=50)
    phone: Optional[str] = Field(None, max_length=20)
    email: Optional[str] = Field(None, max_length=255)
    website: Optional[str] = Field(None, max_length=255)
    address: Optional[str] = None
    district: Optional[str] = Field(None, max_length=100)
    city: Optional[str] = Field(None, max_length=100)
    country: Optional[str] = Field("Türkiye", max_length=100)
    postal_code: Optional[str] = Field(None, max_length=20)
    is_active: Optional[bool] = True
    establishment_date: Optional[datetime] = None

# Properties to receive on company creation
class CompanyCreate(CompanyBase):
    title: str = Field(..., max_length=500)
    tax_number: str = Field(..., max_length=50)

# Properties to receive on company update
class CompanyUpdate(CompanyBase):
    pass

# Properties shared by models stored in DB
class CompanyInDBBase(CompanyBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": 1,
                "title": "Örnek Şirket A.Ş.",
                "trade_name": "Örnek Ticari Ünvan",
                "tax_number": "1234567890",
                "is_active": True,
                "created_at": "2023-01-01T00:00:00",
                "updated_at": "2023-01-01T00:00:00"
            }
        }
    }

# Properties to return to client
class Company(CompanyInDBBase):
    pass

# Properties stored in DB
class CompanyInDB(CompanyInDBBase):
    pass
