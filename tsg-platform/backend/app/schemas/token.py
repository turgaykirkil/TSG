from typing import Optional
from pydantic import BaseModel

class Token(BaseModel):
    """JWT token yanıt şeması"""
    access_token: str
    token_type: str

class TokenPayload(BaseModel):
    """JWT token payload şeması"""
    sub: Optional[str] = None
    exp: Optional[int] = None

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "sub": "00000000-0000-0000-0000-000000000000",
                "exp": 1620000000
            }
        }
    }
