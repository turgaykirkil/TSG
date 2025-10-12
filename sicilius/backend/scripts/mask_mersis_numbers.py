import os
import re
import argparse
from typing import Optional, Tuple
from dotenv import load_dotenv
from sqlalchemy import create_engine, text


def load_db_url() -> str:
    load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))
    url = (
        os.getenv("TSG_DATABASE_URL")
        or os.getenv("DATABASE_URL")
        or ""
    )
    if not url:
        raise SystemExit("TSG_DATABASE_URL/DATABASE_URL bulunamadı")
    return url


def only_digits(s: str) -> str:
    return re.sub(r"\D+", "", s or "")


def mask_mersis(raw: Optional[str]) -> Tuple[Optional[str], bool]:
    if not raw:
        return raw, False
    d = only_digits(raw)
    if len(d) != 16:
        return raw, False
    if d[0] == "0":
        return raw, False
    masked = list(d)
    for i in range(3, 8):
        masked[i] = "*"
    return ("".join(masked), True)


def process_ocr_results(conn, apply: bool, limit: Optional[int]) -> Tuple[int, int]:
    sel_sql = """
        SELECT id, mersis_no
        FROM public.ocr_results
        WHERE mersis_no IS NOT NULL
        ORDER BY id
        {limit}
    """.format(limit=f"LIMIT {int(limit)}" if limit else "")
    rows = list(conn.execute(text(sel_sql)))
    changed = 0
    for r in rows:
        new_val, ok = mask_mersis(r.mersis_no)
        if ok and new_val != r.mersis_no:
            changed += 1
            if apply:
                conn.execute(
                    text("UPDATE public.ocr_results SET mersis_no = :v WHERE id = :id"),
                    {"v": new_val, "id": r.id},
                )
    return len(rows), changed


def process_companies(conn, apply: bool, limit: Optional[int]) -> Tuple[int, int]:
    sel_sql = """
        SELECT id, mersis_number
        FROM public.companies
        WHERE mersis_number IS NOT NULL
        ORDER BY id
        {limit}
    """.format(limit=f"LIMIT {int(limit)}" if limit else "")
    rows = list(conn.execute(text(sel_sql)))
    changed = 0
    for r in rows:
        new_val, ok = mask_mersis(r.mersis_number)
        if ok and new_val != r.mersis_number:
            changed += 1
            if apply:
                conn.execute(
                    text("UPDATE public.companies SET mersis_number = :v WHERE id = :id"),
                    {"v": new_val, "id": r.id},
                )
    return len(rows), changed


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--target", choices=["ocr_results", "companies", "both"], default="ocr_results")
    ap.add_argument("--limit", type=int)
    ap.add_argument("--include-companies", action="store_true")
    args = ap.parse_args()

    if args.target in ("companies", "both") and not args.include_companies and not args.apply:
        pass

    url = load_db_url()
    engine = create_engine(url)
    with engine.begin() as conn:
        total_scanned = 0
        total_changed = 0
        if args.target in ("ocr_results", "both"):
            s, c = process_ocr_results(conn, args.apply, args.limit)
            total_scanned += s
            total_changed += c
        if args.target in ("companies", "both"):
            s, c = process_companies(conn, args.apply, args.limit)
            total_scanned += s
            total_changed += c
    print({"scanned": total_scanned, "changed": total_changed, "applied": args.apply})


if __name__ == "__main__":
    main()
