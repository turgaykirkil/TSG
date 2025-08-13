import logging
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException
from supabase import Client

from app.core.dependencies import get_supabase_client

router = APIRouter()

# Configure logging

logger = logging.getLogger(__name__)

@router.get("/storage-pdfs-count", summary="Get total count of PDF files in gazette-pdfs bucket")
def get_storage_pdfs_count(supabase: Client = Depends(get_supabase_client)):
    """
    Supabase Storage içindeki 'gazette-pdfs' bucket'ında bulunan PDF dosyalarının toplam sayısını döndürür.
    Büyük hacimler için sayımı limit/offset ile sayfalar halinde yapar. Sadece .pdf uzantılı dosyalar sayılır.
    """
    BUCKET = "gazette-pdfs"
    limit = 1000
    total = 0
    # Klasörleri gezmek için BFS kuyruğu
    queue = [""]  # root path
    try:
        while queue:
            current = queue.pop(0)
            offset = 0
            while True:
                # Not: list(path, options) — options: {limit, offset, search, sortBy}
                listing = supabase.storage.from_(BUCKET).list(current, {"limit": limit, "offset": offset, "sortBy": {"column": "name", "order": "asc"}})
                items = listing or []
                # Bazı sürümlerde .list() {'data': [...], 'error': None} döndürebilir
                if isinstance(items, dict) and "data" in items:
                    items = items.get("data") or []
                count = 0
                for obj in items:
                    name = ""
                    try:
                        name = (obj.get("name") or obj.get("Key") or "")
                    except AttributeError:
                        name = ""
                    lower = name.lower()
                    # metadata None ise klasör olarak kabul et
                    is_folder = obj.get("metadata") in (None, {}) and not lower.endswith(".pdf")
                    if is_folder and name:
                        next_path = f"{current}/{name}" if current else name
                        queue.append(next_path)
                    elif lower.endswith(".pdf"):
                        count += 1
                total += count
                logger.debug("storage list page BUCKET=%s path=%s offset=%s got=%s pdf_in_page=%s", BUCKET, current, offset, len(items), count)
                if not items or len(items) < limit:
                    break
                offset += limit
        return {"bucket": BUCKET, "pdf_count": total}
    except Exception as e:
        logger.error("Failed to list storage bucket: %s", e, exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to count PDFs in storage: {e}")

@router.get("/coordinates", summary="Get coordinate statistics")
def get_coordinate_stats(supabase: Client = Depends(get_supabase_client)):
    """
    Retrieves statistics about company coordinates from the database by calling a dedicated RPC function.
    This is highly efficient as all computation is done on the database side.
    """
    try:
        logger.info("Fetching coordinate stats via RPC call...")
        response = supabase.rpc('get_coordinate_statistics').execute()
        
        if not response.data:
            logger.error("Failed to get data from RPC call 'get_coordinate_statistics'")
            raise HTTPException(status_code=500, detail="Could not retrieve coordinate statistics.")

        # The RPC function returns a single JSON object, not a list.
        stats = response.data
        logger.info(f"Successfully fetched coordinate stats: {stats}")
        
        return stats

    except Exception as e:
        logger.error(f"An unexpected error occurred while fetching coordinate stats: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")


@router.get("", summary="Get application-wide statistics", include_in_schema=False)
@router.get("/", summary="Get application-wide statistics")
def get_stats(supabase: Client = Depends(get_supabase_client)):
    """
    Retrieves key statistics from the database by calling a dedicated RPC function.
    This is highly efficient as all computation is done on the database side.
    """
    try:
        logger.info("Fetching general statistics via RPC call 'get_general_statistics'...")
        response = supabase.rpc('get_general_statistics').execute()
        
        if not response.data:
            logger.error("Failed to get data from RPC call 'get_general_statistics'")
            raise HTTPException(status_code=500, detail="Could not retrieve general statistics.")

        # The RPC function returns a single JSON object in a list.
        stats = response.data[0]
        # Storage PDF sayısını da ekle (hata olsa bile ana istatistiği döndür)
        try:
            BUCKET = "gazette-pdfs"
            limit = 1000
            total = 0
            queue = [""]
            while queue:
                current = queue.pop(0)
                offset = 0
                while True:
                    listing = supabase.storage.from_(BUCKET).list(current, {"limit": limit, "offset": offset, "sortBy": {"column": "name", "order": "asc"}})
                    items = listing or []
                    if isinstance(items, dict) and "data" in items:
                        items = items.get("data") or []
                    count = 0
                    for obj in items:
                        name = ""
                        try:
                            name = (obj.get("name") or obj.get("Key") or "")
                        except AttributeError:
                            name = ""
                        lower = name.lower()
                        is_folder = obj.get("metadata") in (None, {}) and not lower.endswith(".pdf")
                        if is_folder and name:
                            next_path = f"{current}/{name}" if current else name
                            queue.append(next_path)
                        elif lower.endswith(".pdf"):
                            count += 1
                    total += count
                    if not items or len(items) < limit:
                        break
                    offset += limit
            stats["storage_pdf_count"] = total
        except Exception:
            # Sükut-u hayal olmasın diye yutuyoruz; stats yine de dönsün
            stats.setdefault("storage_pdf_count", None)
        logger.info(f"Successfully fetched general stats: {stats}")
        return stats

    except Exception as e:
        logger.error(f"An unexpected error occurred while fetching general stats: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
