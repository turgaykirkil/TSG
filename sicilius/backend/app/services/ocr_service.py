import logging
from datetime import datetime
from pathlib import Path
from io import BytesIO
import base64
import pdf2image

from sqlalchemy.orm import Session
from supabase import Client
from app.crud.crud_announcement import announcement as crud_announcement
from app.schemas.announcement import AnnouncementUpdate
from app.schemas.ocr_result import OcrResultUpdate
from app.core.config import settings
from PIL import Image

from surya.recognition import RecognitionPredictor
from surya.detection import DetectionPredictor

logger = logging.getLogger(__name__)

# Global variables to hold the predictors
detection_predictor = None
recognition_predictor = None

def load_ocr_models():
    """Load the OCR predictors into memory."""
    global detection_predictor, recognition_predictor
    if not detection_predictor:
        logger.info("Loading detection model...")
        detection_predictor = DetectionPredictor()
    if not recognition_predictor:
        logger.info("Loading recognition model...")
        recognition_predictor = RecognitionPredictor()
    logger.info("OCR models loaded successfully.")

def process_images_with_surya(images: list[Image.Image]) -> list:
    """Processes a list of images using Surya OCR and returns structured data."""
    load_ocr_models() # Ensure models are loaded
    predictions = recognition_predictor(images, det_predictor=detection_predictor)
    return predictions

def process_specific_pdf_preview(db: Session, supabase: Client, file_name: str):
    """
    Finds an announcement by file_name, downloads the PDF from Supabase, 
    runs OCR, generates a preview image, and returns the combined data.
    """
    logger.info(f"Starting specific OCR preview process for: {file_name}")

    announcement = crud_announcement.get_by_file_name(db, file_name=file_name)
    if not announcement or not announcement.file_path:
        logger.warning(f"Announcement not found or has no file path for: {file_name}")
        return None

    # Use a temporary directory for safety
    with NamedTemporaryFile(delete=True, suffix=".pdf") as temp_pdf_file:
        local_pdf_path = Path(temp_pdf_file.name)
        try:
            logger.info(f"Downloading {announcement.file_path} from Supabase...")
            response = supabase.storage.from_("announcements").download(announcement.file_path)
            with open(local_pdf_path, "wb+") as f:
                f.write(response)
            logger.info(f"Successfully downloaded to {local_pdf_path}")
        except Exception as e:
            logger.error(f"Failed to download {announcement.file_path}: {e}")
            return None

        try:
            images = pdf2image.convert_from_path(local_pdf_path, first_page=1, last_page=1)
            if not images:
                raise ValueError("PDF conversion returned no images.")
            image = images[0]

            # Use the new process_images_with_surya function
            predictions = process_images_with_surya([image])
            ocr_results = predictions[0] # We process only one page

            # Reconstruct the data structure for the database and response
            page_data = {
                "page": 1,
                "lines": [
                    {
                        "text": line.text,
                        "bbox": [round(coord, 2) for coord in line.bbox],
                        "polygon": [[round(p[0], 2), round(p[1], 2)] for p in line.polygon]
                    }
                    for line in ocr_results.text_lines
                ]
            }
            ocr_data_for_db = {"pages": [page_data]}
            ocr_text_content = "\n".join([line.text for line in ocr_results.text_lines])

            # Generate base64 image for preview
            buffered = BytesIO()
            image.save(buffered, format="JPEG")
            img_str = base64.b64encode(buffered.getvalue()).decode()

        except Exception as e:
            logger.error(f"Error during OCR processing for {local_pdf_path}: {e}", exc_info=True)
            return None

    update_data = AnnouncementUpdate(
        ocr_text=ocr_text_content,
        ocr_data=ocr_data_for_db,
        status="processed",
        processed_at=datetime.utcnow()
    )
    crud_announcement.update(db, db_obj=announcement, obj_in=update_data)

    local_pdf_path.unlink(missing_ok=True)
    logger.info(f"Successfully processed and cleaned up {file_name}")

    return {
        "announcement_id": announcement.id,
        "ocr_text": ocr_text_content,
        "ocr_data": ocr_data_for_db.get("pages", []),
        "pdf_image_base64": img_str
    }



def process_pdf_with_surya(pdf_path: str, lang: str = 'tr') -> list[dict]:
    """Processes a PDF file using Surya OCR and returns the structured output."""
    try:
        # Use pdf2image to convert PDF to a list of PIL images
        images = convert_from_path(pdf_path)
        logger.info(f"Successfully converted {len(images)} pages from PDF: {pdf_path}")
    except Exception as e:
        logger.error(f"Failed to convert PDF to images: {pdf_path}. Error: {e}")
        return []

    # Prepare languages for each image. Surya expects a list of lists.
    langs = [lang] * len(images)
    logger.info(f"Running OCR on {len(images)} pages with language: {lang}")

    # Run the OCR process
    predictions = run_ocr(images, [langs], det_model, det_processor, rec_model, rec_processor)

    # Structure the output
    output = []
    for i, page_preds in enumerate(predictions):
        lines_data = []
        for line in page_preds.text_lines:
            line_dict = {
                "text": line.text,
                "bbox": [round(coord, 2) for coord in line.bbox],
                "polygon": [[round(p[0], 2), round(p[1], 2)] for p in line.polygon]
            }
            lines_data.append(line_dict)
        
        page_data = {
            "page": i + 1,
            "lines": lines_data
        }
        output.append(page_data)

    logger.info(f"OCR processing completed. Found text in {len(output)} pages.")
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
