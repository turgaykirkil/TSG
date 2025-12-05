from typing import List, Optional
from uuid import UUID
from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.crud.base import CRUDBase
from app.models.company_error import CompanyError, ErrorStatus
from app.schemas.company_error import CompanyErrorCreate, CompanyErrorUpdate

class CRUDCompanyError(CRUDBase[CompanyError, CompanyErrorCreate, CompanyErrorUpdate]):
    def create_with_user(
        self, db: Session, *, obj_in: CompanyErrorCreate, user_id: UUID
    ) -> CompanyError:
        db_obj = CompanyError(
            company_id=obj_in.company_id,
            user_id=user_id,
            description=obj_in.description,
            status=ErrorStatus.OPEN,
            created_at=datetime.utcnow(),
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_company(
        self, db: Session, *, company_id: UUID, skip: int = 0, limit: int = 100
    ) -> List[CompanyError]:
        return (
            db.query(self.model)
            .filter(CompanyError.company_id == company_id)
            .order_by(desc(CompanyError.created_at))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_all_errors(
        self, db: Session, *, skip: int = 0, limit: int = 100, status: Optional[ErrorStatus] = None
    ) -> List[CompanyError]:
        query = db.query(self.model)
        if status:
            query = query.filter(CompanyError.status == status)
        return (
            query.order_by(desc(CompanyError.created_at))
            .offset(skip)
            .limit(limit)
            .all()
        )

company_error = CRUDCompanyError(CompanyError)
