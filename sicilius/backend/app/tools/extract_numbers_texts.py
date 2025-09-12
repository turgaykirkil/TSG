#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Numbers (.numbers) dosyasından OCR metinlerini otomatik bulup .txt dosyaları olarak dışa aktarır.

Örnek kullanım:
  python3 sicilius/backend/app/tools/extract_numbers_texts.py \
    --file sicilius/ocr_ciktilari/ocr_results_rows.numbers \
    --out-dir /tmp/sicilius_numbers_extract

İsteğe bağlı seçimler:
  --sheet-index N  (0-tabanlı)
  --table-index N  (0-tabanlı)
  --column-index N (0-tabanlı)

Varsayılan: En bilgin kolon (ilk ~200 satırın toplam karakter uzunluğuna göre) otomatik seçilir.
"""
from __future__ import annotations
import argparse
import os
import sys
from typing import Optional


def one_line(x) -> str:
    try:
        s = str(x)
    except Exception:
        s = ""
    return " ".join(s.splitlines())


def pick_best_column(table) -> int:
    rows = table.num_rows
    cols = table.num_cols
    best_c = 0
    best_score = -1
    max_rows = min(rows, 200)
    # Skoru: ilk 200 satırda metin uzunluğu toplamı
    for c in range(cols):
        score = 0
        for r in range(1, max_rows):  # 0. satır çoğunlukla başlık olabilir
            try:
                v = table.cell(r, c).value
            except Exception:
                v = None
            if v is not None:
                score += len(one_line(v))
        if score > best_score:
            best_score = score
            best_c = c
    return best_c


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True)
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--sheet-index", type=int, default=None)
    parser.add_argument("--table-index", type=int, default=None)
    parser.add_argument("--column-index", type=int, default=None)
    args = parser.parse_args()

    try:
        from numbers_parser import Document
    except ImportError:
        print("Hata: numbers-parser paketi kurulu değil. Lütfen: pip3 install numbers-parser", file=sys.stderr)
        sys.exit(2)

    if not os.path.exists(args.file):
        print(f"Hata: dosya yok: {args.file}", file=sys.stderr)
        sys.exit(2)

    os.makedirs(args.out_dir, exist_ok=True)

    doc = Document(args.file)
    sheets = doc.sheets
    if not sheets:
        print("Hata: sheet bulunamadı", file=sys.stderr)
        sys.exit(2)

    s_idx = args.sheet_index if args.sheet_index is not None else 0
    if s_idx < 0 or s_idx >= len(sheets):
        print(f"Hata: sheet-index geçersiz: {s_idx}", file=sys.stderr)
        sys.exit(2)

    sheet = sheets[s_idx]
    tables = sheet.tables
    if not tables:
        print("Hata: tablolar yok", file=sys.stderr)
        sys.exit(2)

    t_idx = args.table_index if args.table_index is not None else 0
    if t_idx < 0 or t_idx >= len(tables):
        print(f"Hata: table-index geçersiz: {t_idx}", file=sys.stderr)
        sys.exit(2)

    table = tables[t_idx]

    c_idx = args.column_index
    if c_idx is None:
        c_idx = pick_best_column(table)

    rows = table.num_rows
    exported = 0
    for r in range(rows):
        try:
            v = table.cell(r, c_idx).value
        except Exception:
            v = None
        if v is None:
            continue
        txt = str(v)
        if not txt.strip():
            continue
        exported += 1
        fp = os.path.join(args.out_dir, f"row-{exported}.txt")
        with open(fp, "w", encoding="utf-8", errors="ignore") as f:
            f.write(txt)

    meta = {
        "selected": {
            "sheet_index": s_idx,
            "table_index": t_idx,
            "column_index": c_idx,
            "rows": rows,
            "exported": exported,
        }
    }
    print(meta)


if __name__ == "__main__":
    main()
