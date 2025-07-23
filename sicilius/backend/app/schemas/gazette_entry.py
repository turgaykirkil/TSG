from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

from .gazette_entry_process import GazetteEntryProcess

# Shared properties
class GazetteEntryBase(BaseModel):
    gazette_id: Optional[int] = None
    company_id: Optional[int] = None
    entry_type: Optional[str] = Field(None, max_length=100)
    entry_date: Optional[datetime] = None
    page_number: Optional[int] = None
    raw_text: Optional[str] = None
    processed_text: Optional[str] = None
    is_processed: Optional[bool] = False
    has_errors: Optional[bool] = False
    error_message: Optional[str] = None

# Properties to receive on gazette entry creation
class GazetteEntryCreate(GazetteEntryBase):
    gazette_id: int
    entry_type: str = Field(..., max_length=100)
    raw_text: str

# Properties to receive on gazette entry update
class GazetteEntryUpdate(GazetteEntryBase):
    pass

# Properties shared by models stored in DB
class GazetteEntryInDBBase(GazetteEntryBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": 1,
                "gazette_id": 1,
                "company_id": 1,
                "entry_type": "trade_registry",
                "entry_date": "2023-01-01T00:00:00",
                "page_number": 1,
                "raw_text": "Örnek metin içeriği...",
                "is_processed": True,
                "has_errors": False,
                "created_at": "2023-01-01T00:00:00",
                "updated_at": "2023-01-01T01:00:00"
            }
        }
    }

# Properties to return to client
class GazetteEntry(GazetteEntryInDBBase):
    pass

# Properties stored in DB
class GazetteEntryInDB(GazetteEntryInDBBase):
    pass
