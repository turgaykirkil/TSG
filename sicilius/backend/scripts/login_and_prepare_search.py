from __future__ import annotations

import io
import sys
from typing import Optional

from PIL import Image, ImageFilter  # type: ignore
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
import pytesseract  # type: ignore

SITE = "https://www.ticaretsicil.gov.tr/"
EMAIL = "turgaykirkil@gmail.com"
PASSWORD = "29769000"
MAX_TRIES = 3


def preprocess(img: Image.Image) -> Image.Image:
    g = img.convert("L")
    w, h = g.size
    g = g.resize((w * 2, h * 2), resample=Image.NEAREST)
    g = g.filter(ImageFilter.MedianFilter(size=3))
    g = g.point(lambda p: 255 if p > 150 else 0)
    return g


def ocr_from_bytes(png_bytes: bytes) -> Optional[str]:
    try:
        img = Image.open(io.BytesIO(png_bytes))
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


def open_login_modal(page):
    # Login modalını açmaya çalış
    try:
        page.get_by_role("link", name=lambda n: n and "GİRİŞ" in n).click(timeout=10_000)
    except Exception:
        page.locator("a:has-text('GİRİŞ')").first.click()
    page.wait_for_selector("#LoginEmail", timeout=20_000)


def fill_login_form(page, email: str, password: str) -> None:
    page.fill("#LoginEmail", email)
    page.fill("#LoginSifre", password)


def solve_and_fill_captcha(page) -> str:
    page.wait_for_selector("#CaptchaImg", timeout=20_000)
    img_el = page.locator("#CaptchaImg").first
    img_el.wait_for(state="visible", timeout=10_000)

    # İlk deneme
    shot = img_el.screenshot(type="png")
    code = ocr_from_bytes(shot) or ""
    if not code:
        # Bir kez yenilemeyi dene
        try:
            old_src = img_el.get_attribute("src")
            img_el.click()
            page.wait_for_function(
                "(el, oldSrc) => el.getAttribute('src') !== oldSrc",
                arg=img_el,
                polling=200,
                timeout=5_000,
                oldSrc=old_src,
            )
            shot = img_el.screenshot(type="png")
            code = ocr_from_bytes(shot) or ""
        except Exception:
            pass
    page.fill("#Captcha", code)
    print(f"[INFO] OCR code -> '{code}'")
    return code


def try_login_once(page) -> bool:
    open_login_modal(page)
    fill_login_form(page, EMAIL, PASSWORD)
    solve_and_fill_captcha(page)

    # GİRİŞ tuşuna bas
    try:
        page.locator("button.c-btn-login").first.click()
    except Exception:
        page.get_by_role("button", name=lambda n: n and "GİRİŞ" in n).first.click()

    # Başarı kontrol (login sonrası arama formu elementleri görünmeli)
    try:
        page.wait_for_selector("#SicilMudurluguId", timeout=10_000)
        return True
    except PlaywrightTimeout:
        return False


def main() -> int:
    with sync_playwright() as p:
        # WebKit tercih et; olmazsa Chromium
        try:
            browser = p.webkit.launch(headless=False)
        except Exception as e:
            print(f"[WARN] WebKit launch failed: {e}. Falling back to Chromium.")
            browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto(SITE, wait_until="domcontentloaded")

        success = False
        for i in range(1, MAX_TRIES + 1):
            print(f"[INFO] Login denemesi {i}/{MAX_TRIES}")
            if i > 1:
                # Sayfayı yenileyip tekrar dene
                page.reload(wait_until="domcontentloaded")
            success = try_login_once(page)
            if success:
                break
        if not success:
            print("[ERR] Login başarısız. OCR hatalı olabilir. İnceleme için duraklatıyorum.")
            page.pause()
            browser.close()
            return 1

        print("[INFO] Login başarılı. Arama formu hazırlanıyor…")
        # Ankara seç ve firma adına PARS GLOBAL yaz
        page.select_option("#SicilMudurluguId", value="18")  # ANKARA
        page.fill("#TicaretUnvani", "Pars Global")

        print("[INFO] Ankara seçildi ve 'PARS GLOBAL' yazıldı. İnceleyebilmen için duraklatıyorum.")
        page.pause()

        browser.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
