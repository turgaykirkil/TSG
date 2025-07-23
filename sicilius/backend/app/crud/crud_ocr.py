from app.crud.base import CRUDBase
from app.models.ocr_result import OcrResult
from app.schemas.ocr_result import OcrResultCreate, OcrResultUpdate

class CRUDOcrResult(CRUDBase[OcrResult, OcrResultCreate, OcrResultUpdate]):
    pass

ocr_result = CRUDOcrResult(OcrResult)
