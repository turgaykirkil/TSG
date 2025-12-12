from datetime import datetime
from typing import Optional, List, Any
from pydantic import BaseModel, Field, field_validator
import uuid

# Schema for Geo Point
class Point(BaseModel):
    lat: float
    lon: float

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
    koordinat: Optional[Point] = None

# Properties to receive on company creation
class CompanyCreate(CompanyBase):
    title: str = Field(..., max_length=500)

# Properties to receive on company update
class CompanyUpdate(CompanyBase):
    pass

# Properties shared by models stored in DB
class CompanyInDBBase(CompanyBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    koordinat: Optional[Any] = None  # Allow Any type from DB

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": "f81d4fae-7dec-11d0-a765-00a0c91e6bf6",
                "title": "Örnek Şirket A.Ş.",
                "trade_name": "Örnek Ticari Ünvan",
                "tax_number": "1234567890",
                "is_active": True,
                "created_at": "2023-01-01T00:00:00",
                "updated_at": "2023-01-01T00:00:00",
                "koordinat": {"lat": 41.015137, "lon": 28.979530}
            }
        }
    }

# Properties to return to client
class Company(CompanyInDBBase):
    @field_validator('koordinat', mode='before')
    @classmethod
    def koordinat_to_point(cls, v: Any) -> Optional[Point]:
        if v is None:
            return None
            
        # Try to convert GeoAlchemy2 element using to_shape
        try:
            # Check if it looks like a GeoElement (has 'desc', 'data', or is WKBElement/WKTElement)
            # Simplest is to try importing to_shape locally to avoid circular deps if any, 
            # but top level import is better. checking for to_shape usage.
            from geoalchemy2.shape import to_shape
            shape = to_shape(v)
            if hasattr(shape, 'x') and hasattr(shape, 'y'):
                 return Point(lon=shape.x, lat=shape.y)
        except Exception:
             pass

        # Valid fallback for objects that might already be shapes or proxies with x/y
        if hasattr(v, 'x') and hasattr(v, 'y'):
            return Point(lon=v.x, lat=v.y)
            
        # Handle if it's already a dict
        if isinstance(v, dict) and 'lat' in v and 'lon' in v:
            return Point(**v)
        if isinstance(v, Point):
            return v
        return None

# Properties stored in DB
class CompanyInDB(CompanyInDBBase):
    pass

# ---------------------
# Nearby Companies
# ---------------------
class NearbyCompany(BaseModel):
    id: uuid.UUID
    title: Optional[str] = None
    trade_name: Optional[str] = None
    unvan: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    distance_km: float = Field(..., description="Referans şirkete kuş uçuşu mesafe (km)")
    koordinat: Optional[Point] = None
