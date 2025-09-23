from datetime import datetime
import os
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.api import deps
from app import models
from app.core.dependencies import get_supabase_client
from supabase import Client

router = APIRouter()


def _limit_from_env() -> int:
    try:
        return int(os.getenv("TSG_DAILY_QUERY_LIMIT", "20"))
    except Exception:
        return 20


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


@router.get("/supabase-overview", summary="Supabase veritabanı ve storage kullanım özeti (admin)")
def supabase_overview(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_superuser),
    supabase: Client = Depends(get_supabase_client),
):
    """
    - DB toplam boyut (bytes)
    - public şeması tablo bazlı toplam boyut (bytes) ve yaklaşık satır sayısı
    - Storage 'gazette-pdfs' bucket toplam dosya sayısı ve toplam byte
    """
    try:
        # Database total size
        db_size_bytes = None
        try:
            res = db.execute(text("SELECT pg_database_size(current_database()) AS size")).mappings().first()
            db_size_bytes = int(res["size"]) if res and res.get("size") is not None else None
        except Exception:
            db_size_bytes = None

        # Per-table sizes and approx rows
        tables = []
        try:
            size_rows = db.execute(text(
                """
                SELECT c.relname AS table,
                       pg_total_relation_size(c.oid) AS total_bytes,
                       COALESCE(s.n_live_tup, 0) AS approx_rows
                FROM pg_class c
                JOIN pg_namespace n ON n.oid = c.relnamespace
                LEFT JOIN pg_stat_user_tables s ON s.relname = c.relname
                WHERE n.nspname = 'public' AND c.relkind = 'r'
                ORDER BY total_bytes DESC
                LIMIT 50
                """
            )).mappings().all()
            for r in size_rows:
                try:
                    tables.append({
                        "table": r.get("table"),
                        "total_bytes": int(r.get("total_bytes") or 0),
                        "approx_rows": int(r.get("approx_rows") or 0),
                    })
                except Exception:
                    continue
        except Exception:
            tables = []

        # Storage usage (gazette-pdfs)
        bucket = "gazette-pdfs"
        total_files = 0
        total_bytes = 0
        try:
            limit = 1000
            queue = [""]
            while queue:
                current = queue.pop(0)
                offset = 0
                while True:
                    listing = supabase.storage.from_(bucket).list(current, {"limit": limit, "offset": offset, "sortBy": {"column": "name", "order": "asc"}})
                    items = listing or []
                    if isinstance(items, dict) and "data" in items:
                        items = items.get("data") or []
                    if not items:
                        break
                    for obj in items:
                        try:
                            name = (obj.get("name") or obj.get("Key") or "")
                            is_folder = obj.get("metadata") in (None, {}) and not str(name).lower().endswith(".pdf")
                            if is_folder and name:
                                next_path = f"{current}/{name}" if current else name
                                queue.append(next_path)
                            else:
                                total_files += 1
                                size = 0
                                md = obj.get("metadata") or {}
                                if isinstance(md, dict) and md.get("size") is not None:
                                    size = int(md.get("size"))
                                elif obj.get("size") is not None:
                                    size = int(obj.get("size"))
                                total_bytes += max(0, size)
                        except Exception:
                            continue
                    if len(items) < limit:
                        break
                    offset += limit
        except Exception:
            # Storage sorgusu başarısız olsa da DB verilerini döndür
            pass

        return {
            "db": {
                "database_size_bytes": db_size_bytes,
                "tables": tables,
            },
            "storage": {
                "bucket": bucket,
                "total_files": total_files,
                "total_bytes": total_bytes,
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
