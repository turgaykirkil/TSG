import asyncio
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from typing import Any

from app import crud, models
from app.api import deps
from app.scraping_browser import browser_manager, start_enhanced_scraping_process
from app.scraping_state import scraping_state
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


@router.get("/browser/status")
async def browser_status(
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Browser ve scraping durumunu döndürür.
    """
    try:
        return {
            "browser": browser_manager.get_status(),
            "scraping": scraping_state.get_status(),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/start")
async def start_scraping(
    payload: dict = Body(...),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Otomatik login + CAPTCHA ile Chromium akışını arka planda başlatır.
    Anında 200 döner.
    """
    try:
        count = int(payload.get("count", 10))
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid 'count' value")

    try:
        # Tarayıcıyı aç (zaten açıksa no-op)
        await browser_manager.open_browser(headless=True)
        # Arka planda scraping'i başlat
        asyncio.create_task(start_enhanced_scraping_process(count))
        return {"status": "started", "message": f"Scraping started for up to {count} companies."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
