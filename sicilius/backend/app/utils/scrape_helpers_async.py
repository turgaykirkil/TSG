import asyncio
import io
import math
import os
import re
import secrets
from typing import Optional, Tuple

from PIL import Image, ImageFilter  # type: ignore
import pytesseract  # type: ignore
from playwright.async_api import Page, TimeoutError as PlaywrightTimeout
from app.core.config import settings

# -------------------- Human-like helpers --------------------

# Configure pytesseract binary and tessdata if provided
try:
    if settings.TESSERACT_CMD:
        pytesseract.pytesseract.tesseract_cmd = settings.TESSERACT_CMD
    if settings.TESSDATA_PREFIX:
        os.environ.setdefault("TESSDATA_PREFIX", settings.TESSDATA_PREFIX)
except Exception:
    pass

async def random_human_delay(min_ms: int = 250, max_ms: int = 900) -> None:
    ms = int(math.floor(min_ms + (max_ms - min_ms) * secrets.randbelow(256) / 255.0))
    await asyncio.sleep(ms / 1000.0)


async def gentle_mouse_wiggle(page: Page) -> None:
    size = await page.viewport_size()
    if not size:
        size = {"width": 1280, "height": 900}
    w, h = size["width"], size["height"]
    x = int(w * 0.25 + (w * 0.5) * secrets.randbelow(256) / 255.0)
    y = int(h * 0.25 + (h * 0.5) * secrets.randbelow(256) / 255.0)
    await page.mouse.move(x, y, steps=8)
    await random_human_delay(120, 280)
    await page.mouse.move(x + 16, y + 12, steps=6)


async def human_click(page: Page, selector: str, timeout: int = 10_000) -> None:
    el = page.locator(selector).first
    await el.wait_for(state="visible", timeout=timeout)
    await el.scroll_into_view_if_needed()
    await random_human_delay(120, 300)
    try:
        await el.hover()
    except Exception:
        pass
    await random_human_delay(120, 300)
    await el.click()


# -------------------- OCR helpers --------------------

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
    except Exception:
        return None
    return None


# -------------------- CAPTCHA helpers --------------------

async def _toast_error_present(p: Page) -> bool:
    try:
        toast = await p.query_selector('div.toast.toast-error:has-text("Güvenlik Kodu Hatalı")')
        return toast is not None
    except Exception:
        return False


async def ensure_captcha(p: Page, max_tries: int = 3) -> bool:
    try:
        await p.wait_for_load_state("domcontentloaded", timeout=10_000)
    except Exception:
        pass

    for attempt in range(1, max_tries + 1):
        try:
            form = await p.query_selector('#FormGuvenlikKodu')
            img_el = await p.query_selector('#FormGuvenlikKodu #CaptchaImg')
            if img_el is None:
                img_el = await p.query_selector('#CaptchaImg')

            # Captcha yoksa
            visible = False
            if img_el is not None:
                try:
                    visible = await img_el.is_visible()
                except Exception:
                    visible = False
            if (img_el is None) or (not visible):
                return True

            print(f"[INFO] CAPTCHA tespit edildi. Deneme {attempt}/{max_tries}")
            # Görseli al, boş ise bir kez yenile (src değişimi)
            shot = await img_el.screenshot(type="png")
            code = ocr_from_bytes(shot) or ""
            if not code:
                try:
                    old_src = await img_el.get_attribute('src')
                    await img_el.click()
                    await p.wait_for_function(
                        "(el, oldSrc) => el && el.getAttribute('src') !== oldSrc",
                        arg=img_el,
                        polling=200,
                        timeout=5_000,
                        oldSrc=old_src,
                    )
                    shot = await img_el.screenshot(type="png")
                    code = ocr_from_bytes(shot) or ""
                except Exception:
                    pass

            # Hedef input'u bul
            target_input = (
                await p.query_selector('#FormGuvenlikKodu #CaptchaIlan')
                or await p.query_selector('#CaptchaIlan')
                or await p.query_selector('#Captcha')
                or await p.query_selector('input[name="CaptchaIlan"]')
                or await p.query_selector('input[name="Captcha"]')
            )
            if target_input:
                # human typing
                try:
                    await target_input.click()
                except Exception:
                    pass
                await random_human_delay(120, 300)
                await target_input.fill("")
                await random_human_delay(100, 220)
                for ch in code:
                    await target_input.type(ch, delay=secrets.randbelow(120) + 30)

            await random_human_delay(200, 480)
            # Submit butonu (form içi öncelik)
            submit_btn = (
                (await form.query_selector('button[type="submit"]') if form else None)
                or await p.query_selector('button:has(i.fa-check)')
                or await p.query_selector('button.c-theme-btn:has(i.fa-check)')
                or await p.query_selector('button[type="submit"]')
            )
            if submit_btn:
                try:
                    await submit_btn.click()
                except Exception:
                    pass

            await random_human_delay(260, 620)

            # CAPTCHA submit sonrası istenmeyen yeni sekme (ör. ilangoruntuleme.php) açılırsa kapat
            try:
                child = await p.wait_for_event("popup", timeout=2_000)
                try:
                    await child.wait_for_load_state("domcontentloaded", timeout=5_000)
                except Exception:
                    pass
                try:
                    if "ilangoruntuleme.php" in (child.url or ""):
                        await child.close()
                    else:
                        await child.close()
                except Exception:
                    pass
            except Exception:
                pass

            if await _toast_error_present(p):
                print("[WARN] Güvenlik Kodu Hatalı; sayfa yenileniyor…")
                try:
                    await p.reload(wait_until="domcontentloaded")
                except Exception:
                    pass
                continue

            # Form görünürlüğü bitti mi?
            try:
                await p.wait_for_selector('#FormGuvenlikKodu', state='hidden', timeout=5_000)
            except Exception:
                try:
                    await p.wait_for_selector('#FormGuvenlikKodu', state='detached', timeout=2_000)
                except Exception:
                    pass

            # Başarılıysa bir miktar yükleme bekle
            try:
                await p.wait_for_load_state("networkidle", timeout=6_000)
            except Exception:
                pass
            return True
        except Exception as e:
            print(f"[WARN] ensure_captcha hata: {e}")
            continue
    return False


# -------------------- PDF helpers --------------------

async def extract_pdf_url_from_page(p: Page) -> Optional[str]:
    # Chrome yerleşik viewer
    try:
        el = p.locator('embed[type="application/x-google-chrome-pdf"][original-url]').first
        if await el.count() > 0:
            original = await el.get_attribute("original-url")
            if original:
                return await p.evaluate("(u) => new URL(u, location.href).toString()", original)
    except Exception:
        pass
    # pdf.js viewer (file param)
    try:
        iframe = p.locator('iframe[src*="viewer"]').first
        if await iframe.count() > 0:
            src = await iframe.get_attribute("src")
            if src:
                abs_url = await p.evaluate("(s) => new URL(s, location.href).toString()", src)
                from urllib.parse import urlparse, parse_qs, unquote
                q = parse_qs(urlparse(abs_url).query)
                f = q.get("file", [None])[0]
                if f:
                    decoded = unquote(f)
                    return await p.evaluate("(u) => new URL(u, location.href).toString()", decoded)
    except Exception:
        pass
    # Generic
    for sel in [
        'embed[type="application/pdf"]',
        'object[type="application/pdf"]',
        'iframe[src$=".pdf"]',
        'embed[src$=".pdf"]',
    ]:
        try:
            el = p.locator(sel).first
            if await el.count() > 0:
                src = await el.get_attribute("src") or await el.get_attribute("data")
                if src:
                    return await p.evaluate("(u) => new URL(u, location.href).toString()", src)
        except Exception:
            continue
    return None


async def open_pdf_in_new_tab(page: Page, href: str) -> Optional[Page]:
    # Önce birebir href eşleşmesini dene
    link = page.locator(f'a[href="{href}"]').first
    if await link.count() == 0:
        # Fallback: pdf_goster.php içeren ilk link (liste üzerinde doğal seçim)
        link = page.locator('a[href*="pdf_goster.php"], a[href^="javascript:"], a[onclick]').first
        if await link.count() == 0:
            # Son çare programatik
            try:
                abs_url = await page.evaluate("(h) => new URL(h, location.href).toString()", href)
            except Exception:
                abs_url = href
            new_page = await page.context.new_page()
            await random_human_delay(250, 600)
            await new_page.goto(abs_url, wait_until="domcontentloaded")
            return new_page

    # href javascript: ise veya boşsa onclick içinden URL çıkar
    try:
        raw_href = await link.get_attribute("href")
        if (not raw_href) or raw_href.strip().lower().startswith("javascript:"):
            onclick = (await link.get_attribute("onclick")) or ""
            candidate = raw_href or onclick
            extracted = None
            # window.open('...') veya openpdf('...') veya pdf_goster('...')
            for pat in [
                r"window\.open\(['\"]([^'\"]+)['\"]",
                r"openpdf\(['\"]([^'\"]+)['\"]",
                r"pdf_goster\(['\"]([^'\"]+)['\"]",
            ]:
                m = re.search(pat, candidate)
                if m:
                    extracted = m.group(1)
                    break
            if extracted:
                try:
                    href = await page.evaluate("(h) => new URL(h, location.href).toString()", extracted)
                except Exception:
                    href = extracted
    except Exception:
        pass

    # Deneme 1: Gerçek tıklamayla popup
    try:
        await link.scroll_into_view_if_needed()
        await random_human_delay(200, 450)
        try:
            await link.hover()
        except Exception:
            pass
        await random_human_delay(180, 420)
        await gentle_mouse_wiggle(page)
        await random_human_delay(220, 520)
        async with page.expect_popup(timeout=6_000) as pop_wait:
            await link.click()
        return await pop_wait.value
    except PlaywrightTimeout:
        # Popup açılmadıysa yeni sekmede programatik aç
        try:
            abs_url = await page.evaluate("(h) => new URL(h, location.href).toString()", href)
        except Exception:
            abs_url = href
        try:
            new_page = await page.context.new_page()
            await random_human_delay(200, 500)
            await new_page.goto(abs_url, wait_until="domcontentloaded")
            return new_page
        except Exception:
            return None
    except Exception:
        # Diğer beklenmedik hatalarda da programatik fallback’u dene
        try:
            abs_url = await page.evaluate("(h) => new URL(h, location.href).toString()", href)
        except Exception:
            abs_url = href
        try:
            new_page = await page.context.new_page()
            await random_human_delay(200, 500)
            await new_page.goto(abs_url, wait_until="domcontentloaded")
            return new_page
        except Exception:
            return None


async def handle_pdf_popup(parent_page: Page, popup: Page) -> Tuple[Optional[bytes], bool]:
    try:
        await popup.wait_for_load_state("domcontentloaded", timeout=20_000)
    except Exception:
        pass

    if popup.is_closed():
        print("[WARN] Popup kapalı; CAPTCHA kontrolü atlanıyor.")
        return (None, False)

    for round_idx in range(1, 4):
        had_captcha_before = (await popup.query_selector('#CaptchaImg')) is not None or (await popup.query_selector('#FormGuvenlikKodu')) is not None
        await ensure_captcha(popup)
        had_captcha_after = (await popup.query_selector('#CaptchaImg')) is not None or (await popup.query_selector('#FormGuvenlikKodu')) is not None
        captcha_solved = had_captcha_before and (not had_captcha_after)

        # Viewer içeriğini tetiklemek için hafif scroll
        try:
            await popup.mouse.wheel(0, 400)
            await random_human_delay(160, 360)
            await popup.mouse.wheel(0, -200)
        except Exception:
            pass

        # Özel durum: aynı sekmede ilan liste yönlenmesi
        try:
            await popup.wait_for_url(re.compile(r"ilangoruntuleme\\.php"), timeout=3_000)
            redirected_to_listing = True
        except Exception:
            redirected_to_listing = ("ilangoruntuleme.php" in (popup.url or ""))
        if redirected_to_listing:
            print("[INFO] CAPTCHA sonrası sekme ilangoruntuleme.php'ye yönlendi; sekme kapatılıyor ve çağırana retry sinyali veriliyor…")
            try:
                await popup.close()
            except Exception:
                pass
            await random_human_delay(200, 500)
            return (None, True)

        # PDF URL çıkar
        pdf_url: Optional[str] = None
        try:
            pdf_url = await extract_pdf_url_from_page(popup)
        except Exception as e:
            print(f"[WARN] PDF URL çıkarımı sırasında hata: {e}")
        if not pdf_url:
            try:
                await popup.wait_for_selector('embed[type="application/x-google-chrome-pdf"], embed[type="application/pdf"], object[type="application/pdf"]', timeout=30_000)
                pdf_url = await extract_pdf_url_from_page(popup)
            except Exception:
                pass
        if not pdf_url:
            try:
                await popup.wait_for_load_state("networkidle", timeout=10_000)
                pdf_url = await extract_pdf_url_from_page(popup)
            except Exception:
                pass
        if not pdf_url:
            try:
                resp = await popup.wait_for_event(
                    "response",
                    timeout=20_000,
                    predicate=lambda r: (".pdf" in r.url.lower()) and r.status == 200,
                )
                pdf_url = resp.url
            except Exception:
                pass
        if not pdf_url:
            try:
                res2 = await popup.request.get(popup.url, headers={"Referer": popup.url})
                ct = (res2.headers or {}).get("content-type", "").lower()
                if "application/pdf" in ct and res2.ok:
                    pdf_url = popup.url
            except Exception:
                pass

        if pdf_url:
            # PDF bytes indir ve döndür
            resp = await popup.context.request.get(pdf_url, headers={"Referer": popup.url})
            if not resp.ok:
                print(f"[WARN] PDF indirme başarısız: {resp.status}")
            else:
                content = await resp.body()
                return (content, captcha_solved)

        # Bu turda bulunamadıysa, bir kez daha yenilemeyi dene ve tekrar tur at
        if round_idx < 3:
            print("[WARN] PDF URL bulunamadı; sayfa yenileniyor ve tekrar denenecek…")
            try:
                await popup.reload(wait_until="domcontentloaded")
            except Exception:
                pass
            continue
        else:
            if captcha_solved:
                return (None, True)
            print("[ERR] PDF URL bulunamadı (popup). Atlanıyor.")
            return (None, False)

    return (None, False)
