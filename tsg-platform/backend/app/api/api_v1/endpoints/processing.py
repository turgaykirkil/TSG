import logging
import httpx
import os
from fastapi import APIRouter, Depends, HTTPException, Body
from pydantic import BaseModel
from supabase import Client
from typing import List, Dict, Any

from app.core.dependencies import get_supabase_client

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# Get LocationIQ Token from environment variables
LOCATIONIQ_TOKEN = os.getenv("TSG_LOCATIONIQ_TOKEN")
LOCATIONIQ_API_URL = "https://us1.locationiq.com/v1/search.php"

class CoordinateProcessingRequest(BaseModel):
    limit: int = 100

@router.post("/process-coordinates", summary="Fetch and update coordinates for companies")
async def process_coordinates(request_body: CoordinateProcessingRequest = Body(...) ,supabase: Client = Depends(get_supabase_client)):
    """
    Fetches companies with missing coordinates, geocodes their addresses using LocationIQ,
    and updates the database.
    """
    limit = request_body.limit
    logger.info(f"Starting coordinate processing job for up to {limit} companies.")

    if not LOCATIONIQ_TOKEN or LOCATIONIQ_TOKEN == 'YOUR_TOKEN_HERE':
        logger.error("LocationIQ token is not configured in the .env file.")
        raise HTTPException(status_code=500, detail="Geocoding service is not configured.")

    processed_count = 0
    failed_count = 0

    try:
        # 1. Fetch companies without coordinates
        logger.info(f"Fetching up to {limit} companies with null coordinates.")
        response = supabase.from_("companies").select("id, address").is_("latitude", "NULL").limit(limit).execute()

        if not response.data:
            logger.info("No companies found without coordinates.")
            return {"message": "No companies to process.", "processed_count": 0, "failed_count": 0}

        companies_to_process = response.data
        logger.info(f"Found {len(companies_to_process)} companies to process.")

        async with httpx.AsyncClient() as client:
            for company in companies_to_process:
                address = company.get('address')
                company_id = company.get('id')

                if not address:
                    logger.warning(f"Company ID {company_id} has no address, skipping.")
                    failed_count += 1
                    continue

                try:
                    # 2. Geocode address using LocationIQ
                    logger.info(f"Geocoding address for company ID {company_id}: {address}")
                    api_response = await client.get(
                        LOCATIONIQ_API_URL,
                        params={"key": LOCATIONIQ_TOKEN, "q": address, "format": "json"}
                    )
                    api_response.raise_for_status() # Raise an exception for 4xx or 5xx status codes
                    
                    geocoding_data = api_response.json()
                    if not geocoding_data:
                        raise ValueError("No geocoding data returned")

                    # 3. Update company with coordinates
                    first_result = geocoding_data[0]
                    lat, lon = float(first_result['lat']), float(first_result['lon'])
                    
                    logger.info(f"Updating company ID {company_id} with coordinates: Lat={lat}, Lon={lon}")
                    update_response = supabase.from_("companies").update({"latitude": lat, "longitude": lon}).eq("id", company_id).execute()

                    if update_response.data:
                        processed_count += 1
                        logger.info(f"Successfully updated company ID {company_id}.")
                    else:
                        raise Exception(f"Failed to update company ID {company_id} in database.")

                except Exception as e:
                    failed_count += 1
                    logger.error(f"Failed to process company ID {company_id}. Reason: {e}", exc_info=True)

        logger.info(f"Coordinate processing job finished. Processed: {processed_count}, Failed: {failed_count}")
        return {"message": "Coordinate processing finished.", "processed_count": processed_count, "failed_count": failed_count}

    except Exception as e:
        logger.error(f"An unexpected error occurred during coordinate processing: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")


@router.post("/resolve-conflicts", summary="Find and resolve coordinate conflicts")
async def resolve_conflicts(supabase: Client = Depends(get_supabase_client)):
    """
    Finds and resolves conflicts where multiple companies share the same coordinates or addresses.
    NOTE: This is a placeholder for a future, more complex implementation.
    """
    logger.info("Conflict resolution process started.")
    try:
        # TODO: Implement the actual conflict resolution logic.
        # This will likely involve complex SQL queries or another RPC function to:
        # 1. Find addresses used by more than one company but with different coordinates.
        # 2. Find coordinates used by more than one company but with different addresses.
        # For now, we just return a success message.
        logger.info("Conflict resolution feature is under development. No action taken.")
        return {"message": "Conflict resolution feature is under development."}
    except Exception as e:
        logger.error(f"An error occurred during conflict resolution placeholder: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="An error occurred during conflict resolution.")
