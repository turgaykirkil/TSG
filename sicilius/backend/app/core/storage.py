from __future__ import annotations

import io
import urllib3
from functools import lru_cache
from typing import Iterable, List, Optional, Union

from minio import Minio
from minio.deleteobjects import DeleteObject
from minio.error import S3Error

from app.core.config import settings


@lru_cache()
def get_minio_client() -> Minio:
    """Return a singleton MinIO client configured from settings."""
    return Minio(
        settings.MINIO_ENDPOINT,
        access_key=settings.MINIO_ACCESS_KEY,
        secret_key=settings.MINIO_SECRET_KEY,
        secure=settings.MINIO_SECURE,
        http_client=urllib3.PoolManager(
            timeout=urllib3.Timeout(connect=5.0, read=30.0),
            retries=urllib3.Retry(3, backoff_factor=0.2)
        ),
        region=settings.minio_region,
    )


def ensure_bucket(bucket_name: str) -> None:
    """Ensure that the given bucket exists."""
    client = get_minio_client()
    if not client.bucket_exists(bucket_name):
        client.make_bucket(bucket_name)


def upload_bytes(
    bucket_name: str,
    object_name: str,
    data: bytes,
    content_type: str = "application/octet-stream",
) -> str:
    """Upload raw bytes to the given bucket/object path."""
    ensure_bucket(bucket_name)
    client = get_minio_client()
    data_stream = io.BytesIO(data)
    client.put_object(
        bucket_name,
        object_name,
        data_stream,
        length=len(data),
        content_type=content_type,
    )
    return object_name


def upload_stream(
    bucket_name: str,
    object_name: str,
    stream,
    length: int,
    content_type: str = "application/octet-stream",
) -> str:
    """Upload a stream with known length to MinIO."""
    ensure_bucket(bucket_name)
    client = get_minio_client()
    client.put_object(
        bucket_name,
        object_name,
        stream,
        length=length,
        content_type=content_type,
    )
    return object_name


def list_objects(bucket_name: str, prefix: Optional[str] = None, limit: Optional[int] = None) -> List[dict]:
    """List objects in a bucket (recursively)."""
    client = get_minio_client()
    if not client.bucket_exists(bucket_name):
        return []
    objects = client.list_objects(bucket_name, prefix=prefix, recursive=True)
    results: List[dict] = []
    
    count = 0
    for obj in objects:
        results.append(
            {
                "object_name": obj.object_name,
                "size": obj.size,
                "last_modified": obj.last_modified.isoformat() if obj.last_modified else None,
                "is_dir": obj.is_dir,
            }
        )
        count += 1
        if limit is not None and count >= limit:
            break
            
    return results


def get_presigned_url(bucket_name: str, object_name: str, expires: Union[int, float] = 3600) -> str:
    """Return a presigned GET url for an object.

    MinIO istemcisi `datetime.timedelta` beklediğinden, saniye cinsinden gelen değerleri
    uygunsa timedelta'ya çeviriyoruz."""
    client = get_minio_client()
    from datetime import timedelta

    expires_delta = expires
    if isinstance(expires, (int, float)):
        # MinIO >=7.1 için alt sınır 1 sn, üst sınır 7 gün (604800 sn)
        total_seconds = max(1, min(int(expires), 604800))
        expires_delta = timedelta(seconds=total_seconds)

    return client.get_presigned_url(
        "GET",
        bucket_name,
        object_name,
        expires=expires_delta,
    )


def remove_objects(bucket_name: str, object_names: Iterable[str]) -> None:
    """Remove a batch of objects."""
    client = get_minio_client()
    if not client.bucket_exists(bucket_name):
        return

    delete_objects = [DeleteObject(name) for name in object_names if name]
    if not delete_objects:
        return

    errors = client.remove_objects(bucket_name, delete_objects)
    for err in errors:
        # Ensure we surface issues during deletion in logs
        raise S3Error(err.code, err.message, err.resource, err.request_id, err.host_id)


def object_exists(bucket_name: str, object_name: str) -> bool:
    client = get_minio_client()
    try:
        client.stat_object(bucket_name, object_name)
        return True
    except S3Error:
        return False
