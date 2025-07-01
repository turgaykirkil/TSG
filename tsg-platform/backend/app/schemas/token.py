from typing import Optional
from pydantic import BaseModel

class Token(BaseModel):
    """JWT token yanıt şeması"""
    access_token: str
    token_type: str

class TokenPayload(BaseModel):
    """JWT token payload şeması"""
    sub: Optional[int] = None
    exp: Optional[int] = None

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "sub": 1,
                "exp": 1620000000
            }
        }
    }
