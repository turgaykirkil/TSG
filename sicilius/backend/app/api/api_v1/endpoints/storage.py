from fastapi import APIRouter, Depends, HTTPException
from supabase import Client
from app.core.dependencies import get_supabase_client
import logging

router = APIRouter()

logger = logging.getLogger(__name__)

@router.get("/list-announcement-files", response_model=list)
def list_announcement_files(
    supabase: Client = Depends(get_supabase_client)
):
    """
    Lists all files in the 'announcements' bucket in Supabase Storage.
    """
    try:
        files = supabase.storage.from_("gazette-pdfs").list()
        # The list() method returns a list of file objects (dictionaries).
        # We return this list directly as the frontend expects this structure.
        return files
    except Exception as e:
        logger.error(f"Error listing files from Supabase: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to list files from Supabase Storage: {str(e)}"
        )
