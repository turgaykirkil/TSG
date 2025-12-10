import asyncio
import logging
import os
import re
import random
import secrets
import uuid
import shutil
import httpx
import traceback
from datetime import datetime, date
from typing import Any, Dict, Optional, List
from urllib.parse import urljoin

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
from app.core.storage import (
    ensure_bucket,
    upload_bytes,
    get_presigned_url,
)
from app.schemas.announcement import AnnouncementCreate
from app.scraping_state import scraping_state
# from app.services.notification_service import notification_service
from app.utils.office_normalization import normalize_office_freeform
from app.utils.scrape_helpers_async import (
    ensure_captcha,
    open_pdf_in_new_tab,
    handle_pdf_popup,
    random_human_delay,
    gentle_mouse_wiggle,
)

logger = logging.getLogger(__name__)

# Helper data and functions for scraping
# Not: Ofis normalizasyonu için merkezî kaynak kullanılmaktadır:
#  - app.utils.office_normalization.normalize_office_freeform



async def ensure_login(page: Page) -> None:
    """Otomatik login (OCR ile CAPTCHA çözme). Idempotent: zaten login ise hızla devam eder."""
    try:
        await page.goto("https://www.ticaretsicil.gov.tr/", wait_until="domcontentloaded")

        async def open_login_modal():
            try:
                await page.get_by_role("link", name=lambda n: n and "GİRİŞ" in n).click(timeout=10_000)
            except Exception:
                try:
                    await page.locator("a:has-text('GİRİŞ')").first.click()
                except Exception:
                    return False
            return True

        async def login_error_present() -> bool:
            # Önce verilen spesifik toast yapısını kontrol et
            try:
                toast = page.locator('div.toast.toast-error').first
                if await toast.count() > 0:
                    try:
                        msg = (await toast.locator('.toast-message').first.text_content()) or ""
                    except Exception:
                        msg = ""
                    if ("Giriş Bilgileri Hatalı" in msg) or ("Güvenlik Kodu Hatalı" in msg):
                        try:
                            # Kapat düğmesine bas (varsa)
                            close_btn = toast.locator('.toast-close-button').first
                            if await close_btn.count() > 0:
                                await close_btn.click()
                        except Exception:
                            pass
                        return True
            except Exception:
                pass

            # Genel hata toast/alert göstergeleri (fallback)
            selectors = [
                ".toast-error",
                "#toast-container .toast-error",
                ".alert-danger",
                ".swal2-popup.swal2-icon-error",
                ".validation-summary-errors",
            ]
            try:
                for sel in selectors:
                    loc = page.locator(sel)
                    if await loc.count() > 0:
                        try:
                            if await loc.first().is_visible():
                                return True
                        except Exception:
                            return True
            except Exception:
                return False
            return False

        async def logged_in() -> bool:
            # GİRİŞ linki kaybolduysa veya kullanıcı menüsü görünüyorsa giriş yapılmış kabul et
            try:
                if await page.locator("a:has-text('GİRİŞ')").count() == 0:
                    return True
            except Exception:
                pass
            # Alternatif bir kontrol daha eklenebilir
            return False

        # GİRİŞ modalini aç
        opened = await open_login_modal()
        if not opened:
            return
        await page.wait_for_selector("#LoginEmail", timeout=20_000)

        async def human_type(sel: str, text: str) -> None:
            try:
                await page.click(sel)
            except Exception:
                pass
            await random_human_delay(100, 220)
            try:
                await page.locator(sel).fill("")
            except Exception:
                pass
            await random_human_delay(100, 220)
            for ch in text:
                try:
                    await page.locator(sel).type(ch, delay=secrets.randbelow(120) + 30)
                except Exception:
                    break
                await random_human_delay(20, 80)

        if settings.SICIL_EMAIL and settings.SICIL_PASSWORD:
            await human_type("#LoginEmail", settings.SICIL_EMAIL)
            await random_human_delay()
            await human_type("#LoginSifre", settings.SICIL_PASSWORD)
            await random_human_delay()

        # Hatalı doğrulama kodu olasılığına karşı 3 denemeye kadar tekrar dene
        for _ in range(3):
            await ensure_captcha(page)
            try:
                await page.locator("button.c-btn-login").first.click()
            except Exception:
                try:
                    await page.get_by_role("button", name=lambda n: n and "GİRİŞ" in n).first.click()
                except Exception:
                    pass
            try:
                await page.wait_for_load_state("networkidle", timeout=10_000)
            except Exception:
                pass

            if await login_error_present():
                # Hata toast'u görüldü; sayfayı yenileyip yeniden dene
                await page.reload(wait_until="domcontentloaded")
                opened = await open_login_modal()
                if not opened:
                    return
                await page.wait_for_selector("#LoginEmail", timeout=20_000)
                if settings.SICIL_EMAIL and settings.SICIL_PASSWORD:
                    await page.fill("#LoginEmail", settings.SICIL_EMAIL)
                    await random_human_delay()
                    await page.fill("#LoginSifre", settings.SICIL_PASSWORD)
                    await random_human_delay()
                continue

            if await logged_in():
                break
    except Exception:
        # Login başarısız olsa da akış devam edebilir (sekme bazlı CAPTCHA çözümleri var)
        return


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
                
                # Tarayıcıyı görünür modda daha küçük pencerede aç (geliştirme için konforlu boyut)
                launch_args = [
                    "--no-sandbox",
                    "--disable-setuid-sandbox",
                    "--disable-dev-shm-usage",
                    "--disable-accelerated-2d-canvas",
                    "--disable-gpu",
                ]
                if not headless:
                    launch_args.append("--window-size=1280,800")
                
                self._browser = await self._playwright.chromium.launch(headless=headless, slow_mo=100, args=launch_args)

                # Oturum saklama/kullanma kaldırıldı; temiz bir context ile başla
                self._context = await self._browser.new_context(
                    ignore_https_errors=True,
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
                    viewport={"width": 1280, "height": 800}
                )
                
                self._context.on("close", self._handle_close)
                logger.info("Browser context launched successfully.")

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

    async def close_browser(self, cleanup: bool = False) -> Dict[str, str]:
        """Closes the browser context and shuts down Playwright. Optionally cleans up local artifacts."""
        async with self._lock:
            if self._save_task and not self._save_task.done():
                self._save_task.cancel()
                logger.info("Periodic save task cancelled.")

            if not self._browser or not self._browser.is_connected():
                msg = "Browser is not open or already closed."
                logger.warning(msg)
                return {"status": "not_open", "message": msg}

            # Oturum kaydetme kaldırıldı

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

            # Optional local cleanup of previous session artifacts inside project root
            if cleanup:
                try:
                    if not os.path.exists('/app/data/uploads'): os.makedirs('/app/data/uploads', exist_ok=True)
                    debug_dir = '/app/data/uploads'
                    # storage state file (legacy)
                    if os.path.exists(self._storage_state_path):
                        os.remove(self._storage_state_path)
                    # user data dir (legacy)
                    legacy_ud = os.path.join(settings.PROJECT_ROOT, ".playwright_user_data")
                    if os.path.isdir(legacy_ud):
                        shutil.rmtree(legacy_ud, ignore_errors=True)
                    # any dot-playwright leftovers in project root
                    for name in os.listdir(settings.PROJECT_ROOT):
                        if name.startswith(".playwright_"):
                            path = os.path.join(settings.PROJECT_ROOT, name)
                            try:
                                if os.path.isdir(path):
                                    shutil.rmtree(path, ignore_errors=True)
                                elif os.path.isfile(path):
                                    os.remove(path)
                            except Exception:
                                pass
                    logger.info("Local Playwright session/cache artifacts cleaned up.")
                except Exception:
                    logger.warning("Failed to clean some local artifacts. Proceeding anyway.")

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
        """Deprecated: session periodic save is disabled."""
        if self._save_task and not self._save_task.done():
            self._save_task.cancel()
            self._save_task = None
            logger.info("Periodic session saving has been stopped.")
        # No further action

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


async def start_enhanced_scraping_process(count: int, city: Optional[str] = None, mode: Optional[str] = 'normal'):
    """
    Fetches unscraped companies, scrapes their announcements, and saves them to the database.
    This function is intended for robust, production-like scraping.
    """
    logger.info(f"Starting scraping process: mode={mode}, city={city}, attempts/count={count}")
    # Session periodic save disabled; no-op
    db: Session = SessionLocal()
    page = await browser_manager.get_page()

    if not page:
        error_msg = "Could not get a page from the browser manager."
        logger.error(error_msg)
        scraping_state.set_error(error_msg)
        db.close()
        return

    try:
        # Otomatik login (gerekirse)
        await ensure_login(page)

        # City-fill modu: sayısal sicil boşluklarını doldurmak için ardışık denemeler
        if mode == 'city_fill' and city:
            from app.utils.office_normalization import normalize_office_freeform

            office_label = normalize_office_freeform(city)
            if not office_label:
                scraping_state.start(total_count=count)
                msg = f"CITY_FILL_ERROR: Verilen şehir normalize edilemedi: {city}"
                scraping_state.add_log(msg)
                logger.error(msg)
                return

            # Aday sicil numaralarını hazırla (gaps + max'tan itibaren)
            # İstanbul için en az 6 haneli (>=100000) kısıtını uygula
            min_threshold = 100000 if office_label == 'İSTANBUL' else 1
            candidates: List[int] = _compute_candidate_sicil_numbers(db, office_label, count, min_threshold=min_threshold)
            if not candidates:
                scraping_state.start(total_count=count)
                scraping_state.add_log("CITY_FILL_INFO: Aday sicil numarası üretilemedi.")
                return

            scraping_state.start(total_count=count)
            bucket_name = "gazette-pdfs"
            try:
                ensure_bucket(bucket_name)
                logger.info("Bucket '%s' hazır", bucket_name)
            except Exception as e:
                logger.error("Bucket kontrolü başarısız oldu: %s", e)
                raise e
            processed = 0
            for num in candidates:
                if scraping_state.should_stop:
                    scraping_state.add_log("STOP_SIGNAL_RECEIVED: Stopping task.")
                    break
                try:
                    found = await search_by_office_and_sicil(page, office_label, num)
                    if found:
                        scraping_state.add_log(f"CITY_FILL_FOUND: {office_label} #{num} için sonuç bulundu.")
                        # Minimal company oluştur/çek ve detaylı scrape yap
                        company = crud.company.get_or_create_minimal_by_sicil(db, office_label=office_label, sicil_no=str(num))
                        await scrape_company(page, db, company)
                    else:
                        scraping_state.add_log(f"CITY_FILL_EMPTY: {office_label} #{num} için sonuç yok. Tekrar denememek için işaretleniyor.")
                        # Boş sonuçta da tekrar denememek için minimal şirket kaydı oluştur ve scraped olarak işaretle
                        empty_company = crud.company.get_or_create_minimal_by_sicil(db, office_label=office_label, sicil_no=str(num))
                        try:
                            crud.company.mark_as_scraped(db, company_id=empty_company.id)
                        except Exception:
                            pass
                except Exception as e:
                    scraping_state.add_log(f"CITY_FILL_ERROR: {office_label} #{num} denemesinde hata: {e}")
                finally:
                    processed += 1
                    scraping_state.update_progress(processed)
                    if processed >= count:
                        break
            return

        # Normal mod: mevcut akış
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
            ensure_bucket(bucket_name)
            logger.info("Bucket '%s' hazır", bucket_name)
        except Exception as e:
            logger.error("Bucket kontrolü başarısız oldu: %s", e)
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
        # Close browser and cleanup project-local artifacts
        try:
            await browser_manager.close_browser(cleanup=True)
        except Exception:
            logger.warning("Failed to close browser during finalization.")


def _compute_candidate_sicil_numbers(db: Session, office_label: str, count: int, min_threshold: int = 1) -> List[int]:
    """Verilen ofis için DB'deki sayısal sicil_no'ları toplayıp aralıklardaki boşlukları (gaps)
    üretir; gerekirse en büyük numaradan itibaren yukarı doğru tamamlayarak toplam 'count' aday üretir.
    """
    try:
        # Ofis eşleşmesi: öncelik sicil_office_code, yoksa sicil_mudurluk ilk kelime eşleşmesi
        from app.models.company import Company
        q = (
            db.query(Company.sicil_no, Company.sicil_office_code, Company.sicil_mudurluk)
            .filter(
                (Company.sicil_office_code == office_label) |
                (Company.sicil_mudurluk.ilike(f"{office_label}%"))
            )
        )
        rows = q.all()
        nums: List[int] = []
        for sicil_no, _, _ in rows:
            try:
                s = (sicil_no or "").strip()
                if not s:
                    continue
                # sadece tam sayısal sicil no'ları al
                if s.isdigit():
                    val = int(s)
                    if val >= max(1, int(min_threshold)):
                        nums.append(val)
            except Exception:
                continue
        if not nums:
            # hiç veri yoksa 1'den başlayarak count kadar üret
            start_n = max(1, int(min_threshold))
            return list(range(start_n, start_n + max(1, count)))[:count]
        nums = sorted(set(nums))
        candidates: List[int] = []
        # Başlangıç boşluğu: min_threshold .. ilk mevcut-1
        start_n = max(1, int(min_threshold))
        first = nums[0]
        if first > start_n:
            for n in range(start_n, first):
                candidates.append(n)
                if len(candidates) >= count:
                    return candidates[:count]
        # Aralıklardaki boşlukları sayac dolana kadar doldur
        prev = nums[0]
        for current in nums[1:]:
            gap_start = prev + 1
            gap_end = current - 1
            if gap_end >= gap_start:
                for n in range(gap_start, gap_end + 1):
                    candidates.append(n)
                    if len(candidates) >= count:
                        return candidates[:count]
            prev = current
        # Gaps yetmezse max'tan itibaren devam
        max_n = nums[-1]
        n = max_n + 1
        while len(candidates) < count:
            candidates.append(n)
            n += 1
        return candidates[:count]
    except Exception:
        logger.exception("Failed to compute candidate sicil numbers.")
        return []


async def search_by_office_and_sicil(page: Page, office_label: str, sicil_no: int) -> bool:
    """Verilen ofis ve sicil numarası için ilan araması yapar. Sonuç varsa True, yoksa False döner.
    CAPTCHA ve ufak gecikmeler mevcut yardımcılarla yönetilir.
    """
    try:
        await page.goto("https://www.ticaretsicil.gov.tr/view/hizlierisim/ilangoruntuleme.php", wait_until="domcontentloaded")
        await ensure_captcha(page)
        await page.select_option('select#SicilMudurluguId', label=office_label)
        await random_human_delay(80, 180)
        await page.fill('input#TicSicNo', str(sicil_no))
        await random_human_delay(80, 180)
        await page.click('button[data-message="İlan Ara"]')
        try:
            await page.wait_for_selector('table#tblIlanGoruntuleme tbody tr', timeout=15000)
        except PlaywrightTimeoutError:
            return False

        rows = await page.query_selector_all('table#tblIlanGoruntuleme tbody tr')
        if not rows:
            return False
        first_text = (await rows[0].inner_text()).strip().upper()
        if "EŞLEŞEN KAYIT BULUNAMADI" in first_text:
            return False
        return True
    except Exception:
        # Ağır hatalarda False dön, üst katmanda loglanır
        return False





async def scrape_company(page: Page, db: Session, company):
    """
    Scrapes a single company's announcements, handling pagination, silent PDF downloads,
    and database operations with robust error handling.
    """
    scraping_state.add_log(f"PROCESSING_COMPANY: Start processing '{company.unvan}' (Sicil No: {company.sicil_no}).")
    try:
        # Öncelik: composite key'de kullanılan normalize alan
        office_value = getattr(company, "sicil_office_code", None) or getattr(company, "sicil_mudurluk", None)
        office_label = normalize_office_freeform(office_value)
        if not office_label:
            scraping_state.add_log(f"COMPANY_ERROR: Could not normalize office for '{company.unvan}'. Raw: {office_value}")
            crud.company.mark_as_scraped(db=db, company_id=company.id)  # Retry önlemek için işaretle
            return

        await page.goto("https://www.ticaretsicil.gov.tr/view/hizlierisim/ilangoruntuleme.php", wait_until="domcontentloaded")
        await page.select_option('select#SicilMudurluguId', label=office_label)
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
                    should_upload_pdf = publication_date >= date(2021, 1, 1)
                    newspaper_text = await cells[7].inner_text()
                    if not should_upload_pdf:
                        newspaper_text = "pre-2021"

                    pdf_link_element = await cells[7].query_selector('a')

                    if should_upload_pdf and pdf_link_element:
                        pdf_href = await pdf_link_element.get_attribute('href')
                        if pdf_href:
                            try:
                                # Önce sayfadaki olası CAPTCHA'yı çöz (overlay/pop-up engel olmasın)
                                await ensure_captcha(page)
                                # İnsanî şekilde yeni sekme aç
                                new_page = await open_pdf_in_new_tab(page, pdf_href)
                                if not new_page:
                                    scraping_state.add_log(f"PDF_WARN: Yeni sekme açılamadı. href={pdf_href}")
                                    raise RuntimeError("Yeni sekme açılamadı.")

                                content, captcha_solved = await handle_pdf_popup(page, new_page)
                                # Sekme handle_pdf_popup içinde kapanır ya da burada kapatılır
                                try:
                                    if not new_page.is_closed():
                                        await new_page.close()
                                except Exception:
                                    pass

                                if content is None and captcha_solved:
                                    # Aynı linki bir kez daha dene
                                    await random_human_delay(300, 800)
                                    await ensure_captcha(page)
                                    retry_page = await open_pdf_in_new_tab(page, pdf_href)
                                    if retry_page:
                                        try:
                                            content, _ = await handle_pdf_popup(page, retry_page)
                                        finally:
                                            try:
                                                if not retry_page.is_closed():
                                                    await retry_page.close()
                                            except Exception:
                                                pass

                                if content:
                                    file_name = f"announcement_{company.id}_{uuid.uuid4()}.pdf"
                                    bucket_name = "gazette-pdfs"
                                    upload_bytes(
                                        bucket_name=bucket_name,
                                        object_name=file_name,
                                        data=content,
                                        content_type="application/pdf",
                                    )
                                    pdf_url = get_presigned_url(bucket_name, file_name, expires=24 * 3600)
                                    scraping_state.add_log(f"PDF_SUCCESS: '{title}' için PDF yüklendi (MinIO).")
                                else:
                                    scraping_state.add_log(f"PDF_SKIP: '{title}' için PDF alınamadı.")

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
                        newspaper_name=newspaper_text, # mark pre-2021 when skipping upload
                        pdf_url=pdf_url
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
