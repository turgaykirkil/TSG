import json
import os
from sqlalchemy import create_engine, text
from app.core.config import settings
from app.core.firebase import get_firestore_client

LOCAL_PROGRESS_PATH = os.path.join(os.path.dirname(__file__), ".ocr_migration_progress.json")


def supabase_count_ocr_results() -> int:
    engine = create_engine(str(settings.DATABASE_URL))
    with engine.connect() as c:
        return int(c.execute(text("select count(*) from app.ocr_results")).scalar() or 0)


def firestore_progress_counts():
    # 1) Local fallback
    try:
        if os.path.exists(LOCAL_PROGRESS_PATH):
            with open(LOCAL_PROGRESS_PATH, "r", encoding="utf-8") as f:
                d = json.load(f) or {}
                return {
                    "exists": True,
                    "last_id": int(d.get("last_id") or 0),
                    "migrated_count": int(d.get("migrated_count") or 0),
                    "done": bool(d.get("done") or False),
                    "updated_at": d.get("updated_at"),
                    "source": "local",
                }
    except Exception:
        pass
    # 2) Firestore doc
    try:
        db = get_firestore_client()
        doc = db.collection("migration_status").document("ocr_results").get()
        if not doc.exists:
            return {"exists": False}
        data = doc.to_dict() or {}
        # Try max id from ocr_results by field 'id'
        max_id_val = None
        try:
            q = db.collection("ocr_results").order_by("id", direction="DESCENDING").limit(1)
            for d in q.stream():
                try:
                    max_id_val = int(d.to_dict().get("id"))
                except Exception:
                    max_id_val = None
                break
        except Exception:
            max_id_val = None
        return {
            "exists": True,
            "last_id": int(data.get("last_id") or 0),
            "migrated_count": int(data.get("migrated_count") or 0),
            "done": bool(data.get("done") or False),
            "updated_at": data.get("updated_at"),
            "source": "firestore",
            "max_firestore_id": max_id_val,
        }
    except Exception as e:
        return {"exists": False, "error": str(e)}


def main() -> None:
    sup_total = supabase_count_ocr_results()
    fs_prog = firestore_progress_counts()
    out = {
        "supabase_total": sup_total,
        "firestore_progress": fs_prog,
        "difference": (sup_total - fs_prog.get("migrated_count", 0)) if fs_prog.get("exists") else None,
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
