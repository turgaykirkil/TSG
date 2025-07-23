from typing import Any, Dict, List, Optional, Union

from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from app.crud.base import CRUDBase
from app.models.gazette import Gazette
from app.schemas.gazette import GazetteCreate, GazetteUpdate

class CRUDGazette(CRUDBase[Gazette, GazetteCreate, GazetteUpdate]):
    def get_by_number(self, db: Session, *, gazette_number: str) -> Optional[Gazette]:
        """Gazete numarasına göre gazete getirir."""
        return db.query(Gazette).filter(Gazette.gazette_number == gazette_number).first()
    
    def get_multi_by_date_range(
        self, db: Session, *, start_date: str, end_date: str, skip: int = 0, limit: int = 100
    ) -> List[Gazette]:
        """Tarih aralığına göre gazeteleri getirir."""
        return (
            db.query(self.model)
            .filter(and_(Gazette.gazette_date >= start_date, Gazette.gazette_date <= end_date))
            .order_by(Gazette.gazette_date.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_processed(
        self, db: Session, *, skip: int = 0, limit: int = 100, processed: bool = True
    ) -> List[Gazette]:
        """İşlenmiş veya işlenmemiş gazeteleri getirir."""
        return (
            db.query(self.model)
            .filter(Gazette.is_processed == processed)
            .order_by(Gazette.gazette_date.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def search(
        self, db: Session, *, query: str, skip: int = 0, limit: int = 100
    ) -> List[Gazette]:
        """Gazete numarası veya dosya adına göre arama yapar."""
        search = f"%{query}%"
        return (
            db.query(Gazette)
            .filter(
                or_(
                    Gazette.gazette_number.ilike(search),
                    Gazette.file_name.ilike(search))
            )
            .order_by(Gazette.gazette_date.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def create(self, db: Session, *, obj_in: GazetteCreate) -> Gazette:
        """Yeni gazete oluşturur."""
        # Gazete numarası benzersiz olmalı
        if obj_in.gazette_number and self.get_by_number(db, gazette_number=obj_in.gazette_number):
            raise ValueError("Bu gazete numarasına sahip bir kayıt zaten mevcut.")
        
        # Dosya yolu benzersiz olmalı
        if db.query(Gazette).filter(Gazette.file_path == obj_in.file_path).first():
            raise ValueError("Bu dosya yolu zaten kullanılıyor.")
        
        return super().create(db, obj_in=obj_in)
    
    def update(
        self, db: Session, *, db_obj: Gazette, obj_in: Union[GazetteUpdate, Dict[str, Any]]
    ) -> Gazette:
        """Gazete bilgilerini günceller."""
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        
        # Gazete numarası değişikliği kontrolü
        if "gazette_number" in update_data and update_data["gazette_number"] != db_obj.gazette_number:
            if update_data["gazette_number"] and self.get_by_number(db, gazette_number=update_data["gazette_number"]):
                raise ValueError("Bu gazete numarasına sahip başka bir kayıt zaten mevcut.")
        
        # Dosya yolu değişikliği kontrolü
        if "file_path" in update_data and update_data["file_path"] != db_obj.file_path:
            if db.query(Gazette).filter(Gazette.file_path == update_data["file_path"]).first():
                raise ValueError("Bu dosya yolu zaten kullanılıyor.")
        
        return super().update(db, db_obj=db_obj, obj_in=update_data)

# Gazette CRUD işlemleri için singleton örneği
gazette = CRUDGazette(Gazette)
