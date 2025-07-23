"""
Gazette API endpoints
"""
from datetime import date, datetime, timedelta
from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File, Form
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.core.config import settings
from app.utils.file_utils import save_upload_file, validate_file_type

router = APIRouter()

@router.get("/", response_model=List[schemas.Gazette])
def read_gazettes(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve gazettes with pagination.
    """
    gazettes = crud.gazette.get_multi(db, skip=skip, limit=limit)
    return gazettes

@router.post("/", response_model=schemas.Gazette)
def create_gazette(
    *,
    db: Session = Depends(deps.get_db),
    gazette_in: schemas.GazetteCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new gazette.
    """
    try:
        gazette = crud.gazette.create(db, obj_in=gazette_in)
        return gazette
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )

@router.get("/date-range/", response_model=List[schemas.Gazette])
def get_gazettes_by_date_range(
    *,
    db: Session = Depends(deps.get_db),
    start_date: date = Query(..., description="Start date (YYYY-MM-DD)"),
    end_date: date = Query(..., description="End date (YYYY-MM-DD)"),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get gazettes by date range.
    """
    if start_date > end_date:
        raise HTTPException(
            status_code=400,
            detail="Start date cannot be after end date",
        )
    
    # Limit date range to 1 year for performance
    max_date_range = timedelta(days=365)
    if (end_date - start_date) > max_date_range:
        raise HTTPException(
            status_code=400,
            detail=f"Date range cannot exceed {max_date_range.days} days",
        )
    
    gazettes = crud.gazette.get_multi_by_date_range(
        db, start_date=start_date, end_date=end_date, skip=skip, limit=limit
    )
    return gazettes

@router.get("/recent/", response_model=List[schemas.Gazette])
def get_recent_gazettes(
    *,
    db: Session = Depends(deps.get_db),
    days: int = Query(7, ge=1, le=365, description="Number of days to look back"),
    skip: int = 0,
    limit: int = 50,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get recent gazettes from the last N days.
    """
    end_date = datetime.utcnow().date()
    start_date = end_date - timedelta(days=days)
    
    return crud.gazette.get_multi_by_date_range(
        db, start_date=start_date, end_date=end_date, skip=skip, limit=limit
    )

@router.get("/processed/", response_model=List[schemas.Gazette])
def get_processed_gazettes(
    *,
    db: Session = Depends(deps.get_db),
    processed: bool = True,
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get processed or unprocessed gazettes.
    """
    return crud.gazette.get_processed(
        db, processed=processed, skip=skip, limit=limit
    )

@router.get("/search/", response_model=List[schemas.Gazette])
def search_gazettes(
    *,
    db: Session = Depends(deps.get_db),
    query: str = Query(..., min_length=3, max_length=100),
    skip: int = 0,
    limit: int = 50,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Search gazettes by number or filename.
    """
    return crud.gazette.search(
        db, query=query, skip=skip, limit=limit
    )

@router.get("/{gazette_id}", response_model=schemas.Gazette)
def read_gazette(
    *,
    db: Session = Depends(deps.get_db),
    gazette_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get gazette by ID.
    """
    gazette = crud.gazette.get(db, id=gazette_id)
    if not gazette:
        raise HTTPException(
            status_code=404,
            detail="The gazette with this ID does not exist in the system",
        )
    return gazette

@router.put("/{gazette_id}", response_model=schemas.Gazette)
def update_gazette(
    *,
    db: Session = Depends(deps.get_db),
    gazette_id: int,
    gazette_in: schemas.GazetteUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a gazette.
    """
    gazette = crud.gazette.get(db, id=gazette_id)
    if not gazette:
        raise HTTPException(
            status_code=404,
            detail="The gazette with this ID does not exist in the system",
        )
    
    try:
        gazette = crud.gazette.update(db, db_obj=gazette, obj_in=gazette_in)
        return gazette
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )

@router.delete("/{gazette_id}", response_model=schemas.Gazette)
def delete_gazette(
    *,
    db: Session = Depends(deps.get_db),
    gazette_id: int,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Delete a gazette.
    """
    gazette = crud.gazette.get(db, id=gazette_id)
    if not gazette:
        raise HTTPException(
            status_code=404,
            detail="The gazette with this ID does not exist in the system",
        )
    
    # TODO: Also delete associated files and entries
    gazette = crud.gazette.remove(db, id=gazette_id)
    return gazette

@router.post("/upload/", response_model=schemas.Gazette)
async def upload_gazette(
    *,
    db: Session = Depends(deps.get_db),
    file: UploadFile = File(..., description="PDF file to upload"),
    gazette_number: str = Form(..., description="Gazette number"),
    gazette_date: date = Form(..., description="Gazette date (YYYY-MM-DD)"),
    gazette_type: str = Form("trade", description="Gazette type"),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Upload a new gazette file.
    """
    # Validate file type
    if not validate_file_type(file.filename, [".pdf"]):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed",
        )
    
    try:
        # Save the uploaded file
        file_path = await save_upload_file(file, "gazettes")
        
        # Create gazette record
        gazette_in = schemas.GazetteCreate(
            gazette_number=gazette_number,
            gazette_date=gazette_date,
            gazette_type=gazette_type,
            file_path=file_path,
            file_name=file.filename,
            file_size=file.size,
        )
        
        gazette = crud.gazette.create(db, obj_in=gazette_in)
        return gazette
    except Exception as e:
        # Clean up file if gazette creation fails
        if 'file_path' in locals():
            import os
            try:
                os.remove(file_path)
            except OSError:
                pass
        
        raise HTTPException(
            status_code=500,
            detail=f"Error uploading file: {str(e)}",
        )
