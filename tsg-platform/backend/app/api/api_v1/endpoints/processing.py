import logging
import httpx
import os
import asyncio
import datetime
from fastapi import APIRouter, Depends, HTTPException, Body, Request
from pydantic import BaseModel
from supabase import Client
from typing import List, Dict, Any

from app.core.dependencies import get_supabase_client
from app.core.config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

LOCATIONIQ_API_URL = "https://us1.locationiq.com/v1/search.php"

class CoordinateProcessingRequest(BaseModel):
    limit: int = 100

@router.post("/process-coordinates", summary="Fetch and update coordinates for companies")
async def process_coordinates(request: Request, request_body: CoordinateProcessingRequest = Body(...), supabase: Client = Depends(get_supabase_client)):
    """
    Fetches companies with missing coordinates, geocodes their addresses using LocationIQ,
    and updates the database. Returns a log of operations.
    """
    limit = request_body.limit
    logs = []

    def add_log(level: str, message: str):
        timestamp = datetime.datetime.now().isoformat()
        logs.append(f"[{timestamp}] [{level.upper()}] {message}")
        # Also log to server console for debugging
        if level == 'error':
            logger.error(message)
        elif level == 'warning':
            logger.warning(message)
        else:
            logger.info(message)

    try:
        add_log("info", f"Starting coordinate processing job for up to {limit} companies.")

        if not settings.locationiq_token or settings.locationiq_token == 'YOUR_TOKEN_HERE':
            add_log("error", "LocationIQ token is not configured in the .env file.")
            raise HTTPException(status_code=500, detail="Geocoding service is not configured.")

        processed_count = 0
        failed_count = 0

        add_log("info", f"Fetching up to {limit} companies with null coordinates.")
        response = supabase.from_("companies").select("id, address").is_("koordinat", "NULL").limit(limit).execute()

        if not response.data:
            add_log("info", "No companies found without coordinates.")
            return {"message": "No companies to process.", "processed_count": 0, "failed_count": 0, "logs": logs}

        companies_to_process = response.data
        add_log("info", f"Found {len(companies_to_process)} companies to process.")

        async with httpx.AsyncClient() as client:
            for company in companies_to_process:
                address = company.get('address')
                company_id = company.get('id')

                if not address:
                    add_log("warning", f"Company ID {company_id} has no address, skipping.")
                    failed_count += 1
                    continue

                try:
                    add_log("info", f"Geocoding address for company ID {company_id}: {address}")
                    api_response = await client.get(
                        LOCATIONIQ_API_URL,
                        params={"key": settings.locationiq_token, "q": address, "format": "json"}
                    )
                    api_response.raise_for_status()
                    
                    geocoding_data = api_response.json()
                    if not geocoding_data:
                        raise ValueError("No geocoding data returned")

                    first_result = geocoding_data[0]
                    lat, lon = float(first_result['lat']), float(first_result['lon'])
                    point_wkt = f"POINT({lon} {lat})"
                    
                    add_log("info", f"Updating company ID {company_id} with geometry coordinates: {point_wkt}")
                    update_response = supabase.from_("companies").update({"koordinat": point_wkt}).eq("id", company_id).execute()

                    if update_response.data:
                        processed_count += 1
                        add_log("info", f"Successfully updated company ID {company_id}.")
                    else:
                        raise Exception(f"Failed to update company ID {company_id} in database.")

                except httpx.HTTPStatusError as e:
                    failed_count += 1
                    if e.response.status_code == 429:
                        add_log("warning", f"Rate limit hit. Pausing for 10 seconds.")
                        await asyncio.sleep(10)
                    add_log("error", f"HTTP error for company ID {company_id}. Status: {e.response.status_code}. Reason: {e}")
                except Exception as e:
                    failed_count += 1
                    add_log("error", f"Failed to process company ID {company_id}. Reason: {e}")

                await asyncio.sleep(1)

        add_log("info", f"Coordinate processing job finished. Processed: {processed_count}, Failed: {failed_count}")
        return {"message": "Coordinate processing finished.", "processed_count": processed_count, "failed_count": failed_count, "logs": logs}

    except Exception as e:
        error_message = f"An unexpected error occurred during coordinate processing: {e}"
        add_log("error", error_message)
        # Do not raise HTTPException here to ensure logs are returned
        return {"message": "An error occurred.", "processed_count": 0, "failed_count": limit, "logs": logs, "error": error_message}
    finally:
        add_log("info", "Coordinate processing job function finished.")


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
