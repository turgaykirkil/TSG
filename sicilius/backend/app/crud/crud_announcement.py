from app.crud.base import CRUDBase
from app.models.announcement import Announcement
from app.schemas.announcement import AnnouncementCreate, AnnouncementUpdate
from sqlalchemy.orm import Session
from app.models.ocr_result import OcrResult
from typing import Any, Dict, Optional, Union, List
from sqlalchemy import and_
from datetime import date

class CRUDAnnouncement(CRUDBase[Announcement, AnnouncementCreate, AnnouncementUpdate]):
    def get_by_details(self, db: Session, *, company_id: str, publication_date: date, title: str) -> Optional[Announcement]:
        return db.query(Announcement).filter(
            and_(
                Announcement.company_id == company_id,
                Announcement.publication_date == publication_date,
                Announcement.title == title
            )
        ).first()

    def get_multi_without_ocr_results(
        self, db: Session, *, limit: int = 100
    ) -> list[Announcement]:
        """
        Get a list of announcements that do not have an associated OcrResult.
        """
        return (
            db.query(self.model)
            .outerjoin(OcrResult, self.model.id == OcrResult.announcement_id)
            .filter(OcrResult.id == None)
            .order_by(self.model.id.desc())
            .limit(limit)
            .all()
        )


announcement = CRUDAnnouncement(Announcement)
