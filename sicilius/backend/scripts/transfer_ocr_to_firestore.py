import time
import argparse
import os
import json
from typing import Any, Dict, List, Optional, Tuple

from sqlalchemy import create_engine, text
from sqlalchemy.engine import CursorResult

from app.core.config import settings
from app.core.firebase import get_firestore_client

BATCH_READ = 500
BATCH_WRITE = 400
INITIAL_BACKOFF_SEC = 5.0
MAX_BACKOFF_SEC = 120.0
THROTTLE_BETWEEN_BATCH_SEC = 0.5


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Transfer OCR results from Supabase to Firestore with throttling")
    parser.add_argument("--max-rows", type=int, default=0, help="Bu çalıştırmada yazılacak maksimum belge sayısı (0=limitsiz)")
    parser.add_argument("--read-batch", type=int, default=BATCH_READ, help="Supabase okuma batch boyutu")
    parser.add_argument("--write-batch", type=int, default=BATCH_WRITE, help="Firestore yazma batch boyutu")
    parser.add_argument("--throttle", type=float, default=THROTTLE_BETWEEN_BATCH_SEC, help="Batch'ler arası bekleme (s)")
    parser.add_argument("--start-after-id", type=int, default=None, help="Belirli bir id'den sonra başla (progressi override eder)")
    parser.add_argument("--reset-progress", action="store_true", help="İlerleme kaydını sıfırla")
    return parser.parse_args()


def _get_engine():
    return create_engine(str(settings.DATABASE_URL))


def _get_progress_doc():
    db = get_firestore_client()
    return db.collection("migration_status").document("ocr_results")


LOCAL_PROGRESS_PATH = os.path.join(os.path.dirname(__file__), ".ocr_migration_progress.json")


def _load_progress() -> Tuple[int, int]:
    try:
        if os.path.exists(LOCAL_PROGRESS_PATH):
            with open(LOCAL_PROGRESS_PATH, "r", encoding="utf-8") as f:
                d = json.load(f) or {}
                return int(d.get("last_id") or 0), int(d.get("migrated_count") or 0)
    except Exception:
        pass
    try:
        doc = _get_progress_doc().get()
        if doc.exists:
            data = doc.to_dict() or {}
            return int(data.get("last_id") or 0), int(data.get("migrated_count") or 0)
    except Exception:
        pass
    return 0, 0


def _save_progress(last_id: int, migrated_count: int, extra: Optional[Dict[str, Any]] = None) -> None:
    d = {"last_id": int(last_id), "migrated_count": int(migrated_count), "updated_at": time.time()}
    if extra:
        d.update(extra)
    try:
        with open(LOCAL_PROGRESS_PATH, "w", encoding="utf-8") as f:
            json.dump(d, f, ensure_ascii=False)
    except Exception:
        pass
    try:
        db = get_firestore_client()
        _get_progress_doc().set(d, merge=True)
    except Exception:
        pass


def _fetch_rows(after_id: int, limit: int) -> List[Dict[str, Any]]:
    q = text(
        """
        select *
        from app.ocr_results
        where id > :after_id
        order by id asc
        limit :limit
        """
    )
    engine = _get_engine()
    with engine.connect() as c:
        res: CursorResult = c.execute(q, {"after_id": after_id, "limit": limit})
        return list(res.mappings().all())


def _sanitize(v: Any) -> Any:
    try:
        import datetime as _dt
        from decimal import Decimal as _Dec
    except Exception:
        _dt = None  # type: ignore
        _Dec = None  # type: ignore
    if isinstance(v, bytes):
        return v.decode("utf-8", errors="ignore")
    if _Dec is not None and isinstance(v, _Dec):
        return float(v)
    return v


def _sanitize_row(row: Dict[str, Any]) -> Dict[str, Any]:
    out: Dict[str, Any] = {}
    for k, v in row.items():
        if isinstance(v, dict):
            out[k] = {kk: _sanitize(vv) for kk, vv in v.items()}
        elif isinstance(v, list):
            out[k] = [
                {kk: _sanitize(vv) for kk, vv in x.items()} if isinstance(x, dict) else _sanitize(x) for x in v
            ]
        else:
            out[k] = _sanitize(v)
    return out


def _write_batch(db, docs: List[Tuple[str, Dict[str, Any]]]) -> None:
    backoff = INITIAL_BACKOFF_SEC
    while True:
        try:
            batch = db.batch()
            for doc_id, payload in docs:
                ref = db.collection("ocr_results").document(doc_id)
                batch.set(ref, payload, merge=True)
            batch.commit()
            return
        except Exception as e:
            if backoff > MAX_BACKOFF_SEC:
                raise e
            time.sleep(backoff)
            backoff = min(backoff * 2.0, MAX_BACKOFF_SEC)


def main() -> None:
    args = _parse_args()
    db = get_firestore_client()

    if args.reset_progress:
        _save_progress(0, 0, {"done": False})

    if args.start_after_id is not None:
        last_id, migrated = int(args.start_after_id), 0
    else:
        last_id, migrated = _load_progress()

    total_written = 0
    written_this_run = 0
    read_batch = int(args.read_batch)
    write_batch = int(args.write_batch)
    throttle = float(args.throttle)
    max_rows = int(args.max_rows or 0)

    should_stop = False
    while not should_stop:
        rows = _fetch_rows(after_id=last_id, limit=read_batch)
        if not rows:
            break
        to_write: List[Tuple[str, Dict[str, Any]]] = []
        for r in rows:
            rid = str(r.get("id"))
            if not rid or rid == "None":
                continue
            payload = _sanitize_row(r)
            to_write.append((rid, payload))
            last_id = int(r.get("id"))
            if len(to_write) >= write_batch:
                _write_batch(db, to_write)
                total_written += len(to_write)
                written_this_run += len(to_write)
                migrated += len(to_write)
                _save_progress(last_id, migrated)
                to_write = []
                time.sleep(throttle)
                if max_rows and written_this_run >= max_rows:
                    should_stop = True
                    break
        if should_stop:
            break
        if to_write:
            # Son kalanları yaz
            # Eğer max_rows sınırı varsa, fazla olanları kes
            if max_rows and written_this_run + len(to_write) > max_rows:
                to_write = to_write[: max_rows - written_this_run]
            if to_write:
                _write_batch(db, to_write)
                total_written += len(to_write)
                written_this_run += len(to_write)
                migrated += len(to_write)
                _save_progress(last_id, migrated)
                to_write = []
                time.sleep(throttle)
        if max_rows and written_this_run >= max_rows:
            break
    _save_progress(last_id, migrated, {"done": written_this_run == 0})
    print({
        "written_in_this_run": total_written,
        "migrated_total": migrated,
        "last_id": last_id,
        "stopped_due_to_limit": bool(max_rows and written_this_run >= max_rows),
    })


if __name__ == "__main__":
    main()
