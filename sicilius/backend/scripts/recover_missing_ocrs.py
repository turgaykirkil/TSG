import sys
import os
from pathlib import Path

# Add the backend app to Python path
backend_dir = Path(__file__).parent.parent
sys.path.append(str(backend_dir))

from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.session import SessionLocal
from app.models.ocr_result import OcrResult
from app.models.announcement import Announcement
from app.services import nlp_service, ingest_service
import logging

# Set up logging to stdout so you can see it in terminal
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

def run_recovery():
    print("======================================================")
    print("Starting Retroactive NLP Recovery Process...")
    print("This will find missing announcements hidden inside existing markdowns.")
    print("======================================================")
    
    db: Session = SessionLocal()
    nlp_service.load_spacy_model()
    
    try:
        # Get all OcrResults that have markdown content, grouping by announcement_id just in case
        # We check both markdown_content (new system) and original_text (legacy system)
        results = db.query(
            OcrResult.announcement_id, 
            func.coalesce(OcrResult.markdown_content, OcrResult.original_text).label('text_content'),
            OcrResult.json_payload,
            OcrResult.processing_time,
            OcrResult.pdf_page_count,
            Announcement.company_id.label('original_company_id'),
            Announcement.title.label('announcement_title')
        ).join(
            Announcement, OcrResult.announcement_id == Announcement.id
        ).filter(
            func.coalesce(OcrResult.markdown_content, OcrResult.original_text).isnot(None)
        ).distinct(OcrResult.announcement_id).all()

        total = len(results)
        print(f"Found {total} unique PDFs with markdown content to analyze.")
        
        recovered_count = 0
        multi_pdf_count = 0
        processed = 0

        for row in results:
            processed += 1
            announcement_id = row.announcement_id
            markdown_str = row.text_content
            original_cid = row.original_company_id
            ann_title = row.announcement_title
            
            try:
                # 1. Parse the markdown
                parsed_items = nlp_service.parse_multiple_announcements(markdown_str)
                
                # 2. If the PDF actually had multiple announcements
                if len(parsed_items) > 1:
                    multi_pdf_count += 1
                    
                    # Delete the single old OcrResult to replace it with the properly split ones
                    db.query(OcrResult).filter(OcrResult.announcement_id == announcement_id).delete()
                    
                    # 3. Process ALL parsed items independently
                    for item in parsed_items:
                        # Fallback for missing trade name
                        if not item.get("trade_name") and ann_title:
                            item["trade_name"] = ann_title
                            
                        target_cid = original_cid
                        try:
                            # Use our new Auto-Discovery feature
                            target_cid = ingest_service.sync_relational_data_from_nlp(db, original_cid, item)
                        except Exception as sync_exc:
                            logger.error(f"Relational sync failed for announcement {announcement_id}: {sync_exc}")

                        # Create the fresh OCR record
                        ocr_record = OcrResult(
                            announcement_id=announcement_id,
                            company_id=target_cid,
                            markdown_content=markdown_str,
                            json_payload=row.json_payload,
                            processing_time=row.processing_time,
                            pdf_page_count=row.pdf_page_count,
                            status="completed",
                            
                            sicil_office_header=item.get("sicil_office_header"),
                            sicil_dosya_no=item.get("sicil_no"),
                            mersis_no=item.get("mersis_no"),
                            trade_name=item.get("trade_name"),
                            old_trade_name=item.get("old_trade_name"),
                            addresses=item.get("addresses"),
                            old_addresses=item.get("old_addresses"),
                            persons=item.get("persons"),
                            masked_ids=item.get("masked_ids"),
                            hususlar=item.get("hususlar"),
                            belgeler=item.get("belgeler"),
                            type=item.get("type"),
                            ilan_sira_no=item.get("ilan_sira_no"),
                        )
                        db.add(ocr_record)
                        recovered_count += 1
                        
                    db.commit()
                    if multi_pdf_count % 10 == 0:
                        print(f"[{processed}/{total}] Found Multi-PDF (ID: {announcement_id}) with {len(parsed_items)} announcements! Recovered so far: {recovered_count - multi_pdf_count} hidden records.")
                        
            except Exception as e:
                db.rollback()
                logger.error(f"Error processing announcement {announcement_id}: {e}")

        print("\n======================================================")
        print("Recovery Process Completed!")
        print(f"Scanned {total} documents.")
        print(f"Found {multi_pdf_count} multi-announcement PDFs.")
        # Total new records = total inserted - the 1 record per PDF we deleted = recovered_count - multi_pdf_count
        print(f"🎉 Successfully recovered and auto-discovered {recovered_count - multi_pdf_count} previously LOST announcements!")
        print("======================================================")

    except Exception as e:
        print(f"Fatal error during recovery: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    run_recovery()
