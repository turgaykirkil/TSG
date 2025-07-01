from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Any

from app import crud, models
from app.api import deps
from app.services import scraper_service

router = APIRouter()

@router.post("/scrape/company/{company_id}")
async def scrape_company(
    company_id: str,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Belirtilen şirket için kazıma işlemi başlatır.
    """
    try:
        result = await scraper_service.scrape_company_by_id(db, company_id=company_id)
        if result["status"] == "error":
            raise HTTPException(status_code=400, detail=result["message"])
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
