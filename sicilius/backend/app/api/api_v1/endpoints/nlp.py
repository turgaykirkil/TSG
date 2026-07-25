import hashlib
import logging
import httpx
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple, Union

from fastapi import APIRouter, Body, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core import storage as storage_core
from app.db.session import get_db
from app.models.announcement import Announcement
from app.services import ingest_service, nlp_service

logger = logging.getLogger(__name__)

router = APIRouter()


class NlpRequest(BaseModel):
    text: str


class SourceFilePayload(BaseModel):
    bucket: str
    path: str


class IngestStructuredPayload(BaseModel):
    items: List[Dict[str, Any]]
    original_text: Optional[str] = None
    publication_date: Optional[str] = None
    issue_number: Optional[int] = None
    page_number: Optional[int] = None
    pdf_url: Optional[str] = None
    pdf_page_count: Optional[int] = None
    announcement_id: Optional[str] = None
    source_file: Optional[SourceFilePayload] = None
    delete_after_ingest: bool = False


@dataclass
class IngestMeta:
    publication_date: Optional[str] = None
    issue_number: Optional[int] = None
    page_number: Optional[int] = None
    pdf_url: Optional[str] = None
    pdf_page_count: Optional[int] = None
    announcement_id: Optional[str] = None
    original_text: Optional[str] = None


def _parse_text_or_400(payload: NlpRequest) -> str:
    text = (payload.text or "").strip()
    if not text:
        raise HTTPException(status_code=400, detail="Text content cannot be empty.")
    return text


def _mask_mersis_value(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    digits = ''.join(ch for ch in str(value) if ch.isdigit())
    if len(digits) == 16 and digits[0] != "0":
        chars = list(digits)
        for idx in range(3, 8):
            chars[idx] = "*"
        return ''.join(chars)
    return value


def _mask_mersis_in_items(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    masked: List[Dict[str, Any]] = []
    for item in items:
        if not isinstance(item, dict):
            continue
        clone = dict(item)
        masked_value = _mask_mersis_value(clone.get("mersis_no"))
        if masked_value is not None:
            clone["mersis_no"] = masked_value
        masked.append(clone)
    return masked


def _pair_masked_ids_to_persons(text: str, persons: List[Dict[str, Any]], masked_ids: List[str]) -> List[Dict[str, Any]]:
    try:
        if not text or not persons or not masked_ids:
            return persons
        lines = text.splitlines()
        id_positions: List[tuple[str, int]] = []
        for token in masked_ids:
            token_clean = (token or "").strip()
            if not token_clean:
                continue
            for idx, raw_line in enumerate(lines):
                if token_clean in raw_line:
                    id_positions.append((token_clean, idx))
                    break
        if not id_positions:
            return persons

        enriched: List[Dict[str, Any]] = []
        assigned: set[int] = set()

        for idx, person in enumerate(persons):
            label = (person.get("label") or "").upper()
            masked_present = bool((person.get("masked_ids") or "").strip())
            if label.startswith("PER") and masked_present:
                enriched.append(dict(person))
                assigned.add(idx)

        def _name_variants(name: str) -> List[str]:
            base = (name or "").strip().lower()
            if not base:
                return []
            prefixes = [
                "",
                "t.c. ", "tc ", "t c ",
                "t.a. ", "ta ",
                "sn. ", "sayin ",
                "bay ", "bayan ",
            ]
            return [prefix + base for prefix in prefixes]

        for masked_id, line_index in id_positions:
            window = "\n".join(lines[line_index:line_index + 4]).lower()
            for idx, person in enumerate(persons):
                if idx in assigned:
                    continue
                label = (person.get("label") or "").upper()
                if not label.startswith("PER"):
                    continue
                name = (person.get("text") or "").strip()
                if not name:
                    continue
                variants = _name_variants(name)
                if any(variant and variant in window for variant in variants):
                    clone = dict(person)
                    clone.setdefault("masked_ids", masked_id)
                    enriched.append(clone)
                    assigned.add(idx)
                    break

        for idx, person in enumerate(persons):
            if idx not in assigned:
                enriched.append(person)

        if len(masked_ids) == 1:
            only_id = masked_ids[0]
            for entry in enriched:
                if (entry.get("label") or "").upper().startswith("PER") and not (entry.get("masked_ids") or "").strip():
                    entry["masked_ids"] = only_id
                    break
        return enriched
    except Exception:
        return persons


def _resolve_announcement_by_id(db: Session, announcement_id: Optional[str]) -> Optional[Announcement]:
    if not announcement_id:
        return None
    try:
        return db.get(Announcement, announcement_id)
    except Exception:
        logger.exception("Announcement fetch failed", extra={"announcement_id": announcement_id})
        return None


def _resolve_announcement_by_file_name(db: Session, file_name: str) -> Optional[Announcement]:
    stmt = select(Announcement).where(Announcement.pdf_url.ilike(f"%{file_name}%")).limit(1)
    return db.execute(stmt).scalars().first()


def _resolve_source_file(payload: Optional[SourceFilePayload]) -> Optional[SourceFilePayload]:
    return payload


def _resolve_announcement_from_filename(db: Session, name: Optional[str]) -> Optional[Announcement]:
    if not name:
        return None
    clean = name.split('/')[-1]
    clean = clean.split('?', 1)[0]
    return _resolve_announcement_by_file_name(db, clean)


def _coerce_int(value: Optional[Union[int, str]]) -> Optional[int]:
    if value is None:
        return None
    try:
        return int(value)
    except Exception:
        return None


def _build_ingest_meta(
    db: Session,
    announcement_id: Optional[str],
    publication_date: Optional[str],
    issue_number: Optional[Union[int, str]],
    page_number: Optional[Union[int, str]],
    pdf_url: Optional[str],
    pdf_page_count: Optional[Union[int, str]],
    pdf_file_name: Optional[str],
    original_text: Optional[str],
) -> IngestMeta:
    meta = IngestMeta(
        publication_date=publication_date,
        issue_number=_coerce_int(issue_number),
        page_number=_coerce_int(page_number),
        pdf_url=pdf_url,
        pdf_page_count=_coerce_int(pdf_page_count),
        announcement_id=announcement_id,
        original_text=original_text,
    )

    ann: Optional[Announcement] = None
    if meta.announcement_id:
        ann = _resolve_announcement_by_id(db, meta.announcement_id)
    if ann is None:
        ann = _resolve_announcement_from_filename(db, pdf_file_name)
    if ann is None:
        ann = _resolve_announcement_from_filename(db, meta.pdf_url)

    if ann:
        if meta.announcement_id is None:
            meta.announcement_id = str(ann.id)
        if meta.publication_date is None and ann.publication_date:
            meta.publication_date = ann.publication_date.isoformat()
        if meta.issue_number is None:
            meta.issue_number = ann.issue_number
        if meta.page_number is None:
            meta.page_number = ann.page_number
        if meta.pdf_url is None:
            meta.pdf_url = ann.pdf_url

    return meta


def _apply_meta_to_items(items: List[Dict[str, Any]], meta: IngestMeta) -> List[Dict[str, Any]]:
    augmented: List[Dict[str, Any]] = []
    for item in items:
        clone = dict(item)
        if meta.publication_date is not None:
            clone.setdefault("publication_date", meta.publication_date)
        if meta.issue_number is not None:
            clone.setdefault("issue_number", meta.issue_number)
        if meta.page_number is not None:
            clone.setdefault("page_number", meta.page_number)
        if meta.pdf_url is not None:
            clone.setdefault("pdf_url", meta.pdf_url)
        if meta.pdf_page_count is not None:
            clone.setdefault("pdf_page_count", meta.pdf_page_count)
        if meta.announcement_id is not None:
            clone.setdefault("announcement_id", meta.announcement_id)
        if meta.original_text and not clone.get("original_text"):
            clone["original_text"] = meta.original_text
        augmented.append(clone)
    return augmented


def _gather_raw_text(items: List[Dict[str, Any]], fallback: Optional[str]) -> Optional[str]:
    if fallback:
        return fallback
    pieces: List[str] = []
    for item in items:
        text = item.get("original_text")
        if isinstance(text, str) and text.strip():
            pieces.append(text.strip())
    return "\n\n".join(pieces) if pieces else None


def _ingest_locally(db: Session, parsed_items: List[Dict[str, Any]], meta: IngestMeta) -> Dict[str, Any]:
    augmented_items = _apply_meta_to_items(parsed_items, meta)
    summary = ingest_service.ingest_companies_and_announcements(augmented_items, db)
    logger.info(
        "Local ingest completed",
        extra={
            "parsed": len(parsed_items),
            "inserted": summary.get("inserted"),
            "updated": summary.get("updated"),
            "skipped": summary.get("skipped"),
        },
    )
    return summary


from app.utils.stats_helper import increment_storage_file_count

def _delete_source_file(db: Session, source: Optional[SourceFilePayload]) -> None:
    if not source:
        return
    try:
        storage_core.remove_objects(source.bucket, [source.path])
        increment_storage_file_count(db, -1)
        logger.info("Source file deleted", extra={"bucket": source.bucket, "path": source.path})
    except Exception:
        logger.exception("Source file deletion failed", extra={"bucket": source.bucket, "path": source.path})


@router.post("/parse-announcement", response_model=Dict[str, Any])
async def parse_text(request_body: NlpRequest):
    text = _parse_text_or_400(request_body)
    try:
        if nlp_service.nlp_model is None:
            nlp_service.load_spacy_model()
        return nlp_service.parse_announcement_text(text)
    except Exception as exc:
        logger.error("parse_announcement failed", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to parse text due to an internal server error: {exc}")


@router.post("/parse-announcements", response_model=List[Dict[str, Any]])
async def parse_text_multiple(
    request_body: NlpRequest,
    db: Session = Depends(get_db),
    skip_ingest: bool = Query(True, description="If true (default), do not persist; parse-only response."),
    announcement_id: Optional[str] = Query(None),
    publication_date: Optional[str] = Query(None),
    issue_number: Optional[Union[int, str]] = Query(None),
    page_number: Optional[Union[int, str]] = Query(None),
    pdf_url: Optional[str] = Query(None),
    pdf_page_count: Optional[Union[int, str]] = Query(None),
    pdf_file_name: Optional[str] = Query(None),
):
    text = _parse_text_or_400(request_body)
    try:
        if nlp_service.nlp_model is None:
            nlp_service.load_spacy_model()
        parsed_list = nlp_service.parse_multiple_announcements(text)
    except Exception as exc:
        logger.error("parse_announcements failed", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to parse text due to an internal server error: {exc}")

    masked_items = _mask_mersis_in_items(parsed_list)

    if skip_ingest:
        return masked_items

    meta = _build_ingest_meta(
        db=db,
        announcement_id=announcement_id,
        publication_date=publication_date,
        issue_number=issue_number,
        page_number=page_number,
        pdf_url=pdf_url,
        pdf_page_count=pdf_page_count,
        pdf_file_name=pdf_file_name,
        original_text=text,
    )

    try:
        summary = _ingest_locally(db, parsed_list, meta)
        logger.info("parse_announcements ingest", extra=summary)
    except Exception as exc:
        logger.error("parse_announcements ingest failed", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to ingest parsed announcements: {exc}")

    return masked_items


@router.post("/parse-announcements-minimal", response_model=List[Dict[str, Any]])
async def parse_text_minimal(request_body: NlpRequest):
    text = _parse_text_or_400(request_body)
    try:
        if nlp_service.nlp_model is None:
            nlp_service.load_spacy_model()
        items = nlp_service.parse_multiple_announcements(text)
    except Exception as exc:
        logger.error("parse_announcements_minimal failed", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to parse text due to an internal server error: {exc}")

    minimal_list: List[Dict[str, Any]] = []
    for item in items:
        ilan_sira = None
        val = item.get("ilan_sira_no")
        if isinstance(val, list) and val:
            ilan_sira = val[0]
        elif isinstance(val, str) and val.strip():
            ilan_sira = val.strip()
        else:
            sd = item.get("sicil_dosya_no")
            if isinstance(sd, str) and sd.strip():
                ilan_sira = sd.strip()

        enriched_persons = _pair_masked_ids_to_persons(
            item.get("original_text") or "",
            item.get("persons") or [],
            item.get("masked_ids") or [],
        )

        minimal = {
            "müdürlük": item.get("sicil_office_header"),
            "ilan Sira No": ilan_sira,
            "Mersis No": _mask_mersis_value(item.get("mersis_no")),
            "Ticaret Sicil/Dosya No": item.get("sicil_dosya_no"),
            "Ticaret Unvan": item.get("trade_name"),
            "Adres": item.get("addresses") or [],
            "Tescil Edilen Hususlar": item.get("hususlar") or [],
            "Tescile Delil Olan Belgeler": item.get("belgeler"),
            "Kişiler": enriched_persons,
            "Maskeli Kimlik Numaraları": item.get("masked_ids") or [],
            "orjinal metin": item.get("original_text"),
        }
        if item.get("old_addresses"):
            minimal["Eski Adres"] = item.get("old_addresses")
        minimal_list.append(minimal)

    return minimal_list


@router.post("/parse-announcements-minimal-single", response_model=Dict[str, Any])
async def parse_text_minimal_single(
    request_body: NlpRequest,
    index: int = Query(1, description="1-based announcement index"),
):
    results = await parse_text_minimal(request_body)
    sel = max(1, index) - 1
    if sel < 0 or sel >= len(results):
        raise HTTPException(status_code=404, detail=f"Index out of range. Provided index={index}")
    return results[sel]


@router.post("/ingest-structured", response_model=Dict[str, Any])
async def ingest_structured(
    payload: IngestStructuredPayload = Body(...),
    db: Session = Depends(get_db),
):
    if not payload.items:
        raise HTTPException(status_code=400, detail="items list cannot be empty")

    masked_items = _mask_mersis_in_items(payload.items)
    raw_text = _gather_raw_text(masked_items, payload.original_text)
    source_file = _resolve_source_file(payload.source_file)

    meta = _build_ingest_meta(
        db=db,
        announcement_id=payload.announcement_id,
        publication_date=payload.publication_date,
        issue_number=payload.issue_number,
        page_number=payload.page_number,
        pdf_url=payload.pdf_url,
        pdf_page_count=payload.pdf_page_count,
        pdf_file_name=source_file.path if source_file else None,
        original_text=raw_text,
    )

    try:
        summary = _ingest_locally(db, masked_items, meta)
    except Exception as exc:
        logger.error("ingest_structured failed", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to ingest structured payload: {exc}")

    if payload.delete_after_ingest and source_file:
        _delete_source_file(db, source_file)

    response: Dict[str, Any] = {
        "parsed_count": len(masked_items),
        **summary,
        "delete_after_ingest": payload.delete_after_ingest,
    }
    if source_file:
        response["source_file"] = source_file.dict()
    return response


@router.get("/resolve-announcement", response_model=Dict[str, Any])
async def resolve_announcement(
    file_name: Optional[str] = Query(None),
    pdf_url: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    name = file_name or pdf_url
    if not name:
        raise HTTPException(status_code=400, detail="file_name or pdf_url is required")
    announcement = _resolve_announcement_from_filename(db, name)
    if not announcement:
        raise HTTPException(status_code=404, detail="not found")
    return {
        "id": str(announcement.id),
        "publication_date": announcement.publication_date.isoformat() if announcement.publication_date else None,
        "issue_number": announcement.issue_number,
        "page_number": announcement.page_number,
        "pdf_url":announcement.pdf_url,
    }


import json
import os
import time
import re
import urllib.request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from sqlalchemy import text as sql_text

# Configurations matching evaluate script
LLM_SERVER_URL = "http://localhost:1234/v1/chat/completions"
MODEL_NAME = "default_model"
PROGRESS_PATH = "/Users/turgaykirkil/Apps/TSG_Platform/sicilius/scratch/evaluation_progress.json"

class SaveEvaluationNoteRequest(BaseModel):
    case_id: str
    user_note: str

@router.post("/save-evaluation-note", response_model=Dict[str, Any])
async def save_evaluation_note(payload: SaveEvaluationNoteRequest):
    if not os.path.exists(PROGRESS_PATH):
        raise HTTPException(status_code=404, detail="evaluation_progress.json not found")
        
    try:
        with open(PROGRESS_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        results = data.get("results", [])
        found = False
        
        for result in results:
            if str(result.get("id")) == str(payload.case_id):
                result["user_note"] = payload.user_note
                found = True
                break
                
        if not found:
            raise HTTPException(status_code=404, detail=f"Case with ID {payload.case_id} not found in results")
            
        with open(PROGRESS_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            
        return {"status": "success", "message": f"Saved note for case {payload.case_id}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/evaluation-stats", response_model=Dict[str, Any])
async def get_evaluation_stats():
    """Returns general stats and all saved results from progress JSON."""
    if not os.path.exists(PROGRESS_PATH):
        # Create empty if not exists
        with open(PROGRESS_PATH, "w", encoding="utf-8") as f:
            json.dump({"results": []}, f)
            
    try:
        with open(PROGRESS_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        results = data.get("results", [])
        
        total = len(results)
        perfect = sum(1 for r in results if r["comparison"]["status"] == "Match")
        llm_better = sum(1 for r in results if r["comparison"]["status"] == "LLM Better")
        partial = sum(1 for r in results if r["comparison"]["status"] == "Partial Match")
        errors = sum(1 for r in results if r["comparison"]["status"] == "Error")
        mismatch = sum(1 for r in results if r["comparison"]["status"] == "Mismatch")
        
        return {
            "total": total,
            "perfect": perfect,
            "llm_better": llm_better,
            "partial": partial,
            "errors": errors,
            "mismatch": mismatch,
            "results": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading progress file: {e}")


@router.get("/get-next-announcement", response_model=Dict[str, Any])
async def get_next_announcement(db: Session = Depends(get_db)):
    """Fetches the next database announcement that has not been evaluated yet."""
    completed_ids = set()
    if os.path.exists(PROGRESS_PATH):
        try:
            with open(PROGRESS_PATH, "r", encoding="utf-8") as f:
                saved = json.load(f)
                completed_ids = set(str(r["id"]) for r in saved.get("results", []))
        except Exception:
            pass
            
    try:
        # Fetch next candidate
        query = sql_text("""
            SELECT 
                id::text as id,
                original_text,
                trade_name,
                addresses,
                old_addresses,
                persons,
                mersis_no,
                sicil_dosya_no,
                belgeler,
                hususlar,
                ilan_sira_no,
                pdf_url,
                pdf_page_count
            FROM app.ocr_results
            WHERE original_text IS NOT NULL AND trade_name IS NOT NULL
            LIMIT 500;
        """)
        db_results = db.execute(query).mappings().all()
        
        next_case = None
        for row in db_results:
            case_id = str(row["id"])
            if case_id in completed_ids:
                continue
                
            # Basic validation to ensure good evaluation cases
            text = row["original_text"] or ""
            if len(text) > 200:
                next_case = row
                break
                
        if not next_case:
            raise HTTPException(status_code=404, detail="No more new evaluation cases found in database.")
            
        def safe_list(val):
            if not val:
                return []
            raw_list = []
            if isinstance(val, list):
                raw_list = val
            elif isinstance(val, str):
                try:
                    parsed = json.loads(val)
                    raw_list = parsed if isinstance(parsed, list) else [parsed]
                except:
                    raw_list = [val]
            
            # Her bir elemanı temizleyip string formatına çeviriyoruz
            cleaned = []
            for item in raw_list:
                if isinstance(item, dict):
                    txt = item.get("text") or item.get("name") or ""
                    if txt:
                        cleaned.append(str(txt).strip())
                elif item is not None:
                    cleaned.append(str(item).strip())
            return cleaned

        return {
            "id": next_case["id"],
            "original_text": next_case["original_text"],
            "trade_name": next_case["trade_name"],
            "addresses": safe_list(next_case["addresses"]),
            "old_addresses": safe_list(next_case["old_addresses"]),
            "persons": safe_list(next_case["persons"]),
            "mersis_no": next_case["mersis_no"],
            "sicil_dosya_no": next_case["sicil_dosya_no"],
            "belgeler": next_case["belgeler"],
            "hususlar": safe_list(next_case["hususlar"]),
            "ilan_sira_no": safe_list(next_case["ilan_sira_no"]),
            "pdf_url": next_case["pdf_url"],
            "pdf_page_count": next_case["pdf_page_count"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database query failed: {e}")


@router.get("/announcement-pdf/{id}")
async def get_announcement_pdf(id: str, db: Session = Depends(get_db)):
    """Fetches the PDF URL from DB, generates a presigned URL, and redirects the client to download/view it."""
    try:
        from app.models.ocr_result import OcrResult
        ocr = db.query(OcrResult).filter(OcrResult.id == int(id)).first()
        if not ocr or not ocr.pdf_url:
            raise HTTPException(status_code=404, detail="PDF path not found in database for this case")
            
        from app.core.storage import get_presigned_url
        from app.core.config import settings
        
        url = get_presigned_url(settings.minio_bucket_gazette_pdfs, ocr.pdf_url.lstrip("/"), expires=600)
        
        from fastapi.responses import RedirectResponse
        return RedirectResponse(url=url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate PDF view URL: {e}")


@router.post("/reset-evaluation", response_model=Dict[str, Any])
async def reset_evaluation():
    """Backs up the evaluation progress file and resets it."""
    import shutil
    backup_path = PROGRESS_PATH.replace(".json", "_backup.json")
    if os.path.exists(PROGRESS_PATH):
        try:
            shutil.copy(PROGRESS_PATH, backup_path)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Yedekleme başarısız: {e}")
            
    try:
        with open(PROGRESS_PATH, "w", encoding="utf-8") as f:
            json.dump({"results": []}, f)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Sıfırlama başarısız: {e}")
        
    return {"status": "success", "message": "Evaluation database backed up and reset successfully."}


class EvaluatePayload(BaseModel):
    case_id: str
    original_text: str
    trade_name: Optional[Any] = None
    addresses: List[Any] = []
    old_addresses: List[Any] = []
    persons: List[Any] = []
    mersis_no: Optional[Any] = None
    sicil_dosya_no: Optional[Any] = None
    belgeler: Optional[Any] = None
    hususlar: List[Any] = []
    ilan_sira_no: List[Any] = []

from pydantic import Field
class SiciliusEvaluateSchema(BaseModel):
    persons: List[str] = Field(default=[], description="İlanda adı geçen yönetim kurulu, ortaklar veya yetkili kişiler")
    trade_name: Optional[str] = Field(None, description="Şirketin güncel ticari unvanı")
    old_trade_name: Optional[str] = Field(None, description="Şirketin varsa eski unvanı")
    sicil_dosya_no: Optional[str] = Field(None, description="Ticaret sicil numarası")
    mersis_no: Optional[str] = Field(None, description="16 haneli MERSİS numarası")
    addresses: List[str] = Field(default=[], description="İlanda geçen güncel açık adresler")
    old_addresses: List[str] = Field(default=[], description="İlanda geçen eski/değişen adresler")
    belgeler: Optional[str] = Field(None, description="Tescile dayanak noter veya karar belgesi bilgileri")
    hususlar: List[str] = Field(default=[], description="Tescil edilen hususlar listesi")
    ilan_sira_no: List[str] = Field(default=[], description="İlan sıra numarası")

@router.post("/evaluate-announcement", response_model=Dict[str, Any])
async def evaluate_announcement(payload: EvaluatePayload):
    """Runs legacy regex extraction and calls Ollama model to produce full side-by-side comparison structure."""
    text = payload.original_text
    
    # 1. Regex Entity Extraction using backend code
    try:
        from backend.process_pdfs import extract_entities_regex as system_extract_entities
        regex_ent = system_extract_entities(text)
    except Exception as e:
        regex_ent = {
            "trade_name": payload.trade_name,
            "old_trade_name": None,
            "sicil_dosya_no": payload.sicil_dosya_no,
            "mersis_no": payload.mersis_no,
            "addresses": payload.addresses,
            "old_addresses": payload.old_addresses,
            "persons": payload.persons,
            "belgeler": payload.belgeler,
            "hususlar": payload.hususlar,
            "ilan_sira_no": payload.ilan_sira_no
        }
        
    expected_persons = []
    for p in regex_ent.get("persons", []):
        if isinstance(p, dict):
            expected_persons.append(p.get("text"))
        else:
            expected_persons.append(p)
    expected_persons = [p for p in expected_persons if p]
        
    ground_truth = {
        "persons": expected_persons,
        "trade_name": regex_ent.get("trade_name") or payload.trade_name,
        "old_trade_name": regex_ent.get("old_trade_name"),
        "sicil_dosya_no": regex_ent.get("sicil_dosya_no") or regex_ent.get("registration_number") or payload.sicil_dosya_no,
        "mersis_no": regex_ent.get("mersis_no") or payload.mersis_no,
        "addresses": regex_ent.get("addresses") or payload.addresses,
        "old_addresses": regex_ent.get("old_addresses") or payload.old_addresses,
        "belgeler": regex_ent.get("belgeler") or payload.belgeler,
        "hususlar": regex_ent.get("hususlar") or payload.hususlar,
        "ilan_sira_no": regex_ent.get("ilan_sira_no") or payload.ilan_sira_no
    }
    
    for k in ["addresses", "old_addresses", "hususlar", "ilan_sira_no"]:
        if not isinstance(ground_truth[k], list):
            ground_truth[k] = [ground_truth[k]] if ground_truth[k] else []
            
    # Ollama prompts & extract helpers
    FEW_SHOT_SYSTEM_PROMPT = """You are a precise JSON extractor. You parse Turkish Trade Registry (Ticaret Sicil) announcements.
Your output must be a single JSON object matching the exact format. Do not add any extra keys, nested dictionaries, or comments.
Do not invent or guess any keys. Ensure spelling of entities exactly matches the input text to prevent typos.

JSON format to return:
{
  "persons": ["Ad Soyad", "Ad2 Soyad2"],
  "trade_name": "Şirket Unvanı",
  "old_trade_name": "Eski Şirket Unvanı veya null",
  "sicil_dosya_no": "sicil no veya null",
  "mersis_no": "16 haneli no veya null",
  "addresses": ["Mevcut Adres Bilgisi"],
  "old_addresses": ["Eski Adres Bilgisi veya boş liste"],
  "belgeler": "Tescile delil olan noter/karar belgesi bilgileri veya null",
  "hususlar": ["Tescil edilen hususlar"],
  "ilan_sira_no": ["İlan sıra no"]
}

Rules:
1. 'persons' must be a list of strings (individual names, e.g. 'Ahmet Yılmaz'). Never return dictionaries.
2. 'addresses' and 'old_addresses' must be a list of strings. Do not invent addresses.
3. 'hususlar' must contain only the short, tescil topics (e.g. 'Sermaye Artırımı', 'Adres Değişikliği'). Do not combine multiple headers or append document details to this list.
4. If a field is not present in the text, use null (or empty list [] for array fields). Do not use dummy data or examples from prompt."""
    
    # 2. Local MLX Server Extract
    t0 = time.time()
    llm_output = None
    
    def is_likely_company(name: str) -> bool:
        name_lower = name.lower()
        company_keywords = [
            "şirket", "ltd", "ştd", "a.ş.", "aş", "ticaret", "sanayi", 
            "holding", "tic.", "san.", "servis", "gıda", "turizm", "inşaat"
        ]
        return len(name) > 35 or any(kw in name_lower for kw in company_keywords)

    def clean_address_text(addr: str) -> str:
        if not addr:
            return ""
        addr = re.sub(r"\s+", " ", addr).strip()
        
        # 1. Truncate trailing junk starting with common gazette stop words
        stop_pat = re.compile(
            r"\b(?:Tasfiyeden|Yukarıda|Yukarida|Tescil|Tescile|MERS[İI]S|Ticaret|Telefon|Tel|GSM|Faks|İlan|Ilan|Sira|Sıra|Madde|Gündem|Gundem|Genel|Vekaletname)\b",
            re.IGNORECASE
        )
        mstop = stop_pat.search(addr)
        if mstop:
            addr = addr[:mstop.start()].strip()
            
        # 2. Truncate trailing text after city name if city name is detected
        cities = [
            "istanbul", "i̇stanbul", "ankara", "izmir", "i̇zmir", "bursa", "kocaeli", 
            "antalya", "adana", "konya", "gaziantep", "şanlıurfa", "mersin", 
            "diyarbakır", "eskişehir", "denizli", "samsun", "sakarya"
        ]
        addr_lower = addr.lower()
        for city in cities:
            idx = addr_lower.find(city)
            if idx != -1:
                cleaned = addr[:idx + len(city)].strip()
                cleaned = re.sub(r"\s*[/,.-]\s*$", "", cleaned).strip()
                if len(cleaned) > 15:
                    addr = cleaned
                    break
                    
        return addr

    try:
        mlx_payload = {
            "model": MODEL_NAME,
            "messages": [
                {"role": "system", "content": FEW_SHOT_SYSTEM_PROMPT},
                {"role": "user", "content": f"Document Text:\n{text}\n\nExtract entities:"}
            ],
            "temperature": 0.0,
        }
        async with httpx.AsyncClient() as client:
            resp = await client.post(LLM_SERVER_URL, json=mlx_payload, timeout=90.0)
            if resp.status_code == 200:
                content = resp.json()["choices"][0]["message"]["content"]
                # Clean potential markdown block wrappers from the model's output
                content_clean = content.strip()
                if "```json" in content_clean:
                    content_clean = content_clean.split("```json")[1].split("```")[0].strip()
                elif "```" in content_clean:
                    content_clean = content_clean.split("```")[1].split("```")[0].strip()
                
                try:
                    import json
                    parsed_dict = json.loads(content_clean)
                    
                    # Coerce types to match SiciliusEvaluateSchema
                    # 1. persons must be List[str] and filter out companies
                    if "persons" in parsed_dict:
                        if isinstance(parsed_dict["persons"], list):
                            parsed_dict["persons"] = [
                                str(x).strip() for x in parsed_dict["persons"] 
                                if x is not None and not is_likely_company(str(x))
                            ]
                        else:
                            p_str = str(parsed_dict["persons"]).strip()
                            parsed_dict["persons"] = [p_str] if p_str and not is_likely_company(p_str) else []
                            
                    # 2. trade_name, old_trade_name, sicil_dosya_no, mersis_no, belgeler must be Optional[str]
                    for k in ["trade_name", "old_trade_name", "sicil_dosya_no", "mersis_no", "belgeler"]:
                        if k in parsed_dict:
                            if isinstance(parsed_dict[k], list):
                                parsed_dict[k] = " ".join([str(x) for x in parsed_dict[k] if x is not None]).strip() or None
                            elif parsed_dict[k] is not None:
                                parsed_dict[k] = str(parsed_dict[k]).strip()
                                
                    # 3. addresses and old_addresses: apply clean_address_text
                    for k in ["addresses", "old_addresses"]:
                        if k in parsed_dict:
                            if isinstance(parsed_dict[k], list):
                                parsed_dict[k] = [
                                    clean_address_text(str(x)) for x in parsed_dict[k] 
                                    if x is not None
                                ]
                            else:
                                a_str = clean_address_text(str(parsed_dict[k]))
                                parsed_dict[k] = [a_str] if a_str else []
                                
                    # 4. hususlar, ilan_sira_no must be List[str]
                    for k in ["hususlar", "ilan_sira_no"]:
                        if k in parsed_dict:
                            if isinstance(parsed_dict[k], list):
                                parsed_dict[k] = [str(x).strip() for x in parsed_dict[k] if x is not None]
                            else:
                                parsed_dict[k] = [str(parsed_dict[k]).strip()] if parsed_dict[k] else []
                                
                    # Validate the coerced dict
                    validated = SiciliusEvaluateSchema.model_validate(parsed_dict)
                    llm_output = validated.model_dump()
                except Exception as eval_err:
                    # Fallback to model_validate_json if manual parsing fails
                    validated = SiciliusEvaluateSchema.model_validate_json(content_clean)
                    llm_output = validated.model_dump()
    except Exception as e:
        llm_output = {"error": str(e)}
        
    if not llm_output or "error" in llm_output:
        llm_output = {
            "error": llm_output.get("error") if llm_output else "Failed to contact local MLX server",
            "persons": [],
            "trade_name": None,
            "old_trade_name": None,
            "sicil_dosya_no": None,
            "mersis_no": None,
            "addresses": [],
            "old_addresses": [],
            "belgeler": None,
            "hususlar": [],
            "ilan_sira_no": []
        }
        
    # 3. Hybrid Merge
    def clean_str_field(val):
        if val is None:
            return None
        if isinstance(val, list):
            val = " ".join(str(x).strip() for x in val if x)
        val_str = str(val).strip()
        if val_str.lower() in ["null", "none", ""]:
            return None
        return val_str
        
    def levenshtein_distance(s1, s2):
        if len(s1) < len(s2):
            return levenshtein_distance(s2, s1)
        if len(s2) == 0:
            return len(s1)
        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
        return previous_row[-1]
        
    def compute_hybrid(regex_data, llm_data):
        # 1. Trade Name Merge (Smarter fuzzy check to avoid LLM typo overrides)
        regex_tn = clean_str_field(regex_data.get("trade_name"))
        llm_tn = clean_str_field(llm_data.get("trade_name"))
        
        trade_name = None
        if regex_tn and regex_tn.lower() in text.lower():
            # Eğer Regex unvanı metinde tam geçiyorsa, LLM eksik bulsa dahi deterministik Regex'i koru
            trade_name = regex_tn
        else:
            trade_name = llm_tn or regex_tn
            
        # 2. Old Trade Name
        regex_otn = clean_str_field(regex_data.get("old_trade_name"))
        llm_otn = clean_str_field(llm_data.get("old_trade_name"))
        old_trade_name = llm_otn or regex_otn
        
        # 3. MERSIS No
        regex_m = clean_str_field(regex_data.get("mersis_no"))
        llm_m = clean_str_field(llm_data.get("mersis_no"))
        mersis_no = None
        if regex_m and re.match(r"^\d{16}$", regex_m):
            mersis_no = regex_m
        else:
            mersis_no = llm_m or regex_m
            
        # 4. Sicil No
        regex_s = clean_str_field(regex_data.get("sicil_dosya_no") or regex_data.get("registration_number"))
        llm_s = clean_str_field(llm_data.get("sicil_dosya_no"))
        sicil = llm_s or regex_s
        
        # 5. Persons
        persons_set = set()
        for p in regex_data.get("persons", []):
            if p and not is_likely_company(str(p)):
                persons_set.add(str(p).strip().upper())
        for p in llm_data.get("persons", []):
            if p and not is_likely_company(str(p)):
                persons_set.add(str(p).strip().upper())
                
        # 6. Addresses
        addresses_set = set()
        for a in regex_data.get("addresses", []):
            if a:
                cleaned_a = clean_address_text(str(a))
                if cleaned_a:
                    addresses_set.add(cleaned_a)
        for a in llm_data.get("addresses", []):
            if a:
                cleaned_a = clean_address_text(str(a))
                if cleaned_a:
                    addresses_set.add(cleaned_a)
                
        # 7. Old Addresses
        old_addresses_set = set()
        for a in regex_data.get("old_addresses", []):
            if a:
                cleaned_a = clean_address_text(str(a))
                if cleaned_a:
                    old_addresses_set.add(cleaned_a)
        for a in llm_data.get("old_addresses", []):
            if a:
                cleaned_a = clean_address_text(str(a))
                if cleaned_a:
                    old_addresses_set.add(cleaned_a)
                
        # 8. Belgeler (Prefer longer, more detailed string)
        regex_b = clean_str_field(regex_data.get("belgeler"))
        llm_b = clean_str_field(llm_data.get("belgeler"))
        if regex_b and llm_b:
            belgeler = llm_b if len(llm_b) >= len(regex_b) else regex_b
        else:
            belgeler = llm_b or regex_b
            
        # 9. Hususlar
        hususlar_set = set()
        for h in regex_data.get("hususlar", []):
            if h:
                hususlar_set.add(str(h).strip())
        for h in llm_data.get("hususlar", []):
            if h:
                hususlar_set.add(str(h).strip())
                
        # 10. İlan Sıra No
        ilan_sira_set = set()
        for i in regex_data.get("ilan_sira_no", []):
            if i:
                ilan_sira_set.add(str(i).strip())
        for i in llm_data.get("ilan_sira_no", []):
            if i:
                ilan_sira_set.add(str(i).strip())
                
        return {
            "trade_name": trade_name,
            "old_trade_name": old_trade_name,
            "sicil_dosya_no": sicil,
            "mersis_no": mersis_no,
            "addresses": sorted(list(addresses_set)),
            "old_addresses": sorted(list(old_addresses_set)),
            "persons": sorted(list(persons_set)),
            "belgeler": belgeler,
            "hususlar": sorted(list(hususlar_set)),
            "ilan_sira_no": sorted(list(ilan_sira_set))
        }
        
    hybrid_output = compute_hybrid(ground_truth, llm_output)
    
    # 4. Status analysis
    def analyze_matching(expected, llm, hybrid):
        status = "Match"
        reasons = []
        gt_tn = clean_str_field(expected.get("trade_name")) or ""
        llm_tn = clean_str_field(llm.get("trade_name")) or ""
        hy_tn = clean_str_field(hybrid.get("trade_name")) or ""
        
        if gt_tn.lower() != llm_tn.lower():
            if hy_tn.lower() == gt_tn.lower():
                status = "Hybrid Restored"
                reasons.append("Hybrid fixed Trade Name")
            else:
                status = "Mismatch"
                reasons.append("Trade Name Mismatch")
                
        gt_pers = set(str(p).lower().strip() for p in expected.get("persons", []) if p)
        llm_pers = set(str(p).lower().strip() for p in llm.get("persons", []) if p)
        
        if gt_pers != llm_pers:
            if llm_pers.issubset(gt_pers) and len(llm_pers) < len(gt_pers):
                reasons.append(f"LLM missed persons: {gt_pers - llm_pers}")
                status = "Partial Match"
            elif gt_pers.issubset(llm_pers) and len(llm_pers) > len(gt_pers):
                status = "LLM Better"
                reasons.append(f"LLM found extra persons: {llm_pers - gt_pers}")
            else:
                status = "Partial Match"
                
        if "error" in llm:
            status = "Error"
            reasons.append(str(llm["error"]))
            
        return {"status": status, "reasons": reasons}
        
    comparison = analyze_matching(ground_truth, llm_output, hybrid_output)
    latency = time.time() - t0
    
    return {
        "id": payload.case_id,
        "original_text": text,
        "ground_truth": ground_truth,
        "llm_only": llm_output,
        "hybrid": hybrid_output,
        "latency": latency,
        "comparison": comparison,
        "user_note": "",
        "field_notes": {},
        "field_notes_regex": {},
        "field_notes_hybrid": {},
        "field_approvals_hybrid": {}
    }


class SaveEvaluationResultPayload(BaseModel):
    id: str
    original_text: str
    ground_truth: Dict[str, Any]
    llm_only: Dict[str, Any]
    hybrid: Dict[str, Any]
    latency: float
    comparison: Dict[str, Any]
    user_note: str
    field_notes: Optional[Dict[str, str]] = None
    field_notes_regex: Optional[Dict[str, str]] = None
    field_notes_hybrid: Optional[Dict[str, str]] = None
    field_approvals_hybrid: Optional[Dict[str, bool]] = None

@router.post("/save-evaluation-result", response_model=Dict[str, Any])
async def save_evaluation_result(payload: SaveEvaluationResultPayload):
    """Appends a completed case and its note to evaluation_progress.json."""
    if not os.path.exists(PROGRESS_PATH):
        with open(PROGRESS_PATH, "w", encoding="utf-8") as f:
            json.dump({"results": []}, f)
            
    try:
        with open(PROGRESS_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        results = data.get("results", [])
        
        # Check if already exists to overwrite, or append
        existing_idx = -1
        for idx, r in enumerate(results):
            if str(r.get("id")) == str(payload.id):
                existing_idx = idx
                break
                
        new_entry = {
            "id": payload.id,
            "original_text": payload.original_text,
            "ground_truth": payload.ground_truth,
            "llm_only": payload.llm_only,
            "hybrid": payload.hybrid,
            "latency": payload.latency,
            "comparison": payload.comparison,
            "user_note": payload.user_note,
            "field_notes": payload.field_notes or {},
            "field_notes_regex": payload.field_notes_regex or {},
            "field_notes_hybrid": payload.field_notes_hybrid or {},
            "field_approvals_hybrid": payload.field_approvals_hybrid or {}
        }
        
        if existing_idx != -1:
            results[existing_idx] = new_entry
        else:
            results.append(new_entry)
            
        data["results"] = results
        with open(PROGRESS_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return {"status": "success", "message": f"Successfully appended case {payload.id} to progress file"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/evaluation", response_class=HTMLResponse)
async def serve_evaluation_dashboard():
    """Serves the dynamic live evaluation dashboard to perform interactive OCR comparison & annotation."""
    html_path = os.path.join(os.path.dirname(__file__), "nlp_evaluation.html")
    if not os.path.exists(html_path):
        raise HTTPException(status_code=404, detail="nlp_evaluation.html template file not found")
        
    try:
        with open(html_path, "r", encoding="utf-8") as f:
            html_content = f.read()
        return HTMLResponse(content=html_content, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read template file: {e}")
