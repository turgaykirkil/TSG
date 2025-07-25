from pydantic import BaseModel
from typing import Optional, Any

class OcrPreviewResponse(BaseModel):
    announcement_id: str
    ocr_text: str
    pdf_image_base64: Optional[str] = None
    ocr_data: Optional[Any] = None # To hold the structured OCR data
