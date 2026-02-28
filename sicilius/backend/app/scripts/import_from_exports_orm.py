import os
from typing import Optional
import sys
import json
import uuid
import unicodedata
from datetime import datetime, date

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.company import Company
from app.models.announcement import Announcement
from app.models.ocr_result import OcrResult

_env_dir = os.getenv("EXPORTS_DIR")
_repo_dir = os.path.join(os.path.dirname(__file__), "..", "..", "exports")
_container_dir = "/app/exports"
if _env_dir and os.path.isdir(_env_dir):
    EXPORTS_DIR = _env_dir
elif os.path.isdir(_container_dir):
    EXPORTS_DIR = _container_dir
else:
    EXPORTS_DIR = _repo_dir

# --- helpers ---

def read_ndjson(path):
    with open(path, "r", encoding="utf-8") as f:
        for i, line in enumerate(f, start=1):
            s = line.strip()
            if not s:
                continue
            try:
                yield json.loads(s)
            except Exception as e:
                raise RuntimeError(f"JSON parse error at {path}:{i}: {e}")

def to_date(v):
    if not v:
        return None
    try:
        return date.fromisoformat(str(v))
    except Exception:
        return None

def to_ts(v):
    if not v:
        return None
    try:
        return datetime.fromisoformat(str(v))
    except Exception:
        return None

# --- importers using ORM metadata + ON CONFLICT ---


def _normalize_company_name(name: Optional[str]) -> Optional[str]:
    if not name:
        return None
    normalized = unicodedata.normalize("NFKC", name)
    normalized = normalized.strip().casefold()
    return normalized or None


def _load_company_maps(db: Session) -> tuple[set[str], dict[str, str]]:
    from sqlalchemy import select

    existing_ids: set[str] = set()
    name_map: dict[str, str] = {}
    result = db.execute(select(Company.id, Company.unvan))
    for cid, unvan in result:
        cid_str = str(cid)
        existing_ids.add(cid_str)
        norm = _normalize_company_name(unvan)
        if norm:
            name_map.setdefault(norm, cid_str)
    return existing_ids, name_map

def upsert_companies(db: Session, batch):
    if not batch:
        return
    stmt = insert(Company.__table__).values(batch)
    update_cols = {
        c.name: getattr(stmt.excluded, c.name)
        for c in Company.__table__.columns
        if c.name not in ("id",)
    }
    stmt = stmt.on_conflict_do_update(
        index_elements=[Company.__table__.c.id],
        set_=update_cols,
    )
    db.execute(stmt)


def import_companies(db: Session):
    path = os.path.join(EXPORTS_DIR, "companies.ndjson")
    if not os.path.exists(path):
        print("companies.ndjson not found, skipping")
        return
    total = 0
    batch = []
    for obj in read_ndjson(path):
        total += 1
        rec = {
            "id": obj.get("id"),
            "unvan": obj.get("unvan"),
            "mersis_number": obj.get("mersis_number"),
            "phone": obj.get("phone"),
            "email": obj.get("email"),
            "website": obj.get("website"),
            "address": obj.get("address"),
            "district": obj.get("district"),
            "city": obj.get("city"),
            "country": obj.get("country") or "Türkiye",
            "is_active": bool(obj.get("is_active", True)),
            "establishment_date": to_date(obj.get("establishment_date")),
            "scraped_at": to_ts(obj.get("scraped_at")),
            "created_at": to_ts(obj.get("created_at")),
            "updated_at": to_ts(obj.get("updated_at")),
            "sicil_mudurluk": obj.get("sicil_mudurluk"),
            "sicil_no": obj.get("sicil_no"),
            "sicil_office_code": obj.get("sicil_office_code"),
            "nace_code": obj.get("nace_code"),
            "pdf_name": obj.get("pdf_name"),
            "pdf_path": obj.get("pdf_path"),
            # koordinat is Geometry; exports has mostly null; omit to avoid SRID parse.
        }
        batch.append(rec)
        if len(batch) >= 200:
            upsert_companies(db, batch)
            db.commit()
            batch.clear()
            print(f"companies upserted ~{total}")
    if batch:
        upsert_companies(db, batch)
        db.commit()
        print(f"companies upserted {total}")


def _load_existing_company_ids(db: Session) -> set[str]:
    existing_ids, _ = _load_company_maps(db)
    return existing_ids


def ensure_companies_for_announcements(db: Session, announcement_path: str) -> None:
    if not os.path.exists(announcement_path):
        return
    existing_ids = _load_existing_company_ids(db)
    new_records: dict[str, dict] = {}
    for obj in read_ndjson(announcement_path):
        cid = obj.get("company_id")
        if not cid or cid in existing_ids or cid in new_records:
            continue
        new_records[cid] = {
            "id": cid,
            "unvan": obj.get("title"),
            "sicil_mudurluk": obj.get("trade_registry_name"),
            "sicil_no": None,
            "sicil_office_code": None,
            "country": "Türkiye",
            "is_active": True,
        }
    if new_records:
        print(f"Ensuring {len(new_records)} missing companies referenced by announcements...")
        upsert_companies(db, list(new_records.values()))
        db.commit()


def ensure_companies_for_ocr(
    db: Session,
    ocr_path: str,
    existing_ids: set[str],
    name_map: dict[str, str],
) -> None:
    if not os.path.exists(ocr_path):
        return
    new_records: dict[str, dict] = {}
    for obj in read_ndjson(ocr_path):
        cid = obj.get("company_id")
        if not cid or cid in existing_ids or cid in new_records:
            continue
        new_records[cid] = {
            "id": cid,
            "unvan": obj.get("trade_name") or obj.get("company_name"),
            "country": "Türkiye",
            "is_active": True,
        }
    if new_records:
        print(f"Ensuring {len(new_records)} missing companies referenced by ocr_results...")
        batch = list(new_records.values())
        upsert_companies(db, batch)
        db.commit()
        for record in batch:
            cid = record["id"]
            existing_ids.add(cid)
            norm = _normalize_company_name(record.get("unvan"))
            if norm:
                name_map.setdefault(norm, cid)


def upsert_announcements(db: Session, batch):
    if not batch:
        return
    tbl = Announcement.__table__
    stmt = insert(tbl).values(batch)
    update_cols = {
        c.name: getattr(stmt.excluded, c.name)
        for c in tbl.columns
        if c.name not in ("id",)
    }
    stmt = stmt.on_conflict_do_update(
        index_elements=[tbl.c.id],
        set_=update_cols,
    )
    db.execute(stmt)


def import_announcements(db: Session):
    path = os.path.join(EXPORTS_DIR, "announcements.ndjson")
    if not os.path.exists(path):
        print("announcements.ndjson not found, skipping")
        return
    ensure_companies_for_announcements(db, path)
    total = 0
    batch = []
    for obj in read_ndjson(path):
        total += 1
        rec = {
            "id": obj.get("id"),
            "trade_registry_name": obj.get("trade_registry_name"),
            "trade_registry_number": obj.get("trade_registry_number"),
            "title": obj.get("title"),
            "publication_date": to_date(obj.get("publication_date")),
            "issue_number": obj.get("issue_number"),
            "page_number": obj.get("page_number"),
            "announcement_type": obj.get("announcement_type"),
            "newspaper_name": obj.get("newspaper_name"),
            "pdf_url": obj.get("pdf_url"),
            "company_id": obj.get("company_id"),
            "created_at": to_ts(obj.get("created_at")),
            "updated_at": to_ts(obj.get("updated_at")),
        }
        batch.append(rec)
        if len(batch) >= 1000:
            upsert_announcements(db, batch)
            db.commit()
            batch.clear()
            print(f"announcements upserted ~{total}")
    if batch:
        upsert_announcements(db, batch)
        db.commit()
        print(f"announcements upserted {total}")


def upsert_ocr_results(db: Session, batch):
    if not batch:
        return
    tbl = OcrResult.__table__
    stmt = insert(tbl).values(batch)
    update_cols = {
        c.name: getattr(stmt.excluded, c.name)
        for c in tbl.columns
        if c.name not in ("id",)
    }
    stmt = stmt.on_conflict_do_update(
        index_elements=[tbl.c.id],
        set_=update_cols,
    )
    db.execute(stmt)


def import_ocr_results(db: Session):
    path = os.path.join(EXPORTS_DIR, "ocr_results.ndjson")
    if not os.path.exists(path):
        print("ocr_results.ndjson not found, skipping")
        return
    existing_ids, name_map = _load_company_maps(db)
    ensure_companies_for_ocr(db, path, existing_ids, name_map)
    total = 0
    batch = []
    for obj in read_ndjson(path):
        total += 1
        company_id = obj.get("company_id")
        trade_name = obj.get("trade_name") or obj.get("company_name")
        normalized_name = _normalize_company_name(trade_name)
        if company_id:
            company_id = str(company_id)
            if company_id not in existing_ids:
                # If company_id provided but still missing, fall back to name map
                if normalized_name and normalized_name in name_map:
                    company_id = name_map[normalized_name]
                else:
                    stub = {
                        "id": company_id,
                        "unvan": trade_name or f"OCR Company {company_id}",
                        "country": "Türkiye",
                        "is_active": True,
                    }
                    upsert_companies(db, [stub])
                    db.commit()
                    existing_ids.add(company_id)
                    if normalized_name:
                        name_map.setdefault(normalized_name, company_id)
        structured = obj.get("structured_data")
        if isinstance(structured, str) and structured.lower() == "null":
            structured = None
        if not company_id:
            if normalized_name and normalized_name in name_map:
                company_id = name_map[normalized_name]
            else:
                new_company_id = str(uuid.uuid4())
                stub_unvan = trade_name or obj.get("sicil_office_header") or f"OCR Company {new_company_id}"
                stub = {
                    "id": new_company_id,
                    "unvan": stub_unvan,
                    "country": "Türkiye",
                    "is_active": True,
                }
                upsert_companies(db, [stub])
                db.commit()
                company_id = new_company_id
                existing_ids.add(company_id)
                if normalized_name:
                    name_map.setdefault(normalized_name, company_id)
        rec = {
            "id": obj.get("id"),
            "announcement_id": obj.get("announcement_id"),
            "company_id": company_id,
            "raw_text": obj.get("original_text") or obj.get("raw_text"),
            "structured_data": structured,
            "status": obj.get("status") or "pending",
            "created_at": to_ts(obj.get("created_at")),
            "updated_at": to_ts(obj.get("updated_at")),
        }
        batch.append(rec)
        if len(batch) >= 200:
            upsert_ocr_results(db, batch)
            db.commit()
            batch.clear()
            print(f"ocr_results upserted ~{total}")
    if batch:
        upsert_ocr_results(db, batch)
        db.commit()
        print(f"ocr_results upserted {total}")


def main():
    target = (sys.argv[1] if len(sys.argv) > 1 else "all").lower()
    db = SessionLocal()
    try:
        if target in ("all", "companies"):
            print("Importing companies via ORM...")
            import_companies(db)
        if target in ("all", "announcements"):
            print("Importing announcements via ORM...")
            import_announcements(db)
        if target in ("all", "ocr"):
            print("Importing ocr_results via ORM...")
            import_ocr_results(db)
    finally:
        db.close()
    print("Done.")

if __name__ == "__main__":
    main()
