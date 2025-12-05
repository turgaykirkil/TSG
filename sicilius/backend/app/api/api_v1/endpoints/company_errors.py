from typing import Any, List
from uuid import UUID
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.models.company_error import ErrorStatus

router = APIRouter()

@router.post("/report", response_model=schemas.CompanyError)
def report_error(
    *,
    db: Session = Depends(deps.get_db),
    error_in: schemas.CompanyErrorCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Report an error for a company.
    """
    error = crud.company_error.create_with_user(
        db=db, obj_in=error_in, user_id=current_user.id
    )
    return error

@router.get("/", response_model=List[schemas.CompanyError])
def read_errors(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    status: ErrorStatus = None,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Retrieve company errors (Admin only).
    """
    errors = crud.company_error.get_all_errors(
        db=db, skip=skip, limit=limit, status=status
    )
    
    # Fetch company names for all errors
    result = []
    for error in errors:
        error_dict = schemas.CompanyError.model_validate(error).model_dump()
        # Get company name
        company = db.query(models.Company).filter(models.Company.id == error.company_id).first()
        error_dict['company_name'] = company.unvan if company else None
        result.append(error_dict)
    
    return result

@router.patch("/{id}/resolve", response_model=schemas.CompanyError)
def resolve_error(
    *,
    db: Session = Depends(deps.get_db),
    id: UUID,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Mark an error as resolved (Admin only).
    """
    error = crud.company_error.get(db=db, id=id)
    if not error:
        raise HTTPException(status_code=404, detail="Error report not found")
    
    update_data = schemas.CompanyErrorUpdate(
        status=ErrorStatus.RESOLVED,
        resolved_at=datetime.utcnow()
    )
    error = crud.company_error.update(db=db, db_obj=error, obj_in=update_data)
    return error
