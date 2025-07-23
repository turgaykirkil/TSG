import logging
import time
import json
import requests
from tempfile import NamedTemporaryFile
from PIL import Image
from sqlalchemy.orm import Session
import torch

from app import crud, models
from app.schemas.ocr_result import OcrResultUpdate
from app.core.config import settings

from surya.ocr import run_ocr
from surya.model.detection import segformer
from surya.model.recognition import vit
from surya.input.load import load_from_file, load_pdf, page_to_image
from surya.postprocessing.text import draw_text_on_image

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Surya models once
det_model, det_processor = segformer.load_model(), segformer.load_processor()
rec_model, rec_processor = vit.load_model(), vit.load_processor()

def process_pdf_with_surya(pdf_path: str):
    """Processes a PDF file using Surya OCR and returns the structured output."""
    logger.info(f"Loading PDF for Surya processing: {pdf_path}")
    langs = ["tr"]  # Specify languages for OCR
    images, bboxes, polys = load_from_file(pdf_path, det_model, det_processor)
    
    predictions = run_ocr(images, polys, rec_model, rec_processor, langs)
    
    # Combine predictions with page numbers
    output = []
    for i, page_preds in enumerate(predictions):
        output.append({
            "page": i + 1,
            "text_lines": [
                {
                    "text": line.text,
                    "bbox": [round(coord, 2) for coord in line.bbox],
                    "polygon": [[round(p[0], 2), round(p[1], 2)] for p in line.polygon]
                } for line in page_preds.text_lines
            ]
        })
    return output

def process_pdf_for_ocr(db: Session, *, announcement_id: str):
    """Processes a PDF for a given announcement, performs OCR with Surya, and saves the results."""
    logger.info(f"Starting Surya OCR process for announcement_id: {announcement_id}")

    announcement = crud.announcement.get(db=db, id=announcement_id)
    if not announcement or not announcement.ocr_result:
        logger.error(f"Announcement or its OcrResult entry not found for id {announcement_id}.")
        return

    ocr_result = announcement.ocr_result
    crud.ocr_result.update(db=db, db_obj=ocr_result, obj_in=OcrResultUpdate(status='processing'))
    logger.info(f"OCR status for announcement {announcement_id} updated to 'processing'.")

    try:
        if not announcement.pdf_url:
            raise ValueError("PDF URL is missing.")

        logger.info(f"Downloading PDF from {announcement.pdf_url}")
        response = requests.get(announcement.pdf_url, stream=True)
        response.raise_for_status()

        with NamedTemporaryFile(delete=True, suffix=".pdf") as temp_pdf:
            temp_pdf.write(response.content)
            temp_pdf.flush()
            logger.info(f"PDF downloaded to temporary file: {temp_pdf.name}")

            # Perform OCR using Surya
            ocr_output = process_pdf_with_surya(temp_pdf.name)

        # Save results
        update_data = OcrResultUpdate(
            status='completed',
            result_text=json.dumps(ocr_output, ensure_ascii=False, indent=2),
            raw_text="\n".join([line['text'] for page in ocr_output for line in page['text_lines']])
        )
        crud.ocr_result.update(db=db, db_obj=ocr_result, obj_in=update_data)
        logger.info(f"Successfully completed Surya OCR for announcement {announcement_id}.")

    except Exception as e:
        logger.error(f"An error occurred during Surya OCR processing for announcement {announcement_id}: {e}", exc_info=True)
        # Update status to 'failed'
        crud.ocr_result.update(db=db, db_obj=ocr_result, obj_in=OcrResultUpdate(status='failed', result_text=json.dumps({'error': str(e)})))

from sqlalchemy.orm import Session

from app import crud, models
from app.schemas.ocr_result import OcrResultUpdate

logger = logging.getLogger(__name__)

def process_pdf_for_ocr(db: Session, *, announcement_id: str):
    """
    Processes a PDF for a given announcement, performs OCR, and saves the results.
    This function is intended to be run as a background task.
    """
    logger.info(f"Starting OCR process for announcement_id: {announcement_id}")

    # 1. Get the announcement and its ocr_result entry
    announcement = crud.announcement.get(db=db, id=announcement_id)
    if not announcement or not announcement.ocr_result:
        logger.error(f"Announcement or its OcrResult entry not found for id {announcement_id}.")
        return

    ocr_result = announcement.ocr_result

    # 2. Update OCR status to 'processing'
    crud.ocr_result.update(db=db, db_obj=ocr_result, obj_in=OcrResultUpdate(status='processing'))
    logger.info(f"OCR status for announcement {announcement_id} updated to 'processing'.")

    if not announcement.pdf_url:
        logger.error(f"PDF URL not found for announcement {announcement_id}.")
        crud.ocr_result.update(db=db, db_obj=ocr_result, obj_in=OcrResultUpdate(status='failed'))
        return

    try:
        # 3. Download PDF and perform OCR (Placeholder)
        logger.info(f"Simulating OCR on PDF from {announcement.pdf_url}")
        import time
        time.sleep(15) # Simulate a long-running OCR task
        
        raw_text = f"This is the extracted raw text from the PDF for announcement {announcement_id}."
        structured_data = {"words": [{"text": "This", "bbox": [10, 10, 50, 20]}, {"text": "is", "bbox": [55, 10, 65, 20]}]}

        # 4. Save results and update status to 'completed'
        update_data = OcrResultUpdate(
            raw_text=raw_text,
            structured_data=structured_data,
            status="completed"
        )
        crud.ocr_result.update(db=db, db_obj=ocr_result, obj_in=update_data)
        logger.info(f"Successfully completed OCR for announcement {announcement_id}.")

    except Exception as e:
        logger.error(f"An error occurred during OCR processing for announcement {announcement_id}: {e}", exc_info=True)
        # 5. Update status to 'failed' in case of an error
        crud.ocr_result.update(db=db, db_obj=ocr_result, obj_in=OcrResultUpdate(status='failed'))
