import json
import logging
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, text, select
from sqlalchemy.orm import Session

from app.api import deps
from app.core.config import settings
from app.core.storage import list_objects
from app.models import Announcement, Company, OcrResult

router = APIRouter()

logger = logging.getLogger(__name__)


def _count_storage_pdfs(bucket: str, prefix: str | None = None) -> dict:
    """Count PDF files in a MinIO bucket."""
    try:
        objects = list_objects(bucket, prefix=prefix)
    except Exception as exc:  # pragma: no cover - defensive
        logger.debug("MinIO list_objects failed for bucket %s: %s", bucket, exc)
        return {"bucket": bucket, "pdf_count": 0, "total_bytes": 0, "status": "unavailable"}

    total_files = 0
    total_bytes = 0
    for obj in objects:
        if obj.get("is_dir"):
            continue
        name = (obj.get("object_name") or "").lower()
        if name.endswith(".pdf"):
            total_files += 1
            total_bytes += int(obj.get("size") or 0)
    return {"bucket": bucket, "pdf_count": total_files, "total_bytes": total_bytes, "status": "available"}


def _get_all_storage_stats() -> dict:
    """Get combined storage statistics from all MinIO buckets."""
    gazette_stats = _count_storage_pdfs(settings.minio_bucket_gazette_pdfs)
    company_stats = _count_storage_pdfs(settings.minio_bucket_company_gazettes)
    
    total_files = gazette_stats.get("pdf_count", 0) + company_stats.get("pdf_count", 0)
    total_bytes = gazette_stats.get("total_bytes", 0) + company_stats.get("total_bytes", 0)
    
    return {
        "total_files": total_files,
        "total_bytes": total_bytes,
        "gazette_pdfs": gazette_stats,
        "company_gazettes": company_stats,
    }


def _safe_count_rows(db: Session, schema: str, table: str) -> int | None:
    try:
        result = db.execute(text(f'SELECT COUNT(*) FROM "{schema}"."{table}"')).scalar()
        return int(result or 0)
    except Exception as exc:  # pragma: no cover - defensive
        logger.warning("Failed to count rows for %s.%s: %s", schema, table, exc)
        return None


@router.get("/storage-pdfs-count", summary="Get total count of PDF files in gazette-pdfs bucket")
def get_storage_pdfs_count():
    data = _count_storage_pdfs(settings.minio_bucket_gazette_pdfs)
    return {"bucket": data["bucket"], "pdf_count": data.get("pdf_count", 0)}


@router.get("/coordinates", summary="Get coordinate statistics")
def get_coordinate_stats(db: Session = Depends(deps.get_db)):
    try:
        result = db.execute(text("SELECT get_coordinate_statistics();")).scalar()
        if result is None:
            raise HTTPException(status_code=500, detail="Coordinate statistics function returned no data")
        if isinstance(result, str):
            result = json.loads(result)
        return result
    except HTTPException:
        raise
    except Exception as exc:  # pragma: no cover - defensive
        logger.error("Error fetching coordinate stats: %s", exc, exc_info=True)
        raise HTTPException(status_code=500, detail=f"Could not retrieve coordinate statistics: {exc}")


@router.get("/db-tables", summary="List database tables for usage page")
def list_db_tables(db: Session = Depends(deps.get_db)):
    try:
        sql = text(
            """
            SELECT 
              n.nspname AS schema,
              c.relname AS table,
              c.reltuples::bigint AS approx_rows,
              pg_total_relation_size(c.oid) AS size_bytes,
              pg_size_pretty(pg_total_relation_size(c.oid)) AS size
            FROM pg_class c
            JOIN pg_namespace n ON n.oid = c.relnamespace
            WHERE c.relkind IN ('r','m')
              AND n.nspname IN ('app','public')
            ORDER BY pg_total_relation_size(c.oid) DESC, n.nspname, c.relname
            LIMIT 200
            """
        )
        rows = db.execute(sql).mappings().all()
        enriched = []
        for r in rows:
            schema = r.get("schema") or "public"
            table = r.get("table")
            row_count = _safe_count_rows(db, schema, table) if table else None
            data = dict(r)
            data["row_count"] = row_count
            enriched.append(data)
        return {"tables": enriched}
    except Exception as exc:  # pragma: no cover - defensive
        logger.error("Failed to list tables: %s", exc, exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to list tables: {exc}")


@router.get("", summary="Get application-wide statistics", include_in_schema=False)
@router.get("/", summary="Get application-wide statistics")
def get_stats(db: Session = Depends(deps.get_db)):
    try:
        now = datetime.utcnow()
        last_24h = now - timedelta(hours=24)

        total_companies = db.execute(select(func.count(Company.id))).scalar() or 0
        scraped_companies = db.execute(
            select(func.count(Company.id)).where(Company.scraped_at.isnot(None))
        ).scalar() or 0
        total_announcements = db.execute(select(func.count(Announcement.id))).scalar() or 0
        new_companies_today = db.execute(
            select(func.count(Company.id)).where(Company.created_at >= last_24h)
        ).scalar() or 0
        ocr_processed = db.execute(select(func.count(OcrResult.id))).scalar() or 0

        storage_stats = _get_all_storage_stats()

        return {
            "total_companies": int(total_companies),
            "scraped_companies": int(scraped_companies),
            "total_announcements": int(total_announcements),
            "new_companies_today": int(new_companies_today),
            "ocr_processed": int(ocr_processed),
            "storage_total_files": int(storage_stats.get("total_files", 0)),
            "storage_total_bytes": int(storage_stats.get("total_bytes", 0)),
            "storage_buckets": {
                "gazette_pdfs": storage_stats.get("gazette_pdfs", {}),
                "company_gazettes": storage_stats.get("company_gazettes", {}),
            },
        }
    except Exception as exc:  # pragma: no cover - defensive
        logger.error("Error fetching general stats: %s", exc, exc_info=True)
        raise HTTPException(status_code=500, detail=f"Could not retrieve statistics: {exc}")
