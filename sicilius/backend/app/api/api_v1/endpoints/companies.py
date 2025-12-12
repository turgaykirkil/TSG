"""
Company API endpoints
"""
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.core.config import settings
from app.api.api_v1.endpoints.processing import geocode_company_by_id

router = APIRouter()

@router.get("/", response_model=List[schemas.Company])
def read_companies(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve companies with pagination.
    """
    companies = crud.company.get_multi(db, skip=skip, limit=limit)
    return companies


@router.get("/uncoordinated/", response_model=List[schemas.Company])
def read_uncoordinated_companies(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve companies without coordinates.
    """
    companies = crud.company.get_multi_uncoordinated(db, skip=skip, limit=limit)
    return companies

@router.post("/", response_model=schemas.Company)
def create_company(
    *,
    db: Session = Depends(deps.get_db),
    company_in: schemas.CompanyCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new company.
    """
    try:
        company = crud.company.create(db, obj_in=company_in)
        return company
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.get("/{company_id}/nearby", response_model=List[schemas.NearbyCompany])
def read_nearby_companies(
    *,
    db: Session = Depends(deps.get_db),
    company_id: str,
    max_km: float = Query(5.0, ge=0.1, le=200.0),
    limit: int = Query(10, ge=1, le=100),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Verilen şirketin koordinatına göre yakın şirketleri getirir.
    Koordinatı olmayan referans şirketlerde 400 döner.
    """
    ref = crud.company.get(db, id=company_id)
    if not ref:
        raise HTTPException(status_code=404, detail="Şirket bulunamadı")
    if getattr(ref, 'koordinat', None) is None:
        raise HTTPException(status_code=400, detail="Referans şirketin koordinatı yok")

    items = crud.company.get_nearby_by_id(db, company_id=company_id, max_km=max_km, limit=limit)
    # Pydantic NearbyCompany ile uyumlu alanları döner
    return [
        {
            "id": it["id"],
            "unvan": it.get("unvan"),
            "title": it.get("unvan"),
            "trade_name": None,
            "address": it.get("address"),
            "city": it.get("city"),
            "distance_km": it.get("distance_km", 0.0),
            "koordinat": it.get("koordinat"),
        }
        for it in items
    ]

@router.get("/search/", response_model=List[schemas.Company])
def search_companies(
    *,
    db: Session = Depends(deps.get_db),
    query: str = Query(..., min_length=3, max_length=100),
    skip: int = 0,
    limit: int = 10,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Search companies by title or trade name.
    """
    companies = crud.company.search(db, query=query, skip=skip, limit=limit)
    return companies

@router.get("/{company_id}", response_model=schemas.Company)
async def read_company(
    *,
    db: Session = Depends(deps.get_db),
    company_id: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get company by ID.
    If coordinates are missing, it attempts to fetch them on-the-fly.
    """
    company = crud.company.get(db, id=company_id)
    if not company:
        raise HTTPException(
            status_code=404,
            detail="The company with this ID does not exist in the system",
        )
    
    # On-the-fly geocoding request
    if company.address and not company.koordinat:
        try:
             success = await geocode_company_by_id(db, company.id, company.address)
             if success:
                 # Force explicit refresh by expiring session cache and re-querying
                 # This ensures we get the COMMITTED data from geocode_company_by_id
                 db.expire_all() 
                 company = crud.company.get(db, id=company_id)
        except Exception as e:
            # Log but don't fail the request just because geocoding failed
             import logging
             logging.getLogger(__name__).error(f"On-demand geocoding failed for {company_id}: {e}")

    return company

@router.put("/{company_id}", response_model=schemas.Company)
def update_company(
    *,
    db: Session = Depends(deps.get_db),
    company_id: int,
    company_in: schemas.CompanyUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a company.
    """
    company = crud.company.get(db, id=company_id)
    if not company:
        raise HTTPException(
            status_code=404,
            detail="The company with this ID does not exist in the system",
        )
    
    try:
        company = crud.company.update(db, db_obj=company, obj_in=company_in)
        return company
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )

@router.delete("/{company_id}", response_model=schemas.Company)
def delete_company(
    *,
    db: Session = Depends(deps.get_db),
    company_id: int,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Delete a company.
    """
    company = crud.company.get(db, id=company_id)
    if not company:
        raise HTTPException(
            status_code=404,
            detail="The company with this ID does not exist in the system",
        )
    
    company = crud.company.remove(db, id=company_id)
    return company

@router.get("/tax-number/{tax_number}", response_model=schemas.Company)
def read_company_by_tax_number(
    *,
    db: Session = Depends(deps.get_db),
    tax_number: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get company by tax number.
    """
    company = crud.company.get_by_tax_number(db, tax_number=tax_number)
    if not company:
        raise HTTPException(
            status_code=404,
            detail="The company with this tax number does not exist in the system",
        )
    return company

@router.get("/trade-registry/{registry_number}", response_model=schemas.Company)
def read_company_by_trade_registry(
    *,
    db: Session = Depends(deps.get_db),
    registry_number: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get company by trade registry number.
    """
    company = crud.company.get_by_trade_registry_number(db, registry_number=registry_number)
    if not company:
        raise HTTPException(
            status_code=404,
            detail="The company with this trade registry number does not exist in the system",
        )
    return company
