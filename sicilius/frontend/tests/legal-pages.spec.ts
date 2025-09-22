import { test, expect, type Page } from '@playwright/test';

const legalPaths = [
  '/gizlilik-politikasi',
  '/kullanici-sozlesmesi',
  '/cerez-politikasi',
  '/kvkk-aydinlatma',
];

// Helper to get computed background-color alpha channel
async function backgroundAlpha(page: Page, selector: string): Promise<number> {
  const alpha = await page.$eval(selector, (el: Element) => {
    const cs = window.getComputedStyle(el as HTMLElement);
    const bg = cs.backgroundColor || '';
    if (!bg) return 0;
    // Expect formats like: rgb(r,g,b) or rgba(r,g,b,a)
    if (bg.startsWith('rgba')) {
      const parts = bg.replace('rgba(', '').replace(')', '').split(',').map((p) => p.trim());
      const a = parseFloat(parts[3] ?? '1');
      return isNaN(a) ? 0 : a;
    }
    if (bg.startsWith('rgb')) {
      // rgb has implicit alpha 1
      return 1;
    }
    // transparent or unknown
    if (bg === 'transparent') return 0;
    return 1;
  });
  return alpha as number;
}

test.describe('Legal pages header/footer presence', () => {
  for (const path of legalPaths) {
    test(`header and footer visible on ${path}`, async ({ page }) => {
      await page.goto(path);
      const header = page.getByTestId('public-header');
      const footer = page.getByTestId('public-footer');
      await expect(header).toBeVisible();
      await expect(footer).toBeVisible();
    });
  }
});

test.describe('Mobile menu behavior on legal pages', () => {
  test('mobile menu expands and content remains below header', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 812 });
    await page.goto('/gizlilik-politikasi');

    const header = page.getByTestId('public-header');
    await expect(header).toBeVisible();

    const menuBtn = page.getByTestId('mobile-menu-button');
    await expect(menuBtn).toBeVisible();
    await menuBtn.click();

    const mobileMenu = page.getByTestId('mobile-menu');
    await expect(mobileMenu).toBeVisible();

    const h = await mobileMenu.evaluate((el) => (el as HTMLElement).getBoundingClientRect().height);
    expect(h).toBeGreaterThan(0);

    // Content (main) should be below the fixed header; verify main exists and is below y=0
    // Instead of offsetTop, validate padding-top (pt-24 ~= 96px)
    const mainPaddingTop = await page.$eval('main', (el: Element) => {
      const cs = window.getComputedStyle(el as HTMLElement);
      return parseFloat(cs.paddingTop || '0');
    });
    expect(mainPaddingTop).toBeGreaterThanOrEqual(90);
  });
});

test.describe('Dark mode compatibility on legal pages', () => {
  test('header shows shadow on scroll in dark mode', async ({ page }) => {
    await page.emulateMedia({ colorScheme: 'dark' });
    await page.goto('/gizlilik-politikasi');

    const header = page.getByTestId('public-header');
    await expect(header).toBeVisible();

    const headerSel = '[data-testid="public-header"]';
    const shadowBefore = await page.$eval(headerSel, (el: Element) => {
      return window.getComputedStyle(el as HTMLElement).boxShadow;
    });

    // Scroll and dispatch event to trigger isScrolled state
    await page.evaluate(() => {
      window.scrollTo({ top: 200, behavior: 'auto' });
      window.dispatchEvent(new Event('scroll'));
    });
    await page.waitForTimeout(200);

    const shadowAfter = await page.$eval(headerSel, (el: Element) => {
      return window.getComputedStyle(el as HTMLElement).boxShadow;
    });

    expect(shadowAfter).not.toBe(shadowBefore);
    expect(shadowAfter).not.toBe('none');

    await expect(page.getByTestId('public-footer')).toBeVisible();
  });
});
