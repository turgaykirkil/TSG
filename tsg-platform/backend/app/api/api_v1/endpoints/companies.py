"""
Company API endpoints
"""
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.core.config import settings

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
def read_company(
    *,
    db: Session = Depends(deps.get_db),
    company_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get company by ID.
    """
    company = crud.company.get(db, id=company_id)
    if not company:
        raise HTTPException(
            status_code=404,
            detail="The company with this ID does not exist in the system",
        )
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
