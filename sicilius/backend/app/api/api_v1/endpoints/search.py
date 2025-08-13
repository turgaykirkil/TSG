from fastapi import APIRouter, Depends, HTTPException, Query
from supabase import Client
from app.core.dependencies import get_supabase_client
import logging

router = APIRouter()

# Configure logging

logger = logging.getLogger(__name__)

@router.get("/search", summary="Search for companies")
def search_companies(q: str = Query(..., min_length=2, description="Search term for companies"), supabase: Client = Depends(get_supabase_client)):
    """
    Searches for companies in the database based on a query term.
    The search is performed on company name, registration number, and address.
    """
    try:
        search_query = f"%{q.strip().replace(' ', '%')}%"
        logger.info(f"Executing search for: {search_query}")

        # Construct the 'or' filter string for Supabase
        filter_string = f"firma_unvani.ilike.{search_query},sicil_no.ilike.{search_query},adres.ilike.{search_query}"

        # Execute the query using the correct .or_ method
        response = (
            supabase.table("companies")
            .select("*")
            .or_(filter_string)
            .limit(50)
            .execute()
        )

        if response.data:
            logger.info(f"Found {len(response.data)} companies for query: '{q}'")
        else:
            logger.info(f"No companies found for query: '{q}'")

        return response.data

    except Exception as e:
        logger.error(f"Error during company search for query '{q}': {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="An error occurred while searching for companies.")
