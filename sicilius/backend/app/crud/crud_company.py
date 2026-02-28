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

    def get_unscraped_with_sicil_info(self, db: Session, *, limit: int = 10) -> List[Company]:
        """
        Henüz scrape edilmemiş ve sicil bilgileri (no ve müdürlük) dolu olan şirketleri getirir.
        """
        return (
            db.query(Company)
            .filter(
                Company.scraped_at.is_(None),
                Company.sicil_no.isnot(None),
                Company.sicil_mudurluk.isnot(None)
            )
            .order_by(Company.created_at)  # En eski kayıtlardan başla
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

    def get_by_sicil_composite(self, db: Session, *, office_label: str, sicil_no: str) -> Optional[Company]:
        """Composite unique (sicil_no, sicil_office_code) ile şirket getirir."""
        return (
            db.query(Company)
            .filter(
                Company.sicil_no == sicil_no,
                Company.sicil_office_code == office_label,
            )
            .first()
        )

    def get_or_create_minimal_by_sicil(self, db: Session, *, office_label: str, sicil_no: str) -> Company:
        """Şehir (ofis) ve sicil_no ile minimal bir şirket döndürür; yoksa oluşturur.
        unvan gibi alanlar boş kalabilir; scraping sonrası duyuru/pdflere bağlanır.
        """
        obj = self.get_by_sicil_composite(db, office_label=office_label, sicil_no=sicil_no)
        if obj:
            return obj
        obj = Company(
            unvan=None,
            sicil_no=sicil_no,
            sicil_mudurluk=office_label,
            sicil_office_code=office_label,
            is_active=True,
        )
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj
    
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

    # def get_nearby_by_id(self, db: Session, *, company_id: Union[str, uuid.UUID], max_km: float = 5.0, limit: int = 10) -> List[Dict[str, Any]]:
    #     """
    #     Verilen şirketin koordinatına göre yakın şirketleri getirir.
    #     PostGIS fonksiyonları (ST_DWithin, ST_DistanceSphere) kullanılır.
    #     """
    #     try:
    #         # radius in meters
    #         radius_m = max(0.1, float(max_km)) * 1000.0
    #     except Exception:
    #         radius_m = 5000.0
    #
    #     sql = text(
    #         """
    #         SELECT c.id,
    #                c.unvan,
    #                c.address,
    #                c.city,
    #                ST_Y(c.koordinat) AS lat,
    #                ST_X(c.koordinat) AS lon,
    #                ST_Distance(c.koordinat::geography, ref.koordinat::geography) AS distance_m
    #         FROM app.companies c
    #         JOIN app.companies ref ON ref.id = :company_id
    #         WHERE c.id <> ref.id
    #           AND c.koordinat IS NOT NULL
    #           AND ref.koordinat IS NOT NULL
    #           AND ST_DWithin(c.koordinat::geography, ref.koordinat::geography, :radius_m)
    #         ORDER BY distance_m ASC
    #         LIMIT :limit
    #         """
    #     )
    #
    #     res = db.execute(sql, {
    #         "company_id": str(company_id),
    #         "radius_m": radius_m,
    #         "limit": int(limit),
    #     })
    #
    #     items: List[Dict[str, Any]] = []
    #     for row in res.mappings():
    #         distance_km = float(row.get("distance_m", 0.0)) / 1000.0
    #         items.append({
    #             "id": row["id"],
    #             "unvan": row.get("unvan"),
    #             "address": row.get("address"),
    #             "city": row.get("city"),
    #             "distance_km": round(distance_km, 3),
    #             "koordinat": {"lat": row.get("lat"), "lon": row.get("lon")} if row.get("lat") is not None and row.get("lon") is not None else None,
    #         })
    #
    #     return items

# Şirket CRUD işlemleri için singleton örneği
company = CRUDCompany(Company)
