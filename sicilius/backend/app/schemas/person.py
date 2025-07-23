from datetime import date, datetime
from typing import Optional, List, ClassVar
from pydantic import BaseModel, Field, EmailStr, ConfigDict

# Shared properties
class PersonBase(BaseModel):
    first_name: Optional[str] = Field(None, max_length=100)
    middle_name: Optional[str] = Field(None, max_length=100)
    last_name: Optional[str] = Field(None, max_length=100)
    full_name: Optional[str] = Field(None, max_length=300)
    nationality_id: Optional[str] = Field(None, max_length=20)
    passport_number: Optional[str] = Field(None, max_length=50)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=20)
    birth_date: Optional[date] = None
    birth_place: Optional[str] = Field(None, max_length=100)
    is_active: Optional[bool] = True

# Properties to receive on person creation
class PersonCreate(PersonBase):
    first_name: str = Field(..., max_length=100)
    last_name: str = Field(..., max_length=100)

# Properties to receive on person update
class PersonUpdate(PersonBase):
    pass

# Properties shared by models stored in DB
class PersonInDBBase(PersonBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": 1,
                "first_name": "Ahmet",
                "middle_name": "",
                "last_name": "Yılmaz",
                "full_name": "Ahmet Yılmaz",
                "nationality_id": "12345678901",
                "email": "ahmet@example.com",
                "phone": "+905551234567",
                "birth_date": "1980-01-01",
                "birth_place": "İstanbul",
                "is_active": True,
                "created_at": "2023-01-01T00:00:00",
                "updated_at": "2023-01-01T01:00:00"
            }
        }
    }

# Properties to return to client
class Person(PersonInDBBase):
    pass

# Properties stored in DB
class PersonInDB(PersonInDBBase):
    pass
