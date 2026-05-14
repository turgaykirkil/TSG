import asyncio
import sys
import logging
import os

# Ensure backend dir is in path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.scraping_browser import start_enhanced_scraping_process, browser_manager
from app.db.session import SessionLocal
from app.models.ocr_result import OcrResult

logging.basicConfig(level=logging.INFO)

async def test_verification():
    print("🚀 Starting Integrated OCR Verification Scrape...")
    
    # Check current count
    db = SessionLocal()
    initial_count = db.query(OcrResult).count()
    print(f"Initial OcrResult count: {initial_count}")
    
    try:
        print("Opening browser...")
        await browser_manager.open_browser(headless=True)
        
        # Test for 1 item in Istanbul
        print("Scraping 1 item for Istanbul...")
        await start_enhanced_scraping_process(count=1, city="İSTANBUL", mode="city_fill")
        
        # Check final count
        db.expire_all()
        final_count = db.query(OcrResult).count()
        print(f"Final OcrResult count: {final_count}")
        
        if final_count > initial_count:
            print("✅ SUCCESS: At least one OcrResult was created during scraping!")
        else:
            print("❌ FAILURE: No OcrResult created. Check logs.")
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
    finally:
        await browser_manager.close_browser()
        db.close()

if __name__ == "__main__":
    asyncio.run(test_verification())
