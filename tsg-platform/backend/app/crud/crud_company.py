from typing import Any, Dict, List, Optional, Union

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.company import Company
from app.schemas.company import CompanyCreate, CompanyUpdate

class CRUDCompany(CRUDBase[Company, CompanyCreate, CompanyUpdate]):
    def get_by_tax_number(self, db: Session, *, tax_number: str) -> Optional[Company]:
        """Vergi numarasına göre şirket getirir."""
        return db.query(Company).filter(Company.tax_number == tax_number).first()
    
    def get_by_trade_registry_number(self, db: Session, *, registry_number: str) -> Optional[Company]:
        """Ticaret sicil numarasına göre şirket getirir."""
        return db.query(Company).filter(Company.trade_registry_number == registry_number).first()
    
    def search(
        self, db: Session, *, query: str, skip: int = 0, limit: int = 100
    ) -> List[Company]:
        """Şirket adına veya ticari unvana göre arama yapar."""
        search = f"%{query}%"
        return (
            db.query(Company)
            .filter(Company.title.ilike(search) | Company.trade_name.ilike(search))
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def create(self, db: Session, *, obj_in: CompanyCreate) -> Company:
        """Yeni şirket oluşturur."""
        # Vergi numarası benzersiz olmalı
        if self.get_by_tax_number(db, tax_number=obj_in.tax_number):
            raise ValueError("Bu vergi numarasına sahip bir şirket zaten mevcut.")
        
        # Ticaret sicil numarası benzersiz olmalı
        if obj_in.trade_registry_number and self.get_by_trade_registry_number(db, registry_number=obj_in.trade_registry_number):
            raise ValueError("Bu ticaret sicil numarasına sahip bir şirket zaten mevcut.")
        
        return super().create(db, obj_in=obj_in)
    
    def update(
        self, db: Session, *, db_obj: Company, obj_in: Union[CompanyUpdate, Dict[str, Any]]
    ) -> Company:
        """Şirket bilgilerini günceller."""
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        
        # Vergi numarası değişikliği kontrolü
        if "tax_number" in update_data and update_data["tax_number"] != db_obj.tax_number:
            if self.get_by_tax_number(db, tax_number=update_data["tax_number"]):
                raise ValueError("Bu vergi numarasına sahip başka bir şirket zaten mevcut.")
        
        # Ticaret sicil numarası değişikliği kontrolü
        if "trade_registry_number" in update_data and update_data["trade_registry_number"] != db_obj.trade_registry_number:
            if update_data["trade_registry_number"] and self.get_by_trade_registry_number(
                db, registry_number=update_data["trade_registry_number"]
            ):
                raise ValueError("Bu ticaret sicil numarasına sahip başka bir şirket zaten mevcut.")
        
        return super().update(db, db_obj=db_obj, obj_in=update_data)

# Şirket CRUD işlemleri için singleton örneği
company = CRUDCompany(Company)
