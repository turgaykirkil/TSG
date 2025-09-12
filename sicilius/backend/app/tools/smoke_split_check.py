#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hızlı smoke test: split_announcements_with_offsets() sonuçlarının doğruluğunu
kontrol eder.

- raw_text slice tutarlılığı: raw_text == full_text[start:end]
- Header dahil mi: segment'in ilk dolu satırı normalize edildiğinde MUDUR/MEMURLU
  ve NDEN/NDAN içeriyor mu?

Kullanım:
  python -m app.tools.smoke_split_check --input-file /path/to/ocr.txt [--print-failures]
"""
from __future__ import annotations

import argparse
import json
import os
from importlib.machinery import SourceFileLoader
from typing import Dict, Any, List

# nlp_service import (dinamik)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "services"))
NLP_PATH = os.path.join(BASE_DIR, "nlp_service.py")
ns = SourceFileLoader("nlp_service", NLP_PATH).load_module()


def read_text_file(fp: str) -> str:
    with open(fp, "r", encoding="utf-8", errors="replace") as f:
        return f.read()


def analyze(text: str, print_failures: bool = False) -> Dict[str, Any]:
    segs: List[Dict[str, Any]] = ns.split_announcements_with_offsets(text)

    def header_ok(seg_text: str) -> bool:
        # İlk dolu satırı al ve normalize et
        for ln in seg_text.splitlines():
            s = ln.strip()
            if not s:
                continue
            norm = ns._normalize_tr_for_header(s)  # type: ignore[attr-defined]
            if not norm:
                continue
            has_core = ("TICARET" in norm and "SICIL" in norm and ("MUDUR" in norm or "MEMURLU" in norm))
            has_suffix = (norm.endswith("NDEN") or norm.endswith("NDAN") or " NDEN" in norm or " NDAN" in norm)
            return bool(has_core and has_suffix)
        return False

    raw_slice_mismatch_idx: List[int] = []
    header_missing_idx: List[int] = []

    for i, sg in enumerate(segs, start=1):
        start = sg.get("start")
        end = sg.get("end")
        raw = sg.get("raw_text")
        if isinstance(start, int) and isinstance(end, int) and isinstance(raw, str):
            if raw != text[start:end]:
                raw_slice_mismatch_idx.append(i)
        else:
            raw_slice_mismatch_idx.append(i)

        if not header_ok(sg.get("text") or ""):
            header_missing_idx.append(i)

    report = {
        "segment_count": len(segs),
        "raw_slice_match_count": len(segs) - len(raw_slice_mismatch_idx),
        "header_included_count": len(segs) - len(header_missing_idx),
        "raw_slice_mismatch_indices": raw_slice_mismatch_idx[:20],
        "header_missing_indices": header_missing_idx[:20],
    }

    if print_failures:
        report["examples"] = []
        for idx in (raw_slice_mismatch_idx[:3] + header_missing_idx[:3]):
            if 1 <= idx <= len(segs):
                sg = segs[idx - 1]
                report["examples"].append({
                    "index": idx,
                    "start": sg.get("start"),
                    "end": sg.get("end"),
                    "first_line": next((ln.strip() for ln in (sg.get("text") or "").splitlines() if ln.strip()), ""),
                })

    return report


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input-file", required=True, help="Tek bir OCR .txt dosyası")
    p.add_argument("--print-failures", action="store_true", help="Başarısız örnekleri rapora ekle")
    args = p.parse_args()

    if not os.path.isfile(args.input_file):
        raise SystemExit(f"Dosya bulunamadı: {args.input_file}")

    text = read_text_file(args.input_file)
    report = analyze(text, args.print_failures)
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
