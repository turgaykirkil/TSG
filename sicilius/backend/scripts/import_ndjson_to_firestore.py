import argparse
import json
import os
import time
import random
from typing import Any, Dict, List, Optional, Tuple

from app.core.firebase import get_firestore_client


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Import NDJSON to Firestore with merge upserts and throttling")
    p.add_argument("--in", dest="in_path", required=True, help="Input NDJSON file path")
    p.add_argument("--collection", required=True, help="Target Firestore collection name")
    p.add_argument("--id-field", default="id", help="Field name to use as document id")
    p.add_argument("--write-batch", type=int, default=200)
    p.add_argument("--throttle", type=float, default=1.0)
    p.add_argument("--max-rows", type=int, default=0, help="Max rows to import in this run (0=all)")
    p.add_argument("--state", default=None, help="State file path for resume (default: <in>.state.json)")
    p.add_argument("--drop-field", action="append", default=None, help="Field name to drop from documents (repeatable)")
    return p.parse_args()


def _load_state(path: str) -> Dict[str, Any]:
    if not os.path.exists(path):
        return {"lines_processed": 0, "migrated_count": 0, "last_doc_id": None}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f) or {}
    except Exception:
        return {"lines_processed": 0, "migrated_count": 0, "last_doc_id": None}


def _save_state(path: str, st: Dict[str, Any]) -> None:
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(st, f, ensure_ascii=False)
    except Exception:
        pass


def _write_batch(db, coll: str, docs: List[Tuple[str, Dict[str, Any]]]) -> None:
    backoff = 5.0
    while True:
        try:
            batch = db.batch()
            for doc_id, payload in docs:
                ref = db.collection(coll).document(doc_id)
                batch.set(ref, payload, merge=True)
            batch.commit()
            return
        except Exception:
            if backoff > 120.0:
                raise
            time.sleep(backoff + random.uniform(0, backoff * 0.5))
            backoff = min(backoff * 2.0, 120.0)


def main() -> None:
    args = _parse_args()
    db = get_firestore_client()

    state_path = args.state or (args.in_path + ".state.json")
    st = _load_state(state_path)
    lines_processed = int(st.get("lines_processed") or 0)
    migrated = int(st.get("migrated_count") or 0)

    written_this_run = 0
    batch_size = int(args.write_batch)
    throttle = float(args.throttle)
    max_rows = int(args.max_rows or 0)

    to_write: List[Tuple[str, Dict[str, Any]]] = []
    current_line_no = 0

    with open(args.in_path, "r", encoding="utf-8") as f:
        for line in f:
            current_line_no += 1
            if current_line_no <= lines_processed:
                continue
            line = line.strip()
            if not line:
                continue
            data = json.loads(line)
            if args.drop_field:
                for fld in args.drop_field:
                    if fld in data:
                        del data[fld]
            doc_id_val = str(data.get(args.id_field)) if args.id_field in data else None
            if not doc_id_val or doc_id_val == "None":
                continue
            if batch_size <= 1:
                try:
                    db.collection(args.collection).document(doc_id_val).set(data, merge=True)
                except Exception:
                    time.sleep(2.0)
                    db.collection(args.collection).document(doc_id_val).set(data, merge=True)
                migrated += 1
                written_this_run += 1
                lines_processed = current_line_no
                st = {
                    "lines_processed": lines_processed,
                    "migrated_count": migrated,
                    "last_doc_id": doc_id_val,
                }
                _save_state(state_path, st)
                time.sleep(throttle + random.uniform(0, throttle * 0.5))
                if max_rows and written_this_run >= max_rows:
                    break
            else:
                to_write.append((doc_id_val, data))
                if len(to_write) >= batch_size:
                    _write_batch(db, args.collection, to_write)
                    migrated += len(to_write)
                    written_this_run += len(to_write)
                    lines_processed = current_line_no
                    st = {
                        "lines_processed": lines_processed,
                        "migrated_count": migrated,
                        "last_doc_id": doc_id_val,
                    }
                    _save_state(state_path, st)
                    to_write = []
                    time.sleep(throttle + random.uniform(0, throttle * 0.5))
                    if max_rows and written_this_run >= max_rows:
                        break
        if to_write and (not max_rows or written_this_run < max_rows):
            # Trim if exceeding max_rows
            if max_rows and written_this_run + len(to_write) > max_rows:
                to_write = to_write[: max_rows - written_this_run]
            if to_write:
                _write_batch(db, args.collection, to_write)
                migrated += len(to_write)
                written_this_run += len(to_write)
                lines_processed = current_line_no
                st = {
                    "lines_processed": lines_processed,
                    "migrated_count": migrated,
                    "last_doc_id": to_write[-1][0],
                }
                _save_state(state_path, st)
                to_write = []
                time.sleep(throttle + random.uniform(0, throttle * 0.5))

    print(json.dumps({
        "written_in_this_run": written_this_run,
        "migrated_total": migrated,
        "lines_processed": lines_processed,
        "state_file": os.path.abspath(state_path),
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
