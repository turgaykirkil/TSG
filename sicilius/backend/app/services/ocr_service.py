from PIL import Image
from typing import List
import torch
from pdf2image import convert_from_bytes

from surya.recognition import RecognitionPredictor
from surya.detection import DetectionPredictor
from surya.settings import settings
from supabase import Client
from app import schemas
from io import BytesIO
import base64

import logging
logger = logging.getLogger(__name__)

class OcrService:
    """
    A singleton service for handling OCR tasks using the Surya library.
    It initializes the detection and recognition models once and provides a method to run OCR on images.
    """
    _instance = None
    _initialized = False

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(OcrService, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        
        logger.info("Initializing OCR service...")
        try:
            # Set device based on availability for torch
            if torch.cuda.is_available():
                self.device = "cuda"
            elif torch.backends.mps.is_available():
                self.device = "mps"
            else:
                self.device = "cpu"
            
            # Set device for surya models
            import surya.settings as surya_settings
            surya_settings.TORCH_DEVICE_MODEL = self.device
            logger.info(f"OCR service will use device: {self.device}")

            # Initialize detection and recognition predictors
            self.det_predictor = DetectionPredictor()
            self.rec_predictor = RecognitionPredictor()
            
            self._initialized = True
            logger.info("OCR service initialized successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize OCR service: {e}", exc_info=True)
            # Re-raise to prevent the application from starting with a broken service
            raise

    def run_ocr(self, pdf_content: bytes, tasks: list[str] = None) -> list:
        """
        Run OCR on a PDF document.
        
        Args:
            pdf_content: Binary content of the PDF file
            tasks: List of tasks to perform (e.g., ['ocr_with_boxes'])
            
        Returns:
            List of OCR results for each page
        """
        if not self._initialized:
            logger.error("OCR service called before initialization.")
            raise RuntimeError("OCR service is not initialized.")
        
        try:
            # Convert PDF to images
            logger.info("Converting PDF to images...")
            images = convert_from_bytes(pdf_content)
            logger.info(f"Successfully converted PDF to {len(images)} images.")
            
            if not images:
                logger.error("No images were generated from the PDF.")
                return []
                
            # Set default task if none provided
            if not tasks:
                tasks = ['ocr_with_boxes']
                
            logger.info(f"Running OCR on {len(images)} pages with tasks: {tasks}")
            
            # Process each image
            all_results = []
            
            for i, image in enumerate(images, 1):
                try:
                    logger.info(f"Processing page {i}/{len(images)}...")
                    
                    # Run detection - use PIL Image directly as Surya expects
                    detections = self.det_predictor([image])
                    
                    # Check if we have detections
                    if detections and len(detections) > 0:
                        detection_result = detections[0]
                        
                        # Run recognition with proper Surya API
                        # We need to pass images, task_names, and detections
                        predictions = self.rec_predictor([image], [tasks[0]], [detection_result])
                        
                        if predictions and len(predictions) > 0:
                            all_results.extend(predictions)
                            logger.info(f"Page {i}: Found {len(predictions[0].lines)} text lines")
                        else:
                            logger.warning(f"Page {i}: No text detected")
                            all_results.append([])
                    else:
                        logger.warning(f"Page {i}: No text detected")
                        all_results.append([])
                        
                except Exception as page_error:
                    logger.error(f"Error processing page {i}: {str(page_error)}", exc_info=True)
                    all_results.append([])  # Add empty result for this page
            
            logger.info(f"OCR processing completed. Processed {len(all_results)} pages.")
            return all_results
            
        except Exception as e:
            logger.error(f"Critical error in run_ocr: {str(e)}", exc_info=True)
            return []


def process_specific_pdf_preview(supabase: Client, file_name: str) -> schemas.OcrPreviewResponse:
    logger.info(f"Processing specific PDF preview for file: {file_name}")
    try:
        # 1. Download file from Supabase
        response = supabase.storage.from_("announcements").download(file_name)
        pdf_content = response
        logger.info(f"Successfully downloaded {len(pdf_content)} bytes for {file_name}")

        # 2. Get OCR service instance and run OCR
        ocr_service = OcrService()
        ocr_results = ocr_service.run_ocr(pdf_content=pdf_content)

        if not ocr_results:
            logger.warning(f"OCR service returned no results for {file_name}")
            return schemas.OcrPreviewResponse(pages=[])

        # 3. Convert results to OcrPreviewResponse schema
        preview_pages = []
        images = convert_from_bytes(pdf_content)

        for i, (page_result, pil_image) in enumerate(zip(ocr_results, images)):
            # Convert PIL image to base64
            buffered = BytesIO()
            pil_image.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

            # Extract text lines
            text_lines = []
            if page_result and hasattr(page_result, 'lines') and page_result.lines:
                for line in page_result.lines:
                    text_lines.append(schemas.OcrTextLine(text=line.text, bbox=line.bbox))
            
            preview_pages.append(schemas.OcrPagePreview(
                page_number=i + 1,
                image_base64=f"data:image/png;base64,{img_str}",
                lines=text_lines
            ))
        
        logger.info(f"Successfully created preview for {len(preview_pages)} pages.")
        return schemas.OcrPreviewResponse(pages=preview_pages)

    except Exception as e:
        logger.error(f"Failed to process preview for {file_name}: {e}", exc_info=True)
        raise

