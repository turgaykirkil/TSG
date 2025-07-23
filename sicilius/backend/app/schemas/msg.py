from pydantic import BaseModel

class Msg(BaseModel):
    """Temel mesaj şeması"""
    detail: str
