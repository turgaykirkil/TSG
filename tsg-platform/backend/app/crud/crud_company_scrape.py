from typing import Optional, List
from sqlalchemy.orm import Session
from app.models.company_scrape import CompanyScrape
from app.schemas.company_scrape import CompanyScrapeCreate, CompanyScrapeUpdate
from app.crud.base import CRUDBase

class CRUDCompanyScrape(CRUDBase[CompanyScrape, CompanyScrapeCreate, CompanyScrapeUpdate]):
    def get_by_sicil_no(self, db: Session, *, sicil_no: str) -> Optional[CompanyScrape]:
        return db.query(CompanyScrape).filter(CompanyScrape.sicil_no == sicil_no).first()
    
    def get_multi_needing_scraping(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[CompanyScrape]:
        return (
            db.query(CompanyScrape)
            .filter(
                (CompanyScrape.is_scraped == False) |
                (CompanyScrape.last_scraped_at < 
                 func.date_sub(func.now(), text("INTERVAL 90 DAY")))
            )
            .offset(skip)
            .limit(limit)
            .all()
        )

company_scrape = CRUDCompanyScrape(CompanyScrape)
