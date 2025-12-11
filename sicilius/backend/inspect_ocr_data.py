import sys
import os
from sqlalchemy import func, desc, or_

# Add backend directory to path
sys.path.append(os.getcwd())

from app.db.session import SessionLocal
from app.models.ocr_result import OcrResult
from app.models.company import Company

def inspect_capital_data():
    db = SessionLocal()
    try:
        print("\n--- OCR Text Inspection for 'SERMAYE' ---")
        
        # Search for texts containing "SERMAYE" or "TL" to find capital info
        # Using simple query, fetching objects
        results = db.query(OcrResult).filter(
            OcrResult.original_text.ilike("%sermaye%")
        ).limit(5).all()

        if not results:
            print("❌ No OCR results found with 'sermaye'.")
            # Fallback: just get any OCR results
            results = db.query(OcrResult).filter(OcrResult.original_text.isnot(None)).limit(3).all()
            if results:
                 print("⚠️ Showing random OCR texts instead:")
            else:
                 print("❌ No OCR results found at all.")

        for res in results:
            print(f"\n📄 OCR ID: {res.id}")
            if res.company:
                print(f"   Company: {res.company.unvan}")
            
            text = res.original_text
            if not text:
                print("   (Empty Text)")
                continue

            # Find the position of 'sermaye' to show context
            idx = text.lower().find('sermaye')
            if idx != -1:
                start = max(0, idx - 100)
                end = min(len(text), idx + 200)
                snippet = text[start:end].replace('\n', ' [NL] ')
                print(f"   Extract: ...{snippet}...")
            else:
                preview = text[:200].replace('\n', ' ')
                print(f"   Start: {preview}...")

    finally:
        db.close()

if __name__ == "__main__":
    inspect_capital_data()
