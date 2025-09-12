#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Toplu parçalama değerlendirme aracı.

Kullanım örneği:
  python -m app.tools.batch_split_eval --input-dir /tmp/sicilius_numbers_extract --limit 100

Girdi formatı:
  --input-dir: İçinde .txt dosyaları olan bir klasör. Her .txt tek bir OCR metnidir.

Çıktılar:
  - Konsola özet metrikler
  - İsteğe bağlı: örnek başarısızlıklar (çok az/çok fazla segment vb.)
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import dataclass
from importlib.machinery import SourceFileLoader
from typing import List, Dict, Any

# nlp_service import
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "services"))
NLP_PATH = os.path.join(BASE_DIR, "nlp_service.py")
ns = SourceFileLoader("nlp_service", NLP_PATH).load_module()

@dataclass
class DocEval:
    path: str
    text_len: int
    seg_count: int
    seg_lengths: List[int]


def read_text_file(fp: str) -> str:
    with open(fp, "r", encoding="utf-8", errors="replace") as f:
        return f.read()


def iter_txt_files(input_dir: str):
    for name in sorted(os.listdir(input_dir)):
        if not name.lower().endswith(".txt"):
            continue
        yield os.path.join(input_dir, name)


def evaluate_dir(input_dir: str, limit: int | None = None) -> Dict[str, Any]:
    docs: List[DocEval] = []
    total = 0
    for fp in iter_txt_files(input_dir):
        if limit is not None and total >= limit:
            break
        total += 1
        txt = read_text_file(fp)
        segs = ns.split_announcements_with_offsets(txt)
        seg_lens = [len(s.get("text", "")) for s in segs]
        docs.append(DocEval(path=fp, text_len=len(txt), seg_count=len(segs), seg_lengths=seg_lens))

    # metrikler
    dist = {}
    for d in docs:
        dist[d.seg_count] = dist.get(d.seg_count, 0) + 1

    zero_segs = [d for d in docs if d.seg_count == 0]
    one_segs = [d for d in docs if d.seg_count == 1]
    many_segs = [d for d in docs if d.seg_count >= 2]

    # Örnekler: en kısa/uzun metinlerden örnekler seç (teşhis için)
    def head_paths(items, n=5):
        return [x.path for x in items[:n]]

    zero_paths = head_paths(sorted(zero_segs, key=lambda x: x.text_len, reverse=True))
    many_paths = head_paths(sorted(many_segs, key=lambda x: x.seg_count, reverse=True))

    return {
        "total_files": len(docs),
        "segment_distribution": dist,
        "zero_segment_examples": zero_paths,
        "multi_segment_examples": many_paths,
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input-dir", required=True, help=".txt dosyalarının olduğu klasör")
    p.add_argument("--limit", type=int, default=None, help="İlk N dosyayla sınırla")
    args = p.parse_args()

    if not os.path.isdir(args.input_dir):
        print(f"Hata: Klasör bulunamadı: {args.input_dir}", file=sys.stderr)
        sys.exit(2)

    report = evaluate_dir(args.input_dir, args.limit)
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
