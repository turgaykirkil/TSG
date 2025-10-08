#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Re-parse OCR pages (offline evaluation) via the running backend at http://localhost:5001
without writing to DB. It uses the MINIMAL parse endpoint, which only returns structured
items and does not persist.

Usage (example):
  python reparse_minimal_5001.py \
    --ocr-dir \
      /Users/turgaykirkil/Documents/Applications/TSG_Platform/sicilius/ocr_ciktilari \
    --max-samples 100 \
    --out-dir \
      /Users/turgaykirkil/Documents/Applications/TSG_Platform/sicilius/ocr_eval_out

Outputs (created if not exist):
  - samples.jsonl       : One JSON object per line {id, path, size, text_len}
  - parsed_minimal.jsonl: One JSON object per line {id, path, segments_count, items}
  - summary.txt         : Plain text quick summary

Notes:
  - The script never writes to your database. It calls /api/v1/nlp/parse-announcements-minimal
    which returns items and DOES NOT persist.
  - Large files are prioritized by size to better represent full-page OCR.
  - Supports both .txt and .json OCR outputs. For JSON, uses `original_text_full` if present,
    otherwise concatenates `results[].original_text`.
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple

try:
    import requests
except Exception:
    print("This script requires the 'requests' package. Install with: pip install requests", file=sys.stderr)
    sys.exit(2)

API_URL_DEFAULT = "http://localhost:5001/api/v1/nlp/parse-announcements-minimal"


def iter_ocr_files(root: Path) -> List[Tuple[Path, int]]:
    """Return a list of (path, size) for candidate OCR files under root.
    Considers both .txt and .json files.
    """
    out: List[Tuple[Path, int]] = []
    patterns = ["*.txt", "*.json"]
    for pat in patterns:
        for p in root.rglob(pat):
            try:
                sz = p.stat().st_size
            except Exception:
                continue
            if sz <= 0:
                continue
            out.append((p, sz))
    # Largest first
    out.sort(key=lambda x: x[1], reverse=True)
    return out


def read_text(path: Path, max_len: int = 800_000) -> Optional[str]:
    try:
        with path.open("r", encoding="utf-8", errors="ignore") as f:
            t = f.read(max_len)
        return t
    except Exception:
        return None


def read_json_text(path: Path, max_len: int = 800_000) -> Optional[str]:
    """Extract page-level text from a JSON OCR output.
    Prefers `original_text_full`, else concatenates `results[].original_text`.
    """
    try:
        with path.open("r", encoding="utf-8", errors="ignore") as f:
            data = json.load(f)
    except Exception:
        return None
    # Prefer full
    txt = None
    if isinstance(data, dict):
        txt = data.get("original_text_full")
        if not txt and isinstance(data.get("results"), list):
            parts: List[str] = []
            for it in data["results"]:
                if isinstance(it, dict):
                    t0 = it.get("original_text")
                    if isinstance(t0, str) and t0.strip():
                        parts.append(t0)
            if parts:
                txt = "\n\n".join(parts)
    if not isinstance(txt, str):
        return None
    # Truncate safely
    if len(txt) > max_len:
        txt = txt[:max_len]
    return txt


def read_ocr_any(path: Path, max_len: int = 800_000) -> Optional[str]:
    if path.suffix.lower() == ".json":
        return read_json_text(path, max_len=max_len)
    return read_text(path, max_len=max_len)


def call_minimal_api(text: str, api_url: str, timeout: float = 60.0) -> List[Dict[str, Any]]:
    payload = {"text": text}
    headers = {"Content-Type": "application/json"}
    for attempt in range(3):
        try:
            r = requests.post(api_url, headers=headers, json=payload, timeout=timeout)
            if r.status_code == 200:
                data = r.json()
                if isinstance(data, list):
                    return data
                # If not a list, fallthrough to empty
                return []
            # Transient? small backoff
            time.sleep(0.5 * (attempt + 1))
        except Exception:
            time.sleep(0.5 * (attempt + 1))
    return []


def ensure_out_dir(out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)


def write_jsonl(path: Path, rows: List[Dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def main():
    parser = argparse.ArgumentParser(description="Re-parse OCR via localhost:5001 minimal endpoint (no DB writes)")
    parser.add_argument("--ocr-dir", required=True, help="Directory containing OCR outputs (.txt or .json)")
    parser.add_argument("--max-samples", type=int, default=100, help="Max number of pages to evaluate (default: 100)")
    parser.add_argument("--api-url", default=API_URL_DEFAULT, help=f"Parse endpoint (default: {API_URL_DEFAULT})")
    parser.add_argument("--out-dir", required=True, help="Output directory for JSONL and summary")
    args = parser.parse_args()

    ocr_dir = Path(args.ocr_dir)
    out_dir = Path(args.out_dir)
    ensure_out_dir(out_dir)

    if not ocr_dir.exists() or not ocr_dir.is_dir():
        print(f"[ERR] ocr-dir not found or not a directory: {ocr_dir}", file=sys.stderr)
        sys.exit(1)

    candidates = iter_ocr_files(ocr_dir)
    if not candidates:
        print(f"[ERR] No .txt/.json OCR files found under {ocr_dir}", file=sys.stderr)
        sys.exit(1)

    picked = candidates[: max(1, args.max_samples)]

    samples_rows: List[Dict[str, Any]] = []
    parsed_rows: List[Dict[str, Any]] = []

    for idx, (path, sz) in enumerate(picked, start=1):
        text = read_ocr_any(path)
        if not text or len(text.strip()) < 50:
            continue
        samples_rows.append({
            "id": idx,
            "path": str(path),
            "size": sz,
            "text_len": len(text or ""),
        })
        items = call_minimal_api(text, args.api_url)
        parsed_rows.append({
            "id": idx,
            "path": str(path),
            "segments_count": len(items),
            "items": items,
        })
        print(f"[{idx}/{len(picked)}] {path.name}: segments={len(items)}")

    write_jsonl(out_dir / "samples.jsonl", samples_rows)
    write_jsonl(out_dir / "parsed_minimal.jsonl", parsed_rows)

    # Summary
    total_pages = len(samples_rows)
    total_segments = sum(r.get("segments_count", 0) for r in parsed_rows)
    with (out_dir / "summary.txt").open("w", encoding="utf-8") as f:
        f.write(f"pages={total_pages}\n")
        f.write(f"total_segments={total_segments}\n")
        if total_pages:
            f.write(f"avg_segments_per_page={total_segments / max(1, total_pages):.2f}\n")
        f.write(f"api_url={args.api_url}\n")
        f.write(f"ocr_dir={ocr_dir}\n")

    print("\nDone.")
    print(f"samples.jsonl        => {out_dir / 'samples.jsonl'}")
    print(f"parsed_minimal.jsonl => {out_dir / 'parsed_minimal.jsonl'}")
    print(f"summary.txt          => {out_dir / 'summary.txt'}")


if __name__ == "__main__":
    main()
