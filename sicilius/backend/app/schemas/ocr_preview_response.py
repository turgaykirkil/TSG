from pydantic import BaseModel
from typing import Optional

class OcrPreviewResponse(BaseModel):
    announcement_id: str
    ocr_text: str
    pdf_image_base64: Optional[str] = None
