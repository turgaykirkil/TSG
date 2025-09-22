from __future__ import annotations

import os
import time
import math
import pathlib
from typing import Optional

from playwright.sync_api import Page

# Optional imports for CAPTCHA OCR/LLM
try:
    import pytesseract  # type: ignore
    from PIL import Image  # type: ignore
except Exception:  # pragma: no cover
    pytesseract = None  # type: ignore
    Image = None  # type: ignore

try:
    import ollama  # type: ignore
except Exception:  # pragma: no cover
    ollama = None  # type: ignore


def random_human_delay(min_ms: int = 300, max_ms: int = 1200) -> None:
    ms = int(math.floor(min_ms + (max_ms - min_ms) * os.urandom(1)[0] / 255.0))
    time.sleep(ms / 1000.0)


def gentle_mouse_wiggle(page: Page) -> None:
    size = page.viewport_size or {"width": 1200, "height": 800}
    width, height = size["width"], size["height"]
    start_x = int(width * 0.2 + (width * 0.6) * (os.urandom(1)[0] / 255.0))
    start_y = int(height * 0.2 + (height * 0.6) * (os.urandom(1)[0] / 255.0))
    page.mouse.move(start_x, start_y, steps=8)
    random_human_delay(150, 400)
    page.mouse.move(start_x + 20, start_y + 10, steps=6)
    random_human_delay(100, 300)


def extract_pdf_url(page: Page) -> Optional[str]:
    # 1) Chrome built-in PDF viewer <embed type="application/x-google-chrome-pdf" original-url="...">
    embed_chrome = page.locator('embed[type="application/x-google-chrome-pdf"][original-url]')
    if embed_chrome.count() > 0:
        original = embed_chrome.first.get_attribute("original-url")
        if original:
            return str(page.evaluate("(u) => new URL(u, location.href).toString()", original))

    # 2) pdf.js viewer
    iframe_viewer = page.locator('iframe[src*="viewer"]')
    if iframe_viewer.count() > 0:
        src = iframe_viewer.first.get_attribute("src")
        if src:
            abs_url = str(page.evaluate("(s) => new URL(s, location.href).toString()", src))
            from urllib.parse import urlparse, parse_qs, unquote

            parsed = urlparse(abs_url)
            q = parse_qs(parsed.query)
            file_param = q.get("file", [None])[0]
            if file_param:
                try:
                    decoded = unquote(file_param)
                except Exception:
                    decoded = file_param
                return str(page.evaluate("(u) => new URL(u, location.href).toString()", decoded))

    # 3) Generic PDF embeds
    selectors = [
        'embed[type="application/pdf"]',
        'object[type="application/pdf"]',
        'iframe[src$=".pdf"]',
        'embed[src$=".pdf"]',
    ]
    for sel in selectors:
        el = page.locator(sel)
        if el.count() > 0:
            src = el.first.get_attribute("src") or el.first.get_attribute("data")
            if src:
                return str(page.evaluate("(u) => new URL(u, location.href).toString()", src))

    return None


def _solve_captcha_tesseract(image_path: str) -> Optional[str]:  # pragma: no cover
    if pytesseract is None or Image is None:
        return None
    # Basit ikilestirme ve OCR
    try:
        img = Image.open(image_path).convert("L")
        # Basit threshold
        img = img.point(lambda p: 255 if p > 150 else 0)
        text = pytesseract.image_to_string(img, config="--psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
        text = (text or "").strip().replace(" ", "")
        if 3 <= len(text) <= 6:
            return text
    except Exception:
        return None
    return None


def _solve_captcha_llm_ollama(image_path: str, model: str = "llava") -> Optional[str]:  # pragma: no cover
    if ollama is None:
        return None
    try:
        # Ollama server'in lokalde calistigini varsayar (ollama serve)
        with open(image_path, "rb") as f:
            img_bytes = f.read()
        prompt = "Yalnızca görseldeki CAPTCHA metnini yaz. Boşluk veya açıklama ekleme."
        # Ollama Python client'da vision icin base64 iletilir
        import base64

        b64 = base64.b64encode(img_bytes).decode("utf-8")
        res = ollama.chat(
            model=model,
            messages=[
                {"role": "system", "content": "Kısa ve sadece metin yanıt ver."},
                {"role": "user", "content": prompt, "images": [b64]},
            ],
        )
        out = (res.get("message", {}) or {}).get("content", "").strip()
        out = out.replace(" ", "")
        if 3 <= len(out) <= 6:
            return out
    except Exception:
        return None
    return None


def ensure_captcha(page: Page) -> Optional[str]:
    """Varsayılan: manuel bekler. SCRAPE_CAPTCHA_AUTO=1 ise Tesseract/LLM ile dener."""
    captcha = page.locator('#Captcha, #CaptchaIlan, input[name="Captcha"], input[name="CaptchaIlan"], input[id*="Captcha"][type="text"]')
    if captcha.count() > 0 and captcha.first.is_visible():
        auto = os.getenv("SCRAPE_CAPTCHA_AUTO", "0") == "1"
        pause = os.getenv("SCRAPE_CAPTCHA_PAUSE", "0") == "1"
        if auto:
            # Captcha görselini bulup çözmeyi deneriz (örnek selector varsayımı)
            img = page.locator('#CaptchaImg, #CaptchaIlanImg, img[alt*="Captcha" i], img[src*="captcha" i]')
            code: Optional[str] = None
            if img.count() > 0 and img.first.is_visible():
                box = img.first.bounding_box()
                if box:
                    tmp = pathlib.Path("./tmp_captcha.png")
                    page.screenshot(path=str(tmp), clip=box)
                    code = _solve_captcha_tesseract(str(tmp)) or _solve_captcha_llm_ollama(str(tmp))
            if code:
                captcha.first.fill(code)
                return code
            # Otomatik çözemezsek manuel moduna düş
        if pause:
            page.pause()
            return None
        # Manuel çözüm için 45 sn'ye kadar bekleme
        max_wait = time.time() + 45
        while time.time() < max_wait:
            if not captcha.first.is_visible():
                break
            random_human_delay(500, 1000)
    return None


def save_pdf(page: Page, pdf_url: str, suggested_name: Optional[str] = None) -> str:
    out_dir = os.getenv("DOWNLOAD_DIR", "./downloads")
    pathlib.Path(out_dir).mkdir(parents=True, exist_ok=True)
    name = suggested_name or f"ilan-{int(time.time()*1000)}.pdf"
    out_path = str(pathlib.Path(out_dir) / name)

    res = page.request.get(pdf_url, headers={"Referer": page.url})
    if not res.ok:
        raise RuntimeError(f"PDF indirme başarısız: {res.status} {res.text()}")
    with open(out_path, "wb") as f:
        f.write(res.body())
    return out_path


def solve_captcha_image(image_path: str) -> Optional[str]:
    """Önce Tesseract ile dener, olmazsa Ollama LLM ile dener. Başarısızsa None döner."""
    code = _solve_captcha_tesseract(image_path)
    if code:
        return code
    return _solve_captcha_llm_ollama(image_path)
