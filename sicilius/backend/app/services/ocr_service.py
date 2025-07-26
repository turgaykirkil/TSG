from PIL import Image
from typing import List
import torch
from pdf2image import convert_from_bytes
from surya.detection import DetectionPredictor
from surya.recognition import RecognitionPredictor
from surya.settings import settings
from supabase import Client
from app.schemas.ocr_preview_response import OcrPreviewResponse, OcrPagePreview, OcrTextLine
from io import BytesIO
import base64
import logging

logger = logging.getLogger(__name__)

class OcrService:
    _instance = None
    _initialized = False

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(OcrService, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        
        logger.info("Initializing Surya OCR service...")
        try:
            # Use MPS if available for Apple Silicon, otherwise fallback to CPU
            self.device = "mps" if torch.backends.mps.is_available() else "cpu"
            logger.info(f"Surya OCR service will use device: {self.device.upper()}")

            # Initialize predictors with the correct method (passing device to constructor)
            self.det_predictor = DetectionPredictor(device=self.device)
            self.rec_predictor = RecognitionPredictor(device=self.device)

            self._initialized = True
            logger.info("Surya OCR service initialized successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize Surya OCR service: {e}", exc_info=True)
            raise

    def run_ocr(self, images: List[Image.Image]) -> list:
        if not self._initialized:
            logger.error("OCR service called before initialization.")
            raise RuntimeError("OCR service is not initialized.")

        logger.info(f"Running Surya OCR on {len(images)} image(s)...")
        try:
            # Use the correct calling method learned from testing:
            # The recognition predictor is called directly and takes the detection predictor as an argument.
            predictions = self.rec_predictor(images, det_predictor=self.det_predictor)
            logger.info(f"OCR complete. Processed {len(predictions)} pages.")
            return predictions
        except Exception as e:
            logger.error(f"Critical error in run_ocr: {str(e)}", exc_info=True)
            return []



def get_surya_ocr_preview(pdf_content: bytes, file_name: str) -> OcrPreviewResponse:
    logger.info(f"Processing specific PDF preview for file: {file_name}")
    try:
        # The following logic for downloading from Supabase is temporarily commented out
        # to allow for faster local testing via file upload.
        # response = supabase.storage.from_("gazette-pdfs").download(file_name)
        # pdf_content = response
        # logger.info(f"Successfully downloaded {len(pdf_content)} bytes for {file_name}")

        images = convert_from_bytes(pdf_content)
        logger.info(f"Converted PDF to {len(images)} images.")

        ocr_service = OcrService()
        ocr_predictions = ocr_service.run_ocr(images=images)

        if not ocr_predictions:
            logger.warning(f"OCR service returned no results for {file_name}")
            return schemas.OcrPreviewResponse(pages=[])

        preview_pages = []
        for i, (page_result, pil_image) in enumerate(zip(ocr_predictions, images)):
            buffered = BytesIO()
            pil_image.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')

            text_lines = []
            if page_result and hasattr(page_result, 'text_lines') and page_result.text_lines:
                for line in page_result.text_lines:
                    # Ensure bbox is a tuple of 4 integers
                    bbox_tuple = tuple(map(int, line.bbox))
                    text_lines.append(OcrTextLine(text=line.text, bbox=bbox_tuple))
            
            preview_pages.append(OcrPagePreview(
                page_number=i + 1,
                image_base64=f"data:image/png;base64,{img_str}",
                lines=text_lines
            ))
        
        logger.info(f"Successfully created preview for {len(preview_pages)} pages.")
        return OcrPreviewResponse(pages=preview_pages)

    except Exception as e:
        logger.error(f"Failed to process PDF preview for {file_name}: {e}", exc_info=True)
        raise
