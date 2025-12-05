import asyncio
import logging
import os
import traceback
import uuid
from datetime import datetime

from celery import Task
from playwright.async_api import async_playwright
from playwright._impl._errors import TargetClosedError

from app.core.celery_app import celery_app
from app.core.storage import ensure_bucket, upload_bytes, get_presigned_url
from app.utils.text_utils import normalize_city, CITY_VALUE_MAP
from app.utils.scrape_helpers_async import ensure_captcha  # CAPTCHA otomasyonu

logger = logging.getLogger(__name__)



@celery_app.task(bind=True)
def run_scraping_task(self: Task, count: int):
    from app import crud
    from app.db.session import SessionLocal
    """
    Celery task to perform the scraping process.
    """
    browser, context = None, None
    db = None

    def log_and_update_state(message: str, state: str = 'PROGRESS'):
        logger.info(message)
        self.update_state(state=state, meta={'status': message})

    try:
        db = SessionLocal()
        log_and_update_state("DB_SESSION_CREATED: Veritabanı oturumu oluşturuldu.")

        companies_to_scrape = crud.company.get_unscraped(db, limit=count)
        log_and_update_state(f"DB_FETCH_SUCCESS: {len(companies_to_scrape)} şirket bulundu.")

        if not companies_to_scrape:
            log_and_update_state("SCRAPING_INFO: Kazınacak yeni şirket bulunamadı.", state='SUCCESS')
            return {'status': 'No new companies to scrape.'}

        async def scrape():
            nonlocal browser, context
            async with async_playwright() as p:
                log_and_update_state("PLAYWRIGHT_INIT: Playwright başlatılıyor...")
                
                project_backend_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
                user_data_dir = os.path.join(project_backend_root, ".playwright_webkit_user_data")
                os.makedirs(user_data_dir, exist_ok=True)

                context = await p.webkit.launch_persistent_context(
                    user_data_dir,
                    headless=True,
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
                )
                browser = context.browser
                log_and_update_state("PLAYWRIGHT_SUCCESS: WebKit tarayıcı ve context hazır.")
                page = await context.new_page()
                log_and_update_state("PAGE_OPENED: Yeni tarayıcı sayfası açıldı.")

                log_and_update_state("NAVIGATING: İlan görüntüleme sayfasına gidiliyor...")
                await page.goto("https://www.ticaretsicil.gov.tr/view/hizlierisim/ilangoruntuleme.php", wait_until="domcontentloaded", timeout=60000)
                log_and_update_state("NAVIGATION_SUCCESS: Sayfa başarıyla yüklendi.")
                # İlk ekranda olası CAPTCHA'yı çöz
                try:
                    await ensure_captcha(page)
                except Exception:
                    pass



                for i, company in enumerate(companies_to_scrape):
                    log_and_update_state(f"PROCESSING_COMPANY [{i+1}/{len(companies_to_scrape)}]: {company.title}")
                    try:
                        # 1. Formu doldurma ve gönderme
                        normalized_city = normalize_city(company.sicil_mudurluk)
                        city_value = CITY_VALUE_MAP.get(normalized_city)
                        if not city_value or not company.trade_registry_number:
                            log_and_update_state(f"SKIPPING_COMPANY: Eksik bilgi: Şehir='{company.sicil_mudurluk}', SicilNo='{company.trade_registry_number}'")
                            continue

                        await page.select_option('select[name="SicilMudurluguId"]', value=city_value, timeout=30000)
                        await page.fill('input[name="SicilNo"]', company.trade_registry_number)
                        # Form submit öncesi olası CAPTCHA
                        try:
                            await ensure_captcha(page)
                        except Exception:
                            pass
                        await page.click('button:has-text("Sorgula")')
                        await page.wait_for_load_state('networkidle', timeout=30000)
                        # Sonrasında tekrar kontrol (bazı durumlarda submit sonrası da CAPTCHA çıkabiliyor)
                        try:
                            await ensure_captcha(page)
                        except Exception:
                            pass
                        log_and_update_state(f"FORM_SUBMITTED: {company.title} için form gönderildi.")

                        # 2. Sonuçları işleme (sayfa sayfa)
                        page_number = 1
                        while True:
                            log_and_update_state(f"PROCESSING_PAGE: Sayfa {page_number} işleniyor...")
                            rows = await page.query_selector_all('table.table-bordered > tbody > tr')
                            if not rows or 'kayıt bulunamadı' in (await rows[0].inner_text()):
                                log_and_update_state("INFO: Bu şirket için yeni ilan bulunamadı.")
                                break
                            
                            for row in rows:
                                cells = await row.query_selector_all('td')
                                if len(cells) < 8: continue

                                data = {
                                    'trade_registry_name': (await cells[0].inner_text()).strip(),
                                    'trade_registry_number': (await cells[1].inner_text()).strip(),
                                    'title': (await cells[2].inner_text()).strip(),
                                    'publication_date_str': (await cells[3].inner_text()).strip(),
                                    'issue_number': int((await cells[4].inner_text()).strip() or 0),
                                    'page_number': int((await cells[5].inner_text()).strip() or 0),
                                    'announcement_type': (await cells[6].inner_text()).strip(),
                                }
                                try:
                                    data['publication_date'] = datetime.strptime(data['publication_date_str'], '%d.%m.%Y').date()
                                except (ValueError, TypeError): data['publication_date'] = None

                                pdf_url = None
                                pdf_link = await cells[7].query_selector('a')
                                if pdf_link:
                                    try:
                                        # PDF bağlantısına tıklamadan önce CAPTCHA kontrolü
                                        try:
                                            await ensure_captcha(page)
                                        except Exception:
                                            pass
                                        async with page.context.expect_page(timeout=60000) as new_page_info:
                                            await pdf_link.click()
                                        new_page = await new_page_info.value
                                        await new_page.wait_for_load_state('domcontentloaded', timeout=60000)
                                        # Popup sayfasında da CAPTCHA kontrolü yap
                                        try:
                                            await ensure_captcha(new_page)
                                        except Exception:
                                            pass

                                        pdf_content = await new_page.pdf(format='A4')
                                        pdf_name = f"gazette_{uuid.uuid4()}.pdf"
                                        storage_path = f"gazette_pdfs/{company.id}/{pdf_name}"

                                        bucket = "company-gazettes"
                                        ensure_bucket(bucket)
                                        upload_bytes(
                                            bucket_name=bucket,
                                            object_name=storage_path,
                                            data=pdf_content,
                                            content_type="application/pdf",
                                        )
                                        pdf_url = get_presigned_url(bucket, storage_path, expires=24 * 3600)
                                        log_and_update_state(f"PDF_UPLOADED: {pdf_name} MinIO'ya yüklendi.")
                                        await new_page.close()
                                    except Exception as pdf_e:
                                        logger.error(f"PDF_ERROR: PDF işlenirken hata: {pdf_e}")

                                crud.company.create_scraped_announcement(
                                    db=db, company_id=company.id, data=data, pdf_url=pdf_url
                                )

                            next_page_link = await page.query_selector('li.next:not(.disabled) > a')
                            if not next_page_link:
                                log_and_update_state("INFO: Son sayfaya ulaşıldı.")
                                break
                            
                            # Sayfa değişmeden önce bir kontrol daha
                            try:
                                await ensure_captcha(page)
                            except Exception:
                                pass
                            await next_page_link.click()
                            await page.wait_for_load_state('networkidle', timeout=30000)
                            page_number += 1

                        crud.company.mark_as_scraped(db=db, company_id=company.id)
                        log_and_update_state(f"COMPANY_SCRAPED_SUCCESS: {company.title} şirketi tamamen kazındı.")

                    except Exception as e:
                        error_msg = f"COMPANY_PROCESS_ERROR: {company.title} işlenirken hata oluştu: {traceback.format_exc()}"
                        logger.error(error_msg)

                        # Hata ayıklama için ekran görüntüsü ve HTML içeriğini kaydet
                        debug_dir = os.path.join(project_backend_root, "debug_output")
                        os.makedirs(debug_dir, exist_ok=True)
                        screenshot_path = os.path.join(debug_dir, f"error_screenshot_{company.id}.png")
                        html_path = os.path.join(debug_dir, f"error_page_{company.id}.html")
                        
                        log_and_update_state(f"DEBUG_INFO: Hata anında sayfanın ekran görüntüsü ve HTML'i kaydediliyor...")
                        try:
                            await page.screenshot(path=screenshot_path, full_page=True)
                            with open(html_path, "w", encoding="utf-8") as f:
                                f.write(await page.content())
                            log_and_update_state(f"DEBUG_FILES_SAVED: Ekran görüntüsü: {screenshot_path}, HTML: {html_path}")
                        except Exception as debug_e:
                            log_and_update_state(f"DEBUG_FILES_ERROR: Hata ayıklama dosyaları kaydedilemedi: {debug_e}")
                        # Continue with the next company
                        continue

        asyncio.run(scrape())
        log_and_update_state("SCRAPING_COMPLETE: Tüm şirketlerin işlemi tamamlandı.", state='SUCCESS')
        return {'status': 'Scraping completed successfully.'}

    except Exception as e:
        error_message = f"PROCESS_ERROR: Scraping sürecinde genel bir hata oluştu: {traceback.format_exc()}"
        logger.error(error_message)
        self.update_state(state='FAILURE', meta={'status': error_message})
        # Re-raise the exception to let Celery know the task failed
        raise
    finally:
        logger.info("CLEANUP: Görev temizleme bloğuna giriliyor.")
        if 'context' in locals() and context:
            try:
                # Create a small async function to close the context and run it.
                async def close_context_safely():
                    if not context.is_closed():
                        await context.close()
                asyncio.run(close_context_safely())
                logger.info("CLEANUP: Tarayıcı context'i kapatıldı.")
            except Exception as e:
                # Log errors, especially if an event loop is already running.
                logger.error(f"CLEANUP_ERROR: Tarayıcı context'i kapatılırken hata: {e}")
        if db:
            db.close()
            logger.info("CLEANUP: Veritabanı bağlantısı kapatıldı.")
