import os
import sys
import json
from typing import List, Dict, Optional, Set

from sqlalchemy import create_engine, MetaData, Table, text
from sqlalchemy.engine import Engine

from app.db.session import engine as default_engine
from app.db.base import Base
from app import models  # noqa

EXCLUDE_COLUMNS: Dict[str, Set[str]] = {
    "companies": {"koordinat"},
}

def reflect(engine: Engine, schema: Optional[str], table: str):
    md = MetaData()
    tbl = Table(table, md, schema=schema, autoload_with=engine)
    return tbl, {c.name for c in tbl.columns}


def build_upsert_sql(schema: Optional[str], table: str, columns: List[str], pk: str) -> str:
    fq = f'"{schema}"."{table}"' if schema else f'"{table}"'
    cols = ", ".join([f'"{c}"' for c in columns])
    vals = ", ".join([f':{c}' for c in columns])
    set_sql = ", ".join([f'"{c}" = EXCLUDED."{c}"' for c in columns if c != pk])
    return f"INSERT INTO {fq} ({cols}) VALUES ({vals}) ON CONFLICT (\"{pk}\") DO UPDATE SET {set_sql}"


def load_ndjson(file_path: str, target: str, pk: str) -> int:
    dest_url = os.environ.get("DEST_DATABASE_URL")
    engine = create_engine(dest_url, pool_pre_ping=True) if dest_url else default_engine
    Base.metadata.create_all(bind=engine)

    if "." in target:
        schema, table = target.split(".", 1)
    else:
        schema, table = None, target

    tbl, cols = reflect(engine, schema, table)
    excluded = EXCLUDE_COLUMNS.get(table, set())
    cols = [c for c in cols if c not in excluded]
    if pk not in cols:
        cols = [pk] + cols

    sql = build_upsert_sql(schema, table, cols, pk)

    count = 0
    batch: List[Dict] = []
    BATCH_SIZE = 2000

    def flush():
        nonlocal batch, count
        if not batch:
            return
        with engine.begin() as conn:
            conn.execute(text(sql), batch)
        count += len(batch)
        batch = []

    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            obj = json.loads(line)
            row = {k: v for k, v in obj.items() if k in cols}
            # Ensure all columns present
            for c in cols:
                if c not in row:
                    row[c] = None
            batch.append(row)
            if len(batch) >= BATCH_SIZE:
                flush()
        flush()
    return count


def main(argv: List[str]) -> int:
    if len(argv) < 3:
        print("Usage: load_ndjson_to_table.py <file_path> <schema.table> [pk=id]", file=sys.stderr)
        return 2
    file_path = argv[1]
    target = argv[2]
    pk = argv[3] if len(argv) > 3 else "id"
    n = load_ndjson(file_path, target, pk)
    print(f"Loaded {n} rows into {target}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
