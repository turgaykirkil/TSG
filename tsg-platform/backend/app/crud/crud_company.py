from typing import Any, Dict, List, Optional, Union

from sqlalchemy import func
from sqlalchemy.orm import Session
from datetime import datetime
import uuid

from app.crud.base import CRUDBase
from app.models.company import Company
from app.schemas.company import CompanyCreate, CompanyUpdate
from sqlalchemy import text


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

    def get_unscraped(self, db: Session, *, limit: int = 10) -> List[Company]:
        """
        Henüz scrape edilmemiş şirketleri getirir.
        scraped_at alanı null olanları seçer.
        """
        return (
            db.query(Company)
            .filter(Company.scraped_at.is_(None))
            .order_by(Company.id)  # Tutarlılık için sıralama eklendi
            .limit(limit)
            .all()
        )

    def get_multi_uncoordinated(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[Company]:
        """
        Koordinatı olmayan şirketleri getirir.
        koordinat alanı null olanları seçer.
        """
        return (
            db.query(self.model)
            .filter(self.model.koordinat.is_(None))
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def create(self, db: Session, *, obj_in: CompanyCreate) -> Company:
        """Yeni şirket oluşturur ve koordinatları işler."""
        if obj_in.tax_number and self.get_by_tax_number(db, tax_number=obj_in.tax_number):
            raise ValueError("Bu vergi numarasına sahip bir şirket zaten mevcut.")
        if obj_in.trade_registry_number and self.get_by_trade_registry_number(
            db, registry_number=obj_in.trade_registry_number
        ):
            raise ValueError("Bu ticaret sicil numarasına sahip bir şirket zaten mevcut.")

        obj_in_data = obj_in.model_dump(exclude_unset=True)
        koordinat_data = obj_in_data.pop("koordinat", None)

        db_obj = self.model(**obj_in_data)

        if koordinat_data:
            point_wkt = f"POINT({koordinat_data['lon']} {koordinat_data['lat']})"
            db_obj.koordinat = func.ST_GeomFromText(point_wkt, 4326)

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    


    def mark_as_scraped(self, db: Session, *, company_id: uuid.UUID) -> None:
        """Bir şirketi kazındı olarak işaretler (sadece scraped_at günceller)."""
        company = self.get(db, id=company_id)
        if company:
            company.scraped_at = datetime.utcnow()
            db.add(company)
            db.commit()
            db.refresh(company)
    
    def update(
        self,
        db: Session,
        *,
        db_obj: Company,
        obj_in: Union[CompanyUpdate, Dict[str, Any]],
    ) -> Company:
        """Şirket bilgilerini günceller ve koordinatları işler."""
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)

        if "tax_number" in update_data and update_data["tax_number"] != db_obj.tax_number:
            if self.get_by_tax_number(db, tax_number=update_data["tax_number"]):
                raise ValueError("Bu vergi numarasına sahip başka bir şirket zaten mevcut.")

        if (
            "trade_registry_number" in update_data
            and update_data["trade_registry_number"] != db_obj.trade_registry_number
        ):
            if update_data["trade_registry_number"] and self.get_by_trade_registry_number(
                db, registry_number=update_data["trade_registry_number"]
            ):
                raise ValueError(
                    "Bu ticaret sicil numarasına sahip başka bir şirket zaten mevcut."
                )

        koordinat_data = update_data.pop("koordinat", None)
        if koordinat_data:
            point_wkt = f"POINT({koordinat_data['lon']} {koordinat_data['lat']})"
            db_obj.koordinat = func.ST_GeomFromText(point_wkt, 4326)

        return super().update(db, db_obj=db_obj, obj_in=update_data)

# Şirket CRUD işlemleri için singleton örneği
company = CRUDCompany(Company)
