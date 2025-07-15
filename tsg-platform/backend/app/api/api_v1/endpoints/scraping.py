import logging
import asyncio
from fastapi import APIRouter, BackgroundTasks, HTTPException, Depends, Body
from pydantic import BaseModel
from typing import Any, Dict

from app.scraping_browser import browser_manager, start_enhanced_scraping_process
from app.api import deps
from app.models import User

router = APIRouter()

# Pydantic Models
class LoginSessionResponse(BaseModel):
    session_id: str
    captcha_url: str

class ScrapingRequest(BaseModel):
    count: int = 10

# Endpoints
@router.post("/start-login", response_model=LoginSessionResponse)
async def start_login_session(
    current_user: User = Depends(deps.get_current_active_superuser)
):
    """
    Starts a login session for the ticaret sicil website using the shared browser manager.
    """
    try:
        if not browser_manager.get_status()["is_open"]:
            logging.info("Browser not open. Opening a new one for login session.")
            await browser_manager.open_browser(headless=True)

        page = await browser_manager.get_page()
        if not page:
            raise HTTPException(status_code=500, detail="Failed to get browser page.")

        session_id = browser_manager.get_session_id()
        logging.info(f"Starting login session with ID: {session_id}")

        await page.goto("https://www.ticaretsicil.gov.tr/view/hizlierisim/girisyap.php", wait_until="networkidle")

        login_button_selector = 'button[data-target="#UyeGirisi"]'
        await page.wait_for_selector(login_button_selector, state='visible')
        await page.click(login_button_selector)
        logging.info("Login modal opened.")

        captcha_selector = '#CaptchaImg'
        await page.wait_for_selector(captcha_selector, state='visible')
        
        captcha_element = await page.query_selector(captcha_selector)
        if not captcha_element:
            raise HTTPException(status_code=500, detail="CAPTCHA image element not found.")

        captcha_src = await captcha_element.get_attribute('src')
        if not captcha_src:
            raise HTTPException(status_code=500, detail="CAPTCHA image src attribute not found.")

        base_url = "https://www.ticaretsicil.gov.tr"
        captcha_full_url = f"{base_url}{captcha_src}"
        logging.info(f"CAPTCHA URL found: {captcha_full_url}")

        return {"session_id": session_id, "captcha_url": captcha_full_url}
    
    except Exception as e:
        logging.error(f"Error starting login session: {e}", exc_info=True)
        # Do not close the shared browser on error
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/browser/open", response_model=Dict[str, Any])
async def open_browser(headless: bool = Body(False, embed=True)) -> Any:
    """
    Opens a persistent browser instance for scraping.
    Set `headless` to `True` to run in the background.
    """
    result = await browser_manager.open_browser(headless=headless)
    if result.get("status") == "error":
        raise HTTPException(status_code=500, detail=result.get("message"))
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

@router.post("/start")
async def start_scraping(
    request: ScrapingRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(deps.get_current_active_superuser)
) -> Dict[str, str]:
    """
    Starts the enhanced scraping process in the background.
    """
    if not browser_manager.get_status()["is_open"]:
        raise HTTPException(status_code=400, detail="Browser is not open. Please open the browser first.")

    logging.info(f"User {current_user.email} initiated enhanced scraping for {request.count} companies.")
    
    # Run the scraping process in the background
    background_tasks.add_task(start_enhanced_scraping_process, count=request.count)
    
    return {"message": f"Enhanced scraping process started in the background for {request.count} companies."}
