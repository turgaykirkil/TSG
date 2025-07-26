from pydantic import BaseModel
from typing import Optional, Any

from typing import List, Tuple

class OcrTextLine(BaseModel):
    """Represents a single line of text detected by OCR."""
    text: str
    bbox: Tuple[int, int, int, int]  # Bounding box as (x_min, y_min, x_max, y_max)

class OcrPagePreview(BaseModel):
    """Represents the OCR preview for a single page."""
    page_number: int
    image_base64: str  # Base64 encoded image of the page
    lines: List[OcrTextLine]

class OcrPreviewResponse(BaseModel):
    """The final response model for the OCR preview, containing all pages."""
    pages: List[OcrPagePreview]
