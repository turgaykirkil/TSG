from typing import Any, Dict, List, Optional
import logging

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from supabase import Client

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/", response_model=List[schemas.Announcement])
def read_announcements(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve announcements.
    """
    announcements = crud.announcement.get_multi(db, skip=skip, limit=limit)
    return announcements


@router.get("/resolve", response_model=Dict[str, Any])
def resolve_announcement(
    publication_date: str = Query(..., description="YYYY-MM-DD"),
    issue_number: int = Query(...),
    page_number: int = Query(...),
    pdf_url: Optional[str] = Query(None),
    supabase: Client = Depends(deps.get_supabase_client),
) -> Dict[str, Any]:
    """
    Verilen (tarih, sayı, sayfa) ve opsiyonel pdf_url bilgisi ile Supabase üzerindeki
    announcements tablosundan ilgili ilan kimliğini ve temel metadatasını döner.
    """
    try:
        params = {
            "_publication_date": publication_date,
            "_issue_number": issue_number,
            "_page_number": page_number,
            "_pdf_url": pdf_url,
        }
        ann_res = supabase.rpc("fn_find_announcement_id", params).execute()
        ann_id = (ann_res.data if hasattr(ann_res, "data") else None) or None
        if not ann_id:
            raise HTTPException(status_code=404, detail="Announcement not found for given keys")

        row_res = (
            supabase
            .table("announcements")
            .select("id, publication_date, issue_number, page_number, pdf_url")
            .eq("id", ann_id)
            .limit(1)
            .execute()
        )
        rows = getattr(row_res, "data", None) or []
        meta = rows[0] if rows else {"id": ann_id}
        return {
            "found": True,
            "id": ann_id,
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error("/announcements/resolve failed: %s", e, exc_info=True)
        raise HTTPException(status_code=500, detail=f"resolve failed: {e}")

@router.get("/resolve-by-file-name", response_model=Dict[str, Any])
def resolve_by_file_name(
    *,
    file_name: str = Query(..., description="The PDF file name as stored in Supabase (e.g., announcement_<uuid>_<...>.pdf)"),
    db: Session = Depends(deps.get_db),
):
    """
    Resolve an announcement by its PDF file_name (matches within `pdf_url`).
    Returns the `id` (announcement_id) and basic meta fields if found.
    """
    try:
        ann = crud.announcement.get_by_file_name(db, file_name=file_name)
        if not ann:
            raise HTTPException(status_code=404, detail="Announcement not found for given file_name")
        # Build minimal meta payload
        try:
            logger.info("resolve-by-file-name: file_name=%s -> announcement_id=%s", file_name, str(ann.id))
        except Exception:
            pass
        meta = {
            "id": str(ann.id),
            "publication_date": getattr(ann, "publication_date", None),
            "issue_number": getattr(ann, "issue_number", None),
            "page_number": getattr(ann, "page_number", None),
            "pdf_url": getattr(ann, "pdf_url", None),
        }
        return {"found": True, "id": str(ann.id), "announcement": meta}
    except HTTPException:
        raise
    except Exception as e:
        logger.error("/announcements/resolve-by-file-name failed: %s", e, exc_info=True)
        raise HTTPException(status_code=500, detail=f"resolve-by-file-name failed: {e}")
