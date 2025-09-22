from __future__ import annotations

import os
import pathlib
import time
import pytest
from playwright.sync_api import Page

from .utils.scrape_helpers import (
    gentle_mouse_wiggle,
    random_human_delay,
    ensure_captcha,
    extract_pdf_url,
    save_pdf,
)

TARGET_URL = os.getenv("SCRAPE_URL", "https://www.ticaretsicil.gov.tr/")

pytestmark = pytest.mark.playwright


@pytest.mark.skipif(not TARGET_URL, reason="SCRAPE_URL is not set")
@pytest.mark.parametrize("multi", [False])
def test_kullanici_ilan_pdf_indir(page: Page, multi: bool):
    # Başlangıç
    page.goto(TARGET_URL, wait_until="domcontentloaded", timeout=60_000)

    # Kullanıcı tüm giriş ve arama adımlarını manuel yapacaksa pause ile bırak
    if os.getenv("SCRAPE_DEBUG_PAUSE", "0") == "1":
        # Inspector açılır, kullanıcı devam ettikten sonra test sürer
        page.pause()

    # İnsan benzeri davranış
    gentle_mouse_wiggle(page)
    random_human_delay(300, 900)

    # CAPTCHA varsa çözüm moduna gir (manuel/otomatik opsiyon)
    ensure_captcha(page)

    # Kullanıcı PDF viewer sayfasına geçtiğinde gömülü viewer/iframe/objeyi bekleyelim (maks 180 sn)
    selector_any = (
        'embed[type="application/x-google-chrome-pdf"][original-url], '
        'iframe[src*="viewer"], '
        'embed[type="application/pdf"], '
        'object[type="application/pdf"], '
        'iframe[src$=".pdf"], '
        'embed[src$=".pdf"]'
    )
    try:
        page.wait_for_selector(selector_any, timeout=180_000)
    except Exception:
        pass

    # Olası yeni CAPTCHA için tekrar kontrol
    ensure_captcha(page)

    # PDF URL tespiti (embed/pdf.js/chrome-viewer)
    pdf_url = extract_pdf_url(page)
    assert pdf_url, "PDF URL bulunamadı. Lütfen ilan detay sayfasında PDF viewer'ın yüklendiğini doğrulayın."

    # Dosyaya kaydet
    # URL'den ad çıkarımı
    suggested = None
    try:
        from urllib.parse import urlparse

        last = pathlib.Path(urlparse(pdf_url).path).name
        if last.lower().endswith(".pdf"):
            suggested = last
    except Exception:
        pass

    out_path = save_pdf(page, pdf_url, suggested_name=suggested)
    print(f"PDF kaydedildi: {out_path}")

    # İkinci ilanı da indirmek isterseniz SCRAPE_MULTI=1 ve tekrar pause ile kullanıcıya bırakın
    if os.getenv("SCRAPE_MULTI", "0") == "1":
        page.pause()
        ensure_captcha(page)
        pdf_url2 = extract_pdf_url(page)
        assert pdf_url2, "2. ilan için PDF URL bulunamadı."
        out_path2 = save_pdf(page, pdf_url2)
        print(f"PDF kaydedildi: {out_path2}")
