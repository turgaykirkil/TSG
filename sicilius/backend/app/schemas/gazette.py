from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from app.models.gazette import GazetteType

# Shared properties
class GazetteBase(BaseModel):
    gazette_number: Optional[str] = Field(None, max_length=100)
    gazette_date: Optional[datetime] = None
    gazette_type: Optional[GazetteType] = GazetteType.TRADE
    file_path: Optional[str] = Field(None, max_length=500)
    file_name: Optional[str] = Field(None, max_length=255)
    file_size: Optional[int] = None
    page_count: Optional[int] = None
    is_processed: Optional[bool] = False
    processed_at: Optional[datetime] = None

# Properties to receive on gazette creation
class GazetteCreate(GazetteBase):
    gazette_date: datetime
    file_name: str = Field(..., max_length=255)
    file_path: str = Field(..., max_length=500)

# Properties to receive on gazette update
class GazetteUpdate(GazetteBase):
    pass

# Properties shared by models stored in DB
class GazetteInDBBase(GazetteBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": 1,
                "gazette_number": "2023/12345",
                "gazette_date": "2023-01-01T00:00:00",
                "gazette_type": "trade",
                "file_name": "2023-12345.pdf",
                "file_path": "/path/to/file.pdf",
                "file_size": 1024,
                "page_count": 10,
                "is_processed": True,
                "processed_at": "2023-01-01T01:00:00",
                "created_at": "2023-01-01T00:00:00",
                "updated_at": "2023-01-01T01:00:00"
            }
        }
    }

# Properties to return to client
class Gazette(GazetteInDBBase):
    pass

# Properties stored in DB
class GazetteInDB(GazetteInDBBase):
    pass
