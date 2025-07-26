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

    def update(self, db: Session, *, db_obj: Announcement, obj_in: Union[AnnouncementUpdate, Dict[str, Any]]) -> Announcement:
        db_obj = super().update(db, db_obj=db_obj, obj_in=obj_in)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_without_ocr_results(
        self, db: Session, *, limit: int = 100
    ) -> list[Announcement]:
        """
        Get a list of announcements that do not have an associated OcrResult.
        """
        """
        Get a list of announcements.
        For testing, this simply gets the first announcements from the DB.
        """
        return db.query(self.model).order_by(self.model.id).limit(limit).all()

    def get_by_file_name(self, db: Session, *, file_name: str) -> Optional[Announcement]:
        return db.query(self.model).filter(self.model.pdf_url.like(f"%{file_name}%")).first()

    def get_unprocessed_announcement(self, db: Session) -> Optional[Announcement]:
        return db.query(self.model).filter(self.model.status == 'pending').order_by(self.model.id.asc()).first()

announcement = CRUDAnnouncement(Announcement)
