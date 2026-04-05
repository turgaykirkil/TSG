"""
OCR Tasks — Celery background workers for AI-powered PDF → Markdown conversion.

Flow:
  1. Query announcements that have a pdf_url but no ocr_result yet.
  2. Extract the MinIO object name from the stored pdf_url (which may be a presigned URL).
  3. Fetch the PDF bytes directly from MinIO (doesn't expire like presigned URLs do).
  4. Send PDF bytes to docling-serve (http://localhost:5002).
  5. Persist the resulting Markdown + JSON into ocr_results table.
"""

import asyncio
import io
import logging
import re
from urllib.parse import urlparse

from sqlalchemy.orm import Session
from sqlalchemy import text

from app.core.celery_app import celery_app
from app.core.config import settings
from app.core.storage import get_minio_client
from app.db.session import SessionLocal
from app.models.announcement import Announcement
from app.models.ocr_result import OcrResult
from app.services.pdf_ocr_service import extract_markdown_from_docling
from app.services import ingest_service

logger = logging.getLogger(__name__)


def _get_pdf_bytes_from_minio(pdf_url: str) -> bytes:
    """
    Given either:
      - A plain MinIO object name: "announcement_{company_id}_{uuid}.pdf"
      - A presigned MinIO URL:    "http://host:port/gazette-pdfs/announcement_xxx.pdf?X-Amz-..."
    Fetch and return the raw PDF bytes directly via the MinIO SDK (no expiry concerns).
    """
    bucket = settings.minio_bucket_gazette_pdfs  # "gazette-pdfs"

    # Detect: is it a URL or a plain object name?
    if pdf_url.startswith("http://") or pdf_url.startswith("https://"):
        # Extract object name from URL path
        parsed = urlparse(pdf_url)
        path = parsed.path  # e.g. /gazette-pdfs/announcement_xxx_yyy.pdf
        prefix = f"/{bucket}/"
        if path.startswith(prefix):
            object_name = path[len(prefix):]
        else:
            # Fallback: strip leading slash and bucket name if present
            object_name = path.lstrip("/")
            if object_name.startswith(f"{bucket}/"):
                object_name = object_name[len(bucket) + 1:]
    else:
        # Plain object name stored directly (new format from scraper)
        object_name = pdf_url  # e.g. "announcement_{company_id}_{uuid}.pdf"

    if not object_name:
        raise ValueError(f"Could not determine MinIO object name from pdf_url: {pdf_url!r}")

    logger.info("Fetching PDF from MinIO: bucket=%s object=%s", bucket, object_name)
    client = get_minio_client()
    response = client.get_object(bucket, object_name)
    try:
        pdf_bytes = response.read()
    finally:
        response.close()
        response.release_conn()

    return pdf_bytes


async def process_pdf_for_announcement(db: Session, announcement: Announcement):
    """
    Fetches the PDF for a single announcement from MinIO, sends it to docling-serve,
    and persists the resulting Markdown + JSON into the database.
    """
    if not announcement.pdf_url:
        logger.warning("Announcement %s has no pdf_url — skipping.", announcement.id)
        return

    try:
        pdf_bytes = _get_pdf_bytes_from_minio(announcement.pdf_url)
    except Exception as exc:
        logger.error("Failed to download PDF from MinIO for announcement %s: %s", announcement.id, exc)
        _save_failed_record(db, announcement, message=f"MinIO download error: {exc}")
        return

    file_name = f"announcement_{announcement.id}.pdf"
    logger.info("Sending %s to Docling AI backend (%d bytes)…", file_name, len(pdf_bytes))

    try:
        markdown_str, json_payload, pages, processing_time = await extract_markdown_from_docling(
            pdf_bytes, filename=file_name
        )
    except Exception as exc:
        logger.error("Docling processing failed for announcement %s: %s", announcement.id, exc)
        _save_failed_record(db, announcement, message=f"Docling error: {exc}")
        return

    if markdown_str or json_payload:
        structured_data = {}
        if markdown_str:
            try:
                from app.services import nlp_service
                if nlp_service.nlp_model is None:
                    nlp_service.load_spacy_model()
                
                # Parse the Docling Markdown to extract names, addresses, etc.
                parsed_items = nlp_service.parse_multiple_announcements(markdown_str)
                
                if parsed_items:
                    # PICK THE BEST MATCH: If multiple announcements are in one PDF, find the one that matches our record
                    structured_data = parsed_items[0] 
                    if len(parsed_items) > 1:
                        logger.info(f"Multiple announcements detected ({len(parsed_items)}) in PDF for {announcement.id}. Attempting to match...")
                        found_match = False
                        for item in parsed_items:
                            # 1) Try Mersis match (only if available on announcement)
                            ann_mersis = getattr(announcement, "mersis_no", None)
                            if item.get("mersis_no") and ann_mersis and item["mersis_no"] == ann_mersis:
                                structured_data = item
                                found_match = True
                                break
                            # 2) Try Sicil No match (use correct schema name: trade_registry_number)
                            if item.get("sicil_no") and announcement.trade_registry_number and item["sicil_no"] == announcement.trade_registry_number:
                                structured_data = item
                                found_match = True
                                break
                        
                        if not found_match:
                            logger.warning(f"Could not conclusively match PDF content to announcement {announcement.id}. Falling back to first item.")

                    # DATABASE FALLBACK: If NLP failed to find a trade name, use the existing one from the DB
                    # This is crucial for 'Continued' announcements where the header is on the previous page.
                    if not structured_data.get("trade_name") and announcement.title:
                        logger.info(f"NLP found no trade name for {announcement.id}. Falling back to DB: {announcement.title}")
                        structured_data["trade_name"] = announcement.title

                    # SYNC TO RELATIONAL: Bridge the gap between OCR and Search/Nexus
                    try:
                        corrected_cid = ingest_service.sync_relational_data_from_nlp(db, announcement.company_id, structured_data)
                        if corrected_cid != announcement.company_id:
                            logger.info(f"Cascading split for Announcement {announcement.id}: {announcement.company_id} -> {corrected_cid}")
                            announcement.company_id = corrected_cid
                            db.flush()
                    except Exception as sync_exc:
                        logger.error(f"Relational sync failed for announcement {announcement.id}: {sync_exc}")
                        corrected_cid = announcement.company_id
                else:
                    structured_data = {}
                    corrected_cid = announcement.company_id

            except Exception as exc:
                logger.error("NLP extraction failed for announcement %s: %s", announcement.id, exc)
                structured_data = {}
                corrected_cid = announcement.company_id

        # Upsert: remove any previous failed record first (so we don't violate the unique constraint)
        db.query(OcrResult).filter(OcrResult.announcement_id == announcement.id).delete()
        ocr_record = OcrResult(
            announcement_id=announcement.id,
            company_id=corrected_cid,
            markdown_content=markdown_str,
            json_payload=json_payload,
            processing_time=processing_time,
            pdf_page_count=pages,
            status="completed",
            message=None,
            
            # NLP Extracted fields
            sicil_office_header=structured_data.get("sicil_office_header"),
            sicil_dosya_no=structured_data.get("sicil_no"), # Changed from "sicil_dosya_no" to "sicil_no"
            mersis_no=structured_data.get("mersis_no"),
            trade_name=structured_data.get("trade_name"),
            old_trade_name=structured_data.get("old_trade_name"),
            addresses=structured_data.get("addresses"),
            old_addresses=structured_data.get("old_addresses"),
            persons=structured_data.get("persons"),
            masked_ids=structured_data.get("masked_ids"),
            hususlar=structured_data.get("hususlar"),
            belgeler=structured_data.get("belgeler"),
            type=structured_data.get("type"),
            ilan_sira_no=structured_data.get("ilan_sira_no"),
        )
        db.add(ocr_record)
        db.commit()
        logger.info("✅ OCR completed for announcement %s (%d pages, %.1fs)", announcement.id, pages or 0, processing_time)
    else:
        logger.error("Docling returned no content for %s", file_name)
        _save_failed_record(db, announcement, message="Docling returned empty output")


def _save_failed_record(db: Session, announcement: Announcement, message: str = None):
    """Insert (or update) a failed OCR record for the given announcement."""
    try:
        existing = db.query(OcrResult).filter(OcrResult.announcement_id == announcement.id).first()
        if existing:
            existing.status = "failed"
            existing.message = message
        else:
            db.add(OcrResult(
                announcement_id=announcement.id,
                company_id=announcement.company_id,
                status="failed",
                message=message,
            ))
        db.commit()
    except Exception as exc:
        logger.error("Could not save failed OCR record for %s: %s", announcement.id, exc)
        db.rollback()


@celery_app.task(bind=True)
def run_historical_ocr_backfill(self, limit: int = 100):
    """
    Celery task: picks announcements that have a PDF in MinIO but no completed OCR result,
    then runs them through docling-serve in a batch.
    """
    logger.error("!!! [CELERY] STARTING OCR BACKFILL TASK. LIMIT: %s !!!", limit)
    db = SessionLocal()
    db.execute(text("SET search_path TO app, public"))

    try:
        # Only pick announcements whose pdf_url is set AND either have no ocr_result OR a previously failed one.
        # CRITICAL: We filter for 'announcement_%' or '%localhost:9000%' to narrow down to the 
        # new scraping results among the 52k legacy records.
        unprocessed = db.execute(text("""
            SELECT a.id, a.company_id, a.pdf_url
            FROM app.announcements a
            LEFT JOIN app.ocr_results o ON a.id = o.announcement_id
            WHERE a.pdf_url IS NOT NULL
              AND (o.id IS NULL OR o.status = 'failed')
              AND (a.pdf_url LIKE 'announcement_%' OR a.pdf_url LIKE '%localhost:9000%')
            ORDER BY a.publication_date DESC NULLS LAST, a.id DESC
            LIMIT :limit
        """), {"limit": limit}).mappings().all()


        total = len(unprocessed)
        logger.info("OCR backfill started: %d documents to process.", total)
        self.update_state(state="PROGRESS", meta={"status": f"Processing {total} documents…"})

        async def run_batch():
            for i, row in enumerate(unprocessed, 1):
                logger.info("[%d/%d] Processing announcement %s", i, total, row["id"])
                ann_mock = Announcement(
                    id=row["id"],
                    company_id=row["company_id"],
                    pdf_url=row["pdf_url"],
                )
                await process_pdf_for_announcement(db, ann_mock)

        asyncio.run(run_batch())

        logger.info("OCR backfill batch complete: %d documents processed.", total)
        return {"status": "success", "processed_count": total}

    finally:
        db.close()
