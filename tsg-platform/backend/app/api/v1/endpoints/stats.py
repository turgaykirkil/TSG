import logging
from fastapi import APIRouter, Depends, HTTPException
from supabase import create_client, Client

from app.core.config import settings

router = APIRouter()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_supabase_client() -> Client:
    if not settings.SUPABASE_URL or not settings.SUPABASE_KEY:
        raise HTTPException(status_code=500, detail="Supabase URL or Key not configured")
    supabase_url = str(settings.SUPABASE_URL)
    supabase_key = settings.SUPABASE_KEY
    return create_client(supabase_url, supabase_key)

@router.get("/stats", summary="Get application-wide statistics")
def get_stats(supabase: Client = Depends(get_supabase_client)):
    """
    Retrieves key statistics from the database, such as total companies, 
    scraped companies, and companies with coordinates.
    """
    try:
        logger.info("Fetching total companies...")
        total_companies_res = supabase.table("companies").select("id", count="exact").execute()
        total_companies = total_companies_res.count
        logger.info(f"Total companies: {total_companies}")

        logger.info("Fetching scraped companies...")
        scraped_companies_res = supabase.table("companies").select("id", count="exact").filter("last_scraped_at", "not.is", "null").execute()
        scraped_companies = scraped_companies_res.count
        logger.info(f"Scraped companies: {scraped_companies}")

        logger.info("Fetching companies with coordinates...")
        with_coordinates_res = supabase.table("companies").select("id", count="exact").filter("koordinat", "not.is", "null").execute()
        with_coordinates = with_coordinates_res.count
        logger.info(f"Companies with coordinates: {with_coordinates}")

        return {
            "totalCompanies": total_companies,
            "scrapedCompanies": scraped_companies,
            "withCoordinates": with_coordinates
        }
    except Exception as e:
        logger.error(f"Error fetching stats from Supabase: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to fetch statistics from database.")
