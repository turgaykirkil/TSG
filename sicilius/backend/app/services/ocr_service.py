from PIL import Image
from typing import List
import torch
from pdf2image import convert_from_bytes
from surya.detection import DetectionPredictor
from surya.recognition import RecognitionPredictor
from surya.layout import LayoutPredictor
from surya.settings import settings
from supabase import Client
from app.schemas.ocr_preview_response import OcrPreviewResponse, OcrPagePreview, OcrTextLine
from io import BytesIO
import base64
import logging
import os
from pathlib import Path

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
            self.layout_predictor = LayoutPredictor(device=self.device)

            self._initialized = True
            logger.info("Surya OCR service initialized successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize Surya OCR service: {e}", exc_info=True)
            raise

    def _calculate_iou(self, box1, box2):
        # box: (x1, y1, x2, y2)
        x1_inter = max(box1[0], box2[0])
        y1_inter = max(box1[1], box2[1])
        x2_inter = min(box1[2], box2[2])
        y2_inter = min(box1[3], box2[3])

        inter_area = max(0, x2_inter - x1_inter) * max(0, y2_inter - y1_inter)
        if inter_area == 0:
            return 0

        box1_area = (box1[2] - box1[0]) * (box1[3] - box1[1])
        box2_area = (box2[2] - box2[0]) * (box2[3] - box2[1])

        union_area = box1_area + box2_area - inter_area
        return inter_area / union_area

    def run_ocr(self, images: List[Image.Image]) -> list:
        if not self._initialized:
            logger.error("OCR service called before initialization.")
            raise RuntimeError("OCR service is not initialized.")

        logger.info(f"Running full OCR pipeline on {len(images)} image(s)...")
        try:
            # We get text predictions first, which gives us a flat list of text lines.
            text_predictions = self.rec_predictor(images, det_predictor=self.det_predictor)

            if not any(p.text_lines for p in text_predictions):
                logger.error("Recognition Predictor did not find any text lines.")
                return []

            processed_pages = []
            for i, (page_text, image) in enumerate(zip(text_predictions, images)):
                page_width, _ = image.size
                column_threshold = page_width / 2
                logger.info(f"--- Processing Page {i+1}: Found {len(page_text.text_lines)} text lines. Page width: {page_width}, Column threshold: {column_threshold} ---")

                if not page_text.text_lines:
                    logger.warning(f"No text lines found on page {i+1}. Skipping.")
                    processed_pages.append(page_text)
                    continue

                # Separate lines into left and right columns
                left_column = []
                right_column = []
                unclassified = []

                for line in page_text.text_lines:
                    line_center_x = (line.bbox[0] + line.bbox[2]) / 2
                    # Simple heuristic: if a line's center is past the halfway mark, it's in the right column.
                    if line_center_x > column_threshold:
                        right_column.append(line)
                    else:
                        left_column.append(line)

                # Sort each column by vertical position (top to bottom)
                left_column.sort(key=lambda line: line.bbox[1])
                right_column.sort(key=lambda line: line.bbox[1])

                # Combine the columns in the correct reading order
                final_ordered_lines = left_column + right_column

                logger.info(f"Page {i+1}: Sorted {len(left_column)} lines in left col and {len(right_column)} in right col. Total: {len(final_ordered_lines)} lines.")
                
                # Update the page's text_lines with the newly sorted list
                page_text.text_lines = final_ordered_lines
                processed_pages.append(page_text)

            logger.info(f"OCR and layout analysis complete. Processed {len(processed_pages)} pages.")
            return processed_pages
        except Exception as e:
            logger.error(f"Critical error in run_ocr: {str(e)}", exc_info=True)
            raise



def get_surya_ocr_preview(pdf_content: bytes, file_name: str) -> OcrPreviewResponse:
    logger.info(f"Processing specific PDF preview for file: {file_name}")
    try:
        # --- DEBUG OUTPUT SETUP ---
        output_dir = Path("test_output")
        os.makedirs(output_dir, exist_ok=True)
        base_filename = Path(file_name).stem
        # --- END DEBUG OUTPUT SETUP ---

        images = convert_from_bytes(pdf_content)
        logger.info(f"Converted PDF to {len(images)} images.")

        ocr_service = OcrService()
        ocr_predictions = ocr_service.run_ocr(images=images)

        if not ocr_predictions:
            logger.warning(f"OCR service returned no results for {file_name}")
            # Return type should be OcrPreviewResponse, not schema object
            return OcrPreviewResponse(pages=[])

        preview_pages = []
        for i, (page_result, pil_image) in enumerate(zip(ocr_predictions, images)):
            page_num = i + 1
            # --- SAVE DEBUG IMAGE --- 
            img_debug_path = output_dir / f"{base_filename}_page_{page_num}.png"
            pil_image.save(img_debug_path, "PNG")
            logger.info(f"Saved debug image to {img_debug_path}")
            # --- END SAVE DEBUG IMAGE ---

            buffered = BytesIO()
            pil_image.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')

            text_lines = []
            full_text_for_debug = []
            if page_result and hasattr(page_result, 'text_lines') and page_result.text_lines:
                for line in page_result.text_lines:
                    bbox_tuple = tuple(map(int, line.bbox))
                    text_lines.append(OcrTextLine(text=line.text, bbox=bbox_tuple))
                    full_text_for_debug.append(line.text)
            
            # --- SAVE DEBUG TEXT --- 
            text_debug_path = output_dir / f"{base_filename}_page_{page_num}.txt"
            with open(text_debug_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(full_text_for_debug))
            logger.info(f"Saved debug text to {text_debug_path}")
            # --- END SAVE DEBUG TEXT ---

            preview_pages.append(OcrPagePreview(
                page_number=page_num,
                image_base64=f"data:image/png;base64,{img_str}",
                lines=text_lines
            ))
        
        logger.info(f"Successfully created preview for {len(preview_pages)} pages.")
        return OcrPreviewResponse(pages=preview_pages)

    except Exception as e:
        logger.error(f"Failed to process PDF preview for {file_name}: {e}", exc_info=True)
        raise
