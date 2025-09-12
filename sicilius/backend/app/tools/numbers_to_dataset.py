#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Numbers (.numbers) dosyasından uzun metin sütununu otomatik tespit edip
JSONL ve .txt çıktısı üreten yardımcı araç.

Kullanım örnekleri:
  python -m app.tools.numbers_to_dataset --file \
    \
    /Users/turgaykirkil/Documents/Applications/TSG_Platform/sicilius/ocr_ciktilari/ocr_results_rows.numbers \
    --out-dir /tmp/sicilius_numbers_extract

Opsiyonel:
  --column-name "Metin"            # Sütun adı biliniyorsa
  --column-index 3                 # Veya indeks (0 tabanlı)
  --min-chars 120                  # Yalnızca en az 120 karakterlik metinleri al
  --limit 0                        # 0: limitsiz (varsayılan)

Çıktı yapısı:
  - {out-dir}/extract.jsonl        : Her satır bir kayıt
  - {out-dir}/txt/row_<seq>.txt    : Her kayıt için orijinal metni içeren .txt

Notlar:
  - Orijinal metin korunur (golden rules).
  - Sütun adı/indeksi verilmezse, otomatik seçim: medyan karakter
    uzunluğu en yüksek olan metin sütunu (eşik: >= 80).
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import asdict, dataclass
from statistics import median
from typing import Any, List, Optional, Tuple


def _require_numbers_parser():
    try:
        from numbers_parser import Document  # type: ignore
        return Document
    except Exception as e:
        print(
            "Hata: 'numbers-parser' paketi gerekli fakat bulunamadı.\n"
            "Kurulum: pip install numbers-parser\n"
            f"Ayrıntı: {e}",
            file=sys.stderr,
        )
        sys.exit(2)


@dataclass
class ExtractedRow:
    sheet: str
    table: str
    row_index: int
    column_index: int
    column_name: str
    text: str


def _slugify(text: str, max_len: int = 50) -> str:
    t = re.sub(r"\s+", " ", text).strip()
    t = t[:max_len]
    t = t.lower()
    t = re.sub(r"[^a-z0-9çğıöşü\-_. ]", "", t)
    t = t.replace(" ", "-")
    t = re.sub(r"-+", "-", t)
    return t or "row"


def _iter_cells_rows(table) -> List[List[Any]]:
    # numbers_parser API uyumluluğu: rows() varsa kullan, yoksa cell erişimiyle oluştur
    rows = []
    try:
        # Newer API
        for row in table.rows():
            # row.cells -> list of Cell
            rows.append([getattr(c, "value", None) for c in row.cells])
        return rows
    except Exception:
        pass

    # Fallback
    try:
        num_rows = table.num_rows
        num_cols = table.num_cols
    except Exception:
        # Son çare: hiçbir şey yapma
        return rows

    for r in range(num_rows):
        current = []
        for c in range(num_cols):
            try:
                current.append(table.cell(r, c).value)
            except Exception:
                current.append(None)
        rows.append(current)
    return rows


def _get_header(table, rows: List[List[Any]]) -> Tuple[List[str], int]:
    # numbers genelde ilk satırı başlık; header_rows varsa ona bak
    header_row_count = 0
    try:
        header_row_count = int(getattr(table, "header_rows", 0) or 0)
    except Exception:
        header_row_count = 0

    if header_row_count >= 1 and len(rows) >= header_row_count:
        header = [str(x) if x is not None else f"col_{i}" for i, x in enumerate(rows[header_row_count - 1])]
        data_start = header_row_count
        return header, data_start

    # Fallback: ilk satırı başlık kabul et
    if rows:
        header = [str(x) if x is not None else f"col_{i}" for i, x in enumerate(rows[0])]
        return header, 1

    return [], 0


def _auto_detect_text_column(rows: List[List[Any]], header: List[str], data_start: int, min_len_threshold: int) -> Optional[int]:
    if not rows or data_start >= len(rows):
        return None
    num_cols = max((len(r) for r in rows), default=0)

    candidates = []  # (median_len, col_index)
    for c in range(num_cols):
        lengths = []
        for r in rows[data_start:]:
            if c >= len(r):
                continue
            v = r[c]
            if isinstance(v, str):
                s = v.strip()
                if s:
                    lengths.append(len(s))
        if lengths:
            med = median(lengths)
            candidates.append((med, c))

    if not candidates:
        return None

    # En yüksek medyana sahip sütun + eşiği geçmeli
    candidates.sort(reverse=True)
    best_med, best_col = candidates[0]
    if best_med >= max(80, min_len_threshold):
        return best_col
    return None


def _coerce_int(val: Optional[str]) -> Optional[int]:
    if val is None:
        return None
    try:
        v = int(val)
        if v < 0:
            return None
        return v
    except Exception:
        return None


def extract_from_numbers(file_path: str, out_dir: str, column_name: Optional[str], column_index: Optional[int], min_chars: int, limit: Optional[int]) -> Tuple[int, int]:
    Document = _require_numbers_parser()
    doc = Document(file_path)

    os.makedirs(out_dir, exist_ok=True)
    txt_dir = os.path.join(out_dir, "txt")
    os.makedirs(txt_dir, exist_ok=True)
    jsonl_path = os.path.join(out_dir, "extract.jsonl")

    total_rows = 0
    written = 0

    with open(jsonl_path, "w", encoding="utf-8") as jout:
        for sheet in getattr(doc, "sheets", []):
            sheet_name = getattr(sheet, "name", "Sheet")
            for table in getattr(sheet, "tables", []):
                table_name = getattr(table, "name", "Table")
                rows = _iter_cells_rows(table)
                if not rows:
                    continue

                header, data_start = _get_header(table, rows)
                # Kolon belirleme
                col_idx = None
                col_title = ""
                if column_index is not None:
                    col_idx = column_index
                    col_title = header[col_idx] if 0 <= col_idx < len(header) else f"col_{col_idx}"
                elif column_name is not None:
                    lowered = [str(h).strip().lower() for h in header]
                    try:
                        col_idx = lowered.index(column_name.strip().lower())
                        col_title = header[col_idx]
                    except ValueError:
                        pass
                if col_idx is None:
                    col_idx = _auto_detect_text_column(rows, header, data_start, min_chars)
                    if col_idx is not None:
                        col_title = header[col_idx] if 0 <= col_idx < len(header) else f"col_{col_idx}"

                if col_idx is None:
                    print(
                        f"Uyarı: {sheet_name}/{table_name} için uygun metin sütunu bulunamadı.",
                        file=sys.stderr,
                    )
                    continue

                # Satırlar
                for i, r in enumerate(rows[data_start:], start=data_start):
                    if limit is not None and written >= limit:
                        break
                    v = r[col_idx] if col_idx < len(r) else None
                    if not isinstance(v, str):
                        continue
                    s = v.strip()
                    if len(s) < min_chars:
                        continue

                    rec = ExtractedRow(
                        sheet=sheet_name,
                        table=table_name,
                        row_index=i,
                        column_index=col_idx,
                        column_name=col_title,
                        text=s,
                    )
                    # JSONL yaz
                    jout.write(json.dumps(asdict(rec), ensure_ascii=False) + "\n")

                    # TXT yaz (orijinal metin)
                    fname = f"row_{written+1:06d}_{_slugify(s)}.txt"
                    with open(os.path.join(txt_dir, fname), "w", encoding="utf-8") as tf:
                        tf.write(s)

                    written += 1
                    total_rows += 1
                # limit kontrolü dış döngü kırma
                if limit is not None and written >= limit:
                    break
            if limit is not None and written >= limit:
                break

    return total_rows, written


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", required=True, help=".numbers dosyası")
    ap.add_argument("--out-dir", required=True, help="Çıktı klasörü")
    ap.add_argument("--column-name", default=None, help="Metin sütunu adı (opsiyonel)")
    ap.add_argument("--column-index", type=int, default=None, help="Metin sütunu indeks (0 tabanlı, opsiyonel)")
    ap.add_argument("--min-chars", type=int, default=100, help="Satır metni minimum karakter uzunluğu")
    ap.add_argument("--limit", type=int, default=None, help="İlk N kaydı işle (0 veya None = limitsiz)")
    args = ap.parse_args()

    limit = _coerce_int(str(args.limit)) if args.limit is not None else None
    if limit == 0:
        limit = None

    if not os.path.isfile(args.file):
        print(f"Hata: Dosya bulunamadı: {args.file}", file=sys.stderr)
        sys.exit(2)

    total_rows, written = extract_from_numbers(
        file_path=args.file,
        out_dir=args.out_dir,
        column_name=args.column_name,
        column_index=args.column_index,
        min_chars=args.min_chars,
        limit=limit,
    )

    # Özet
    print(
        json.dumps(
            {
                "status": "ok",
                "source": args.file,
                "out_dir": args.out_dir,
                "txt_dir": os.path.join(args.out_dir, "txt"),
                "jsonl": os.path.join(args.out_dir, "extract.jsonl"),
                "min_chars": args.min_chars,
                "processed_rows": total_rows,
                "written": written,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
