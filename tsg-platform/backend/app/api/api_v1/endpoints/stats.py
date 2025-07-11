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
    Retrieves key statistics from the database:
    - Total number of companies
    - Number of companies processed by scraping
    - Number of companies processed by OCR
    """
    try:
        logger.info("Fetching company statistics using supabase-py methods...")

        # Get total companies
        total_res = supabase.table("companies").select("sicil_no", count="exact").execute()
        total_companies = total_res.count if total_res.count is not None else 0

        # Get scraped companies (where scraped_at is not null)
        scraped_res = supabase.table("companies").select("scraped_at", count="exact").not_.is_("scraped_at", "null").execute()
        scraped_companies = scraped_res.count if scraped_res.count is not None else 0

        # Get OCR processed companies
        # Get total announcements (assuming this is what OCR processed count represents)
        announcements_res = supabase.table("announcements").select("*", count="exact").execute()
        total_announcements = announcements_res.count if announcements_res.count is not None else 0

        # Get companies added in the last 24 hours
        time_24_hours_ago = (datetime.now(timezone.utc) - timedelta(hours=24)).isoformat()
        new_companies_res = (
            supabase.table("companies")
            .select("created_at", count="exact")
            .gte("created_at", time_24_hours_ago)
            .execute()
        )
        new_companies_today = new_companies_res.count if new_companies_res.count is not None else 0

        logger.info(f"Stats fetched: Total={total_companies}, Scraped={scraped_companies}, Announcements={total_announcements}, NewToday={new_companies_today}")

        return {
            "total_companies": total_companies,
            "scraped_companies": scraped_companies,
            "total_announcements": total_announcements,
            "new_companies_today": new_companies_today,
        }

    except Exception as e:
        logger.error(f"Error fetching stats from Supabase: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to fetch statistics from database.")
