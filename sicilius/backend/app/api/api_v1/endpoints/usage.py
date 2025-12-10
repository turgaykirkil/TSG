import logging
import os
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from app import models
from app.api import deps
from app.core.config import settings
from app.core.storage import list_objects

router = APIRouter()

logger = logging.getLogger(__name__)


def _limit_from_env() -> int:
    try:
        return int(os.getenv("TSG_DAILY_QUERY_LIMIT", "20"))
    except Exception:
        return 20


def _minio_usage(bucket: str) -> dict:
    """Get MinIO bucket usage. Returns empty stats if MinIO is unavailable."""
    try:
        objs = list_objects(bucket)
        total_files = 0
        total_bytes = 0
        for obj in objs:
            if obj.get("is_dir"):
                continue
            total_files += 1
            total_bytes += int(obj.get("size") or 0)
        return {
            "bucket": bucket, 
            "total_files": total_files, 
            "total_bytes": total_bytes,
            "status": "available"
        }
    except Exception as exc:
        logger.debug("MinIO unavailable for bucket %s: %s", bucket, exc)
        return {
            "bucket": bucket,
            "total_files": 0,
            "total_bytes": 0,
            "status": "unavailable",
            "error": "MinIO connection failed"
        }


def _safe_count_rows(db: Session, schema: str, table: str) -> int | None:
    try:
        result = db.execute(text(f'SELECT COUNT(*) FROM "{schema}"."{table}"')).scalar()
        return int(result or 0)
    except Exception as exc:  # pragma: no cover - defensive
        logger.warning("Failed to count rows for %s.%s: %s", schema, table, exc)
        return None


@router.get("/me", summary="Get today's usage and remaining queries for current user")
def my_usage(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    today = datetime.utcnow().date()
    usage = (
        db.query(models.DailyUsage)
        .filter(models.DailyUsage.user_id == current_user.id, models.DailyUsage.day == today)
        .first()
    )
    limit = _limit_from_env()
    count = usage.count if usage else 0
    remaining = max(0, limit - count)
    return {
        "date": str(today),
        "count": int(count),
        "limit": int(limit),
        "remaining": int(remaining),
    }


@router.post("/reset-me", summary="Reset today's usage counter for current user")
def reset_my_usage(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    """
    Bugünün kullanım sayacını 0'a çeker. Geliştirme/test amaçlıdır.
    """
    today = datetime.utcnow().date()
    usage = (
        db.query(models.DailyUsage)
        .filter(models.DailyUsage.user_id == current_user.id, models.DailyUsage.day == today)
        .first()
    )
    if usage is None:
        usage = models.DailyUsage(user_id=current_user.id, day=today, count=0)
        db.add(usage)
        db.commit()
        db.refresh(usage)
    else:
        usage.count = 0
        db.add(usage)
        db.commit()

    limit = _limit_from_env()
    return {
        "date": str(today),
        "count": 0,
        "limit": int(limit),
        "remaining": int(limit),
        "reset": True,
    }


@router.get("/overview", summary="Database and storage usage overview (admin)")
def usage_overview(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_superuser),
):
    """Return database size, top tables, and MinIO storage usage."""
    try:
        db_size_bytes = None
        try:
            res = db.execute(text("SELECT pg_database_size(current_database()) AS size")).mappings().first()
            db_size_bytes = int(res["size"]) if res and res.get("size") is not None else None
        except Exception as exc:
            logger.warning("Failed to fetch database size: %s", exc)
            db_size_bytes = None

        tables = []
        try:
            size_rows = db.execute(text(
                """
                SELECT 
                  n.nspname AS schema,
                  c.relname AS table,
                  pg_total_relation_size(c.oid) AS total_bytes,
                  COALESCE(st.n_live_tup, 0) AS approx_rows
                FROM pg_class c
                JOIN pg_namespace n ON n.oid = c.relnamespace
                LEFT JOIN pg_stat_all_tables st ON st.relid = c.oid
                WHERE n.nspname IN ('app','public')
                  AND c.relkind IN ('r','m')
                ORDER BY pg_total_relation_size(c.oid) DESC
                LIMIT 200
                """
            )).mappings().all()
            for r in size_rows:
                try:
                    schema = r.get("schema") or "public"
                    table_name = r.get("table")
                    approx = int(r.get("approx_rows") or 0)
                    row_count = _safe_count_rows(db, schema, table_name) if table_name else None
                    tables.append({
                        "schema": schema,
                        "table": table_name,
                        "total_bytes": int(r.get("total_bytes") or 0),
                        "approx_rows": approx,
                        "row_count": row_count,
                    })
                except Exception:
                    continue
        except Exception as exc:
            logger.warning("Failed to list tables: %s", exc)
            tables = []

        storage_usage = {
            "gazette_pdfs": _minio_usage(settings.minio_bucket_gazette_pdfs),
            "company_gazettes": _minio_usage(settings.minio_bucket_company_gazettes),
        }

        return {
            "db": {
                "database_size_bytes": db_size_bytes,
                "tables": tables,
            },
            "storage": storage_usage,
        }
    except HTTPException:
        raise
    except Exception as exc:
        logger.error("usage_overview failed: %s", exc, exc_info=True)
        raise HTTPException(status_code=500, detail=str(exc))
