import os
import httpx
import asyncio
import hashlib
import logging
import re
import unicodedata
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from app.models.geocoding_cache import GeocodingCache

logger = logging.getLogger(__name__)

# Nominatim API endpoint (Free, 1 req/sec limit)
NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
HEADERS = {"User-Agent": "TSG-Platform-Geocoder/1.0 (internal-use)"}

def clean_address(address: str) -> str:
    if not address:
        return ""
    address = address.strip()
    # Remove repeated city names like / İZMİR at the end
    parts = address.split('/')
    if len(parts) > 1 and 'İZMİR' in parts[-1].upper():
        if parts[-1].strip().upper() == 'İZMİR':
            address = '/'.join(parts[:-1]).strip()
    return ' '.join(address.split())

def normalize_for_geocoding(address: str) -> str:
    s = address or ""
    s = unicodedata.normalize("NFC", s)
    s = re.sub(r"\s+", " ", s).strip()
    s = s.replace("ISTANBUL", "İstanbul").replace("İSTANBUL", "İstanbul").replace("istanbul", "İstanbul")
    s = s.replace("IZMIR", "İzmir").replace("İZMİR", "İzmir").replace("izmir", "İzmir")
    s = re.sub(r"\b(MH|MH\.|MAH|MAH\.)\b", "Mahallesi", s, flags=re.IGNORECASE)
    s = re.sub(r"\b(CD|CD\.|CAD|CAD\.|CADD?E?)\b", "Cadde", s, flags=re.IGNORECASE)
    s = re.sub(r"\b(SOK|SOK\.|SK|SK\.)\b", "Sokak", s, flags=re.IGNORECASE)
    s = re.sub(r"\b(BUL|BUL\.|BLV|BLV\.|BLVR?)\b", "Bulvarı", s, flags=re.IGNORECASE)
    s = re.sub(r"\bST\b\.?", "Sokak", s, flags=re.IGNORECASE)
    s = re.sub(r"\bBLK?\b\.?", "Blok", s, flags=re.IGNORECASE)
    s = re.sub(r"\bNO\s*[:\.]?\s*", "No ", s, flags=re.IGNORECASE)
    s = re.sub(r"\bİÇ\s*KAPI\s*NO\s*[:\.]?\s*", "İç Kapı No ", s, flags=re.IGNORECASE)
    s = re.sub(r"\bN[O\.]?\s*[:\.]?\s*(\d+)", r"No \1", s, flags=re.IGNORECASE)
    s = re.sub(r"\b(Mahallesi|Cadde|Sokak|Bulvarı)\.", r"\1", s, flags=re.IGNORECASE)
    s = re.sub(r"\s*\.\s*", " ", s)
    s = re.sub(r"\b(Mahallesi|Cadde|Sokak|Bulvarı|Blok)(?=[A-ZÇĞİÖŞÜ0-9])", r"\1 ", s)
    s = re.sub(r"\b(Blok|Sokak)No\b", r"\1 No", s, flags=re.IGNORECASE)
    s = re.sub(r"([a-zçğıöşü])([A-ZÇĞİÖŞÜ])", r"\1 \2", s)
    s = re.sub(r"([0-9])([A-Za-zÇĞİÖŞÜçğıöşü])", r"\1 \2", s)
    s = re.sub(r"([A-Za-zÇĞİÖŞÜçğıöşü])([0-9])", r"\1 \2", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s

def _get_hash(text: str) -> str:
    return hashlib.sha256(text.lower().encode('utf-8')).hexdigest()

async def _fetch_from_api(client: httpx.AsyncClient, address: str) -> Optional[Dict[str, float]]:
    """Fetches coordinates from Nominatim API with strict 1.1s rate limiting."""
    await asyncio.sleep(1.1)  # Strict Rate Limiting for Nominatim (1 req/sec)
    encoded = address.replace(" ", "+")
    url = f"{NOMINATIM_URL}?format=json&q={encoded}&countrycodes=tr&limit=1"
    
    try:
        resp = await client.get(url, headers=HEADERS, timeout=10.0)
        resp.raise_for_status()
        data = resp.json()
        if data and len(data) > 0:
            best = data[0]
            # Nominatim 'importance' can be low, but since we narrow down we accept it if it found something
            return {
                "lat": float(best["lat"]),
                "lon": float(best["lon"])
            }
    except Exception as e:
        logger.error(f"Geocoding API failed for '{address}': {e}")
    return None

async def geocode_address(db: Session, address: str) -> Optional[Dict[str, float]]:
    """
    Robust Geocoding Engine:
    1. Cleans and normalizes address.
    2. Checks Database Cache (GeocodingCache) - Returns instantly if found (even if previously failed).
    3. If missing, attempts API: Exact Match -> Street Match -> Neighbourhood Match.
    4. Saves the final result (success or failure) to the Cache.
    """
    if not address:
        return None

    cleaned = clean_address(address)
    normalized = normalize_for_geocoding(cleaned)
    if not normalized:
        return None

    address_hash = _get_hash(normalized)
    
    # --- 1. CHECK CACHE ---
    cached = db.query(GeocodingCache).filter(GeocodingCache.address_hash == address_hash).first()
    if cached:
        if cached.success:
            return {"lat": cached.lat, "lon": cached.lon}
        else:
            return None # We already tried this address and it failed before

    # --- 2. API LOOKUPS WITH FALLBACK ---
    async with httpx.AsyncClient() as client:
        result = None
        
        # Attempt 1: Exact Match
        logger.info(f"Geocoding Attempt 1 (Exact): '{normalized}'")
        result = await _fetch_from_api(client, normalized)

        # Attempt 2: Street Level
        if not result:
            street = re.sub(r'(\s(\d+\s)?No\s\d+.*)', '', normalized, flags=re.IGNORECASE).strip()
            street = re.sub(r'\s+[A-Za-z0-9]+\s+(APT|APARTMANI|SİTESİ|İŞ MERKEZİ|PLAZA)\b.*', '', street, flags=re.IGNORECASE).strip()
            if street and street != normalized and len(street) > 10:
                logger.info(f"Geocoding Attempt 2 (Street): '{street}'")
                result = await _fetch_from_api(client, street)

        # Attempt 3: Neighbourhood Level
        if not result:
            mahalle_match = re.search(r'([A-Za-zÇĞİÖŞÜçğıöşü\s]+Mahallesi)', normalized, re.IGNORECASE)
            if mahalle_match:
                mahalle = mahalle_match.group(1).strip()
                suffix = ""
                if "/" in normalized:
                    parts = normalized.split("/")
                    if len(parts) >= 2:
                        city = parts[-1].strip()
                        pre_slash = parts[-2].strip()
                        district = pre_slash.split()[-1] if pre_slash else ""
                        if district and not any(c.isdigit() for c in district) and district.lower() not in mahalle.lower():
                            suffix = f" {district} {city}"
                        else:
                            suffix = f" {city}"
                if not suffix:
                    lower_addr = normalized.lower()
                    if "istanbul" in lower_addr: suffix = " İstanbul"
                    elif "ankara" in lower_addr: suffix = " Ankara"
                    elif "izmir" in lower_addr: suffix = " İzmir"
                
                neigh = f"{mahalle}{suffix}".strip()
                if neigh and neigh != address:
                    logger.info(f"Geocoding Attempt 3 (Neighbourhood): '{neigh}'")
                    result = await _fetch_from_api(client, neigh)

    # --- 3. SAVE TO CACHE ---
    try:
        new_cache = GeocodingCache(
            address_hash=address_hash,
            address_text=normalized,
            success=bool(result),
            lat=result["lat"] if result else None,
            lon=result["lon"] if result else None,
            provider="nominatim"
        )
        db.add(new_cache)
        db.commit()
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to save geocoding cache for '{normalized}': {e}")

    return result
