import asyncio
import logging
import os
import re
import random
import uuid
import httpx
import traceback
from datetime import datetime
from typing import Any, Dict, Optional
from urllib.parse import urljoin

from storage3.utils import StorageException

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

from app import crud, models, schemas
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
        except StorageException as e:
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





async def scrape_company(page: Page, db: Session, company):
    """
    Scrapes a single company's announcements, handling pagination, silent PDF downloads,
    and database operations with robust error handling.
    """
    scraping_state.add_log(f"PROCESSING_COMPANY: Start processing '{company.unvan}' (Sicil No: {company.sicil_no}).")
    try:
        city_name = normalize_city_name(company.sicil_mudurluk)
        if not city_name:
            scraping_state.add_log(f"COMPANY_ERROR: Could not normalize city name for '{company.unvan}'.")
            crud.company.mark_as_scraped(db=db, company_id=company.id) # Mark as scraped to avoid retries
            return

        await page.goto("https://www.ticaretsicil.gov.tr/view/hizlierisim/ilangoruntuleme.php", wait_until="domcontentloaded")
        await page.select_option('select#SicilMudurluguId', label=city_name)
        await page.fill('input#TicSicNo', str(company.sicil_no))
        await page.click('button[data-message=\"İlan Ara\"]')
        scraping_state.add_log("FORM_SUBMITTED: Search form submitted.")

        page_number = 1
        while True:
            if scraping_state.should_stop:
                scraping_state.add_log("STOP_SIGNAL_RECEIVED: Stopping company processing.")
                return

            scraping_state.add_log(f"PROCESSING_PAGE: Scraping page {page_number} for '{company.unvan}'.")
            try:
                await page.wait_for_selector('table#tblIlanGoruntuleme tbody tr', timeout=20000)
                # Set page size to 100 on the first page
                if page_number == 1:
                    try:
                        size_selector = 'select[name=\"tblIlanGoruntuleme_length\"]'
                        await page.wait_for_selector(size_selector, timeout=10000)
                        await page.select_option(size_selector, label='100')
                        await page.wait_for_load_state('networkidle', timeout=15000)
                        scraping_state.add_log("Successfully set page size to 100.")
                    except Exception as e:
                        scraping_state.add_log(f"Could not set page size to 100, proceeding with default. Reason: {e}")
            except PlaywrightTimeoutError:
                scraping_state.add_log("NO_RESULTS_TABLE: No results found for this company.")
                break

            rows = await page.query_selector_all('table#tblIlanGoruntuleme tbody tr')
            if not rows or "Eşleşen kayıt bulunamadı" in await rows[0].inner_text():
                scraping_state.add_log("NO_ANNOUNCEMENTS: No announcements found on this page.")
                break

            for row in rows:
                try:
                    cells = await row.query_selector_all('td')
                    if len(cells) < 8:
                        continue

                    publication_date_str = await cells[3].inner_text()
                    title = await cells[2].inner_text()
                    publication_date = datetime.strptime(publication_date_str, '%d.%m.%Y').date()

                    if crud.announcement.get_by_details(db, company_id=company.id, publication_date=publication_date, title=title):
                        scraping_state.add_log(f"DUPLICATE_SKIP: Skipping existing announcement: {title}")
                        continue

                    pdf_url = None
                    storage_path = None
                    pdf_link_element = await cells[7].query_selector('a')

                    if pdf_link_element:
                        pdf_href = await pdf_link_element.get_attribute('href')
                        if pdf_href:
                            try:
                                # Start waiting for both the download and the new page (popup) that the click triggers.
                                async with page.expect_popup() as popup_info, page.expect_download() as download_info:
                                    await pdf_link_element.click() # This click opens a new tab and starts a download.
                                
                                new_page = await popup_info.value
                                download = await download_info.value

                                # We have the download, so we no longer need the new page.
                                await new_page.close()

                                # Read the downloaded content into memory
                                download_path = await download.path()
                                with open(download_path, "rb") as f:
                                    pdf_content = f.read()
                                scraping_state.add_log(f"Playwright captured download for '{title}'.")

                                file_name = f"announcement_{company.id}_{uuid.uuid4()}.pdf"
                                bucket_name = "gazette-pdfs"

                                # Upload to Supabase
                                supabase.storage.from_(bucket_name).upload(
                                    file=pdf_content, path=file_name, file_options={"content-type": "application/pdf"}
                                )

                                pdf_url = supabase.storage.from_(bucket_name).get_public_url(file_name)
                                storage_path = f"{bucket_name}/{file_name}"
                                scraping_state.add_log(f"PDF_SUCCESS: PDF for '{title}' downloaded and uploaded.")

                            except Exception as pdf_error:
                                scraping_state.add_log(f"PDF_ERROR: Failed to download/upload PDF for '{title}'. Reason: {pdf_error}")
                                logger.error(f"PDF_ERROR for {company.unvan}", exc_info=True)

                    announcement_data = schemas.AnnouncementCreate(
                        company_id=company.id,
                        trade_registry_name=await cells[0].inner_text(),
                        trade_registry_number=await cells[1].inner_text(),
                        title=title,
                        publication_date=publication_date,
                        issue_number=int(await cells[4].inner_text()),
                        page_number=int(await cells[5].inner_text()),
                        announcement_type=await cells[6].inner_text(),
                        newspaper_name=await cells[7].inner_text(), # This might contain the link text
                        pdf_url=pdf_url,
                        storage_path=storage_path
                    )
                    crud.announcement.create(db=db, obj_in=announcement_data)
                    scraping_state.add_log(f"DB_SUCCESS: Saved announcement: {title}")

                except Exception as e:
                    db.rollback() # Rollback on row error
                    scraping_state.add_log(f"ROW_ERROR: Failed to process row. Reason: {e}")
                    logger.error(f"ROW_ERROR for {company.unvan}", exc_info=True)
                    continue # Continue to the next row

            next_page_button = await page.query_selector('li.paginate_button.next:not(.disabled) a')
            if next_page_button:
                await next_page_button.click()
                page_number += 1
                await page.wait_for_load_state('domcontentloaded')
            else:
                scraping_state.add_log("PAGINATION_END: No more pages.")
                break

    except Exception as e:
        db.rollback()
        error_message = f"COMPANY_CRITICAL_ERROR: Failed to process company '{company.unvan}'. Reason: {e}"
        logger.error(f"COMPANY_CRITICAL_ERROR for {company.unvan}", exc_info=True)
        scraping_state.add_log(error_message)
    finally:
        crud.company.mark_as_scraped(db=db, company_id=company.id)
        scraping_state.add_log(f"PROCESSING_COMPLETE: Finished processing for '{company.unvan}'.")
        db.commit()
