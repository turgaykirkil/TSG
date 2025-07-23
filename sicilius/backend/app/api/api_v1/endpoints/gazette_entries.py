"""
Gazette Entry API endpoints
"""
from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.core.config import settings

router = APIRouter()

@router.get("/", response_model=List[schemas.GazetteEntry])
def read_gazette_entries(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve gazette entries with pagination.
    """
    entries = crud.gazette_entry.get_multi(db, skip=skip, limit=limit)
    return entries

@router.get("/gazette/{gazette_id}", response_model=List[schemas.GazetteEntry])
def read_entries_by_gazette(
    *,
    db: Session = Depends(deps.get_db),
    gazette_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get all entries for a specific gazette.
    """
    # Check if gazette exists
    gazette = crud.gazette.get(db, id=gazette_id)
    if not gazette:
        raise HTTPException(
            status_code=404,
            detail="The gazette with this ID does not exist in the system",
        )
    
    return crud.gazette_entry.get_multi_by_gazette(
        db, gazette_id=gazette_id, skip=skip, limit=limit
    )

@router.get("/company/{company_id}", response_model=List[schemas.GazetteEntry])
def read_entries_by_company(
    *,
    db: Session = Depends(deps.get_db),
    company_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get all entries for a specific company.
    """
    # Check if company exists
    company = crud.company.get(db, id=company_id)
    if not company:
        raise HTTPException(
            status_code=404,
            detail="The company with this ID does not exist in the system",
        )
    
    return crud.gazette_entry.get_multi_by_company(
        db, company_id=company_id, skip=skip, limit=limit
    )

@router.get("/type/{entry_type}", response_model=List[schemas.GazetteEntry])
def read_entries_by_type(
    *,
    db: Session = Depends(deps.get_db),
    entry_type: str,
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get all entries of a specific type.
    """
    return crud.gazette_entry.get_by_type(
        db, entry_type=entry_type, skip=skip, limit=limit
    )

@router.get("/unprocessed/", response_model=List[schemas.GazetteEntry])
def read_unprocessed_entries(
    *,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get all unprocessed entries.
    """
    return crud.gazette_entry.get_unprocessed(db, skip=skip, limit=limit)

@router.get("/search/", response_model=List[schemas.GazetteEntry])
def search_entries(
    *,
    db: Session = Depends(deps.get_db),
    query: str = Query(..., min_length=3, max_length=100),
    entry_type: Optional[str] = None,
    skip: int = 0,
    limit: int = 50,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Search entries by text in raw or processed text.
    """
    return crud.gazette_entry.search(
        db, query=query, entry_type=entry_type, skip=skip, limit=limit
    )

@router.post("/", response_model=schemas.GazetteEntry)
def create_gazette_entry(
    *,
    db: Session = Depends(deps.get_db),
    entry_in: schemas.GazetteEntryCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new gazette entry.
    """
    # Check if gazette exists
    if entry_in.gazette_id:
        gazette = crud.gazette.get(db, id=entry_in.gazette_id)
        if not gazette:
            raise HTTPException(
                status_code=404,
                detail="The gazette with this ID does not exist in the system",
            )
    
    # Check if company exists if company_id is provided
    if entry_in.company_id:
        company = crud.company.get(db, id=entry_in.company_id)
        if not company:
            raise HTTPException(
                status_code=404,
                detail="The company with this ID does not exist in the system",
            )
    
    return crud.gazette_entry.create(db, obj_in=entry_in)

@router.post("/bulk/", response_model=List[schemas.GazetteEntry])
def bulk_create_gazette_entries(
    *,
    db: Session = Depends(deps.get_db),
    entries_in: List[schemas.GazetteEntryCreate],
    gazette_id: int = None,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create multiple gazette entries at once.
    """
    if gazette_id is None and not all(e.gazette_id for e in entries_in):
        raise HTTPException(
            status_code=400,
            detail="gazette_id must be provided either in the URL or in each entry",
        )
    
    # If gazette_id is provided in URL, use it for all entries
    if gazette_id is not None:
        # Check if gazette exists
        gazette = crud.gazette.get(db, id=gazette_id)
        if not gazette:
            raise HTTPException(
                status_code=404,
                detail="The gazette with this ID does not exist in the system",
            )
        
        # Update all entries with the gazette_id
        for entry in entries_in:
            entry.gazette_id = gazette_id
    
    # Check if all companies exist
    company_ids = {e.company_id for e in entries_in if e.company_id is not None}
    if company_ids:
        existing_companies = {c.id for c in crud.company.get_multi_by_ids(db, ids=list(company_ids))}
        non_existing = company_ids - existing_companies
        if non_existing:
            raise HTTPException(
                status_code=404,
                detail=f"The following company IDs do not exist: {', '.join(map(str, non_existing))}",
            )
    
    return crud.gazette_entry.create_multi(db, objs_in=entries_in, gazette_id=gazette_id)

@router.get("/{entry_id}", response_model=schemas.GazetteEntry)
def read_gazette_entry(
    *,
    db: Session = Depends(deps.get_db),
    entry_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get gazette entry by ID.
    """
    entry = crud.gazette_entry.get(db, id=entry_id)
    if not entry:
        raise HTTPException(
            status_code=404,
            detail="The gazette entry with this ID does not exist in the system",
        )
    return entry

@router.put("/{entry_id}", response_model=schemas.GazetteEntry)
def update_gazette_entry(
    *,
    db: Session = Depends(deps.get_db),
    entry_id: int,
    entry_in: schemas.GazetteEntryUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a gazette entry.
    """
    entry = crud.gazette_entry.get(db, id=entry_id)
    if not entry:
        raise HTTPException(
            status_code=404,
            detail="The gazette entry with this ID does not exist in the system",
        )
    
    # Check if gazette exists if being updated
    if entry_in.gazette_id is not None:
        gazette = crud.gazette.get(db, id=entry_in.gazette_id)
        if not gazette:
            raise HTTPException(
                status_code=404,
                detail="The gazette with this ID does not exist in the system",
            )
    
    # Check if company exists if being updated
    if entry_in.company_id is not None:
        company = crud.company.get(db, id=entry_in.company_id)
        if not company:
            raise HTTPException(
                status_code=404,
                detail="The company with this ID does not exist in the system",
            )
    
    return crud.gazette_entry.update(db, db_obj=entry, obj_in=entry_in)

@router.delete("/{entry_id}", response_model=schemas.GazetteEntry)
def delete_gazette_entry(
    *,
    db: Session = Depends(deps.get_db),
    entry_id: int,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Delete a gazette entry.
    """
    entry = crud.gazette_entry.get(db, id=entry_id)
    if not entry:
        raise HTTPException(
            status_code=404,
            detail="The gazette entry with this ID does not exist in the system",
        )
    
    return crud.gazette_entry.remove(db, id=entry_id)

@router.post("/{entry_id}/process/", response_model=schemas.GazetteEntry)
def process_gazette_entry(
    *,
    db: Session = Depends(deps.get_db),
    entry_id: int,
    processed_data: schemas.GazetteEntryProcess,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Mark a gazette entry as processed and update with processed data.
    """
    entry = crud.gazette_entry.get(db, id=entry_id)
    if not entry:
        raise HTTPException(
            status_code=404,
            detail="The gazette entry with this ID does not exist in the system",
        )
    
    # If this entry is associated with a company, update the company status
    if entry.company_id:
        # Here you would typically update the company with the extracted data
        # For example, update company details, create relations, etc.
        pass
    
    # Update the entry with the processed data
    update_data = processed_data.dict(exclude_unset=True)
    update_data["is_processed"] = True
    
    return crud.gazette_entry.update(db, db_obj=entry, obj_in=update_data)
