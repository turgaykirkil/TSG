
from app.core.config import settings
print(f"DEBUG_SETTINGS: MINIO_ENDPOINT='{settings.MINIO_ENDPOINT}'")
print(f"DEBUG_SETTINGS: MINIO_ACCESS_KEY='{settings.MINIO_ACCESS_KEY}'")
print(f"DEBUG_SETTINGS: BUCKET_PDFS='{settings.minio_bucket_gazette_pdfs}'")
print(f"DEBUG_SETTINGS: BUCKET_COMPS='{settings.minio_bucket_company_gazettes}'")
