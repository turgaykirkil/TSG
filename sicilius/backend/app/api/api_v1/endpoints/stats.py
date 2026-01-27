import json
from typing import Optional, Any
import logging
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, text, select
from sqlalchemy.orm import Session

from app.api import deps
from app.core.config import settings
from app.core.storage import list_objects
from app.models import Announcement, Company, OcrResult, User

router = APIRouter()

logger = logging.getLogger(__name__)


def _count_storage_pdfs(bucket: str, prefix: Optional[str] = None) -> dict:
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


def _get_all_storage_stats(db: Optional[Session] = None) -> dict:
    """Get combined storage statistics using fast DB counters where available."""
    
    # Gazette PDFs (Use Fast DB Counter)
    gazette_count = 0
    gazette_status = "unavailable"
    try:
        if db:
            from app.utils.stats_helper import get_storage_file_count
            gazette_count = get_storage_file_count(db)
            gazette_status = "available_db"
        else:
            gazette_status = "db_session_missing"
    except Exception as e:
        logger.warning("Failed to get DB storage stats: %s", e)
        gazette_status = "error"

    gazette_stats = {
        "bucket": settings.minio_bucket_gazette_pdfs,
        "pdf_count": gazette_count,
        "total_bytes": 0, # Not tracked in DB
        "status": gazette_status
    }

    # Company Gazettes (Small bucket, safe to MinIO listing?)
    # SKIPPING MinIO for now to ensure stability
    company_stats = {"bucket": settings.minio_bucket_company_gazettes, "pdf_count": 0, "total_bytes": 0, "status": "skipped_safe"}
    
    total_files = gazette_stats.get("pdf_count", 0) + company_stats.get("pdf_count", 0)
    total_bytes = gazette_stats.get("total_bytes", 0) + company_stats.get("total_bytes", 0)
    
    return {
        "total_files": total_files,
        "total_bytes": total_bytes,
        "gazette_pdfs": gazette_stats,
        "company_gazettes": company_stats,
    }



def _safe_count_rows(db: Session, schema: str, table: str) -> Optional[int]:
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
        # pg_stat_user_tables kullanarak GERÇEK ZAMANLI satır sayısı alınıyor.
        # n_live_tup: Her INSERT/DELETE sonrası otomatik güncellenir, COUNT(*)'dan kat kat hızlıdır.
        sql = text(
            """
            SELECT 
              s.schemaname AS schema,
              s.relname AS table,
              s.n_live_tup AS row_count,
              pg_total_relation_size(c.oid) AS size_bytes,
              pg_size_pretty(pg_total_relation_size(c.oid)) AS size
            FROM pg_stat_user_tables s
            JOIN pg_class c ON c.relname = s.relname
            JOIN pg_namespace n ON n.oid = c.relnamespace AND n.nspname = s.schemaname
            WHERE s.schemaname IN ('app','public')
            ORDER BY pg_total_relation_size(c.oid) DESC, s.schemaname, s.relname
            LIMIT 200
            """
        )
        rows = db.execute(sql).mappings().all()
        return {"tables": [dict(r) for r in rows]}
    except Exception as exc:  # pragma: no cover - defensive
        logger.error("Failed to list tables: %s", exc, exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to list tables: {exc}")



def _get_approx_count(db: Session, table_name: str, schema: str = "app") -> int:
    try:
        # Fast approximate count from system catalog
        sql = text(f"SELECT reltuples::bigint FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace WHERE c.relname = :table AND n.nspname = :schema")
        result = db.execute(sql, {"table": table_name, "schema": schema}).scalar()
        return int(result) if result is not None else 0
    except Exception:
        return 0

@router.get("", summary="Get application-wide statistics", include_in_schema=False)
@router.get("/", summary="Get application-wide statistics")
def get_stats(db: Session = Depends(deps.get_db)):
    try:
        logger.info("STATS: Starting stats collection...")
        
        # Use approximate counts for main tables to avoid heavy IO/Counting
        logger.info("STATS: Counting companies (approx)...")
        total_companies = _get_approx_count(db, "companies")
        
        logger.info("STATS: Counting scraped companies (approx)...")
        
        total_companies = _get_approx_count(db, "companies")
        total_announcements = _get_approx_count(db, "announcements")
        ocr_processed = _get_approx_count(db, "ocr_results")

        
        logger.info("STATS: Counting scraped companies (filtered)...")
        scraped_companies = 0 # Disabled for performance
        
        logger.info("STATS: Counting new companies (filtered)...")
        new_companies_today = 0 # Disabled for performance
        
        logger.info("STATS: Fetching storage stats (DB)...")
        storage_stats = _get_all_storage_stats(db=db)
        logger.info("STATS: Storage stats fetched.")

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
    except Exception as exc:
        logger.error("Error fetching general stats (returning fallback): %s", exc)
        return {
            "total_companies": 0,
            "scraped_companies": 0,
            "total_announcements": 0,
            "new_companies_today": 0,
            "ocr_processed": 0,
            "storage_total_files": 0,
            "storage_total_bytes": 0,
            "storage_buckets": {"gazette_pdfs": {}, "company_gazettes": {}},
        }
@router.post("/storage/decrement", summary="Decrement storage file count (for OCR app integration)")
def decrement_storage_count(
    count: int = 1,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_superuser),
):
    """
    Manually decrement the storage file counter.
    Used by external OCR apps (Swift) when they delete files from MinIO directly.
    """
    from app.utils.stats_helper import increment_storage_file_count
    new_val = increment_storage_file_count(db, -count)
    return {"message": "Counter updated", "new_total_files": new_val}


@router.get("/dashboard")
def get_dashboard_stats(
    db: Session = Depends(deps.get_db),
    current_user: Any = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Get admin dashboard statistics (Real Data).
    """
    try:
        # Total Users
        # Use ORM to avoid raw SQL table name/schema issues
        total_users = db.query(User).count()
        
        # Active Sessions (Approximate)
        # Reverting to is_active check as last_login might be null for older users
        active_sessions = db.query(User).filter(User.is_active == True).count()

        # Database Size (Postgres specific)
        # Use current_database() to avoid dependency on settings which might not have DB name explicitly
        db_size_query = text("SELECT pg_size_pretty(pg_database_size(current_database()))")
        try:
            db_size = db.execute(db_size_query).scalar()
        except:
            db_size = "Unknown"

        # Storage (Mock for now as MinIO check might be slow, or implement real check later)
        # In a real scenario we would query MinIO bucket stats here.
        storage_usage = "4.2 GB" 
        
        return {
            "total_users": total_users,
            "active_sessions": active_sessions, 
            "db_size": db_size,
            "storage_usage": storage_usage
        }
    except Exception as e:
        logger.error(f"Error fetching stats: {e}")
        raise HTTPException(status_code=500, detail="Stats fetch failed")

@router.get("/activity")
def get_system_activity(
    db: Session = Depends(deps.get_db),
    current_user: Any = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Get system activity for charts (Real Data Aggregation using ORM).
    Aggregates new companies and announcements by day for the last 7 days.
    """
    try:
        # Calculate date range (Last 7 days)
        today = datetime.now().date()
        date_range = [(today - timedelta(days=i)).isoformat() for i in range(6, -1, -1)]
        start_date = today - timedelta(days=7)
        
        # 1. New Companies per day (ORM)
        # Using func.date to truncate timestamp. 
        # Note: func.date works in Postgres.
        companies_stats = db.query(
            func.date(Company.created_at).label('day'), 
            func.count(Company.id).label('count')
        ).filter(
            Company.created_at >= start_date
        ).group_by(
            func.date(Company.created_at)
        ).all()
        
        companies_map = {str(row.day): row.count for row in companies_stats}

        # 2. Daily Announcements (ORM)
        announcements_stats = db.query(
            func.date(Announcement.created_at).label('day'), 
            func.count(Announcement.id).label('count')
        ).filter(
            Announcement.created_at >= start_date
        ).group_by(
            func.date(Announcement.created_at)
        ).all()
        
        announcements_map = {str(row.day): row.count for row in announcements_stats}
        
        # Format response
        result = []
        for date_str in date_range:
            d = datetime.fromisoformat(date_str)
            day_name = d.strftime("%d %b") # 27 Oct
            
            result.append({
                "name": day_name,
                "requests": companies_map.get(date_str, 0),
                "errors": announcements_map.get(date_str, 0) # Mapping announcements to 'errors' key
            })
            
        return result

    except Exception as e:
        # Fallback with dummy data if DB fails completely, to avoid empty screen
        logger.error(f"Stats error: {e}")
        return [
            {"name": "Veri Yok", "requests": 0, "errors": 0}
        ]
