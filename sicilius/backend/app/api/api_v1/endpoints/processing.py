import logging
import httpx
import os
import asyncio
import datetime
from fastapi import APIRouter, Depends, HTTPException, Body, Request
from pydantic import BaseModel
from supabase import Client
from typing import List, Dict, Any

from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.dependencies import get_db, get_supabase_client
from app.core.config import settings

# Configure logging

logger = logging.getLogger(__name__)

router = APIRouter()

LOCATIONIQ_API_URL = "https://us1.locationiq.com/v1/search.php"

def clean_address(address: str) -> str:
    if not address:
        return ""
    # Common cleaning steps
    address = address.strip()
    # Remove repeated city names like / İZMİR at the end
    parts = address.split('/')
    if len(parts) > 1 and 'İZMİR' in parts[-1].upper():
        # Check if the last part is just the city name (possibly with whitespace)
        if parts[-1].strip().upper() == 'İZMİR':
            address = '/'.join(parts[:-1]).strip()
    
    # Remove extra spaces
    address = ' '.join(address.split())
    return address


class CoordinateProcessingRequest(BaseModel):
    limit: int = 100

@router.post("/process-coordinates", summary="Fetch and update coordinates for companies")
async def process_coordinates(request: Request, request_body: CoordinateProcessingRequest = Body(...), db: Session = Depends(get_db)):
    """
    Fetches companies without coordinates, geocodes their addresses using LocationIQ API,
    and updates the database with the real coordinates.
    """
    limit = request_body.limit
    logger.info(f"Initiating coordinate processing for up to {limit} companies...")

    processed_count = 0
    failed_count = 0
    processed_details = []

    try:
        # 1. Fetch companies that need geocoding
        fetch_query = text("SELECT id, address FROM public.companies WHERE address IS NOT NULL AND koordinat IS NULL LIMIT :limit")
        companies_to_process = db.execute(fetch_query, {"limit": limit}).mappings().all()

        if not companies_to_process:
            logger.info("No companies found that require coordinate processing.")
            return {"message": "No companies to process.", "processed_count": 0}

        async with httpx.AsyncClient() as client:
            for company in companies_to_process:
                company_id = company['id']
                original_address = company['address']
                cleaned_address = clean_address(original_address)

                if not cleaned_address:
                    failed_count += 1
                    continue

                try:
                    # 2. Call LocationIQ API
                    params = {"key": settings.locationiq_token, "q": cleaned_address, "format": "json"}
                    api_response = await client.get(LOCATIONIQ_API_URL, params=params)
                    api_response.raise_for_status()
                    geocoding_data = api_response.json()

                    if geocoding_data:
                        first_result = geocoding_data[0]
                        lat, lon = float(first_result['lat']), float(first_result['lon'])
                        
                        # 3. Update company with new coordinates
                        update_query = text("UPDATE public.companies SET koordinat = ST_SetSRID(ST_MakePoint(:lon, :lat), 4326) WHERE id = :id")
                        db.execute(update_query, {"lon": lon, "lat": lat, "id": company_id})
                        
                        processed_count += 1
                        processed_details.append({"id": company_id, "address": original_address, "coordinate": f"POINT({lon} {lat})"})
                        logger.info(f"Successfully processed company {company_id}")
                    else:
                        logger.warning(f"Could not geocode address for company {company_id}: '{cleaned_address}'")
                        failed_count += 1

                except Exception as e:
                    logger.error(f"Error processing company {company_id}: {e}", exc_info=True)
                    failed_count += 1
                
                await asyncio.sleep(1) # Rate limit to avoid overwhelming the API

        db.commit()
        logger.info(f"Coordinate processing job finished. Processed: {processed_count}, Failed: {failed_count}")

        return {
            "message": f"Successfully processed {processed_count} companies. Failed to process {failed_count}.",
            "processed_count": processed_count,
            "failed_count": failed_count,
            "details": processed_details
        }

    except Exception as e:
        # The logger is already available in the function's scope.
        logger.error(f"An unexpected error occurred during coordinate processing: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"An unexpected server error occurred: {str(e)}")
        return {"message": "An error occurred.", "processed_count": 0, "failed_count": limit, "logs": logs, "error": error_message}


@router.post("/resolve-conflicts", summary="Find and resolve coordinate conflicts")
async def resolve_conflicts(supabase: Client = Depends(get_supabase_client)):
    """
    Finds and resolves conflicts where multiple companies share the same coordinates or addresses.
    This involves two main scenarios:
    1. Same address with multiple different coordinates.
    2. Same coordinate with multiple different addresses.

    The function re-geocodes the addresses to ensure consistency.
    """
    logs = []
    def add_log(level: str, message: str):
        timestamp = datetime.datetime.now().isoformat()
        logs.append(f"[{timestamp}] [{level.upper()}] {message}")
        logger.info(message)

    add_log("info", "Starting conflict resolution process.")

    try:
        # Fetch all companies with address and coordinates
        add_log("info", "Fetching all companies with coordinate and address data.")
        response = supabase.from_("companies").select("id, address, koordinat").not_.is_("address", "NULL").not_.is_("koordinat", "NULL").execute()
        
        if not response.data:
            add_log("info", "No companies with address and coordinate data found.")
            return {"message": "No data to process.", "logs": logs}

        companies = response.data
        add_log("info", f"Found {len(companies)} companies to analyze.")

        # --- 1. Resolve Address Conflicts (Same address, different coordinates) ---
        add_log("info", "Analyzing for address conflicts (same address, different coordinates).")
        address_map = {}
        for company in companies:
            if company.get('address') and company.get('koordinat'):
                cleaned_address = clean_address(company['address'])
                coord_val = company['koordinat']
                
                # Convert GeoJSON dict to a hashable tuple, or keep as is if already hashable
                hashable_coord = None
                if isinstance(coord_val, dict) and 'coordinates' in coord_val and isinstance(coord_val['coordinates'], list):
                    hashable_coord = tuple(coord_val['coordinates'])
                elif isinstance(coord_val, str) or isinstance(coord_val, tuple):
                    hashable_coord = coord_val
                else:
                    add_log("warning", f"Skipping unhashable or unexpected coordinate format for company ID {company.get('id')}: {coord_val}")
                    continue

                if cleaned_address not in address_map:
                    address_map[cleaned_address] = []
                address_map[cleaned_address].append(hashable_coord)

        address_conflicts = {addr: coords for addr, coords in address_map.items() if len(set(coords)) > 1}
        add_log("info", f"Found {len(address_conflicts)} addresses with conflicting coordinates.")

        async with httpx.AsyncClient() as client:
            for address, coords in address_conflicts.items():
                add_log("info", f"Resolving conflict for address: '{address}'")
                cleaned_address = clean_address(address)
                try:
                    params = {"key": settings.locationiq_token, "q": cleaned_address, "format": "json"}
                    api_response = await client.get(LOCATIONIQ_API_URL, params=params)
                    api_response.raise_for_status()
                    geocoding_data = api_response.json()

                    if geocoding_data:
                        first_result = geocoding_data[0]
                        lat, lon = float(first_result['lat']), float(first_result['lon'])
                        correct_point_wkt = f"POINT({lon} {lat})"
                        add_log("info", f"Standardizing address to coordinate: {correct_point_wkt}")
                        
                        update_response = supabase.from_("companies").update({"koordinat": correct_point_wkt}).eq("address", address).execute()
                        if not update_response.data:
                            add_log("error", f"Failed to update companies with address: {address}")
                    else:
                        add_log("warning", f"Could not re-geocode address: {address}")
                except Exception as e:
                    add_log("error", f"Error re-geocoding address '{address}': {e}")
                await asyncio.sleep(1) # Rate limiting

        # --- 2. Resolve Coordinate Conflicts (Same coordinate, different addresses) ---
        add_log("info", "Analyzing for coordinate conflicts (same coordinate, different addresses).")
        coordinate_map = {}
        for company in companies:
            if company.get('koordinat') and company.get('address'):
                cleaned_address = clean_address(company['address'])
                coord_val = company['koordinat']

                hashable_coord = None
                if isinstance(coord_val, dict) and 'coordinates' in coord_val and isinstance(coord_val['coordinates'], list):
                    hashable_coord = tuple(coord_val['coordinates'])
                elif isinstance(coord_val, str) or isinstance(coord_val, tuple):
                    hashable_coord = coord_val
                else:
                    # Already logged in the first loop, so we can just skip
                    continue

                if hashable_coord not in coordinate_map:
                    coordinate_map[hashable_coord] = []
                coordinate_map[hashable_coord].append(cleaned_address)
        
        coordinate_conflicts = {coord: addrs for coord, addrs in coordinate_map.items() if len(set(addrs)) > 1}
        add_log("info", f"Found {len(coordinate_conflicts)} coordinates with conflicting addresses.")

        summary = {
            "address_conflicts_found": len(address_conflicts),
            "coordinate_conflicts_found": len(coordinate_conflicts),
        }

        async with httpx.AsyncClient() as client:
            for coord, addresses in coordinate_conflicts.items():
                add_log("info", f"Resolving conflict for coordinate: {coord}")
                for address in set(addresses):
                    cleaned_address = clean_address(address)
                    try:
                        params = {"key": settings.locationiq_token, "q": cleaned_address, "format": "json"}
                        api_response = await client.get(LOCATIONIQ_API_URL, params=params)
                        api_response.raise_for_status()
                        geocoding_data = api_response.json()

                        if geocoding_data:
                            first_result = geocoding_data[0]
                            lat, lon = float(first_result['lat']), float(first_result['lon'])
                            new_point_wkt = f"POINT({lon} {lat})"
                            add_log("info", f"Updating address '{address}' to new coordinate: {new_point_wkt}")
                            
                            update_response = supabase.from_("companies").update({"koordinat": new_point_wkt}).eq("address", address).execute()
                            if not update_response.data:
                                add_log("error", f"Failed to update company with address: {address}")
                        else:
                            add_log("warning", f"Could not re-geocode address for conflict resolution: {address}")
                    except Exception as e:
                        add_log("error", f"Error re-geocoding address '{address}' for coordinate conflict: {e}")
                    await asyncio.sleep(1) # Rate limiting

        add_log("info", "Conflict resolution process finished.")
        return {"message": "Conflict resolution finished.", "logs": logs, "summary": summary}

    except Exception as e:
        error_message = f"An unexpected error occurred during conflict resolution: {e}"
        add_log("error", error_message)
        return {"message": "An error occurred.", "logs": logs, "error": error_message}
