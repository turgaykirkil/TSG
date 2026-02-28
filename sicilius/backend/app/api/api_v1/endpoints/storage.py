import logging
from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Path, Query
from pydantic import BaseModel

from app import models
from app.api import deps
from app.core.config import settings
from app.core.storage import get_presigned_url, list_objects, object_exists

router = APIRouter()

logger = logging.getLogger(__name__)


class StorageObject(BaseModel):
    object_name: str
    size: int
    last_modified: Optional[datetime]


class PresignedUrlResponse(BaseModel):
    url: str
    expires_in: int


@router.get("/announcements", response_model=List[StorageObject])
def list_announcement_files(
    prefix: Optional[str] = Query(default=None, description="Alt klasör filtrelemesi"),
    limit: int = Query(default=500, ge=1, le=5000, description="Döndürülecek maksimum kayıt sayısı"),
    _: models.User = Depends(deps.get_current_active_superuser),
):
    """MinIO üzerindeki gazete PDF’lerini listeler."""
    try:
        objects = list_objects(settings.minio_bucket_gazette_pdfs, prefix=prefix, limit=limit)
    except Exception as exc:  # pragma: no cover - ağ/erişim hatası
        logger.error("MinIO list_objects failed: %s", exc, exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to list files from storage: {exc}")

    serialized: List[StorageObject] = []
    for entry in objects:
        try:
            last_modified = (
                datetime.fromisoformat(entry["last_modified"]) if entry.get("last_modified") else None
            )
        except Exception:
            last_modified = None
        serialized.append(
            StorageObject(
                object_name=entry.get("object_name"),
                size=int(entry.get("size", 0)),
                last_modified=last_modified,
            )
        )
    return serialized


@router.get(
    "/announcements/{object_path:path}/download",
    response_model=PresignedUrlResponse,
)
def get_announcement_download_url(
    object_path: str = Path(..., description="MinIO içindeki dosya yolu"),
    expires: int = Query(default=3600, ge=60, le=604800, description="İmzanın geçerlilik süresi (saniye)"),
    _: deps.models.User = Depends(deps.get_current_active_superuser),
):
    """Gazete PDF’si için ön imzalı URL oluştur."""
    normalized_path = object_path.lstrip("/")
    if not normalized_path:
        raise HTTPException(status_code=400, detail="object_path boş olamaz")
    if ".." in normalized_path.split("/"):
        raise HTTPException(status_code=400, detail="Geçersiz object_path")

    if not object_exists(settings.minio_bucket_gazette_pdfs, normalized_path):
        raise HTTPException(status_code=404, detail="Dosya bulunamadı")

    try:
        url = get_presigned_url(settings.minio_bucket_gazette_pdfs, normalized_path, expires=expires)
    except Exception as exc:  # pragma: no cover - ağ/erişim hatası
        logger.error("MinIO presigned URL generation failed: %s", exc, exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to generate download URL: {exc}")

    return PresignedUrlResponse(url=url, expires_in=min(expires, 604800))
