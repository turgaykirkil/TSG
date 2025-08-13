from app.crud.base import CRUDBase
from app.models.ocr_result import OcrResult
from app.schemas.ocr_result import OcrResultCreate, OcrResultUpdate
from sqlalchemy.orm import Session
from typing import Optional

class CRUDOcrResult(CRUDBase[OcrResult, OcrResultCreate, OcrResultUpdate]):
    def get_by_announcement(self, db: Session, *, announcement_id) -> Optional[OcrResult]:
        return db.query(OcrResult).filter(OcrResult.announcement_id == announcement_id).first()

    def get_by_company(self, db: Session, *, company_id) -> Optional[OcrResult]:
        return db.query(OcrResult).filter(OcrResult.company_id == company_id).first()

ocr_result = CRUDOcrResult(OcrResult)
