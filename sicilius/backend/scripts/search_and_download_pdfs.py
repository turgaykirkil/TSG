from __future__ import annotations

import io
import os
import time
from pathlib import Path
from typing import Optional, List, Tuple
import json
import argparse

from PIL import Image, ImageFilter  # type: ignore
import re
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout, Page
import pytesseract  # type: ignore

SITE = "https://www.ticaretsicil.gov.tr/"
EMAIL = "turgaykirkil@gmail.com"
PASSWORD = "29769000"
MAX_LOGIN_TRIES = 3
MAX_CAPTCHA_TRIES = 3
DOWNLOAD_DIR = Path(os.getenv("DOWNLOAD_DIR", "./downloads")).resolve()
INDEX_PATH = DOWNLOAD_DIR / "download_index.json"


# -------------------- Human-like helpers --------------------
import math
import secrets

def random_human_delay(min_ms: int = 250, max_ms: int = 900) -> None:
    ms = int(math.floor(min_ms + (max_ms - min_ms) * secrets.randbelow(256) / 255.0))
    time.sleep(ms / 1000.0)


def gentle_mouse_wiggle(page: Page) -> None:
    size = page.viewport_size or {"width": 1280, "height": 900}
    w, h = size["width"], size["height"]
    x = int(w * 0.25 + (w * 0.5) * secrets.randbelow(256) / 255.0)
    y = int(h * 0.25 + (h * 0.5) * secrets.randbelow(256) / 255.0)
    page.mouse.move(x, y, steps=8)
    random_human_delay(120, 280)
    page.mouse.move(x + 16, y + 12, steps=6)


def human_click(page: Page, selector: str, timeout: int = 10_000) -> None:
    el = page.locator(selector).first
    el.wait_for(state="visible", timeout=timeout)
    el.scroll_into_view_if_needed()
    random_human_delay(120, 300)
    try:
        el.hover()
    except Exception:
        pass
    random_human_delay(120, 300)
    el.click()


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


# -------------------- Site interactions --------------------

def _toast_error_present(p: Page) -> bool:
    try:
        toast = p.query_selector('div.toast.toast-error:has-text("Güvenlik Kodu Hatalı")')
        return toast is not None
    except Exception:
        return False


def ensure_captcha(p: Page, max_tries: int = MAX_CAPTCHA_TRIES) -> bool:
    """Sayfada #CaptchaImg var mı kontrol et; varsa Tesseract ile çöz ve onayla.
    Başarılı ise True, değilse False döner.
    """
    try:
        p.wait_for_load_state("domcontentloaded", timeout=10_000)
    except Exception:
        pass
    for attempt in range(1, max_tries + 1):
        try:
            form = p.query_selector('#FormGuvenlikKodu')
            img_el = p.query_selector('#FormGuvenlikKodu #CaptchaImg') or p.query_selector('#CaptchaImg')
            # Captcha yoksa
            if (img_el is None) or (not img_el.is_visible()):
                return True

            print(f"[INFO] CAPTCHA tespit edildi. Deneme {attempt}/{max_tries}")
            # Görseli al, boş ise bir kez yenile (src değişimi)
            shot = img_el.screenshot(type="png")
            code = ocr_from_bytes(shot) or ""
            if not code:
                try:
                    old_src = img_el.get_attribute('src')
                    img_el.click()
                    p.wait_for_function(
                        "(el, oldSrc) => el && el.getAttribute('src') !== oldSrc",
                        arg=img_el,
                        polling=200,
                        timeout=5_000,
                        oldSrc=old_src,
                    )
                    shot = img_el.screenshot(type="png")
                    code = ocr_from_bytes(shot) or ""
                except Exception:
                    pass

            # Hedef input'u bul
            target_input = (
                p.query_selector('#FormGuvenlikKodu #CaptchaIlan')
                or p.query_selector('#CaptchaIlan')
                or p.query_selector('#Captcha')
                or p.query_selector('input[name="CaptchaIlan"]')
                or p.query_selector('input[name="Captcha"]')
            )
            if target_input:
                # human typing
                try:
                    target_input.click()
                except Exception:
                    pass
                random_human_delay(120, 300)
                target_input.fill("")
                random_human_delay(100, 220)
                for ch in code:
                    target_input.type(ch, delay=secrets.randbelow(120) + 30)

            random_human_delay(200, 480)
            # Submit butonu (form içi öncelik)
            submit_btn = (
                (form.query_selector('button[type="submit"]') if form else None)
                or p.query_selector('button:has(i.fa-check)')
                or p.query_selector('button.c-theme-btn:has(i.fa-check)')
                or p.query_selector('button[type="submit"]')
            )
            if submit_btn:
                try:
                    submit_btn.click()
                except Exception:
                    pass

            random_human_delay(260, 620)
            # CAPTCHA submit sonrası istenmeyen yeni sekme (ör. ilangoruntuleme.php) açılırsa kapat
            try:
                child = p.wait_for_event("popup", timeout=2_000)
                try:
                    child.wait_for_load_state("domcontentloaded", timeout=5_000)
                except Exception:
                    pass
                try:
                    if "ilangoruntuleme.php" in (child.url or ""):
                        child.close()
                    else:
                        # Bu akışta beklenmeyen her yeni pop-up'ı kapatıyoruz
                        child.close()
                except Exception:
                    pass
            except Exception:
                pass

            if _toast_error_present(p):
                print("[WARN] Güvenlik Kodu Hatalı; sayfa yenileniyor…")
                try:
                    p.reload(wait_until="domcontentloaded")
                except Exception:
                    pass
                continue

            # Form görünürlüğü bitti mi?
            try:
                p.wait_for_selector('#FormGuvenlikKodu', state='hidden', timeout=5_000)
            except Exception:
                # bazı sayfalarda detach olur
                try:
                    p.wait_for_selector('#FormGuvenlikKodu', state='detached', timeout=2_000)
                except Exception:
                    pass

            # Başarılıysa bir miktar yükleme bekle
            try:
                p.wait_for_load_state("networkidle", timeout=6_000)
            except Exception:
                pass
            return True
        except Exception as e:
            print(f"[WARN] ensure_captcha hata: {e}")
            continue
    return False

def open_login_modal(page: Page) -> None:
    try:
        page.get_by_role("link", name=lambda n: n and "GİRİŞ" in n).click(timeout=10_000)
    except Exception:
        page.locator("a:has-text('GİRİŞ')").first.click()
    page.wait_for_selector("#LoginEmail", timeout=20_000)


def fill_login_form(page: Page, email: str, password: str) -> None:
    page.fill("#LoginEmail", email)
    random_human_delay()
    page.fill("#LoginSifre", password)
    random_human_delay()


def solve_and_fill_captcha(page: Page) -> str:
    page.wait_for_selector("#CaptchaImg", timeout=20_000)
    img_el = page.locator("#CaptchaImg").first
    img_el.wait_for(state="visible", timeout=10_000)
    code = ""
    for i in range(1, MAX_CAPTCHA_TRIES + 1):
        shot = img_el.screenshot(type="png")
        code = ocr_from_bytes(shot) or ""
        if code:
            break
        # yenileme denemesi: görsele tıkla ve src değişimini bekle
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
        except Exception:
            pass
    page.fill("#Captcha", code)
    print(f"[INFO] OCR code -> '{code}'")
    return code


def try_login_once(page: Page) -> bool:
    open_login_modal(page)
    gentle_mouse_wiggle(page)
    fill_login_form(page, EMAIL, PASSWORD)
    solve_and_fill_captcha(page)

    # GİRİŞ tuşuna bas
    try:
        page.locator("button.c-btn-login").first.click()
    except Exception:
        page.get_by_role("button", name=lambda n: n and "GİRİŞ" in n).first.click()

    # Başarı kontrol (login sonrası arama formu elementleri görünmeli)
    try:
        page.wait_for_selector("#SicilMudurluguId", timeout=12_000)
        # Login sonrası ana sayfada captcha çıkmışsa çöz
        ensure_captcha(page)
        return True
    except PlaywrightTimeout:
        return False


def login_with_retries(page: Page) -> bool:
    for i in range(1, MAX_LOGIN_TRIES + 1):
        print(f"[INFO] Login denemesi {i}/{MAX_LOGIN_TRIES}")
        if i > 1:
            page.reload(wait_until="domcontentloaded")
        if try_login_once(page):
            print("[INFO] Login başarılı.")
            return True
    print("[ERR] Login başarısız.")
    return False


def select_ankara_and_fill_company(page: Page) -> None:
    # Robust seçim: önce value, olmazsa label
    try:
        page.select_option("#SicilMudurluguId", value="18")  # ANKARA
    except Exception:
        page.select_option("#SicilMudurluguId", label="ANKARA")
    page.fill("#TicaretUnvani", "Pars Global")


def click_search(page: Page) -> None:
    # Önce olası captcha
    ensure_captcha(page)
    # data-message="İlan Ara" olan buton
    try:
        human_click(page, 'button[data-message="İlan Ara"]')
    except Exception:
        # Sınıfına göre fallback
        human_click(page, "button.c-theme-btn:has(i.fa-search)")
    page.wait_for_selector("table#tblIlanGoruntuleme", timeout=30_000)


def set_results_length_100(page: Page) -> None:
    try:
        sel = page.locator('select[name="tblIlanGoruntuleme_length"]').first
        sel.scroll_into_view_if_needed()
        random_human_delay(160, 360)
        page.select_option('select[name="tblIlanGoruntuleme_length"]', value="100")
        random_human_delay()
    except Exception:
        pass


def collect_pdf_links(page: Page) -> List[str]:
    links = page.locator('a[href*="pdf_goster.php?Guid="]')
    hrefs: List[str] = []
    count = links.count()
    for i in range(count):
        href = links.nth(i).get_attribute("href")
        if href:
            hrefs.append(href)
    print(f"[INFO] {len(hrefs)} adet PDF linki bulundu.")
    return hrefs


def extract_pdf_url_from_page(p: Page) -> Optional[str]:
    # Chrome yerleşik viewer
    try:
        el = p.locator('embed[type="application/x-google-chrome-pdf"][original-url]').first
        if el.count() > 0:
            original = el.get_attribute("original-url")
            if original:
                return p.evaluate("(u) => new URL(u, location.href).toString()", original)
    except Exception:
        pass
    # pdf.js viewer (file param)
    try:
        iframe = p.locator('iframe[src*="viewer"]').first
        if iframe.count() > 0:
            src = iframe.get_attribute("src")
            if src:
                abs_url = p.evaluate("(s) => new URL(s, location.href).toString()", src)
                from urllib.parse import urlparse, parse_qs, unquote
                q = parse_qs(urlparse(abs_url).query)
                f = q.get("file", [None])[0]
                if f:
                    decoded = unquote(f)
                    return p.evaluate("(u) => new URL(u, location.href).toString()", decoded)
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
            if el.count() > 0:
                src = el.get_attribute("src") or el.get_attribute("data")
                if src:
                    return p.evaluate("(u) => new URL(u, location.href).toString()", src)
        except Exception:
            continue
    return None


def download_pdf(context, referer_page: Page, pdf_url: str, suggested: Optional[str] = None) -> Path:
    DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)
    if not suggested:
        # GUID ya da zaman temelli isim
        name = f"ilan-{int(time.time()*1000)}.pdf"
    else:
        name = suggested
    out = DOWNLOAD_DIR / name
    res = referer_page.request.get(pdf_url, headers={"Referer": referer_page.url})
    if not res.ok:
        raise RuntimeError(f"PDF indirme başarısız: {res.status} {res.text()}")
    out.write_bytes(res.body())
    print(f"[OK] PDF kaydedildi: {out}")
    return out


def _has_captcha(p: Page) -> bool:
    try:
        el = p.query_selector('#CaptchaImg')
        return el is not None and el.is_visible()
    except Exception:
        return False


def open_pdf_in_new_tab(page: Page, href: str, guid: Optional[str]) -> Optional[Page]:
    """Gerçek linke tıklayarak yeni sekmeyi açmayı dener; olmazsa programatik yeni sekme ile gider.
    Daha insani davranış: scroll + hover + bekleme. Başarılı olursa yeni Page döner.
    """
    # Önce linki DOM'da bulmaya çalış (GUID ile hedefleme daha sağlam)
    link = None
    try:
        # 1) Önce birebir href eşleşmesini dene (en doğal yol)
        link = page.locator(f'a[href="{href}"]').first
        if link and link.count() == 0:
            link = None
    except Exception:
        link = None
    if link is None:
        try:
            # 2) Fallback: pdf_goster.php içeren ilk link (liste üzerinde doğal seçim)
            link = page.locator('a[href*="pdf_goster.php"]').first
        except Exception:
            link = None

    # Link görünürse tıklayıp popup bekle
    if link:
        try:
            link.scroll_into_view_if_needed()
            random_human_delay(200, 450)
            try:
                link.hover()
            except Exception:
                pass
            random_human_delay(180, 420)
            gentle_mouse_wiggle(page)
            random_human_delay(220, 520)
            with page.expect_popup(timeout=8_000) as pop_wait:
                link.click()
            return pop_wait.value
        except Exception:
            pass

    # Fallback: programatik yeni sekme + goto(abs_url)
    try:
        from urllib.parse import urljoin
        abs_url = urljoin(page.url, href)
    except Exception:
        try:
            abs_url = page.evaluate("(h) => new URL(h, location.href).toString()", href)
        except Exception:
            abs_url = href

    new_tab = page.context.new_page()
    try:
        # İnsanî gecikme
        random_human_delay(250, 600)
        new_tab.goto(abs_url, wait_until="domcontentloaded")
        return new_tab
    except Exception:
        try:
            new_tab.close()
        except Exception:
            pass
        return None


def handle_pdf_popup(page: Page, popup: Page, suggested_name: Optional[str] = None) -> Tuple[bool, bool]:
    # Önce CAPTCHA var mı bak
    try:
        popup.wait_for_load_state("domcontentloaded", timeout=20_000)
    except Exception:
        pass

    if popup.is_closed():
        print("[WARN] Popup kapalı; CAPTCHA kontrolü atlanıyor.")
        return (False, False)

    # 3 tur: captcha -> url çıkarımı -> (gerekirse) reload
    for round_idx in range(1, 4):
        # Genel captcha çözme (retry içerir)
        had_captcha_before = (_has_captcha(popup) or (popup.query_selector('#FormGuvenlikKodu') is not None))
        ensure_captcha(popup)
        had_captcha_after = (_has_captcha(popup) or (popup.query_selector('#FormGuvenlikKodu') is not None))
        captcha_solved = had_captcha_before and (not had_captcha_after)

        # Viewer içeriğini tetiklemek için hafif scroll
        try:
            popup.mouse.wheel(0, 400)
            random_human_delay(160, 360)
            popup.mouse.wheel(0, -200)
        except Exception:
            pass

        # ÖZEL DURUM: CAPTCHA sonrası aynı sekmede ilan liste sayfasına yönlenme
        try:
            popup.wait_for_url(re.compile(r"ilangoruntuleme\\.php"), timeout=3_000)
            redirected_to_listing = True
        except Exception:
            redirected_to_listing = ("ilangoruntuleme.php" in (popup.url or ""))
        if redirected_to_listing:
            print("[INFO] CAPTCHA sonrası sekme ilangoruntuleme.php'ye yönlendi; sekme kapatılıyor ve çağırana retry sinyali veriliyor…")
            try:
                popup.close()
            except Exception:
                pass
            random_human_delay(200, 500)
            return (False, True)

        # PDF URL çıkar ve indir
        pdf_url = None
        try:
            pdf_url = extract_pdf_url_from_page(popup)
        except Exception as e:
            print(f"[WARN] PDF URL çıkarımı sırasında hata: {e}")
        if not pdf_url:
            # Viewer bekleme ve yeniden deneme
            try:
                popup.wait_for_selector(
                    'embed[type="application/x-google-chrome-pdf"], embed[type="application/pdf"], object[type="application/pdf"]',
                    timeout=30_000,
                )
                pdf_url = extract_pdf_url_from_page(popup)
            except Exception:
                pass
        if not pdf_url:
            # Yüklenme/navigation için ek bekleme
            try:
                popup.wait_for_load_state("networkidle", timeout=10_000)
                pdf_url = extract_pdf_url_from_page(popup)
            except Exception:
                pass
        # Ağ yanıtı dinleyerek .pdf yakala
        if not pdf_url:
            try:
                resp = popup.wait_for_event(
                    "response",
                    predicate=lambda r: (".pdf" in r.url.lower()) and r.status == 200,
                    timeout=20_000,
                )
                pdf_url = resp.url
            except Exception:
                pass
        # Son çare: mevcut popup URL'sine request.get yapıp content-type kontrol et
        if not pdf_url:
            try:
                res2 = popup.request.get(popup.url, headers={"Referer": popup.url})
                ct = (res2.headers or {}).get("content-type", "").lower()
                if "application/pdf" in ct and res2.ok:
                    # Kendi URL'si doğrudan PDF döndürüyor
                    pdf_url = popup.url
            except Exception:
                pass

        if pdf_url:
            # İsim önerisi
            from urllib.parse import urlparse
            if suggested_name and suggested_name.lower().endswith('.pdf'):
                suggested = suggested_name
            else:
                last = Path(urlparse(pdf_url).path).name
                suggested = last if last.lower().endswith(".pdf") else suggested_name
            download_pdf(popup.context, popup, pdf_url, suggested)
            return (True, captcha_solved)

        # Bu turda bulunamadıysa, bir kez daha yenilemeyi dene ve tekrar tur at
        if round_idx < 3:
            print("[WARN] PDF URL bulunamadı; sayfa yenileniyor ve tekrar denenecek…")
            try:
                popup.reload(wait_until="domcontentloaded")
            except Exception:
                pass
            continue
        else:
            # Captcha yeni çözülmüşse, asıl sayfada aynı linki tekrar denemek için çağırana haber ver
            if captcha_solved:
                return (False, True)
            print("[ERR] PDF URL bulunamadı (popup). Atlanıyor.")
            return (False, False)


def main() -> int:
    # -------------------- CLI args --------------------
    parser = argparse.ArgumentParser(description="Search and download gazette PDFs with CAPTCHA handling.")
    parser.add_argument("--retry-remaining", action="store_true", help="Sadece daha önce indirilemeyen (indexe göre) PDF linklerini dene")
    parser.add_argument("--only-guid", action="append", help="Sadece belirtilen GUID(leri) dene. Birden fazla için birden çok --only-guid kullan.")
    parser.add_argument("--limit", type=int, default=0, help="En fazla N adet link işle")
    args, unknown = parser.parse_known_args()

    # -------------------- Index helpers --------------------
    def load_index() -> dict:
        try:
            if INDEX_PATH.exists():
                return json.loads(INDEX_PATH.read_text())
        except Exception:
            pass
        return {}

    def save_index(d: dict) -> None:
        try:
            DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)
            INDEX_PATH.write_text(json.dumps(d, ensure_ascii=False, indent=2))
        except Exception:
            pass

    def parse_guid_from_href(h: str) -> Optional[str]:
        try:
            from urllib.parse import urlparse, parse_qs
            q = parse_qs(urlparse(h).query)
            g = q.get("Guid", q.get("guid"))
            if g and len(g) > 0 and g[0]:
                return g[0]
        except Exception:
            return None
        return None

    index = load_index()
    with sync_playwright() as p:
        browser_pref = os.getenv("BROWSER", "webkit").lower()
        try:
            if browser_pref == "chromium":
                browser = p.chromium.launch(headless=False, slow_mo=100)
            else:
                browser = p.webkit.launch(headless=False, slow_mo=100)
        except Exception as e:
            print(f"[WARN] {browser_pref} launch failed: {e}. Falling back to the other engine.")
            if browser_pref == "chromium":
                browser = p.webkit.launch(headless=False, slow_mo=100)
            else:
                browser = p.chromium.launch(headless=False, slow_mo=100)
        context = browser.new_context(ignore_https_errors=True)
        page = context.new_page()
        page.goto(SITE, wait_until="domcontentloaded")

        if not login_with_retries(page):
            print("[ERR] Login başarısız. İnceleme için duraklatıyorum.")
            page.pause()
            browser.close()
            return 1

        select_ankara_and_fill_company(page)
        gentle_mouse_wiggle(page)
        click_search(page)
        set_results_length_100(page)
        random_human_delay()

        # Ana sayfada captcha var mı kontrol et ve çöz
        ensure_captcha(page)
        all_hrefs = collect_pdf_links(page)

        # Filtreleme: only-guid ve retry-remaining
        # argparse uses only_guid attribute; Python identifier
        only_list = getattr(args, "only_guid", None)
        hrefs: List[str] = []
        for h in all_hrefs:
            g = parse_guid_from_href(h)
            if only_list:
                if (g is None) or (g not in set(only_list)):
                    continue
            if args.retry_remaining:
                if g and index.get(g, {}).get("downloaded"):
                    continue
            hrefs.append(h)

        # Limit uygula
        if args.limit and args.limit > 0:
            hrefs = hrefs[: args.limit]

        print(f"[INFO] İşlenecek link: {len(hrefs)} (toplam {len(all_hrefs)})")
        if not hrefs:
            # Filtreli çalıştırmalarda (retry-remaining / only-guid) interaktif duraksama yapmayalım
            if getattr(args, "retry_remaining", False) or getattr(args, "only_guid", None):
                print("[DONE] İşlenecek link yok (filtreleme sonrası). Çıkılıyor.")
                browser.close()
                return 0
            print("[WARN] PDF linki bulunamadı. İnceleme için duraklatıyorum.")
            page.pause()
            browser.close()
            return 0

        # Tüm linkleri sırayla işle (çok fazla ise gerekirse sınır koy)
        from urllib.parse import urljoin
        for idx, href in enumerate(hrefs, start=1):
            print(f"[INFO] PDF {idx}/{len(hrefs)} işleniyor…")
            # Her linkten önce ana sayfada captcha kontrolü
            ensure_captcha(page)
            try:
                abs_url = urljoin(page.url, href)
            except Exception:
                # Son çare: sayfa içinde absolute hesapla
                try:
                    abs_url = page.evaluate("(h) => new URL(h, location.href).toString()", href)
                except Exception:
                    abs_url = href

            # GUID ve önerilen dosya adı
            guid = parse_guid_from_href(href)
            suggested_name = f"{guid}.pdf" if guid else None

            # Daha insani: linki gerçekten tıklayarak yeni sekme açmayı dene; olmazsa fallback
            new_tab = open_pdf_in_new_tab(page, href, guid)
            if not new_tab:
                print("[WARN] Yeni sekme açılamadı; link atlanıyor.")
                continue

            downloaded, captcha_solved = handle_pdf_popup(page, new_tab, suggested_name=suggested_name)
            # Sekmeyi kapat
            try:
                new_tab.close()
            except Exception:
                pass

            # Dönüşte ana sayfada captcha kontrolü
            ensure_captcha(page)

            # Eğer sadece CAPTCHA çözüldüyse, aynı href'i tekrar dene (yeni sekmede)
            if (not downloaded) and captcha_solved:
                print("[INFO] CAPTCHA çözüldü, aynı PDF linki yeniden deneniyor…")
                random_human_delay(300, 800)
                ensure_captcha(page)
                retry_tab = page.context.new_page()
                try:
                    retry_tab.goto(abs_url, wait_until="domcontentloaded")
                    downloaded2, _ = handle_pdf_popup(page, retry_tab, suggested_name=suggested_name)
                except Exception as e:
                    print(f"[WARN] Retry sekmesine gidilemedi: {e}")
                    downloaded2 = False
                finally:
                    try:
                        retry_tab.close()
                    except Exception:
                        pass
                ensure_captcha(page)
                if not downloaded2:
                    print("[WARN] CAPTCHA sonrası yeniden denemede PDF indirilemedi; sonraki linke geçiliyor.")
                else:
                    downloaded = True

            # Başarılı indirme indexe yaz
            if downloaded and guid:
                index[guid] = {
                    "downloaded": True,
                    "filename": str(DOWNLOAD_DIR / (guid + ".pdf")),
                    "href": href,
                    "ts": int(time.time()),
                }
                save_index(index)

            random_human_delay(300, 900)

        print("[DONE] Tüm PDF bağlantıları işlendi. Duraklatıyorum.")
        page.pause()
        browser.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
