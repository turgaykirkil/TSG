from typing import Any, Dict, List, Optional, Union

from sqlalchemy.orm import Session
from sqlalchemy import or_


from app.crud.base import CRUDBase
from app.models.person import Person
from app.schemas.person import PersonCreate, PersonUpdate

class CRUDPerson(CRUDBase[Person, PersonCreate, PersonUpdate]):
    def get_by_national_id(self, db: Session, *, national_id: str) -> Optional[Person]:
        """TC Kimlik numarasına göre kişi getirir."""
        return db.query(Person).filter(Person.nationality_id == national_id).first()
    
    def get_by_passport(self, db: Session, *, passport_number: str) -> Optional[Person]:
        """Pasaport numarasına göre kişi getirir."""
        return db.query(Person).filter(Person.passport_number == passport_number).first()
    
    def search(
        self, db: Session, *, query: str, skip: int = 0, limit: int = 100
    ) -> List[Person]:
        """İsim, soyisim veya tam isme göre arama yapar."""
        search = f"%{query}%"
        return (
            db.query(Person)
            .filter(
                or_(
                    Person.first_name.ilike(search),
                    Person.last_name.ilike(search),
                    Person.full_name.ilike(search))
            )
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def create(self, db: Session, *, obj_in: PersonCreate) -> Person:
        """Yeni kişi oluşturur."""
        # TC Kimlik numarası benzersiz olmalı
        if obj_in.nationality_id and self.get_by_national_id(db, national_id=obj_in.nationality_id):
            raise ValueError("Bu TC Kimlik numarasına sahip bir kişi zaten mevcut.")
        
        # Pasaport numarası benzersiz olmalı
        if obj_in.passport_number and self.get_by_passport(db, passport_number=obj_in.passport_number):
            raise ValueError("Bu pasaport numarasına sahip bir kişi zaten mevcut.")
        
        # Tam adı oluştur
        full_name = f"{obj_in.first_name or ''} {obj_in.middle_name or ''} {obj_in.last_name or ''}".strip()
        
        # Veritabanına kaydet
        db_obj = Person(
            **obj_in.dict(exclude_unset=True),
            full_name=full_name
        )
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def update(
        self, db: Session, *, db_obj: Person, obj_in: Union[PersonUpdate, Dict[str, Any]]
    ) -> Person:
        """Kişi bilgilerini günceller."""
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        
        # TC Kimlik numarası değişikliği kontrolü
        if "nationality_id" in update_data and update_data["nationality_id"] != db_obj.nationality_id:
            if update_data["nationality_id"] and self.get_by_national_id(db, national_id=update_data["nationality_id"]):
                raise ValueError("Bu TC Kimlik numarasına sahip başka bir kişi zaten mevcut.")
        
        # Pasaport numarası değişikliği kontrolü
        if "passport_number" in update_data and update_data["passport_number"] != db_obj.passport_number:
            if update_data["passport_number"] and self.get_by_passport(db, passport_number=update_data["passport_number"]):
                raise ValueError("Bu pasaport numarasına sahip başka bir kişi zaten mevcut.")
        
        # Tam adı güncelle
        if any(field in update_data for field in ["first_name", "middle_name", "last_name"]):
            first_name = update_data.get("first_name", db_obj.first_name)
            middle_name = update_data.get("middle_name", db_obj.middle_name)
            last_name = update_data.get("last_name", db_obj.last_name)
            update_data["full_name"] = f"{first_name or ''} {middle_name or ''} {last_name or ''}".strip()
        
        return super().update(db, db_obj=db_obj, obj_in=update_data)

# Person CRUD işlemleri için singleton örneği
person = CRUDPerson(Person)
