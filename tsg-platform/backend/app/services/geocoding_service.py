import httpx
import os
from typing import Optional, Dict, Any

async def geocode_address(address: str) -> Optional[Dict[str, float]]:
    """
    Bir adresi, yedekli bir strateji kullanarak coğrafi koordinatlara dönüştürür:
    Önce Nominatim, başarısız olursa veya güven düşükse LocationIQ kullanılır.
    
    Args:
        address: Koordinatları bulunacak adres.

    Returns:
        Enlem ve boylam içeren bir sözlük veya None.
    """
    if not address:
        return None

    encoded_address = address.replace(" ", "+")

    # 1. Nominatim'i dene
    nominatim_url = f"https://nominatim.openstreetmap.org/search?format=json&q={encoded_address}&countrycodes=tr&limit=1"
    headers = {"User-Agent": "TSG-Platform-Scraper/1.0 (https://github.com/your-repo)"}
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(nominatim_url, headers=headers)
            response.raise_for_status()
            nominatim_result = response.json()

            if nominatim_result:
                best_result = nominatim_result[0]
                if float(best_result.get("importance", 0)) > 0.4:
                    return {
                        "lat": float(best_result["lat"]),
                        "lon": float(best_result["lon"]),
                    }
    except Exception as e:
        print(f"[BİLGİ] Nominatim ile ilgili bir hata oluştu: {e}")

    # 2. LocationIQ'ya geç
    print(f'[BİLGİ] Nominatim başarısız oldu veya güven düşüktü: "{address}". LocationIQ deneniyor.')
    api_key = os.getenv("LOCATIONIQ_API_KEY")
    if not api_key:
        print("[HATA] LOCATIONIQ_API_KEY ortam değişkeni ayarlanmamış. Geocoding atlanıyor.")
        return None

    locationiq_url = f"https://us1.locationiq.com/v1/search?key={api_key}&q={encoded_address}&countrycodes=tr&limit=1&format=json"
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(locationiq_url)
            response.raise_for_status()
            locationiq_result = response.json()

            if locationiq_result:
                best_result = locationiq_result[0]
                return {
                    "lat": float(best_result["lat"]),
                    "lon": float(best_result["lon"]),
                }
    except Exception as e:
        print(f"[HATA] LocationIQ ile ilgili bir hata oluştu: {e}")

    print(f'[UYARI] Adres iki serviste de bulunamadı: "{address}"')
    return None
