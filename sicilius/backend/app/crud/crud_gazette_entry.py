from typing import Any, Dict, List, Optional, Union

from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from app.crud.base import CRUDBase
from app.models.gazette import GazetteEntry
from app.schemas.gazette_entry import GazetteEntryCreate, GazetteEntryUpdate

class CRUDGazetteEntry(CRUDBase[GazetteEntry, GazetteEntryCreate, GazetteEntryUpdate]):
    def get_multi_by_gazette(
        self, db: Session, *, gazette_id: int, skip: int = 0, limit: int = 100
    ) -> List[GazetteEntry]:
        """Get all entries for a specific gazette."""
        return (
            db.query(self.model)
            .filter(GazetteEntry.gazette_id == gazette_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_multi_by_company(
        self, db: Session, *, company_id: int, skip: int = 0, limit: int = 100
    ) -> List[GazetteEntry]:
        """Get all entries for a specific company."""
        return (
            db.query(self.model)
            .filter(GazetteEntry.company_id == company_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_by_type(
        self, db: Session, *, entry_type: str, skip: int = 0, limit: int = 100
    ) -> List[GazetteEntry]:
        """Get all entries of a specific type."""
        return (
            db.query(self.model)
            .filter(GazetteEntry.entry_type == entry_type)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_unprocessed(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[GazetteEntry]:
        """Get all unprocessed entries."""
        return (
            db.query(self.model)
            .filter(GazetteEntry.is_processed == False)  # noqa: E712
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def search(
        self, 
        db: Session, 
        *, 
        query: str, 
        skip: int = 0, 
        limit: int = 100,
        entry_type: Optional[str] = None
    ) -> List[GazetteEntry]:
        """Search entries by text in raw or processed text."""
        search = f"%{query}%"
        query_filter = [
            GazetteEntry.raw_text.ilike(search) | 
            GazetteEntry.processed_text.ilike(search)
        ]
        
        if entry_type:
            query_filter.append(GazetteEntry.entry_type == entry_type)
        
        return (
            db.query(self.model)
            .filter(and_(*query_filter))
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def create_with_gazette(
        self, db: Session, *, obj_in: GazetteEntryCreate, gazette_id: int
    ) -> GazetteEntry:
        """Create a new gazette entry with a gazette ID."""
        db_obj = GazetteEntry(
            **obj_in.dict(exclude_unset=True),
            gazette_id=gazette_id
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def create_multi(
        self, db: Session, *, objs_in: List[GazetteEntryCreate], gazette_id: int
    ) -> List[GazetteEntry]:
        """Create multiple gazette entries at once."""
        db_objs = []
        for obj_in in objs_in:
            db_obj = GazetteEntry(
                **obj_in.dict(exclude_unset=True),
                gazette_id=gazette_id
            )
            db.add(db_obj)
            db_objs.append(db_obj)
        
        db.commit()
        for db_obj in db_objs:
            db.refresh(db_obj)
        
        return db_objs
    
    def mark_as_processed(
        self, 
        db: Session, 
        *, 
        db_obj: GazetteEntry, 
        processed_text: Optional[str] = None,
        has_errors: bool = False,
        error_message: Optional[str] = None
    ) -> GazetteEntry:
        """Mark an entry as processed."""
        update_data = {
            "is_processed": True,
            "has_errors": has_errors,
            "error_message": error_message
        }
        
        if processed_text is not None:
            update_data["processed_text"] = processed_text
        
        return self.update(db, db_obj=db_obj, obj_in=GazetteEntryUpdate(**update_data))

# GazetteEntry CRUD işlemleri için singleton örneki
gazette_entry = CRUDGazetteEntry(GazetteEntry)
