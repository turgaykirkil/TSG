from __future__ import annotations

import io
import sys
import time
from pathlib import Path
from typing import Optional

from playwright.sync_api import sync_playwright
from PIL import Image, ImageFilter  # type: ignore
import pytesseract  # type: ignore

# Backend kökünü sys.path'e ekle ki 'app.core.config' importu çalışsın
import sys
import os as _os
_BACKEND_ROOT = _os.path.abspath(_os.path.join(_os.path.dirname(__file__), ".."))
if _BACKEND_ROOT not in sys.path:
    sys.path.insert(0, _BACKEND_ROOT)

from app.core.config import settings

SITE = "https://www.ticaretsicil.gov.tr/"
EMAIL = settings.SICIL_EMAIL
PASSWORD = settings.SICIL_PASSWORD


def preprocess(img: Image.Image) -> Image.Image:
    # Gri ton, ölçek büyütme, hafif bulanıklaştırma ve eşikleme
    g = img.convert("L")
    # 2x büyütme
    w, h = g.size
    g = g.resize((w * 2, h * 2), resample=Image.NEAREST)
    # hafif median blur, gürültü azaltma
    g = g.filter(ImageFilter.MedianFilter(size=3))
    # threshold
    g = g.point(lambda p: 255 if p > 150 else 0)
    return g


def ocr_from_bytes(img_bytes: bytes) -> Optional[str]:
    try:
        img = Image.open(io.BytesIO(img_bytes))
        img = preprocess(img)
        txt = pytesseract.image_to_string(
            img,
            config="--oem 3 --psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
        )
        txt = (txt or "").strip().replace(" ", "")
        if 3 <= len(txt) <= 6:
            return txt
    except Exception as e:
        print(f"[WARN] OCR failed: {e}")
    return None


def main() -> int:
    with sync_playwright() as p:
        # Tercihen webkit; yoksa chromium fallback
        browser_type = p.webkit
        try:
            browser = browser_type.launch(headless=False)
        except Exception as e:
            print(f"[WARN] WebKit launch failed: {e}. Falling back to Chromium.")
            browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto(SITE, wait_until="domcontentloaded")

        # Login modalını aç (link adı içinde GİRİŞ geçen bir link)
        try:
            page.get_by_role("link", name=lambda n: n and "GİRİŞ" in n).click(timeout=10_000)
        except Exception:
            # Alternatif: sayfadaki GİRİŞ linklerinden ilkini tıkla
            page.locator("a:has-text('GİRİŞ')").first.click()

        # Form alanlarını doldur
        page.fill("#LoginEmail", EMAIL)
        page.fill("#LoginSifre", PASSWORD)

        # Captcha görüntüsünü yakala (element screenshot)
        page.wait_for_selector("#CaptchaImg", timeout=20_000)
        el = page.locator("#CaptchaImg").first
        el.wait_for(state="visible", timeout=10_000)
        # İlk deneme
        shot = el.screenshot(type="png")
        code = ocr_from_bytes(shot) or ""
        # Boş geldiyse bir kez daha yenilemeyi dene: görsele tıkla ve src değişimini bekle
        if not code:
            try:
                old_src = el.get_attribute("src")
                el.click()
                page.wait_for_function(
                    "(el, oldSrc) => el.getAttribute('src') !== oldSrc",
                    arg=el,
                    polling=200,
                    timeout=5_000,
                    oldSrc=old_src,
                )
                shot = el.screenshot(type="png")
                code = ocr_from_bytes(shot) or ""
            except Exception:
                pass
        print(f"[INFO] OCR -> '{code}'")

        # Captcha alanına yaz
        page.fill("#Captcha", code)

        # Girişe BASMA — kullanıcı görsün diye bekle
        print("[INFO] OCR sonucu #Captcha alanına yazıldı. İnceleyebilmen için duraklatıyorum.")
        page.pause()  # Inspector açılır

        # Kapat
        browser.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
