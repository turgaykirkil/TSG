import logging
import httpx
import os
import asyncio
import datetime
import re
import unicodedata
from fastapi import APIRouter, Depends, HTTPException, Body, Request
from pydantic import BaseModel
from app.core.dependencies import get_db
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy import text
from app.core.config import settings
from app.db.session import SessionLocal
from app.models.company import Company
from geoalchemy2.elements import WKTElement

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


from app.services.geocoding_service import geocode_address, clean_address

class CoordinateProcessingRequest(BaseModel):
    limit: int = 100

async def geocode_company_by_id(db: Session, company_id: Any, address: str) -> bool:
    """
    Geocodes a single company by ID and updates the DB using the central geocoding service.
    Returns True if successful, False otherwise.
    """
    if not address:
        return False
        
    try:
        # Use the central geocoding engine
        geocoding_result = await geocode_address(db, address)

        if geocoding_result:
            lat, lon = geocoding_result['lat'], geocoding_result['lon']
            
            # Use ORM to avoid table name resolution issues
            company = db.query(Company).filter(Company.id == company_id).first()
            if company:
                company.koordinat = WKTElement(f'POINT({lon} {lat})', srid=4326)
                db.commit()
                return True
            else:
                logger.error(f"Company {company_id} not found during geocoding update.")
                return False
        else:
            logger.warning(f"Could not geocode address via engine for company {company_id}: '{address}'")
            return False

    except Exception as e:
        # Critical: Rollback session on DB errors to prevent 'Aborted Transaction' loops
        db.rollback()
        logger.error(f"Error geocoding company {company_id}: {e}")
        return False

async def process_background_geocoding(company_ids: List[str]):
    """
    Background task to process a list of missing coordinates.
    Creates its own DB session to ensure separate lifecycle from the request.
    """
    if not company_ids:
        return

    logger.info(f"Background Geocoding initiated for {len(company_ids)} companies.")
    db = SessionLocal()
    try:
        companies = db.query(Company).filter(Company.id.in_(company_ids)).all()
        for comp in companies:
            if comp.address and not comp.koordinat:
                await geocode_company_by_id(db, comp.id, comp.address)
    except Exception as e:
        logger.error(f"Error in background geocoding task: {e}")
    finally:
        db.close()

@router.post("/process-coordinates", summary="Fetch and update coordinates for companies")
@router.post("/process-coordinates/", summary="Fetch and update coordinates for companies")
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
        fetch_query = text("SELECT id, address FROM app.companies WHERE address IS NOT NULL AND koordinat IS NULL LIMIT :limit")
        companies_to_process = db.execute(fetch_query, {"limit": limit}).mappings().all()

        if not companies_to_process:
            logger.info("No companies found that require coordinate processing.")
            return {"message": "No companies to process.", "processed_count": 0}

        for company in companies_to_process:
            company_id = company['id']
            original_address = company['address']
            
            success = await geocode_company_by_id(db, company_id, original_address)
            
            if success:
                processed_count += 1
                # We can't easily get the lon/lat back without re-querying or modifying the helper return,
                # but for bulk logs simple success/fail is usually enough or we assume it worked.
                processed_details.append({"id": company_id, "address": original_address, "status": "processed"})
            else:
                failed_count += 1
            
            await asyncio.sleep(0.5) # Rate limit

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


@router.post("/resolve-conflicts", summary="Find and resolve coordinate conflicts")
@router.post("/resolve-conflicts/", summary="Find and resolve coordinate conflicts")
async def resolve_conflicts(db: Session = Depends(get_db)):
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
        # Using raw SQL for PostGIS types handling might be easier, or just fetch as text
        fetch_query = text("SELECT id, address, ST_AsText(koordinat) as koordinat_wkt FROM app.companies WHERE address IS NOT NULL AND koordinat IS NOT NULL")
        result = db.execute(fetch_query).mappings().all()
        
        if not result:
            add_log("info", "No companies with address and coordinate data found.")
            return {"message": "No data to process.", "logs": logs}

        companies = result
        add_log("info", f"Found {len(companies)} companies to analyze.")

        # --- 1. Resolve Address Conflicts (Same address, different coordinates) ---
        add_log("info", "Analyzing for address conflicts (same address, different coordinates).")
        address_map = {}
        for company in companies:
            if company['address'] and company['koordinat_wkt']:
                cleaned_address = clean_address(company['address'])
                coord_val = company['koordinat_wkt'] # WKT string like POINT(30 40)
                
                if cleaned_address not in address_map:
                    address_map[cleaned_address] = []
                address_map[cleaned_address].append(coord_val)

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
                        # Update using SQL
                        update_query = text("UPDATE app.companies SET koordinat = ST_SetSRID(ST_MakePoint(:lon, :lat), 4326) WHERE address = :address")
                        db.execute(update_query, {"lon": lon, "lat": lat, "address": address})
                        db.commit()
                        
                        add_log("info", f"Standardizing address to coordinate: POINT({lon} {lat})")
                    else:
                        add_log("warning", f"Could not re-geocode address: {address}")
                except Exception as e:
                    add_log("error", f"Error re-geocoding address '{address}': {e}")
                await asyncio.sleep(1) # Rate limiting

        # --- 2. Resolve Coordinate Conflicts (Same coordinate, different addresses) ---
        add_log("info", "Analyzing for coordinate conflicts (same coordinate, different addresses).")
        coordinate_map = {}
        for company in companies:
            if company['koordinat_wkt'] and company['address']:
                cleaned_address = clean_address(company['address'])
                coord_val = company['koordinat_wkt']

                if coord_val not in coordinate_map:
                    coordinate_map[coord_val] = []
                coordinate_map[coord_val].append(cleaned_address)
        
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
                            
                            update_query = text("UPDATE app.companies SET koordinat = ST_SetSRID(ST_MakePoint(:lon, :lat), 4326) WHERE address = :address")
                            db.execute(update_query, {"lon": lon, "lat": lat, "address": address})
                            db.commit()
                            
                            add_log("info", f"Updating address '{address}' to new coordinate: POINT({lon} {lat})")
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
