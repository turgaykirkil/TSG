from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Any

from app.services.geocoding_service import geocode_address
from app import models, schemas
from app.api import deps

router = APIRouter()

@router.get("/geocode", response_model=schemas.Coordinates)
async def get_coordinates_from_address(
    address: str = Query(..., description="Koordinatları alınacak adres."),
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Verilen bir adres için coğrafi koordinatları (enlem ve boylam) alır.
    """
    if not address:
        raise HTTPException(status_code=400, detail="Adres parametresi boş olamaz.")

    coordinates = await geocode_address(db, address)

    if not coordinates:
        raise HTTPException(status_code=404, detail="Bu adres için koordinat bulunamadı.")

    return coordinates
