"""
Utility API endpoints
"""
from typing import Any, Dict

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()

@router.get("/health")
async def health_check() -> Dict[str, str]:
    """
    Health check endpoint.
    """
    return {"status": "ok"}

@router.get("/version")
async def get_version() -> Dict[str, str]:
    """
    Get API version information.
    """
    return {
        "name": "TSG Research Platform API",
        "version": "1.0.0",
        "status": "active"
    }

@router.get("/settings")
async def get_settings(
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Dict[str, Any]:
    """
    Get public application settings.
    """
    return {
        "app_name": "TSG Research Platform",
        "max_upload_size": 50,  # MB
        "allowed_file_types": [
            "application/pdf",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            "application/vnd.ms-excel",
            "text/csv",
            "image/jpeg",
            "image/png"
        ]
    }

@router.post("/search")
async def search(
    query: str,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Dict[str, Any]:
    """
    Global search across all models.
    """
    if not query or len(query.strip()) < 3:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Search query must be at least 3 characters long",
        )
    
    results = {
        "query": query,
        "companies": [],
        "persons": [],
        "gazettes": [],
    }
    
    # Search companies
    companies = crud.company.search(db, query=query, limit=5)
    if companies:
        results["companies"] = [
            {
                "id": company.id,
                "title": company.title,
                "tax_number": company.tax_number,
                "type": "company"
            } for company in companies
        ]
    
    # Search persons
    persons = crud.person.search(db, query=query, limit=5)
    if persons:
        results["persons"] = [
            {
                "id": person.id,
                "full_name": person.full_name,
                "nationality_id": person.nationality_id,
                "type": "person"
            } for person in persons
        ]
    
    # Search gazettes
    gazettes = crud.gazette.search(db, query=query, limit=5)
    if gazettes:
        results["gazettes"] = [
            {
                "id": gazette.id,
                "gazette_number": gazette.gazette_number,
                "gazette_date": gazette.gazette_date.isoformat() if gazette.gazette_date else None,
                "type": "gazette"
            } for gazette in gazettes
        ]
    
    return results
