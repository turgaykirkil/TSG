import logging
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException
from supabase import Client

from app.core.dependencies import get_supabase_client

router = APIRouter()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
        logger.info(f"Successfully fetched general stats: {stats}")
        
        return stats

    except Exception as e:
        logger.error(f"An unexpected error occurred while fetching general stats: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
