#!/usr/bin/env python3
"""
OCR çıktılarındaki JSON dosyalarını sadeleştirme betiği.

- Varsayılan klasör: ../../ocr_ciktilari (betiğin bulunduğu dizine göre)
- Kaldırılacak gürültülü anahtarlar: persons, organizations, locations, dates, money, misc, entities_full
- Dry-run ile önce gösterir, sonra isteğe bağlı olarak yazma yapar ve .bak yedek oluşturur.

Kullanım örnekleri:
  Dry-run (yazma YOK):
    python3 cleanup_ocr_json.py --dir /path/to/ocr_ciktilari

  Yaz ve yedek al:
    python3 cleanup_ocr_json.py --dir /path/to/ocr_ciktilari --apply
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path
from typing import Any, Dict, List

REMOVE_KEYS = {
    "persons",
    "organizations",
    "locations",
    "dates",
    "money",
    "misc",
    "entities_full",
    "registration_number",
}


def iter_dicts(value: Any):
    """Yield içindeki tüm dict'leri gezer (liste veya tek sözlük olabilir)."""
    if isinstance(value, dict):
        yield value
        for v in value.values():
            yield from iter_dicts(v)
    elif isinstance(value, list):
        for item in value:
            yield from iter_dicts(item)


def cleanup_json_obj(obj: Any) -> Dict[str, List[str]]:
    """Objedeki (dict/list) tüm sözlüklerde REMOVE_KEYS anahtarlarını siler.
    Silinen anahtarları raporlar: {"removed": [..], "touched_files": [...]}
    """
    removed: List[str] = []
    for d in iter_dicts(obj):
        for k in list(d.keys()):
            if k in REMOVE_KEYS and k in d:
                d.pop(k, None)
                removed.append(k)
    return {"removed": removed}


def process_file(path: Path, dry_run: bool = True, backup: bool = True) -> Dict[str, Any]:
    try:
        raw = path.read_text(encoding="utf-8")
        data = json.loads(raw)
    except Exception as e:
        return {"file": str(path), "ok": False, "error": f"read/parse failed: {e}"}

    report = cleanup_json_obj(data)
    removed_set = sorted(set(report["removed"]))

    if dry_run:
        return {"file": str(path), "ok": True, "removed_keys": removed_set, "written": False}

    # Yazma modunda önce yedek al
    try:
        if backup:
            backup_path = path.with_suffix(path.suffix + ".bak")
            shutil.copy2(path, backup_path)
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        return {"file": str(path), "ok": True, "removed_keys": removed_set, "written": True}
    except Exception as e:
        return {"file": str(path), "ok": False, "error": f"write failed: {e}"}


def main(argv: List[str]) -> int:
    parser = argparse.ArgumentParser(description="OCR JSON sadeleştirme")
    parser.add_argument("--dir", dest="dir", type=str, default=None, help="JSON klasörü (varsayılan: ../../ocr_ciktilari)")
    parser.add_argument("--no-backup", dest="backup", action="store_false", help="Yedek alma")
    parser.add_argument("--apply", dest="apply", action="store_true", help="Dry-run yerine yaz (uygula)")
    parser.add_argument("--glob", dest="glob", type=str, default="*.json", help="Dosya deseni (vars: *.json)")
    args = parser.parse_args(argv)

    script_dir = Path(__file__).resolve().parent
    default_dir = (script_dir / ".." / ".." / "ocr_ciktilari").resolve()
    target_dir = Path(args.dir).resolve() if args.dir else default_dir

    if not target_dir.exists() or not target_dir.is_dir():
        print(f"Hata: Klasör bulunamadı: {target_dir}", file=sys.stderr)
        return 2

    files = sorted(target_dir.glob(args.glob))
    if not files:
        print(f"Uyarı: Desene uyan dosya yok: {target_dir}/{args.glob}")
        return 0

    dry_run = not args.apply
    total = 0
    changed = 0
    for f in files:
        total += 1
        res = process_file(f, dry_run=dry_run, backup=args.backup)
        if res.get("ok"):
            removed_keys = res.get("removed_keys", [])
            if removed_keys:
                changed += 1
            status = "DRY-RUN" if not res.get("written", False) else "WROTE"
            print(f"[{status}] {f.name} -> removed: {removed_keys}")
        else:
            print(f"[ERROR] {f.name} -> {res.get('error')}")

    print(f"\nÖzet: {total} dosya, {changed} dosyada gürültü anahtar(lar)ı tespit edildi.")
    if dry_run:
        print("Not: Değişiklikler UYGULANMADI. Yazmak için --apply ekleyin.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
