import torch
from PIL import Image
from surya.detection import DetectionPredictor
from surya.recognition import RecognitionPredictor
from pdf2image import convert_from_path
from pathlib import Path
import time
import argparse

def main():
    parser = argparse.ArgumentParser(description="Run Surya OCR on a single PDF file.")
    parser.add_argument("pdf_path", type=str, help="Path to the PDF file to process.")
    args = parser.parse_args()

    # --- 1. Define Paths ---
    pdf_path = Path(args.pdf_path)
    output_dir = Path(__file__).parent / "test_output"
    output_dir.mkdir(exist_ok=True)
    output_txt_path = output_dir / f"{pdf_path.stem}.txt"

    print(f"Starting OCR process for: {pdf_path}")

    if not pdf_path.exists():
        print(f"\nERROR: Test file not found at {pdf_path}")
        return

    # --- 2. Convert PDF to Images ---
    print("Converting PDF to images...")
    try:
        images = convert_from_path(str(pdf_path))
        print(f"Successfully converted PDF to {len(images)} image(s).")
    except Exception as e:
        print(f"\nAn error occurred during PDF to image conversion: {e}")
        print("Please ensure 'poppler' is installed on your system.")
        print("On macOS, you can install it with: brew install poppler")
        return

    # --- 3. Load Models ---
    print("Loading OCR models... This may take a while on first run.")
    start_time = time.time()
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    print(f"Using device: {device.upper()}")

    det_predictor = DetectionPredictor(device=device)
    rec_predictor = RecognitionPredictor(device=device)
    print(f"Models loaded in {time.time() - start_time:.2f} seconds.")

    # --- 4. Run OCR ---
    try:
        print(f"Running OCR on {len(images)} page(s)...")
        start_time = time.time()
        predictions = rec_predictor(images, det_predictor=det_predictor)
        print(f"OCR completed in {time.time() - start_time:.2f} seconds.")

        # --- 5. Save Results ---
        full_text = ""
        for pred in predictions:
            for line in pred.text_lines:
                full_text += line.text + "\n"

        with open(output_txt_path, "w", encoding="utf-8") as f:
            f.write(full_text)

        print("-" * 50)
        print("\u2705 SUCCESS!")
        print(f"OCR output saved to: {output_txt_path}")
        print("-" * 50)

    except Exception as e:
        print(f"An error occurred during OCR processing: {e}")

if __name__ == "__main__":
    main()
