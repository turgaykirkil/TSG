import logging
from fastapi import APIRouter, HTTPException, Body
from typing import Any, Dict
from sqlalchemy.orm import Session

from app.scraping_browser import browser_manager, start_enhanced_scraping_process
from app.db.session import SessionLocal

router = APIRouter()

@router.post("/browser/open", response_model=Dict[str, Any])
async def open_browser(headless: bool = Body(False, embed=True)) -> Any:
    """
    Opens a persistent browser instance for scraping.
    Set `headless` to `True` to run in the background.
    """
    result = await browser_manager.open_browser(headless=headless)
    if result["status"] == "error":
        raise HTTPException(status_code=500, detail=result["message"])
    return result


@router.post("/browser/close", response_model=Dict[str, str])
async def close_browser() -> Any:
    """
    Closes the persistent browser instance.
    """
    return await browser_manager.close_browser()


@router.get("/browser/status", response_model=Dict[str, Any])
def get_browser_status() -> Any:
    """
    Returns the current status of the browser.
    """
    return browser_manager.get_status()


from pydantic import BaseModel

class ScrapingRequest(BaseModel):
    count: int = 10

@router.post("/start")
async def start_scraping(request: ScrapingRequest) -> Dict[str, str]:
    """
    Starts the enhanced scraping process with automatic form filling and data extraction.
    """
    if not browser_manager.get_status()["is_open"]:
        raise HTTPException(status_code=400, detail="Browser is not open. Please open it first.")

    page = await browser_manager.get_page()
    if not page:
        raise HTTPException(status_code=500, detail="Browser page not available.")

    try:
        # Start the enhanced scraping process
        await start_enhanced_scraping_process(request.count)
        
        return {"message": f"Enhanced scraping process started for {request.count} companies."}

    except Exception as e:
        logging.error(f"An error occurred during enhanced scraping: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

