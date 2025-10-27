import os
import sys
import time
import json
from typing import Any, Dict, List, Optional, Tuple, Set

import httpx
from sqlalchemy import MetaData, Table, text, create_engine
from sqlalchemy.engine import Engine

# Reuse project DB engine/config
from app.db.session import engine as default_engine
from app.db.base import Base
from app import models  # ensure models are imported

DEFAULT_CHUNK = 1000

PUBLIC_TABLES_DEFAULT = [
    # public schema tables to migrate (exclude app_users)
    "announcements",
    "app_settings",
    "companies",
    "company_person_relations",
    "daily_usages",
    "file_uploads",
    "gazette_entries",
    "gazettes",
    "job_histories",
    "ocr_results",
    "persons",
    "user_invites",
]

PK_HINTS: Dict[str, str] = {
    # table -> primary key column (if known)
    "announcements": "id",
    "app_settings": "key",
    "companies": "id",
    "company_person_relations": "id",
    "daily_usages": "id",
    "file_uploads": "id",
    "gazette_entries": "id",
    "gazettes": "id",
    "job_histories": "id",
    "ocr_results": "id",
    "persons": "id",
    "user_invites": "id",
    # app schema tables (use when SUPABASE_SOURCE_SCHEMA=app)
    "company_trade_names": "id",
    "addresses_history": "id",
    "ocr_person_mentions": "id",
    "ocr_address_mentions": "id",
    "ocr_id_mentions": "id",
}

# Optional per-table excluded columns (e.g., geometry types)
EXCLUDE_COLUMNS: Dict[str, Set[str]] = {
    "companies": {"koordinat"},
}


def _reflect_table(engine: Engine, schema: Optional[str], table_name: str) -> Tuple[Table, Set[str]]:
    md = MetaData()
    tbl = Table(table_name, md, schema=schema, autoload_with=engine)
    cols = {c.name for c in tbl.columns}
    return tbl, cols


def _build_upsert_sql(schema: Optional[str], table: str, columns: List[str], id_field: Optional[str]) -> str:
    fqtn = f'"{schema}"."{table}"' if schema else f'"{table}"'
    cols_sql = ", ".join([f'"{c}"' for c in columns])
    vals_sql = ", ".join([f':{c}' for c in columns])
    if id_field and id_field in columns:
        update_cols = [c for c in columns if c != id_field]
        set_sql = ", ".join([f'"{c}" = EXCLUDED."{c}"' for c in update_cols])
        return (
            f"INSERT INTO {fqtn} ({cols_sql}) VALUES ({vals_sql}) "
            f"ON CONFLICT (\"{id_field}\") DO UPDATE SET {set_sql}"
        )
    else:
        return f"INSERT INTO {fqtn} ({cols_sql}) VALUES ({vals_sql}) ON CONFLICT DO NOTHING"


def _fetch_chunk(client: httpx.Client, base_url: str, table: str, schema: Optional[str], offset: int, limit: int) -> List[Dict[str, Any]]:
    url = f"{base_url}/rest/v1/{table}"
    headers = {
        "apikey": os.environ.get("TSG_SUPABASE_SERVICE_ROLE_KEY") or os.environ.get("SUPABASE_SERVICE_ROLE_KEY") or "",
        "Authorization": f"Bearer {os.environ.get('TSG_SUPABASE_SERVICE_ROLE_KEY') or os.environ.get('SUPABASE_SERVICE_ROLE_KEY') or ''}",
    }
    if schema:
        headers["Accept-Profile"] = schema
    params = {
        "select": "*",
        # Stable ordering to ensure deterministic pagination
        "order": "id.asc",
        "limit": str(limit),
        "offset": str(offset),
    }
    try:
        r = client.get(url, headers=headers, params=params, timeout=60.0)
        r.raise_for_status()
    except httpx.HTTPStatusError as e:
        status = getattr(e.response, "status_code", None)
        body = None
        try:
            body = e.response.text
        except Exception:
            body = str(e)
        raise RuntimeError(f"REST error for {schema or 'public'}.{table}: HTTP {status} {body}")
    if not r.text:
        return []
    try:
        data = r.json()
    except Exception:
        data = []
    if isinstance(data, list):
        return data
    return []


def migrate_table(source_schema: Optional[str], source_table: str, target_schema: Optional[str], target_table: str, id_field: Optional[str], chunk_size: int = DEFAULT_CHUNK) -> Tuple[int, int]:
    base_url = os.environ.get("TSG_SUPABASE_URL") or os.environ.get("SUPABASE_URL")
    if not base_url:
        raise RuntimeError("Supabase URL env not set (TSG_SUPABASE_URL or SUPABASE_URL)")
    if not (os.environ.get("TSG_SUPABASE_SERVICE_ROLE_KEY") or os.environ.get("SUPABASE_SERVICE_ROLE_KEY")):
        raise RuntimeError("Supabase Service Role Key env not set (TSG_SUPABASE_SERVICE_ROLE_KEY or SUPABASE_SERVICE_ROLE_KEY)")

    engine: Engine = default_engine
    # Override destination engine if provided
    dest_url = os.environ.get("DEST_DATABASE_URL")
    engine = create_engine(dest_url, pool_pre_ping=True) if dest_url else default_engine
    # Ensure tables exist on destination
    try:
        Base.metadata.create_all(bind=engine)
    except Exception:
        pass
    print(f"[migrate] start: src={source_schema}.{source_table} -> dst={(target_schema or 'public')}.{target_table}")
    try:
        print(f"[migrate][diag] dest={getattr(engine, 'url', '<engine>')}")
        tbl, col_names = _reflect_table(engine, target_schema, target_table)
    except Exception as e:
        import traceback
        print(f"[migrate][ERROR] reflect failed for {(target_schema or 'public')}.{target_table}: {e}")
        traceback.print_exc()
        raise
    # prefer model PK hint
    id_col = id_field or PK_HINTS.get(target_table)

    inserted = 0
    updated = 0

    offset = 0
    with httpx.Client() as http:
        while True:
            rows = _fetch_chunk(http, base_url, source_table, source_schema, offset, chunk_size)
            if not rows:
                break
            batch = []
            for r in rows:
                # keep only known columns
                payload = {k: v for k, v in r.items() if k in col_names}
                batch.append(payload)
            if batch:
                # compute batch columns as union of payload keys intersect dest columns
                batch_keys = set()
                for p in batch:
                    batch_keys.update(p.keys())
                # exclude configured columns
                excluded = EXCLUDE_COLUMNS.get(target_table, set())
                batch_cols = [c for c in col_names if c in batch_keys and c not in excluded]
                # ensure id_col is included first if available
                if id_col and id_col in batch_cols:
                    batch_cols = [id_col] + [c for c in batch_cols if c != id_col]
                # normalize rows: fill missing keys with None
                norm_batch = []
                for p in batch:
                    norm = {c: p.get(c, None) for c in batch_cols}
                    norm_batch.append(norm)
                sql = _build_upsert_sql(target_schema, target_table, batch_cols, id_col)
                try:
                    with engine.begin() as conn:
                        conn.execute(text(sql), norm_batch)
                except Exception as e:
                    print(f"[migrate][ERROR] upsert failed at offset={offset} size={len(batch)}: {e}")
                    raise
                # res.rowcount is unreliable for upserts; we can’t separate inserts vs updates
            inserted += len(batch)
            offset += len(rows)
            if len(rows) < chunk_size:
                break
            # be nice to API
            time.sleep(0.05)

    return inserted, updated


def main(argv: List[str]) -> int:
    # Simple CLI: optional table list via args; default PUBLIC_TABLES_DEFAULT
    tables = PUBLIC_TABLES_DEFAULT
    source_schema = os.environ.get("SUPABASE_SOURCE_SCHEMA", "public").strip() or "public"
    if len(argv) > 1:
        # allow comma-separated tables
        tables = [t.strip() for t in argv[1].split(",") if t.strip()]
    total = 0
    for t in tables:
        if t == "app_users":
            continue
        try:
            # support mapping: source=>schema.table
            target_schema = None
            target_table = t
            source_table = t
            if "=>" in t:
                src, dst = t.split("=>", 1)
                source_table = src.strip()
                if "." in dst:
                    target_schema, target_table = dst.strip().split(".", 1)
                else:
                    target_schema = None
                    target_table = dst.strip()
            id_field = PK_HINTS.get(target_table)
            ins, upd = migrate_table(source_schema, source_table, target_schema, target_table, id_field, DEFAULT_CHUNK)
            print(f"[migrate] done: {source_schema}.{source_table} -> {(target_schema or 'public')}.{target_table}: upserted={ins} (batch-count, not exact inserts)")
        except Exception as e:
            print(f"[migrate][ERROR] {source_schema}.{t}: {e}")
    print(f"Done. Total upserted rows (approx): {total}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
