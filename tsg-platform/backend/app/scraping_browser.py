import asyncio
import logging
from storage3.exceptions import StorageApiError
import os
import re
import traceback
import uuid
from datetime import datetime
from typing import Any, Dict, Optional

from playwright.async_api import (
    Browser,
    BrowserContext,
    Error as PlaywrightError,
    Page,
    Playwright,
    TimeoutError as PlaywrightTimeoutError,
    async_playwright,
)
from sqlalchemy.orm import Session

from app import crud
from app.core.config import settings
from app.db.session import SessionLocal
from app.core.supabase_client import supabase
from app.schemas.announcement import AnnouncementCreate
from app.scraping_state import scraping_state
# from app.services.notification_service import notification_service

logger = logging.getLogger(__name__)

# Helper data and functions for scraping
VALID_CITIES = [
    "İSTANBUL", "ANKARA", "İZMİR", "ACIPAYAM", "ADANA", "ADIYAMAN", "AFYONKARAHİSAR",
    "AFŞİN", "AKHİSAR", "AKSARAY", "AKYAZI", "AKÇAKOCA", "AKŞEHİR", "ALACA", "ALANYA",
    "ALAPLI", "ALAŞEHİR", "ALİAĞA", "AMASYA", "ANAMUR", "ANTALYA", "ARDAHAN", "ARDEŞEN",
    "ARHAVİ", "ARTVİN", "AYDIN", "AYVALIK", "AĞRI", "BABADAĞ", "BABAESKİ", "BAFRA",
    "BALIKESİR", "BANDIRMA", "BARTIN", "BATMAN", "BAYBURT", "BAYINDIR", "BERGAMA", "BEYPAZARI",
    "BEYŞEHİR", "BODRUM", "BOLU", "BOLVADİN", "BOR", "BORÇKA", "BOYABAT", "BOZÜYÜK",
    "BOĞAZLIYAN", "BUCAK", "BULANCAK", "BULDAN", "BURDUR", "BURHANİYE", "BURSA", "BÜNYAN",
    "BİGA", "BİLECİK", "BİNGÖL", "BİRECİK", "BİTLİS", "CEYHAN", "CİZRE", "DEMİRCİ",
    "DENİZLİ", "DEVELİ", "DEVREK", "DOĞANHİSAR", "DOĞUBAYAZIT", "DÖRTYOL", "DÜZCE", "DİDİM",
    "DİNAR", "DİYARBAKIR", "EDREMİT", "EDİRNE", "ELAZIĞ", "ELBİSTAN", "EMİRDAĞ", "ERBAA",
    "ERCİŞ", "ERDEK", "ERDEMLİ", "ERZURUM", "ERZİN", "ERZİNCAN", "ESKİŞEHİR", "FATSA",
    "FETHİYE", "GAZİANTEP", "GEBZE", "GEDİZ", "GELİBOLU", "GEMLİK", "GEREDE", "GÖNEN",
    "GÖRDES", "GÜMÜŞHACIKÖY", "GÜMÜŞHANE", "GİRESUN", "HAKKARİ", "HATAY", "HAVZA",
    "HAYMANA", "HAYRABOLU", "HOPA", "ILGIN", "ISPARTA", "IĞDIR", "KAHRAMANMARAŞ", "KADİRLİ",
    "KAMAN", "KARABÜK", "KARACABEY", "KARAHALLI", "KARAMAN", "KARAPINAR", "KARS",
    "KASTAMONU", "KAYSERİ", "KELKİT", "KEŞAN", "KIRIKHAN", "KIRIKKALE", "KIRKLARELİ",
    "KIRŞEHİR", "KIZILTEPE", "KOCAELİ", "KONYA EREĞLİ", "KONYA", "KOZAN", "KUMLUCA",
    "KUŞADASI", "KÖRFEZ", "KÜTAHYA", "KİLİS", "LÜLEBURGAZ", "MALATYA", "MALKARA",
    "MANAVGAT", "MANİSA", "MARDİN", "MARMARİS", "MENEMEN", "MERSİN", "MERZİFON", "MUCUR",
    "MUSTAFAKEMALPAŞA", "MUT", "MUĞLA", "MUŞ", "MİLAS", "NAZİLLİ", "NEVŞEHİR",
    "NUSAYBİN", "NİKSAR", "NİZİP", "NİĞDE", "OLTU", "ORDU", "ORHANGAZİ", "OSMANİYE",
    "PASİNLER", "PAZAR", "POLATLI", "REYHANLI", "RİZE", "SAFRANBOLU", "SAKARYA",
    "SALİHLİ", "SAMSUN", "SANDIKLI", "SARAYKÖY", "SELÇUK", "SEYDİŞEHİR", "SOMA",
    "SULUOVA", "SUNGURLU", "SUSURLUK", "SÖKE", "SİLİFKE", "SİMAV", "SİNOP", "SİVAS",
    "SİVEREK", "SİİRT", "TARSUS", "TATVAN", "TAVAS", "TAVŞANLI", "TAŞKÖPRÜ", "TEKİRDAĞ",
    "TERME", "TOKAT", "TORBALI", "TOSYA", "TRABZON", "TUNCELİ", "TURGUTLU", "TURHAL",
    "TİRE", "UZUNKÖPRÜ", "UŞAK", "VAN", "VEZİRKÖPRÜ", "YAHYALI", "YALOVA", "YALVAÇ",
    "YENİŞEHİR", "YERKÖY", "YOZGAT", "YÜKSEKOVA", "ZONGULDAK", "ZİLE", "ÇANAKKALE",
    "ÇANKIRI", "ÇARŞAMBA", "ÇAY", "ÇAYCUMA", "ÇAYELİ", "ÇERKEZKÖY", "ÇORLU", "ÇORUM",
    "ÇUMRA", "ÖDEMİŞ", "ÜNYE", "ÜRGÜP", "İNEBOLU", "İNEGÖL", "İSKENDERUN", "İSLAHİYE",
    "İZNİK", "ŞANLIURFA", "ŞEREFLİKOÇHİSAR", "ŞIRNAK", "SORGUN", "OF", "ŞEFAATLİ",
    "KARADENİZ EREĞLİ"
]

def normalize_city_name(db_city_name: str) -> str | None:
    """
    Veritabanından gelen sicil müdürlüğü adını, sitedeki dropdown ile uyumlu hale getirir.
    """
    if not db_city_name:
        return None
    normalized = db_city_name.upper().strip()
    suffixes_to_remove = [
        'TİCARET SİCİLİ MÜDÜRLÜĞÜ',
        'TİCARET SİCİL MÜDÜRLÜĞÜ',
        'TİCARET VE SANAYİ ODASI'
    ]
    cleaned_name = normalized
    for suffix in suffixes_to_remove:
        cleaned_name = cleaned_name.replace(suffix, '')
    cleaned_name = cleaned_name.strip()
    if cleaned_name in VALID_CITIES:
        return cleaned_name
    logger.warning(f"Could not normalize city name: {db_city_name}")
    return None



class BrowserManager:
    """Singleton class to manage a persistent Playwright browser instance."""
    _instance = None
    _playwright: Optional[Playwright] = None
    _browser: Optional[Browser] = None
    _context: Optional[BrowserContext] = None
    _storage_state_path = os.path.join(settings.PROJECT_ROOT, ".playwright_storage_state.json")
    _lock = asyncio.Lock()
    _save_task: Optional[asyncio.Task] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(BrowserManager, cls).__new__(cls)
        return cls._instance

    async def open_browser(self, headless: bool = False) -> Dict[str, Any]:
        """Initializes Playwright and launches a persistent browser context."""
        async with self._lock:
            if self._browser and self._browser.is_connected():
                msg = "Browser is already open."
                logger.warning(msg)
                return {"status": "already_open", "message": msg, "context_status": self.get_status()}

            try:
                logger.info("Initializing Playwright...")
                self._playwright = await async_playwright().start()
                
                user_data_dir = os.path.join(settings.PROJECT_ROOT, ".playwright_user_data")
                os.makedirs(user_data_dir, exist_ok=True)
                logger.info(f"Using user data directory: {user_data_dir}")

                self._browser = await self._playwright.webkit.launch(headless=headless)

                storage_state = self._storage_state_path if os.path.exists(self._storage_state_path) else None
                if storage_state:
                    logger.info(f"Found existing session state at: {self._storage_state_path}")
                else:
                    logger.info("No session state found, starting a new session.")

                self._context = await self._browser.new_context(
                    storage_state=storage_state,
                    user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Safari/605.1.15",
                    viewport={"width": 1920, "height": 1080}
                )
                
                self._context.on("close", self._handle_close)
                logger.info("Browser context launched successfully.")

                # Start periodic saving
                self._save_task = asyncio.create_task(self._periodic_save())
                
                # Open a default page
                page = await self.get_page()
                await page.goto("https://www.ticaretsicil.gov.tr/", wait_until="domcontentloaded")
                logger.info("Navigated to the target website.")

                return {"status": "opened", "message": "Browser opened successfully for manual login."}

            except PlaywrightError as e:
                error_msg = f"Failed to open browser: {e}"
                logger.error(error_msg, exc_info=True)
                await self.close_browser()
                return {"status": "error", "message": error_msg}

    async def close_browser(self) -> Dict[str, str]:
        """Closes the browser context and shuts down Playwright."""
        async with self._lock:
            if self._save_task and not self._save_task.done():
                self._save_task.cancel()
                logger.info("Periodic save task cancelled.")

            if not self._browser or not self._browser.is_connected():
                msg = "Browser is not open or already closed."
                logger.warning(msg)
                return {"status": "not_open", "message": msg}

            try:
                # Save session state before closing
                if self._context:
                    logger.info(f"Saving session state to {self._storage_state_path}")
                    await self._context.storage_state(path=self._storage_state_path)
            except PlaywrightError as e:
                logger.error(f"Failed to save session state: {e}", exc_info=True)

            try:
                logger.info("Closing browser context...")
                await self._browser.close()
                self._context = None
                self._browser = None
            except PlaywrightError as e:
                logger.error(f"Error closing browser context: {e}", exc_info=True)
            
            if self._playwright and self._playwright.is_connected():
                logger.info("Stopping Playwright...")
                await self._playwright.stop()
                self._playwright = None

            logger.info("Browser closed successfully.")
            return {"status": "closed", "message": "Browser closed successfully."}

    async def navigate_to_url(self, url: str) -> Dict[str, str]:
        if not self.context or not self.page:
            return {"status": "error", "message": "Browser is not open."}
        
        try:
            logger.info(f"Navigating to: {url}")
            await self.page.goto(url, wait_until="domcontentloaded")
            return {"status": "success", "message": f"Successfully navigated to {url}"}
        except Exception as e:
            logger.error(f"Failed to navigate to {url}: {e}")
            return {"status": "error", "message": str(e)}

    async def scrape_current_page_data(self) -> Dict[str, Any]:
        """
        Scrapes relevant data (address, NACE code, etc.) from the current page and extracts sicil_no from URL.
        """
        if not self.page:
            return {"status": "error", "message": "No active page to scrape."}

        try:
            page = self.page
            logger.info(f"Scraping data from URL: {page.url}")

            await page.wait_for_selector("body", timeout=15000)

            # Helper JS function to find text in a sibling cell
            js_eval_helper = """
            (label_text) => {
                const all_cells = Array.from(document.querySelectorAll('td, th'));
                const label_element = all_cells.find(el => el.textContent.trim().includes(label_text));
                if (label_element && label_element.nextElementSibling) {
                    return label_element.nextElementSibling.textContent.trim();
                }
                return null;
            }
            """

            address = await page.evaluate(js_eval_helper, 'Adresi')
            nace_code = await page.evaluate(js_eval_helper, 'NACE Kodu')
            
            # Extract sicil_no from URL
            sicil_no = None
            if "ilanlar.php?id=" in page.url:
                sicil_no = page.url.split("id=")[-1].split('&')[0]

            scraped_data = {
                "address": address,
                "nace_code": nace_code,
                "sicil_no": sicil_no,
            }

            if not any(scraped_data.values()):
                logger.warning("Could not find any data points on the page.")

            logger.info(f"Successfully scraped data: {scraped_data}")
            return {"status": "success", "data": scraped_data}

        except PlaywrightTimeoutError as e:
            error_msg = f"Timeout while waiting for page elements during scraping: {e}"
            logger.error(error_msg)
            return {"status": "error", "message": error_msg}
        except Exception as e:
            error_msg = f"An unexpected error occurred during scraping: {e}"
            logger.error(error_msg, exc_info=True)
            return {"status": "error", "message": error_msg}

    def get_status(self) -> Dict[str, Any]:
        """Returns the current status of the browser and context."""
        if not self._browser or not self._browser.is_connected() or not self._context:
            return {"is_open": False, "pages": 0, "url": None}
        
        try:
            pages = self._context.pages
            current_url = pages[0].url if pages else None
            return {"is_open": True, "pages": len(pages), "url": current_url}
        except PlaywrightError:
            # This can happen if the context is closed during the check
            return {"is_open": False, "pages": 0, "url": None}

    async def get_page(self) -> Optional[Page]:
        """Returns the primary page from the context, or creates one if none exist."""
        if not self.get_status()["is_open"]:
            logger.error("Cannot get page, browser is not open.")
            return None
        
        if not self._context.pages:
            logger.info("No pages found in context, creating a new one.")
            return await self._context.new_page()
        
        return self._context.pages[0]

    async def _periodic_save(self):
        """Periodically saves the browser session state."""
        while self._browser and self._browser.is_connected():
            await asyncio.sleep(10)  # Save every 10 seconds
            if self._browser and self._browser.is_connected() and self._context:
                try:
                    logger.info("Periodically saving session state...")
                    await self._context.storage_state(path=self._storage_state_path)
                except PlaywrightError as e:
                    logger.error(f"Periodic save failed: {e}")
        logger.info("Periodic save task finished.")

    async def stop_periodic_save(self):
        """Stops the periodic saving of the browser session state."""
        if self._save_task and not self._save_task.done():
            self._save_task.cancel()
            self._save_task = None
            logger.info("Periodic session saving has been stopped.")
        else:
            logger.info("Periodic session saving was not running or was already stopped.")

    async def _handle_close(self):
        """Callback function for when the browser context is closed."""
        logger.warning("Browser context was closed, possibly by the user.")
        if self._save_task and not self._save_task.done():
            self._save_task.cancel()
        # Reset state, but don't try to run async code here
        self._context = None
        self._browser = None

# Instantiate the singleton
browser_manager = BrowserManager()


async def start_enhanced_scraping_process(count: int):
    """
    Fetches unscraped companies, scrapes their announcements, and saves them to the database.
    This function is intended for robust, production-like scraping.
    """
    logger.info(f"Starting scraping process for up to {count} companies with DB saving.")
    await browser_manager.stop_periodic_save()
    db: Session = SessionLocal()
    page = await browser_manager.get_page()

    if not page:
        error_msg = "Could not get a page from the browser manager."
        logger.error(error_msg)
        scraping_state.set_error(error_msg)
        db.close()
        return

    try:
        companies = crud.company.get_unscraped_with_sicil_info(db, limit=count)
        scraping_state.start(total_count=len(companies))

        if not companies:
            logger.info("No unscraped companies with sicil info found.")
            scraping_state.add_log("INFO: No new companies to scrape.")
            return

        logger.info(f"Found {len(companies)} companies to scrape.")

        # Ensure the Supabase bucket exists before starting to scrape
        bucket_name = "gazette-pdfs"
        try:
            buckets = supabase.storage.list_buckets()
            if not any(b.name == bucket_name for b in buckets):
                logger.info(f"Bucket '{bucket_name}' not found. Creating it...")
                supabase.storage.create_bucket(id=bucket_name, name=bucket_name, options={"public": True})
                logger.info(f"Bucket '{bucket_name}' created successfully.")
            else:
                logger.info(f"Bucket '{bucket_name}' already exists.")
        except StorageApiError as e:
            logger.error(f"An error occurred while checking or creating bucket '{bucket_name}': {e}")
            # RLS hatası gibi kritik bir durumda işlemi durdurmak için hatayı yükselt
            raise e

        for company in companies:
            if scraping_state.should_stop:
                scraping_state.add_log("STOP_SIGNAL_RECEIVED: Stopping task.")
                break
            # We use the main, robust scrape_company function which handles all logic including DB operations.
            await scrape_company(page, db, company)

    except Exception as e:
        error_message = f"An unexpected error occurred during the main scraping loop: {traceback.format_exc()}"
        logger.error(error_message)
        scraping_state.add_log(error_message)
        scraping_state.set_error(str(e))
    finally:
        db.close()
        scraping_state.finish()
        logger.info("Scraping process with DB saving has finished.")


async def get_companies_for_scraping(db: Session, limit: int = 10):
    """Get companies from database that need scraping."""
    try:
        # Use MCP to get companies from Supabase
        from app.core.supabase_client import supabase
        
        result = supabase.table("companies").select(
            "id, unvan, sicil_no, sicil_mudurluk"
        ).not_.is_("sicil_no", "null").not_.is_("sicil_mudurluk", "null").is_("scraped_at", "null").order(
            "created_at", desc=False
        ).limit(limit).execute()
        
        companies = []
        if result.data:
            for row in result.data:
                companies.append((row['id'], row['unvan'], row['sicil_no'], row['sicil_mudurluk']))
        
        logger.info(f"Found {len(companies)} companies for scraping")
        return companies
    except Exception as e:
        logger.error(f"Error fetching companies: {e}")
        return []


async def scrape_company_enhanced(page, db: Session, company):
    """Enhanced scraping for a single company with automatic form filling."""
    company_id, unvan, sicil_no, sicil_mudurluk = company
    
    scraping_state.add_log(f"PROCESSING_COMPANY: Start processing '{unvan}' (Sicil No: {sicil_no}).")
    
    try:
        # Normalize city name for dropdown
        normalized_city = normalize_city_name_for_dropdown(sicil_mudurluk)
        if not normalized_city:
            error_msg = f"Could not normalize sicil_mudurluk: '{sicil_mudurluk}' for company '{unvan}'."
            scraping_state.add_log(f"COMPANY_ERROR: {error_msg}")
            await mark_company_as_scraped(db, company_id)
            return

        scraping_state.add_log(f"NORMALIZED_CITY: Using '{normalized_city}' for city selection.")

        # Navigate to search page
        await page.goto("https://www.ticaretsicil.gov.tr/view/hizlierisim/ilangoruntuleme.php", wait_until="domcontentloaded")
        await page.wait_for_selector("select[name='SicilMudurluguId']", state="visible", timeout=15000)

        # Fill form with company data
        await fill_search_form(page, normalized_city, sicil_no)
        
        # Set table rows to 100
        await set_table_rows_to_100(page)
        
        # Extract and save announcements
        await extract_and_save_announcements(page, db, company_id, unvan)
        
        # Mark company as scraped
        await mark_company_as_scraped(db, company_id)
        scraping_state.add_log(f"COMPANY_SCRAPED_SUCCESS: Successfully finished scraping '{unvan}'.")

    except Exception as e:
        error_message = f"Failed to process company '{unvan}': {traceback.format_exc()}"
        logger.error(error_message)
        scraping_state.add_log(f"COMPANY_ERROR: {error_message}")
        await mark_company_as_scraped(db, company_id)


def normalize_city_name_for_dropdown(sicil_mudurluk: str) -> str:
    """Normalize sicil_mudurluk to match dropdown options."""
    if not sicil_mudurluk:
        return None
    
    # Extract city name from various formats
    city_name = sicil_mudurluk.upper().strip()
    
    # Remove common suffixes
    suffixes_to_remove = [
        'TİCARET SİCİLİ MÜDÜRLÜĞÜ',
        'TİCARET SİCİL MÜDÜRLÜĞÜ', 
        'TİCARET VE SANAYİ ODASI',
        'MÜDÜRLÜĞÜ',
        'MÜDÜRLÜK'
    ]
    
    for suffix in suffixes_to_remove:
        city_name = city_name.replace(suffix, '').strip()
    
    # Map common variations
    city_mappings = {
        'İSTANBUL': 'İSTANBUL',
        'ANKARA': 'ANKARA', 
        'İZMİR': 'İZMİR',
        'BURSA': 'BURSA',
        'ANTALYA': 'ANTALYA'
    }
    
    return city_mappings.get(city_name, city_name)


async def fill_search_form(page, city_name: str, sicil_no: str):
    """Fill the search form with company data."""
    try:
        # Select city from dropdown
        await page.select_option("select[name='SicilMudurluguId']", label=city_name)
        scraping_state.add_log(f"FORM_FILLED: Selected city '{city_name}'")
        
        # Fill sicil no
        await page.fill("input[name='TicSicNo']", sicil_no)
        scraping_state.add_log(f"FORM_FILLED: Entered sicil no '{sicil_no}'")
        
        # Submit form
        await page.click("button[type='submit']")
        await page.wait_for_load_state("domcontentloaded")
        scraping_state.add_log("FORM_SUBMITTED: Search form submitted")
        
    except Exception as e:
        scraping_state.add_log(f"FORM_ERROR: Error filling form: {e}")
        raise


async def mark_company_as_scraped(db: Session, company_id: str):
    """Mark company as scraped in the database."""
    try:
        from app.core.supabase_client import supabase
        
        result = supabase.table("companies").update({
            "scraped_at": datetime.utcnow().isoformat()
        }).eq("id", company_id).execute()
        
        if result.data:
            scraping_state.add_log(f"COMPANY_MARKED: Company {company_id} marked as scraped")
        else:
            scraping_state.add_log(f"COMPANY_MARK_ERROR: Failed to mark company as scraped")
            
    except Exception as e:
        scraping_state.add_log(f"MARK_ERROR: Error marking company as scraped: {e}")


async def start_scraping_process(count: int):
    """Main function to perform the scraping task using the managed browser."""
    db: Optional[Session] = None
    try:
        scraping_state.start(total_count=count)
        scraping_state.add_log("SCRAPING_TASK_STARTED: Scraping process initiated.")

        if not browser_manager.get_status()["is_open"]:
            error_msg = "Browser is not open. Please open it first to log in."
            scraping_state.add_log(f"SCRAPING_ERROR: {error_msg}")
            scraping_state.set_error(error_msg)
            return

        page = await browser_manager.get_page()
        if not page:
            error_msg = "Failed to get a browser page."
            scraping_state.add_log(f"SCRAPING_ERROR: {error_msg}")
            scraping_state.set_error(error_msg)
            return

        db = SessionLocal()
        scraping_state.add_log("DB_SESSION_CREATED: Database session opened.")

        companies_to_scrape = crud.company.get_unscraped(db, limit=count)
        if not companies_to_scrape:
            scraping_state.add_log("INFO: No new companies to scrape.")
            return

        scraping_state.add_log(f"DB_FETCH_SUCCESS: Found {len(companies_to_scrape)} companies to scrape.")
        await page.goto("https://www.ticaretsicil.gov.tr/view/hizlierisim/ilangoruntuleme.php", wait_until="domcontentloaded")

        for company in companies_to_scrape:
            if scraping_state.should_stop:
                scraping_state.add_log("STOP_SIGNAL_RECEIVED: Stopping task.")
                break
            await scrape_company(page, db, company)

    except Exception as e:
        error_message = f"An unexpected error occurred during scraping: {traceback.format_exc()}"
        logger.error(error_message)
        scraping_state.add_log(error_message)
        scraping_state.set_error(str(e))
    finally:
        if db:
            db.close()
            scraping_state.add_log("DB_CLOSED: Database session closed.")
        scraping_state.finish()
        logger.info("Scraping task finished.")


async def scrape_company(page: Page, db: Session, company):
    """
    Scrapes a single company's announcements using its trade registry number (sicil_no).
    This is the primary, robust scraping function.
    """
    scraping_state.add_log(f"PROCESSING_COMPANY: Start processing '{company.unvan}' (Sicil No: {company.sicil_no}, Mudurluk: {company.sicil_mudurluk}).")

    try:
        # 1. Normalize city name
        city_name = normalize_city_name(company.sicil_mudurluk)
        if not city_name:
            error_msg = f"Could not normalize city name: '{company.sicil_mudurluk}' for company '{company.unvan}'."
            scraping_state.add_log(f"COMPANY_ERROR: {error_msg}")
            crud.company.mark_as_scraped(db=db, company_id=company.id)
            return

        # 2. Navigate and fill the form
        await page.goto("https://www.ticaretsicil.gov.tr/view/hizlierisim/ilangoruntuleme.php", wait_until="domcontentloaded")
        await page.select_option('select#SicilMudurluguId', label=city_name)
        await page.fill('input#TicSicNo', str(company.sicil_no))
        
        # 3. Click search and wait for results
        search_button_selector = 'button[data-message="İlan Ara"]'
        await page.click(search_button_selector)
        scraping_state.add_log("FORM_SUBMITTED: Search form submitted.")

        # 4. Process results page by page
        page_number = 1
        while True:
            if scraping_state.should_stop:
                scraping_state.add_log("STOP_SIGNAL_RECEIVED: Stopping company processing.")
                return

            scraping_state.add_log(f"PROCESSING_PAGE: Scraping page {page_number} for '{company.unvan}'.")

            try:
                await page.wait_for_selector('table#tblIlanGoruntuleme tbody tr', timeout=20000)
            except PlaywrightTimeoutError:
                scraping_state.add_log(f"NO_RESULTS_TABLE: No results table found on page {page_number}. Assuming no results.")
                break

            rows = await page.query_selector_all('table#tblIlanGoruntuleme tbody tr')
            if not rows or "Eşleşen kayıt bulunamadı" in await rows[0].inner_text():
                if page_number == 1:
                    scraping_state.add_log(f"NO_RESULTS: No announcements found for '{company.unvan}'.")
                else:
                    scraping_state.add_log(f"PAGINATION_END: Reached end of results on page {page_number}.")
                break

            scraping_state.add_log(f"RESULTS_FOUND: Found {len(rows)} announcements on page {page_number}.")

            for row in rows:
                try:
                    cells = await row.query_selector_all('td')
                    if len(cells) < 8:
                        scraping_state.add_log(f"ROW_SKIP: Skipping row with insufficient columns ({len(cells)}).")
                        continue

                    # Extract data from cells
                    publication_date_str = await cells[3].inner_text()
                    title = await cells[2].inner_text()
                    publication_date = datetime.strptime(publication_date_str, '%d.%m.%Y').date()

                    # Check for duplicates before proceeding
                    if crud.announcement.get_by_details(db, company_id=company.id, publication_date=publication_date, title=title):
                        scraping_state.add_log(f"DUPLICATE_SKIP: Skipping existing announcement from {publication_date_str} for '{company.unvan}'.")
                        continue

                    # Extract remaining data
                    trade_registry_name = await cells[0].inner_text()
                    trade_registry_number = await cells[1].inner_text()
                    issue_number_str = await cells[4].inner_text()
                    page_number_str = await cells[5].inner_text()
                    announcement_type = await cells[6].inner_text()
                    newspaper_name = await cells[7].inner_text()
                    
                    pdf_url = None
                    pdf_link_element = await cells[7].query_selector('a')
                    if pdf_link_element:
                        try:
                            # Start waiting for the download before clicking
                            async with page.expect_download() as download_info:
                                await pdf_link_element.click()
                            
                            download = await download_info.value
                            temp_pdf_path = await download.path()
                            with open(temp_pdf_path, 'rb') as f:
                                pdf_content = f.read()
                            await download.delete()  # Clean up the downloaded file
                            
                            file_name = f"announcement_{company.id}_{uuid.uuid4()}.pdf"
                            bucket_name = "gazette-pdfs"
                            
                            # Upload to Supabase Storage
                            upload_response = supabase.storage.from_(bucket_name).upload(
                                file=pdf_content, 
                                path=file_name, 
                                file_options={"content-type": "application/pdf"}
                            )
                            
                            # Get public URL
                            res = supabase.storage.from_(bucket_name).get_public_url(file_name)
                            pdf_url = res

                            scraping_state.add_log(f"PDF_UPLOADED: PDF for '{title}' uploaded to Supabase.")

                        except Exception as pdf_error:
                            scraping_state.add_log(f"PDF_ERROR: Failed to download/upload PDF for '{title}'. Error: {pdf_error}")
                            logger.error(f"PDF download/upload error for company {company.id}", exc_info=True)
                            pdf_url = None # Ensure pdf_url is None on failure

                    # Create announcement object
                    announcement_in = AnnouncementCreate(
                        company_id=company.id,
                        trade_registry_name=trade_registry_name,
                        trade_registry_number=trade_registry_number,
                        title=title,
                        publication_date=publication_date,
                        issue_number=int(issue_number_str) if issue_number_str.strip().isdigit() else None,
                        page_number=int(page_number_str) if page_number_str.strip().isdigit() else None,
                        announcement_type=announcement_type,
                        newspaper_name=newspaper_name,
                        pdf_url=pdf_url
                    )
                    
                    # Save to DB
                    crud.announcement.create(db, obj_in=announcement_in)
                    scraping_state.add_log(f"SUCCESS: Saved announcement from {publication_date_str} for '{company.unvan}'.")

                except Exception as e:
                    db.rollback()
                    error_msg = f"ROW_ERROR: Failed to process a row for '{company.unvan}'. Error: {e}"
                    logger.error(error_msg, exc_info=True)
                    scraping_state.add_log(error_msg)
                    continue # Continue to the next row
            
            # 5. Handle pagination
            next_button = await page.query_selector('a.paginate_button.next:not(.disabled)')
            if not next_button:
                scraping_state.add_log("PAGINATION_END: No 'next' button found.")
                break
            
            await next_button.click()
            page_number += 1
            await page.wait_for_timeout(2000) # Wait for next page to load

        # 6. Mark company as scraped after processing all pages
        crud.company.mark_as_scraped(db=db, company_id=company.id)
        scraping_state.add_log(f"COMPANY_SCRAPED_SUCCESS: Successfully finished scraping '{company.unvan}'.")

    except Exception as e:
        error_message = f"COMPANY_ERROR: Failed to process company '{company.unvan}'. Error: {traceback.format_exc()}"
        logger.error(error_message)
        scraping_state.add_log(error_message)
        # Mark as scraped even on critical failure to avoid retrying a broken company
        crud.company.mark_as_scraped(db=db, company_id=company.id)
