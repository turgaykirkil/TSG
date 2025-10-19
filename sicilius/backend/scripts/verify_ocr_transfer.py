import json
import pathlib
from typing import Any, Optional

from app.core.firebase import get_firestore_client

NDJSON_PATH = "exports/ocr_results.ndjson"
STATE_PATH = "exports/ocr_results.ndjson.state.json"
COLLECTION = "ocr_results"


def count_lines(path: str) -> int:
    p = pathlib.Path(path)
    if not p.exists():
        return 0
    with p.open("r", encoding="utf-8") as f:
        return sum(1 for _ in f)


def firestore_aggregate_count() -> Optional[int]:
    db = get_firestore_client()
    try:
        # Prefer new aggregate count API if available
        try:
            # google-cloud-firestore >= 2.11
            from google.cloud import firestore  # type: ignore
            q = db.collection(COLLECTION)
            agg = q.count().get()  # type: ignore[attr-defined]
            res = list(agg)
            if res:
                # Try multiple access patterns for compatibility
                try:
                    from google.cloud.firestore import AggregateField  # type: ignore
                    return int(res[0][AggregateField.COUNT])  # type: ignore[index]
                except Exception:
                    pass
                try:
                    # Some versions expose a dict-like result with 'count'
                    return int(res[0].get("count"))  # type: ignore[attr-defined]
                except Exception:
                    pass
        except Exception:
            pass
        return None
    except Exception:
        return None


def load_state() -> dict[str, Any]:
    p = pathlib.Path(STATE_PATH)
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return {}


def main() -> None:
    expected = count_lines(NDJSON_PATH)
    state = load_state()
    lines_processed = int(state.get("lines_processed") or 0)
    migrated_count = int(state.get("migrated_count") or 0)

    fs_count = firestore_aggregate_count()

    out = {
        "expected_from_ndjson": expected,
        "state_lines_processed": lines_processed,
        "state_migrated_count": migrated_count,
        "firestore_aggregate_count": fs_count,
        "all_processed_locally": (expected > 0 and lines_processed == expected),
        "diff_vs_fs_count": (expected - fs_count) if (fs_count is not None) else None,
        "fs_count_note": "None means aggregate count API unavailable or failed; rely on local state",
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
