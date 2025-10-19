import argparse
import json
import os
import sys
from typing import Any, Dict, Iterable, List, Optional

from sqlalchemy import create_engine, text
from sqlalchemy.engine import CursorResult

from app.core.config import settings


def _ensure_dir(path: str) -> None:
    d = os.path.dirname(os.path.abspath(path))
    if d and not os.path.exists(d):
        os.makedirs(d, exist_ok=True)


def _sanitize(v: Any) -> Any:
    try:
        import datetime as _dt
        from decimal import Decimal as _Dec
        import uuid as _uuid
    except Exception:
        _dt = None  # type: ignore
        _Dec = None  # type: ignore
        _uuid = None  # type: ignore
    if v is None:
        return None
    if _uuid is not None and isinstance(v, _uuid.UUID):
        return str(v)
    if _Dec is not None and isinstance(v, _Dec):
        return float(v)
    if isinstance(v, bytes):
        return v.decode("utf-8", errors="ignore")
    # datetime/date
    try:
        if isinstance(v, (_dt.datetime, _dt.date)):  # type: ignore[attr-defined]
            return v.isoformat()
    except Exception:
        pass
    return v


def _sanitize_row(row: Dict[str, Any]) -> Dict[str, Any]:
    out: Dict[str, Any] = {}
    for k, v in row.items():
        if isinstance(v, dict):
            out[k] = {kk: _sanitize(vv) for kk, vv in v.items()}
        elif isinstance(v, list):
            out[k] = [({kk: _sanitize(vv) for kk, vv in x.items()} if isinstance(x, dict) else _sanitize(x)) for x in v]
        else:
            out[k] = _sanitize(v)
    return out


def export_keyset(schema: str, table: str, out_path: str, columns: str, id_column: str, batch: int, start_after_id: Optional[str], where_sql: Optional[str]) -> int:
    engine = create_engine(str(settings.DATABASE_URL))
    total = 0
    last_id = start_after_id
    sel_cols = columns if columns.strip() else "*"

    with engine.connect() as conn, open(out_path, "a", encoding="utf-8") as f:
        while True:
            where_clauses: List[str] = []
            params: Dict[str, Any] = {"limit": batch}
            if last_id is not None:
                where_clauses.append(f"{id_column} > :last_id")
                params["last_id"] = last_id
            if where_sql:
                where_clauses.append(f"({where_sql})")
            where_block = (" where " + " and ".join(where_clauses)) if where_clauses else ""
            sql = text(
                f"select {sel_cols} from {schema}.{table}{where_block} order by {id_column} asc limit :limit"
            )
            res: CursorResult = conn.execute(sql, params)
            rows = list(res.mappings().all())
            if not rows:
                break
            for r in rows:
                data = _sanitize_row(dict(r))
                f.write(json.dumps(data, ensure_ascii=False) + "\n")
                total += 1
                last_id = r[id_column]
            if len(rows) < batch:
                break
    return total


def export_offset(schema: str, table: str, out_path: str, columns: str, order_column: str, batch: int, where_sql: Optional[str], start_offset: int) -> int:
    engine = create_engine(str(settings.DATABASE_URL))
    total = 0
    offset = start_offset
    sel_cols = columns if columns.strip() else "*"

    with engine.connect() as conn, open(out_path, "a", encoding="utf-8") as f:
        while True:
            where_block = f" where {where_sql}" if where_sql else ""
            sql = text(
                f"select {sel_cols} from {schema}.{table}{where_block} order by {order_column} asc offset :offset limit :limit"
            )
            res: CursorResult = conn.execute(sql, {"offset": offset, "limit": batch})
            rows = list(res.mappings().all())
            if not rows:
                break
            for r in rows:
                data = _sanitize_row(dict(r))
                f.write(json.dumps(data, ensure_ascii=False) + "\n")
                total += 1
            offset += len(rows)
            if len(rows) < batch:
                break
    return total


def main() -> None:
    p = argparse.ArgumentParser(description="Export Supabase(Postgres) table to NDJSON")
    p.add_argument("--schema", default="app")
    p.add_argument("--table", required=True)
    p.add_argument("--out", required=True, help="Output NDJSON file path")
    p.add_argument("--columns", default="*", help="Comma-separated columns or *")
    p.add_argument("--id-column", default="id", help="Keyset pagination column (comparable, e.g., numeric)")
    p.add_argument("--batch", type=int, default=1000)
    p.add_argument("--start-after-id", default=None, help="Keyset start id value (string ok)")
    p.add_argument("--where", default=None, help="Optional SQL where expression without 'where'")
    p.add_argument("--use-offset", action="store_true", help="Use offset/limit pagination instead of keyset")
    p.add_argument("--order-column", default="id", help="Order column when using offset pagination")
    p.add_argument("--start-offset", type=int, default=0, help="Start offset when using offset pagination")

    args = p.parse_args()
    _ensure_dir(args.out)

    if args.use_offset:
        total = export_offset(
            schema=args.schema,
            table=args.table,
            out_path=args.out,
            columns=args.columns,
            order_column=args.order_column,
            batch=args.batch,
            where_sql=args.where,
            start_offset=args.start_offset,
        )
    else:
        total = export_keyset(
            schema=args.schema,
            table=args.table,
            out_path=args.out,
            columns=args.columns,
            id_column=args.id_column,
            batch=args.batch,
            start_after_id=args.start_after_id,
            where_sql=args.where,
        )

    print(json.dumps({"exported": total, "table": f"{args.schema}.{args.table}", "out": os.path.abspath(args.out)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
