import os
import pytesseract
from PIL import Image, ImageDraw

# Mock settings based on user's .env
TESSERACT_CMD = "/opt/homebrew/bin/tesseract"
TESSDATA_PREFIX = "/opt/homebrew/share/tessdata"

# Set configuration manually as the app does
pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD
os.environ["TESSDATA_PREFIX"] = TESSDATA_PREFIX

def test_ocr():
    print(f"Testing Tesseract at: {TESSERACT_CMD}")
    print(f"Tessdata prefix: {TESSDATA_PREFIX}")
    
    # Create a dummy image with text "123456"
    img = Image.new('L', (200, 50), color=255)
    d = ImageDraw.Draw(img)
    d.text((10, 10), "123456", fill=0)
    
    try:
        # Check if binary exists
        if not os.path.exists(TESSERACT_CMD):
            print("❌ Tesseract binary not found at path!")
            return

        # Simple OCR test
        text = pytesseract.image_to_string(
            img,
            config="--oem 3 --psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        )
        print(f"OCR Result: '{text.strip()}'")
        
        if "123456" in text:
            print("✅ Tesseract is working correctly.")
        else:
            print("❌ Tesseract produced unexpected output.")
            
    except Exception as e:
        print(f"❌ OCR Failed: {e}")

if __name__ == "__main__":
    test_ocr()
