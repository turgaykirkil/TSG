import asyncio
import re
from playwright.async_api import async_playwright, Page
from app.db.session import SessionLocal
from app.models.company import Company
from sqlalchemy import text

# Ticaret Sicil Gazetesi sitesindeki şehir/ilçe adları (kullanıcının sağladığı HTML'den alınmıştır)
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
    Örnek: 'İZMİR TİCARET SİCİLİ MÜDÜRLÜĞÜ' -> 'İZMİR'
    """
    if not db_city_name:
        return None
    
    # Büyük harfe çevir ve başında/sonunda boşlukları kaldır
    normalized = db_city_name.upper().strip()
    
    # Önce tam eşleşme ara
    if normalized in VALID_CITIES:
        return normalized
    
    # Tam eşleşme yoksa, geçerli şehir listesindeki her bir şehir adının
    # veritabanı kaydında geçip geçmediğini kontrol et.
    for city in VALID_CITIES:
        if city in normalized:
            return city
            
    # 'KONYA EREĞLİ' gibi özel durumlar için kelime bazlı kontrol
    # 'EREĞLİ' kelimesi tek başına 'KONYA EREĞLİ' ile karışmasın diye
    if 'EREĞLİ' in normalized and 'KONYA' in normalized:
        return 'KONYA EREĞLİ'
    if 'EREĞLİ' in normalized and 'KARADENİZ' in normalized:
        return 'KARADENİZ EREĞLİ'

    print(f"[UYARI] Eşleştirilemeyen şehir adı: {db_city_name}")
    return None

async def start_scraping_process(count: int):
    """
    Ana scraping sürecini yönetir.
    """
    print(f"{count} adet firma için scraping işlemi başlatılıyor...")
    db = SessionLocal()
    try:
        # Scrape edilmemiş şirketleri veritabanından çek
        query = text("SELECT * FROM companies WHERE scraped_at IS NULL ORDER BY id ASC LIMIT :count")
        companies_to_scrape = db.execute(query, {'count': count}).fetchall()
        
        if not companies_to_scrape:
            print("Scrape edilecek yeni firma bulunamadı.")
            return

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False) # Geliştirme için False, deploy için True
            page = await browser.new_page()
            await page.goto("https://www.ticaretsicil.gov.tr/view/hizlierisim/ilangoruntuleme.php")
            print("Tarayıcı açıldı ve siteye gidildi.")

            for company_data in companies_to_scrape:
                company = Company(**company_data._asdict())
                print(f"İşleniyor: {company.title} ({company.trade_registry_name})")

                normalized_city = normalize_city_name(company.trade_registry_name)
                if not normalized_city:
                    print(f"Şehir adı normalize edilemediği için atlanıyor: {company.trade_registry_name}")
                    continue

                try:
                    # Formu doldur
                    await page.select_option('select[name="SicilMudurluguId"]', label=normalized_city)
                    await page.fill('input[name="SicilNo"]', company.trade_registry_number)
                    
                    # Sorgula butonuna tıkla
                    await page.click('button:has-text("Sorgula")')
                    
                    # Sonuçların yüklenmesini bekle (örneğin, bir sonuç tablosu veya mesajı)
                    # Bu kısım, sitenin gerçek davranışına göre ayarlanmalıdır.
                    await page.wait_for_selector('#embed-pdf-container', timeout=10000) # Örnek bir selector
                    
                    print(f"Başarılı: {company.title}")
                    # TODO: PDF'i indir veya veriyi işle, scraped_at güncelle

                except Exception as e:
                    print(f"[HATA] {company.title} işlenirken hata oluştu: {e}")
                    # TODO: Hata durumunu veritabanına kaydet
                
                await asyncio.sleep(2) # İstekler arası bekleme

            await browser.close()
    finally:
        db.close()

# Bu dosya doğrudan çalıştırıldığında test amaçlıdır.
if __name__ == "__main__":
    # Test için örnek bir çalıştırma
    asyncio.run(start_scraping_process(count=5))

