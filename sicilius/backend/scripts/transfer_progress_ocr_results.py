import json
from sqlalchemy import create_engine, text
from app.core.config import settings
from app.core.firebase import get_firestore_client

PAGE = 1000

def supabase_count_ocr_results() -> int:
    engine = create_engine(str(settings.DATABASE_URL))
    with engine.connect() as c:
        return int(c.execute(text("select count(*) from app.ocr_results")).scalar() or 0)


def firestore_count_ocr_results() -> tuple[int, list[str], list[str]]:
    db = get_firestore_client()
    page = PAGE
    count = 0
    last_doc = None

    # Head samples
    head_ids: list[str] = []
    try:
        q_head = db.collection("ocr_results").order_by("__name__").limit(3)
        for d in q_head.stream():
            head_ids.append(d.id)
    except Exception:
        pass

    # Tail samples
    tail_ids: list[str] = []
    try:
        q_tail = db.collection("ocr_results").order_by("__name__", direction="DESCENDING").limit(3)
        for d in q_tail.stream():
            tail_ids.append(d.id)
    except Exception:
        pass

    # Paged count
    try:
        q = db.collection("ocr_results").order_by("__name__").limit(page)
        docs = list(q.stream())
        count += len(docs)
        while len(docs) == page:
            last_doc = docs[-1]
            q = (
                db.collection("ocr_results")
                .order_by("__name__")
                .start_after(last_doc)
                .limit(page)
            )
            docs = list(q.stream())
            count += len(docs)
    except Exception:
        # Best-effort; return what we have
        pass

    return count, head_ids, tail_ids


def main() -> None:
    sup_count = supabase_count_ocr_results()
    fs_count, head_ids, tail_ids = firestore_count_ocr_results()

    result = {
        "supabase_total": sup_count,
        "firestore_total": fs_count,
        "difference": sup_count - fs_count,
        "progress_pct": (round((fs_count / sup_count * 100.0), 2) if sup_count else 0.0),
        "head_sample": head_ids,
        "tail_sample": tail_ids,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
