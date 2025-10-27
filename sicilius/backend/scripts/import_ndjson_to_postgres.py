import argparse
import json
import os
import time
import random
from typing import Any, Dict, List, Tuple, Set

from sqlalchemy import MetaData, Table, text
from sqlalchemy.engine import Engine

# Reuse project DB engine/config
from app.db.session import engine as db_engine


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Import NDJSON to Postgres with batch upsert and throttling")
    p.add_argument("--in", dest="in_path", required=True, help="Input NDJSON file path")
    p.add_argument("--table", required=True, help="Target table name (without schema)")
    p.add_argument("--schema", default="app", help="Target schema (default: app)")
    p.add_argument("--id-field", default="id", help="Primary key column for ON CONFLICT")
    p.add_argument("--write-batch", type=int, default=500)
    p.add_argument("--throttle", type=float, default=0.1)
    p.add_argument("--max-rows", type=int, default=0, help="Max rows to import in this run (0=all)")
    p.add_argument("--state", default=None, help="State file path for resume (default: <in>.state.json)")
    p.add_argument("--drop-field", action="append", default=None, help="Field to drop from documents (repeatable)")
    return p.parse_args()


def _load_state(path: str) -> Dict[str, Any]:
    if not os.path.exists(path):
        return {"lines_processed": 0, "migrated_count": 0, "last_id": None}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f) or {}
    except Exception:
        return {"lines_processed": 0, "migrated_count": 0, "last_id": None}


def _save_state(path: str, st: Dict[str, Any]) -> None:
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(st, f, ensure_ascii=False)
    except Exception:
        pass


def _reflect_table(engine: Engine, schema: str, table_name: str) -> Tuple[Table, Set[str]]:
    md = MetaData()
    tbl = Table(table_name, md, schema=schema, autoload_with=engine)
    col_names = {c.name for c in tbl.columns}
    return tbl, col_names


def _build_upsert_sql(schema: str, table: str, columns: List[str], id_field: str) -> str:
    cols_sql = ", ".join([f'"{c}"' for c in columns])
    vals_sql = ", ".join([f':{c}' for c in columns])
    update_cols = [c for c in columns if c != id_field]
    set_sql = ", ".join([f'"{c}" = EXCLUDED."{c}"' for c in update_cols])
    fqtn = f'"{schema}"."{table}"'
    return (
        f"INSERT INTO {fqtn} ({cols_sql}) VALUES ({vals_sql}) "
        f"ON CONFLICT (\"{id_field}\") DO UPDATE SET {set_sql}"
    )


def main() -> None:
    args = _parse_args()

    engine: Engine = db_engine
    table_name = args.table
    schema = args.schema
    id_field = args.id_field

    tbl, col_names = _reflect_table(engine, schema, table_name)
    if id_field not in col_names:
        raise SystemExit(f"id-field '{id_field}' is not a column of {schema}.{table_name}")

    state_path = args.state or (args.in_path + ".state.json")
    st = _load_state(state_path)
    lines_processed = int(st.get("lines_processed") or 0)
    migrated = int(st.get("migrated_count") or 0)

    written_this_run = 0
    batch_size = int(args.write_batch)
    throttle = float(args.throttle)
    max_rows = int(args.max_rows or 0)

    current_line_no = 0
    batch: List[Dict[str, Any]] = []
    union_keys: Set[str] = set()

    drop_fields = set(args.drop_field or [])

    with open(args.in_path, "r", encoding="utf-8") as f:
        for line in f:
            current_line_no += 1
            if current_line_no <= lines_processed:
                continue
            line = line.strip()
            if not line:
                continue
            data: Dict[str, Any] = json.loads(line)
            for fld in drop_fields:
                if fld in data:
                    del data[fld]
            # Ensure id field exists
            if id_field not in data or data[id_field] is None:
                continue
            # Filter to known columns
            filtered = {k: v for k, v in data.items() if k in col_names}
            # Guarantee id_field present
            filtered[id_field] = data[id_field]
            batch.append(filtered)
            union_keys.update(filtered.keys())

            if len(batch) >= batch_size:
                cols = sorted(union_keys | {id_field})
                cols = [c for c in cols if c in col_names]
                sql = _build_upsert_sql(schema, table_name, cols, id_field)
                params: List[Dict[str, Any]] = []
                for row in batch:
                    params.append({c: row.get(c) for c in cols})
                with engine.begin() as conn:
                    conn.execute(text(sql), params)
                migrated += len(batch)
                written_this_run += len(batch)
                lines_processed = current_line_no
                st = {
                    "lines_processed": lines_processed,
                    "migrated_count": migrated,
                    "last_id": batch[-1].get(id_field),
                }
                _save_state(state_path, st)
                batch = []
                union_keys = set()
                time.sleep(throttle + random.uniform(0, throttle * 0.5))
                if max_rows and written_this_run >= max_rows:
                    break

        if batch and (not max_rows or written_this_run < max_rows):
            cols = sorted(union_keys | {id_field})
            cols = [c for c in cols if c in col_names]
            sql = _build_upsert_sql(schema, table_name, cols, id_field)
            params = [{c: row.get(c) for c in cols} for row in batch]
            with engine.begin() as conn:
                conn.execute(text(sql), params)
            migrated += len(batch)
            written_this_run += len(batch)
            lines_processed = current_line_no
            st = {
                "lines_processed": lines_processed,
                "migrated_count": migrated,
                "last_id": batch[-1].get(id_field),
            }
            _save_state(state_path, st)
            batch = []
            union_keys = set()
            time.sleep(throttle + random.uniform(0, throttle * 0.5))

    print(json.dumps({
        "written_in_this_run": written_this_run,
        "migrated_total": migrated,
        "lines_processed": lines_processed,
        "state_file": os.path.abspath(state_path),
        "target": f"{schema}.{table_name}",
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
