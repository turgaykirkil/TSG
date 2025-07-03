from app.crud.base import CRUDBase
from app.models.announcement import Announcement
from app.schemas.announcement import AnnouncementCreate, AnnouncementUpdate
from sqlalchemy.orm import Session
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

announcement = CRUDAnnouncement(Announcement)
