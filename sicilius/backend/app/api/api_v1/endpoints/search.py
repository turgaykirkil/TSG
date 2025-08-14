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

        # Construct the 'or' filter string for Supabase (correct column names)
        filter_string = f"unvan.ilike.{search_query},sicil_no.ilike.{search_query},address.ilike.{search_query}"

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


@router.get("/all", summary="Unified search: companies, persons, history")
def search_all(
    q: str = Query(..., min_length=2, description="Search term for companies, persons and history"),
    supabase: Client = Depends(get_supabase_client),
):
    """
    Perform a unified search across multiple entities and return a combined payload:
    {
      "companies": [...],
      "persons": [...],
      "history": [...]
    }
    """
    try:
        search_term = q.strip()
        search_query = f"%{search_term.replace(' ', '%')}%"
        logger.info(f"[Unified Search] Executing search for: {search_query}")

        # --- Companies ---
        companies_data = []
        try:
            companies_filter = f"unvan.ilike.{search_query},sicil_no.ilike.{search_query},address.ilike.{search_query}"
            companies_data = (
                supabase
                .table("companies")
                .select("*")
                .or_(companies_filter)
                .limit(50)
                .execute()
            ).data or []
        except Exception as ce:
            logger.warning(f"[Unified Search] Companies query failed: {ce}")

        # --- Persons ---
        # Try to match by full name, nationality_id, email
        persons_data = []
        try:
            persons_filter = (
                f"full_name.ilike.{search_query},"
                f"first_name.ilike.{search_query},"
                f"last_name.ilike.{search_query},"
                f"nationality_id.ilike.{search_query},"
                f"email.ilike.{search_query}"
            )
            persons_data = (
                supabase
                .table("persons")
                .select("*")
                .or_(persons_filter)
                .limit(50)
                .execute()
            ).data or []
        except Exception as pe:
            logger.warning(f"[Unified Search] Persons query failed: {pe}")

        # --- History (Gazette Entries) ---
        # Select minimal fields, including related company title if available.
        # If foreign select aliasing is unsupported, backend will still return entry fields.
        history_data = []
        try:
            history_filter = f"entry_type.ilike.{search_query},processed_text.ilike.{search_query}"
            history_data = (
                supabase
                .table("gazette_entries")
                .select("id, entry_type, entry_date, company_id, processed_text")
                .or_(history_filter)
                .limit(50)
                .execute()
            ).data or []
        except Exception as he:
            logger.warning(f"[Unified Search] Gazette entries query failed: {he}")

        payload = {
            "companies": companies_data,
            "persons": persons_data,
            "history": history_data,
        }

        logger.info(
            f"[Unified Search] Results — companies: {len(companies_data)}, persons: {len(persons_data)}, history: {len(history_data)}"
        )
        return payload

    except Exception as e:
        logger.error(f"[Unified Search] Error for query '{q}': {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="An error occurred while performing unified search.")
