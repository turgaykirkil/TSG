#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
İçerik çıkarımı kapsama raporu aracı.

Kullanım örneği:
  python -m app.tools.content_coverage_report --input-dir /tmp/sicilius_numbers_extract --limit 200

Girdi:
  --input-dir: .txt OCR dosyalarının bulunduğu klasör
  --limit: (opsiyonel) İlk N dosyayla sınırlar

Çıktı (stdout):
  - JSON rapor: toplam ilan sayısı, alan kapsama oranları, kişi/adres dağılımları,
    aksiyon dağılımı ve aksiyona göre kapsama.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from collections import Counter, defaultdict
from importlib.machinery import SourceFileLoader
from typing import Dict, Any, List

# nlp_service import (batch_split_eval ile aynı yaklaşım)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "services"))
NLP_PATH = os.path.join(BASE_DIR, "nlp_service.py")
ns = SourceFileLoader("nlp_service", NLP_PATH).load_module()


def read_text_file(fp: str) -> str:
    with open(fp, "r", encoding="utf-8", errors="replace") as f:
        return f.read()


def iter_txt_files(input_dir: str):
    for name in sorted(os.listdir(input_dir)):
        if not name.lower().endswith(".txt"):
            continue
        yield os.path.join(input_dir, name)


def normalize_action(a) -> str:
    """Aksiyon öğesini string koda normalize et.
    Destek: string ya da dict(list) biçimleri.
    """
    if a is None:
        return ""
    if isinstance(a, str):
        return a.strip().upper()
    if isinstance(a, dict):
        val = a.get("type") or a.get("name") or a.get("action") or a.get("code")
        if isinstance(val, str):
            return val.strip().upper()
        return json.dumps(a, ensure_ascii=False)
    return str(a)


def build_report(input_dir: str, limit: Optional[int] = None) -> Dict[str, Any]:
    files_processed = 0
    announcements_total = 0

    # Alan kapsama sayacı
    field_names = [
        "registration_number",
        "sicil_dosya_no",
        "mersis_no",
        "trade_name",
        "addresses",
        "persons",
    ]
    present_counts = {f: 0 for f in field_names}

    # Değer dağılımları
    persons_count_hist = Counter()
    addresses_count_hist = Counter()

    # Aksiyon dağılımı ve aksiyona göre kapsama
    action_dist = Counter()
    coverage_by_action = defaultdict(lambda: {f: 0 for f in field_names} | {"total": 0})

    # Örnek eksikler (teşhis için kısa örnek listeleri)
    missing_examples = {f: [] for f in ["trade_name", "registration_number", "sicil_dosya_no", "mersis_no"]}

    for fp in iter_txt_files(input_dir):
        if limit is not None and files_processed >= limit:
            break
        files_processed += 1
        txt = read_text_file(fp)

        try:
            anns: List[Dict[str, Any]] = ns.parse_multiple_announcements(txt)
        except Exception as e:
            # Dosya bazlı hataları atla ama rapora not düş
            missing_examples.setdefault("errors", []).append({"file": fp, "error": str(e)})
            continue

        for ann in anns:
            announcements_total += 1

            # Alan mevcutluk kontrolü
            reg = ann.get("registration_number")
            sdn = ann.get("sicil_dosya_no")
            mersis = ann.get("mersis_no")
            tname = ann.get("trade_name")
            addrs = ann.get("addresses") or []
            persons = ann.get("persons") or []

            if reg: present_counts["registration_number"] += 1
            else:
                if len(missing_examples["registration_number"]) < 10:
                    missing_examples["registration_number"].append({"file": fp, "index": ann.get("index"), "header": ann.get("sicil_office_header", "")[:160]})

            if sdn: present_counts["sicil_dosya_no"] += 1
            else:
                if len(missing_examples["sicil_dosya_no"]) < 10:
                    missing_examples["sicil_dosya_no"].append({"file": fp, "index": ann.get("index"), "header": ann.get("sicil_office_header", "")[:160]})

            if mersis: present_counts["mersis_no"] += 1
            else:
                if len(missing_examples["mersis_no"]) < 10:
                    missing_examples["mersis_no"].append({"file": fp, "index": ann.get("index"), "header": ann.get("sicil_office_header", "")[:160]})

            if tname: present_counts["trade_name"] += 1
            else:
                if len(missing_examples["trade_name"]) < 10:
                    missing_examples["trade_name"].append({"file": fp, "index": ann.get("index"), "header": ann.get("sicil_office_header", "")[:160]})

            if addrs: present_counts["addresses"] += 1
            if persons: present_counts["persons"] += 1

            persons_count_hist[len(persons)] += 1
            addresses_count_hist[len(addrs)] += 1

            # Aksiyonlar
            actions = ann.get("actions") or []
            norm_actions = [normalize_action(a) for a in actions if normalize_action(a)]
            if not norm_actions:
                action_dist["__NONE__"] += 1
                coverage_by_action["__NONE__"]["total"] += 1
                for f in field_names:
                    # Mevcutsa +1
                    if f in ("addresses", "persons"):
                        has_val = bool(ann.get(f) or [])
                    else:
                        has_val = bool(ann.get(f))
                    if has_val:
                        coverage_by_action["__NONE__"][f] += 1
            else:
                for ac in norm_actions:
                    action_dist[ac] += 1
                    coverage_by_action[ac]["total"] += 1
                    for f in field_names:
                        if f in ("addresses", "persons"):
                            has_val = bool(ann.get(f) or [])
                        else:
                            has_val = bool(ann.get(f))
                        if has_val:
                            coverage_by_action[ac][f] += 1

    # Alan başına oranlar
    field_coverage = {}
    for f in field_names:
        present = present_counts[f]
        rate = (present / announcements_total) if announcements_total else 0.0
        field_coverage[f] = {"present": present, "missing": announcements_total - present, "rate": round(rate, 4)}

    # Aksiyona göre oranlar
    cov_by_action_out = {}
    for ac, counts in coverage_by_action.items():
        total = counts.get("total", 0)
        obj = {"total": total}
        for f in field_names:
            pres = counts.get(f, 0)
            obj[f] = {"present": pres, "rate": round((pres / total) if total else 0.0, 4)}
        cov_by_action_out[ac] = obj

    # Çıktı
    report = {
        "files_processed": files_processed,
        "announcements_total": announcements_total,
        "field_coverage": field_coverage,
        "value_distributions": {
            "persons_count": persons_count_hist,
            "addresses_count": addresses_count_hist,
        },
        "actions": action_dist,
        "coverage_by_action": cov_by_action_out,
        "missing_examples": missing_examples,
    }

    # Counter objelerini serileştirme
    def default(o):
        if isinstance(o, Counter):
            return dict(o)
        return o

    return json.loads(json.dumps(report, default=default, ensure_ascii=False))


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input-dir", default="/tmp/sicilius_numbers_extract", help=".txt dosyalarının olduğu klasör")
    p.add_argument("--limit", type=int, default=None, help="İlk N dosyayla sınırla")
    args = p.parse_args()

    if not os.path.isdir(args.input_dir):
        print(f"Hata: Klasör bulunamadı: {args.input_dir}", file=sys.stderr)
        sys.exit(2)

    report = build_report(args.input_dir, args.limit)
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
