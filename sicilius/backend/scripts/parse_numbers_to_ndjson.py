# -*- coding: utf-8 -*-
"""
Numbers (.numbers) dosyasından OCR ham ilan metinlerini okuyup
regex tabanlı ayrıştırıcı ile NDJSON çıktısı üretir.

Kullanım:
  python scripts/parse_numbers_to_ndjson.py \
      --input "/path/to/ocr_results_rows.numbers" \
      --out "/path/to/out.ndjson" \
      [--text-col "Metin"] [--id-col "ID"]

Notlar:
- Veri kaybını önlemek için her kaydın ham metni 'raw_text' alanında korunur.
- Metin sütunu otomatik tespit: Bilinen başlıklar veya yüksek ortalama uzunluk.
"""
from __future__ import annotations
import argparse
import os
from typing import List, Tuple, Optional

from numbers_parser import Document  # pip install numbers-parser

from app.nlp.segmenter import parse_document, dump_json


TEXT_CANDIDATE_HEADERS = {
    "text",
    "metin",
    "ilan",
    "ocr_text",
    "ocr",
    "content",
    "body",
    "ilan_metin",
}
ID_CANDIDATE_HEADERS = {"id", "doc_id", "row_id", "kayit", "kayıt", "no"}


def detect_columns(rows: List[list], text_col_arg: Optional[str], id_col_arg: Optional[str]) -> Tuple[int, Optional[int]]:
    if not rows:
        raise ValueError("Boş tablo: satır bulunamadı.")
    headers = [str(c.value) if hasattr(c, "value") else str(c) for c in rows[0]]
    header_lc = [h.strip().lower() for h in headers]

    # Text column from arg
    if text_col_arg:
        tl = text_col_arg.strip().lower()
        if tl in header_lc:
            return header_lc.index(tl), (header_lc.index(id_col_arg.strip().lower()) if id_col_arg and id_col_arg.strip().lower() in header_lc else None)
        else:
            raise ValueError(f"Belirtilen text sütunu bulunamadı: {text_col_arg}")

    # Try known headers
    for i, h in enumerate(header_lc):
        if h in TEXT_CANDIDATE_HEADERS:
            id_idx = None
            if id_col_arg and id_col_arg.strip().lower() in header_lc:
                id_idx = header_lc.index(id_col_arg.strip().lower())
            else:
                for j, hh in enumerate(header_lc):
                    if hh in ID_CANDIDATE_HEADERS:
                        id_idx = j
                        break
            return i, id_idx

    # Heuristic: pick column with highest average string length on sample
    best_i, best_score = 0, -1.0
    for i in range(len(headers)):
        lens = []
        for r in rows[1: min(len(rows), 100)]:
            try:
                v = r[i].value if hasattr(r[i], "value") else r[i]
            except IndexError:
                v = None
            if isinstance(v, str):
                lens.append(len(v))
        score = sum(lens) / max(1, len(lens))
        if score > best_score:
            best_i, best_score = i, score

    # id index
    id_idx = None
    for j, hh in enumerate(header_lc):
        if hh in ID_CANDIDATE_HEADERS:
            id_idx = j
            break

    return best_i, id_idx


def read_numbers(input_path: str) -> List[list]:
    doc = Document(input_path)
    if not doc.sheets:
        raise ValueError(".numbers dosyasında sheet bulunamadı")
    sheet = doc.sheets[0]
    if not sheet.tables:
        raise ValueError("İlk sheet içerisinde tablo bulunamadı")
    table = sheet.tables[0]
    rows = table.rows()
    if not rows:
        raise ValueError("Tabloda satır bulunamadı")
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, help="Kaynak .numbers dosyası")
    ap.add_argument("--out", required=True, help="NDJSON çıktı yolu")
    ap.add_argument("--text-col", default=None, help="Metin sütunu adı (opsiyonel)")
    ap.add_argument("--id-col", default=None, help="ID sütunu adı (opsiyonel)")
    args = ap.parse_args()

    if not os.path.exists(args.input):
        raise SystemExit(f"Girdi dosyası yok: {args.input}")

    rows = read_numbers(args.input)
    text_idx, id_idx = detect_columns(rows, args.text_col, args.id_col)

    headers = [str(c.value) if hasattr(c, "value") else str(c) for c in rows[0]]

    count, wrote = 0, 0
    with open(args.out, "w", encoding="utf-8") as f:
        for ridx, row in enumerate(rows[1:], start=1):
            try:
                val = row[text_idx].value if hasattr(row[text_idx], "value") else row[text_idx]
            except IndexError:
                continue
            if not isinstance(val, str) or not val.strip():
                continue
            doc_id = None
            if id_idx is not None:
                try:
                    idv = row[id_idx].value if hasattr(row[id_idx], "value") else row[id_idx]
                    if idv is not None:
                        doc_id = str(idv)
                except IndexError:
                    pass
            if doc_id is None:
                doc_id = f"row-{ridx}"

            rec = parse_document(val, meta={"doc_id": doc_id, "headers": headers})
            f.write(dump_json(rec) + "\n")
            wrote += 1
            count += 1

    print(f"Tamamlandı. Yazılan kayıt: {wrote}")


if __name__ == "__main__":
    main()
