from pydantic import BaseModel
from typing import Optional

class Msg(BaseModel):
    """Temel mesaj şeması"""
    detail: Optional[str] = None
    msg: Optional[str] = None
