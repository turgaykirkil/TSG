import os
import httpx
import asyncio
import hashlib
import logging
import re
import unicodedata
from typing import Optional, Dict, Any, Tuple
from sqlalchemy.orm import Session
from app.models.geocoding_cache import GeocodingCache

logger = logging.getLogger(__name__)

# OpenStreetMap Nominatim API endpoint (Free & Open Source)
NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
HEADERS = {"User-Agent": "Sicilius-B2B-Platform-Geocoder/3.0 (contact@sicilius.com.tr)"}

# Bounding box for Turkey geographic coordinates
MIN_LAT, MAX_LAT = 35.80, 42.20
MIN_LON, MAX_LON = 25.50, 44.80

# Known Major District Bounding Boxes (minLon, maxLat, maxLon, minLat)
DISTRICT_BOUNDING_BOXES: Dict[str, Tuple[float, float, float, float]] = {
    "esenyurt": (28.60, 41.10, 28.75, 40.98),
    "sultanbeyli": (29.20, 41.01, 29.33, 40.92),
    "pendik": (29.18, 41.05, 29.45, 40.85),
    "tuzla": (29.30, 41.00, 29.50, 40.80),
    "kartal": (29.15, 40.96, 29.25, 40.88),
    "maltepe": (29.08, 40.98, 29.20, 40.90),
    "kadıköy": (29.00, 40.99, 29.10, 40.95),
    "üsküdar": (29.00, 41.06, 29.10, 41.00),
    "ümraniye": (29.08, 41.06, 29.20, 41.00),
    "bağcılar": (28.80, 41.06, 28.88, 41.02),
    "küçükçekmece": (28.72, 41.03, 28.82, 40.97),
    "beylikdüzü": (28.60, 41.02, 28.70, 40.95),
    "avcılar": (28.68, 41.05, 28.75, 40.96),
    "başakşehir": (28.72, 41.15, 28.88, 41.05),
    "bayrampaşa": (28.88, 41.06, 28.92, 41.03),
    "beşiktaş": (29.00, 41.08, 29.05, 41.04),
    "şişli": (28.97, 41.07, 29.00, 41.04),
    "sarıyer": (28.98, 41.22, 29.12, 41.10),
    "arnavutköy": (28.60, 41.35, 28.90, 41.15),
    "antalya": (30.40, 37.10, 30.90, 36.70),
    "konyaaltı": (30.50, 36.95, 30.68, 36.82),
    "muratpaşa": (30.68, 36.92, 30.82, 36.84),
}

# Major Istanbul Districts List
ISTANBUL_DISTRICTS = {
    'adalar', 'arnavutköy', 'ataşehir', 'avcılar', 'bağcılar', 'bahçelievler', 'bakırköy',
    'başakşehir', 'bayrampaşa', 'beşiktaş', 'beykoz', 'beylikdüzü', 'beyoğlu', 'büyükçekmece',
    'çatalca', 'çekmeköy', 'esenler', 'esenyurt', 'eyüpsultan', 'fatih', 'gaziosmanpaşa',
    'güngören', 'kadıköy', 'kağıthane', 'kartal', 'küçükçekmece', 'maltepe', 'pendik',
    'sancaktepe', 'sarıyer', 'silivri', 'sultanbeyli', 'sultangazi', 'şile', 'şişli',
    'tuzla', 'ümraniye', 'üsküdar', 'zeytinburnu'
}

def is_valid_turkey_coordinate(lat: float, lon: float) -> bool:
    """Validates if coordinates fall strictly within Turkey boundaries."""
    return MIN_LAT <= lat <= MAX_LAT and MIN_LON <= lon <= MAX_LON

def clean_address(address: str) -> str:
    """Legacy alias export for clean_address_noise."""
    return clean_address_noise(address)

def clean_address_noise(address: str) -> str:
    """Removes legal notices, journal boilerplate text, and interior door numbers."""
    if not address:
        return ""
    
    s = address.strip()

    # 1. Remove legal / gazette notice boilerplate text
    s = re.sub(r'Tasfiyeden\s+Dolayı.*', '', s, flags=re.IGNORECASE)
    s = re.sub(r'Alacaklılara\s+Çağrı.*', '', s, flags=re.IGNORECASE)
    s = re.sub(r'\(?İFLAS\s+NEDENİYLE\)?.*', '', s, flags=re.IGNORECASE)
    s = re.sub(r'\d+\.\s*İLAN.*', '', s, flags=re.IGNORECASE)
    s = re.sub(r'Ticaret\s+Sicil\s+Müdürlüğü.*', '', s, flags=re.IGNORECASE)
    
    # 2. Remove interior door, apartment, floor, block noise
    s = re.sub(r'İç\s*Kapı\s*No[:\.\s]*\d+[a-zA-Z]?', '', s, flags=re.IGNORECASE)
    s = re.sub(r'Daire[:\.\s]*\d+', '', s, flags=re.IGNORECASE)
    s = re.sub(r'Kat[:\.\s]*\d+', '', s, flags=re.IGNORECASE)
    s = re.sub(r'Blok[:\.\s]*[a-zA-Z0-9]+', '', s, flags=re.IGNORECASE)

    # 3. Standardize Turkish OCR typos (e.g. ș -> ş, ț -> ç)
    s = s.replace('ș', 'ş').replace('Ș', 'Ş').replace('ț', 'ç').replace('Ț', 'Ç')
    
    # 4. Standardize abbreviations
    s = re.sub(r'\b(MH|MH\.|MAH|MAH\.)\b', 'Mahallesi', s, flags=re.IGNORECASE)
    s = re.sub(r'\b(CD|CD\.|CAD|CAD\.|CADDESİ)\b', 'Caddesi', s, flags=re.IGNORECASE)
    s = re.sub(r'\b(SOK|SOK\.|SK|SK\.|SOKAĞI)\b', 'Sokak', s, flags=re.IGNORECASE)
    s = re.sub(r'\b(BUL|BUL\.|BLV|BLV\.|BULVARI)\b', 'Bulvarı', s, flags=re.IGNORECASE)
    
    # Fix dot separation issues (e.g., Mah.Burcu -> Mahallesi Burcu)
    s = re.sub(r'\b(Mahallesi|Caddesi|Sokak|Bulvarı|Mah|Cad|Sk)\.?([A-ZÇĞİÖŞÜa-zçğıöşü])', r'\1 \2', s)
    s = re.sub(r'\b(Mahallesi|Caddesi|Sokak|Bulvarı)\.?\s*', r'\1 ', s, flags=re.IGNORECASE)
    
    # Clean whitespace
    s = re.sub(r'\s+', ' ', s).strip()
    return s

def extract_address_components(address: str) -> Tuple[str, str, str, str]:
    """
    Right-to-Left Structured Address Parser.
    Extracts: (street_and_door, mahalle, district, city)
    """
    cleaned = clean_address_noise(address)
    addr_lower = cleaned.lower()
    
    city = ""
    district = ""
    mahalle = ""
    street_and_door = ""

    # 1. Rightmost City Extraction
    if 'istanbul' in addr_lower or 'i̇stanbul' in addr_lower:
        city = 'İstanbul'
    elif 'antalya' in addr_lower:
        city = 'Antalya'
    elif 'ankara' in addr_lower:
        city = 'Ankara'
    elif 'izmir' in addr_lower or 'i̇zmir' in addr_lower:
        city = 'İzmir'
    elif 'bursa' in addr_lower:
        city = 'Bursa'
    elif 'kocaeli' in addr_lower or 'izmit' in addr_lower:
        city = 'Kocaeli'

    # 2. District Extraction from Taxonomy
    for d in ISTANBUL_DISTRICTS:
        if re.search(r'\b' + d + r'\b', addr_lower):
            district = d.capitalize()
            if not city:
                city = 'İstanbul'
            break

    # 3. Slash Fallback for District / City
    parts = [p.strip() for p in cleaned.split('/') if p.strip()]
    if len(parts) >= 2:
        if not city:
            city = parts[-1].strip()
        if not district:
            d_tokens = parts[-2].split()
            if d_tokens:
                district = d_tokens[-1].strip()

    # 4. Mahalle Extraction
    mahalle_match = re.search(r'([A-Za-zÇĞİÖŞÜçğıöşü0-9\s]+Mahallesi)', cleaned, re.IGNORECASE)
    if mahalle_match:
        mahalle = mahalle_match.group(1).strip()

    # 5. Street & Door Number Extraction
    street_match = re.search(r'([A-Za-zÇĞİÖŞÜçğıöşü0-9\s]+(?:Sokak|Caddesi|Bulvarı)[^/,]*)', cleaned, re.IGNORECASE)
    if street_match:
        street_and_door = street_match.group(1).strip()

    return street_and_door, mahalle, district, city

def _get_hash(text: str) -> str:
    return hashlib.sha256(text.lower().encode('utf-8')).hexdigest()

async def _query_nominatim(
    client: httpx.AsyncClient,
    query_text: str,
    viewbox: Optional[Tuple[float, float, float, float]] = None,
    bounded: bool = False
) -> Optional[Dict[str, Any]]:
    """
    Performs HTTP request to OpenStreetMap Nominatim with optional Bounding Box Constraining (Baskılama).
    """
    await asyncio.sleep(1.1) # Respect Nominatim 1 req/sec policy
    
    params: Dict[str, Any] = {
        "q": query_text,
        "format": "json",
        "countrycodes": "tr",
        "limit": 1
    }
    
    if viewbox:
        left, top, right, bottom = viewbox
        params["viewbox"] = f"{left},{top},{right},{bottom}"
        if bounded:
            params["bounded"] = "1"

    try:
        resp = await client.get(NOMINATIM_URL, params=params, headers=HEADERS, timeout=10.0)
        resp.raise_for_status()
        data = resp.json()
        
        if data and len(data) > 0:
            best = data[0]
            lat = float(best["lat"])
            lon = float(best["lon"])
            
            if is_valid_turkey_coordinate(lat, lon):
                return {
                    "lat": lat,
                    "lon": lon,
                    "display_name": best.get("display_name", ""),
                    "place_type": best.get("type", "unknown")
                }
    except Exception as e:
        logger.error(f"Nominatim API query failed for '{query_text}': {e}")
    
    return None

async def geocode_address(db: Session, address: str) -> Optional[Dict[str, Any]]:
    """
    Right-to-Left Progressive Geocoding Engine with Bounding Box Constraining:
    1. Parse Right-to-Left: (Street & Door, Mahalle, District, City)
    2. Lookup District Bounding Box (Baskılama)
    3. Step-by-Step Precision Ladder:
       - Step 1: Door & Street Pinpoint Strike (Sokak + No + Mahalle + İlçe + İl)
       - Step 2: Street Level Strike (Sokak + Mahalle + İlçe + İl)
       - Step 3: Mahalle Level Strike (Mahalle + İlçe + İl)
       - Step 4: District Center Fallback (İlçe + İl)
    """
    if not address or len(address.strip()) < 5:
        return None

    street_door, mahalle, district, city = extract_address_components(address)
    
    # Retrieve Bounding Box for District Constraining (Baskılama)
    viewbox = DISTRICT_BOUNDING_BOXES.get((district or "").lower())

    normalized_full = ", ".join([p for p in [street_door or mahalle, district, city, "Türkiye"] if p])
    if not normalized_full:
        return None

    address_hash = _get_hash(normalized_full)

    # --- 1. CHECK DATABASE CACHE ---
    cached = db.query(GeocodingCache).filter(GeocodingCache.address_hash == address_hash).first()
    if cached:
        if cached.success and cached.lat and cached.lon:
            return {"lat": cached.lat, "lon": cached.lon, "cached": True}
        else:
            return None

    # --- 2. RIGHT-TO-LEFT PROGRESSIVE GEOCODING LADDER ---
    async with httpx.AsyncClient() as client:
        result = None
        precision = "FAILED"

        # STEP 1: Door & Street Pinpoint Strike with Bounding Box Constraining
        if street_door and district and city:
            q1 = f"{street_door}, {mahalle or ''}, {district}, {city}, Türkiye".replace("  ", " ").strip(", ")
            logger.info(f"Geocoding Step 1 (Pinpoint): '{q1}'")
            result = await _query_nominatim(client, q1, viewbox=viewbox, bounded=True)
            if not result:
                # Try without strict bounding box constraint
                result = await _query_nominatim(client, q1, viewbox=viewbox, bounded=False)
            if result:
                precision = "EXACT_BUILDING"

        # STEP 2: Street Level Strike (without door number)
        if not result and street_door:
            street_only = re.sub(r'No[:\.\s]*\d+.*', '', street_door, flags=re.IGNORECASE).strip()
            if street_only:
                q2 = f"{street_only}, {mahalle or ''}, {district or ''}, {city or ''}, Türkiye".replace("  ", " ").strip(", ")
                logger.info(f"Geocoding Step 2 (Street): '{q2}'")
                result = await _query_nominatim(client, q2, viewbox=viewbox, bounded=False)
                if result:
                    precision = "STREET_LEVEL"

        # STEP 3: Mahalle Level Strike
        if not result and mahalle and district:
            q3 = f"{mahalle}, {district}, {city or ''}, Türkiye".strip(", ")
            logger.info(f"Geocoding Step 3 (Mahalle): '{q3}'")
            result = await _query_nominatim(client, q3, viewbox=viewbox, bounded=False)
            if result:
                precision = "NEIGHBOURHOOD_LEVEL"

        # STEP 4: District Center Fallback
        if not result and district and city:
            q4 = f"{district}, {city}, Türkiye"
            logger.info(f"Geocoding Step 4 (District Center): '{q4}'")
            result = await _query_nominatim(client, q4, viewbox=viewbox, bounded=False)
            if result:
                precision = "DISTRICT_LEVEL"

    # --- 3. SAVE TO DATABASE CACHE ---
    try:
        new_cache = GeocodingCache(
            address_hash=address_hash,
            address_text=normalized_full,
            success=bool(result),
            lat=result["lat"] if result else None,
            lon=result["lon"] if result else None,
            provider=f"nominatim_{precision.lower()}" if result else "nominatim_failed"
        )
        db.add(new_cache)
        db.commit()
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to save geocoding cache for '{normalized_full}': {e}")

    if result:
        result["precision"] = precision
    return result
