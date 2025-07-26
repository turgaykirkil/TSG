import asyncio
import logging
import requests
from pathlib import Path
from PIL import Image
import io

# Configure logging to see the output
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Since we are running this script standalone, we need to adjust the Python path
# to allow imports from the 'app' module.
import sys
sys.path.append(str(Path(__file__).parent))

from pdf2image import convert_from_bytes
from app.services.ocr_service import OcrService

# URL of the PDF that was causing issues
PDF_URL = "https://vsimavxzfnuaztfmvogt.supabase.co/storage/v1/object/gazette-pdfs/announcement_004a189a-048b-40e3-b86f-c84d97c9b928_878b964c-3520-4dde-af88-d06198f6bfb1.pdf"

def main():
    """
    Main function to run the isolated OCR test.
    """
    logging.info("Starting isolated OCR test...")

    try:
        # 1. Download the PDF file
        logging.info(f"Downloading test PDF from {PDF_URL}")
        response = requests.get(PDF_URL)
        response.raise_for_status()  # Raise an exception for bad status codes
        pdf_bytes = response.content
        logging.info(f"Successfully downloaded {len(pdf_bytes)} bytes.")

        # 2. Initialize the OcrService
        # The service is already hardcoded to use 'cpu'
        ocr_service = OcrService()

        # 3. Convert PDF to images using pdf2image library
        logging.info("Converting PDF to images...")
        images = convert_from_bytes(pdf_bytes)
        logging.info(f"Converted PDF to {len(images)} image(s).")

        # 4. Run the OCR process
        logging.info("Running OCR process...")
        # This is the step that was failing
        predictions = ocr_service.run_ocr(images, tasks=['ocr_with_boxes'])
        logging.info("OCR process completed successfully!")
        logging.info(f"Found {len(predictions)} pages of results.")

    except Exception as e:
        logging.error(f"An error occurred during the OCR test: {e}", exc_info=True)

if __name__ == "__main__":
    main()
