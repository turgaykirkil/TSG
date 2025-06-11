from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field

# Shared properties
class CompanyScrapeBase(BaseModel):
    sicil_no: str = Field(..., description="Şirket sicil numarası")
    firma_unvani: Optional[str] = Field(None, description="Şirket ünvanı")
    is_scraped: bool = Field(False, description="Scraping işlemi yapıldı mı?")
    last_scraped_at: Optional[datetime] = Field(None, description="Son scraping tarihi")

# Properties to receive on item creation
class CompanyScrapeCreate(CompanyScrapeBase):
    pass

# Properties to receive on item update
class CompanyScrapeUpdate(CompanyScrapeBase):
    sicil_no: Optional[str] = None
    firma_unvani: Optional[str] = None
    is_scraped: Optional[bool] = None
    last_scraped_at: Optional[datetime] = None

# Properties shared by models stored in DB
class CompanyScrapeInDBBase(CompanyScrapeBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# Properties to return to client
class CompanyScrape(CompanyScrapeInDBBase):
    pass

# Properties properties stored in DB
class CompanyScrapeInDB(CompanyScrapeInDBBase):
    pass
