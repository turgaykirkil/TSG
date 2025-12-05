from __future__ import annotations

import hashlib
import logging
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

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


@dataclass(slots=True)
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


def _coerce_int(value: Optional[int | str]) -> Optional[int]:
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
    issue_number: Optional[int | str],
    page_number: Optional[int | str],
    pdf_url: Optional[str],
    pdf_page_count: Optional[int | str],
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


def _delete_source_file(source: Optional[SourceFilePayload]) -> None:
    if not source:
        return
    try:
        storage_core.remove_objects(source.bucket, [source.path])
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
    issue_number: Optional[int | str] = Query(None),
    page_number: Optional[int | str] = Query(None),
    pdf_url: Optional[str] = Query(None),
    pdf_page_count: Optional[int | str] = Query(None),
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
        _delete_source_file(source_file)

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
