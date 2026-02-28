import asyncio
from typing import Optional
from playwright.async_api import async_playwright
from sqlalchemy.orm import Session
from app import crud, models
from app.utils.office_normalization import normalize_office_freeform, VALID_SICIL_OFFICES

def normalize_city_name(db_city_name: str) -> Optional[str]:
    if not db_city_name:
        return None
    official = normalize_office_freeform(db_city_name)
    if official:
        return official
    print(f"[UYARI] Eşleştirilemeyen şehir adı: {db_city_name}")
    return None

async def scrape_company_by_id(db: Session, company_id: str) -> dict:
    company = crud.company.get(db, id=company_id)
    if not company:
        return {"status": "error", "message": "Company not found"}

    if company.scraped_at:
        return {"status": "error", "message": "Company already scraped"}

    normalized_city = normalize_city_name(company.sicil_mudurluk or "")
    if not normalized_city:
        return {"status": "error", "message": f"City name could not be normalized: {company.sicil_mudurluk}"}

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        try:
            await page.goto("https://www.ticaretsicil.gov.tr/view/hizlierisim/ilangoruntuleme.php")
            
            await page.select_option('select[name="SicilMudurluguId"]', label=normalized_city)
            await page.fill('input[name="SicilNo"]', company.sicil_no)
            
            await page.click('button:has-text("Sorgula")')
            
            # TODO: Gerçek sonuçları beklemek ve işlemek için daha sağlam bir mekanizma eklenmeli.
            # Örnek: PDF linkini bul, indir ve veritabanını güncelle.
            await page.wait_for_timeout(5000) # Simulating processing time

            # Başarı durumunda veritabanını güncelle
            crud.company.update_scraped_status(db, company_id=company.id)

            await browser.close()
            return {"status": "success", "message": f"Company {company.firma_unvani} scraped successfully."}
        except Exception as e:
            await browser.close()
            return {"status": "error", "message": str(e)}
