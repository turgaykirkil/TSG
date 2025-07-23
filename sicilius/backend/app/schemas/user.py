from typing import Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field
from app.models.user import UserRole

# Shared properties
class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = True
    role: Optional[UserRole] = UserRole.USER

# Properties to receive via API on creation
class UserCreate(UserBase):
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=100)
    full_name: str = Field(..., min_length=2, max_length=100)

# Properties to receive via API on update
class UserUpdate(UserBase):
    password: Optional[str] = Field(None, min_length=6, max_length=100)

# Properties shared by models stored in DB
class UserInDBBase(UserBase):
    id: UUID
    
    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": "00000000-0000-0000-0000-000000000000",
                "email": "user@example.com",
                "full_name": "John Doe",
                "is_active": True,
                "role": "user"
            }
        }
    }

# Properties to return to client
class User(UserInDBBase):
    pass

# Properties stored in DB
class UserInDB(UserInDBBase):
    hashed_password: str

# Properties to receive via API on password change
class PasswordChange(BaseModel):
    current_password: str
    new_password: str = Field(..., min_length=8, max_length=40)
