#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Export problem-period OCR samples from Supabase (read-only) as plain text files, then
use them with reparse_minimal_5001.py to evaluate segmentation.

- Filters: last N days (default: 14), original_text not null.
- Post-filter client-side for (out_of_bounds OR missing_offsets) and length priority.

Env vars required:
  SUPABASE_URL   e.g. https://xxxx.supabase.co
  SUPABASE_ANON  anon key with read access

Usage:
  python export_problem_samples.py \
    --days 14 \
    --limit 100 \
    --out-dir \
      /Users/turgaykirkil/Documents/Applications/TSG_Platform/sicilius/ocr_eval_in
"""

import argparse
import os
import sys
import json
from pathlib import Path
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List

try:
    import requests
except Exception:
    print("This script requires 'requests'. Install with: pip install requests", file=sys.stderr)
    sys.exit(2)


def iso_utc(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def fetch_candidates(api_url: str, anon_key: str, since_iso: str, page_size: int = 1000) -> List[Dict[str, Any]]:
    url = f"{api_url}/rest/v1/ocr_results"
    params = {
        "select": "id,created_at,original_text,start_offset,end_offset",
        "created_at": f"gte.{since_iso}",
        "original_text": "not.is.null",
        "order": "created_at.desc",
        "limit": str(page_size),
    }
    headers = {
        "apikey": anon_key,
        "Authorization": f"Bearer {anon_key}",
        "Accept": "application/json",
    }
    r = requests.get(url, headers=headers, params=params, timeout=60)
    if r.status_code != 200:
        print(f"[ERR] Supabase fetch failed: {r.status_code} {r.text[:200]}", file=sys.stderr)
        return []
    try:
        data = r.json()
        if isinstance(data, list):
            return data
    except Exception:
        pass
    return []


def is_problem(row: Dict[str, Any]) -> bool:
    txt = row.get("original_text")
    if not isinstance(txt, str) or not txt.strip():
        return False
    start = row.get("start_offset")
    end = row.get("end_offset")
    if start is None or end is None:
        return True
    # out_of_bounds check
    try:
        if isinstance(start, int) and isinstance(end, int) and end > len(txt):
            return True
    except Exception:
        pass
    return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=14)
    ap.add_argument("--limit", type=int, default=100)
    ap.add_argument("--out-dir", required=True)
    args = ap.parse_args()

    supa_url = os.environ.get("SUPABASE_URL", "").strip()
    supa_anon = os.environ.get("SUPABASE_ANON", "").strip()
    if not supa_url or not supa_anon:
        print("[ERR] SUPABASE_URL and SUPABASE_ANON must be set in environment", file=sys.stderr)
        sys.exit(1)

    since = datetime.now(timezone.utc) - timedelta(days=args.days)
    since_iso = iso_utc(since)

    rows = fetch_candidates(supa_url, supa_anon, since_iso, page_size=1000)
    if not rows:
        print("[WARN] No rows fetched from Supabase. Exiting.")
        return

    # Client-side filtering and prioritization
    problems = [r for r in rows if is_problem(r)]
    if not problems:
        print("[WARN] No problem rows matched filters. Will fallback to longest texts.")
        problems = rows

    # Sort by text length desc
    for r in problems:
        t = r.get("original_text")
        r["_len"] = len(t) if isinstance(t, str) else 0
    problems.sort(key=lambda x: x.get("_len", 0), reverse=True)

    picked = problems[: max(1, args.limit)]

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    meta: List[Dict[str, Any]] = []
    for i, r in enumerate(picked, start=1):
        rid = r.get("id")
        txt = r.get("original_text") or ""
        p = out_dir / f"page_{rid or i}.txt"
        with p.open("w", encoding="utf-8") as f:
            f.write(txt)
        meta.append({"id": rid, "path": str(p), "len": len(txt)})
        print(f"[{i}/{len(picked)}] wrote {p.name} len={len(txt)}")

    with (out_dir / "_meta.json").open("w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)

    print(f"Done. Wrote {len(picked)} samples to {out_dir}")


if __name__ == "__main__":
    main()
