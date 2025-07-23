from datetime import date
from typing import Any, Dict, List, Optional, Union

from sqlalchemy.orm import Session
from sqlalchemy import and_, or_


from app.crud.base import CRUDBase
from app.models.relation import CompanyPersonRelation
from app.schemas.relation import CompanyPersonRelationCreate, CompanyPersonRelationUpdate

class CRUDRelation(CRUDBase[CompanyPersonRelation, CompanyPersonRelationCreate, CompanyPersonRelationUpdate]):
    def get_relations_by_company(
        self, db: Session, *, company_id: int, skip: int = 0, limit: int = 100
    ) -> List[CompanyPersonRelation]:
        """Bir şirkete ait tüm ilişkileri getirir."""
        return (
            db.query(CompanyPersonRelation)
            .filter(CompanyPersonRelation.company_id == company_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_relations_by_person(
        self, db: Session, *, person_id: int, skip: int = 0, limit: int = 100
    ) -> List[CompanyPersonRelation]:
        """Bir kişiye ait tüm ilişkileri getirir."""
        return (
            db.query(CompanyPersonRelation)
            .filter(CompanyPersonRelation.person_id == person_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_relation(
        self, db: Session, *, company_id: int, person_id: int, relation_type: str
    ) -> Optional[CompanyPersonRelation]:
        """Belirli bir şirket-kişi ilişkisini getirir."""
        return (
            db.query(CompanyPersonRelation)
            .filter(
                and_(
                    CompanyPersonRelation.company_id == company_id,
                    CompanyPersonRelation.person_id == person_id,
                    CompanyPersonRelation.relation_type == relation_type
                )
            )
            .first()
        )
    
    def get_current_relations(
        self, db: Session, *, company_id: Optional[int] = None, person_id: Optional[int] = None
    ) -> List[CompanyPersonRelation]:
        """Mevcut (bitiş tarihi olmayan) ilişkileri getirir."""
        query = db.query(CompanyPersonRelation).filter(CompanyPersonRelation.end_date.is_(None))
        
        if company_id is not None:
            query = query.filter(CompanyPersonRelation.company_id == company_id)
        
        if person_id is not None:
            query = query.filter(CompanyPersonRelation.person_id == person_id)
        
        return query.all()
    
    def create(self, db: Session, *, obj_in: CompanyPersonRelationCreate) -> CompanyPersonRelation:
        """Yeni bir şirket-kişi ilişkisi oluşturur."""
        # Aynı şirket, kişi ve ilişki türünde zaten bir kayıt var mı kontrol et
        existing = self.get_relation(
            db, 
            company_id=obj_in.company_id, 
            person_id=obj_in.person_id, 
            relation_type=obj_in.relation_type
        )
        
        if existing:
            # Eğer mevcut ilişki bitmişse, yeni bir tane oluştur
            if existing.end_date is not None:
                return super().create(db, obj_in=obj_in)
            # Aksi takdirde hata ver
            raise ValueError(
                f"{obj_in.relation_type} türünde zaten aktif bir ilişki mevcut."
            )
        
        return super().create(db, obj_in=obj_in)
    
    def end_relation(
        self, 
        db: Session, 
        *, 
        db_obj: CompanyPersonRelation,
        end_date: Optional[date] = None
    ) -> CompanyPersonRelation:
        """Bir ilişkiyi sonlandırır (bitiş tarihi ekler)."""
        if end_date is None:
            end_date = date.today()
        
        update_data = {"end_date": end_date, "is_current": False}
        return self.update(db, db_obj=db_obj, obj_in=update_data)
    
    def update(
        self, 
        db: Session, 
        *, 
        db_obj: CompanyPersonRelation, 
        obj_in: Union[CompanyPersonRelationUpdate, Dict[str, Any]]
    ) -> CompanyPersonRelation:
        """İlişki bilgilerini günceller."""
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        
        # Eğer end_date güncelleniyorsa, is_current alanını da güncelle
        if "end_date" in update_data:
            update_data["is_current"] = update_data["end_date"] is None
        
        return super().update(db, db_obj=db_obj, obj_in=update_data)

# CompanyPersonRelation CRUD işlemleri için singleton örneği
company_person_relation = CRUDRelation(CompanyPersonRelation)
