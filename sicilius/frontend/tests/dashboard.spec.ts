import { test, expect } from '@playwright/test';

const DASHBOARD_PATH = '/dashboard';

// Helper: ensure search input is focused
async function expectSearchFocused(page: import('@playwright/test').Page) {
  await expect(page.getByTestId('search-input')).toBeFocused();
}

// Auth bypass for middleware: set dummy auth cookie before each test
test.beforeEach(async ({ context, baseURL }) => {
  if (baseURL) {
    await context.addCookies([
      { name: 'auth_token', value: 'e2e', url: baseURL },
    ]);
  }
});

test.describe('Dashboard keyboard shortcuts', () => {
  test('focus search with "/" and Cmd/Ctrl+K', async ({ page }) => {
    await page.goto(DASHBOARD_PATH);

    // Ensure input is rendered before interacting
    await expect(page.getByTestId('search-input')).toBeVisible();

    // Press "/" and expect focus on search input
    await page.keyboard.press('/');
    await expectSearchFocused(page);

    // Blur by focusing body (click somewhere empty)
    await page.mouse.click(10, 10);

    // Press Meta+K (Cmd+K)
    await page.keyboard.down('Meta');
    await page.keyboard.press('KeyK');
    await page.keyboard.up('Meta');
    await expectSearchFocused(page);

    // Blur again
    await page.mouse.click(10, 10);

    // Press Ctrl+K
    await page.keyboard.down('Control');
    await page.keyboard.press('KeyK');
    await page.keyboard.up('Control');
    await expectSearchFocused(page);
  });
});

// Mobile-only tests
test.describe('Mobile history drawer', () => {
  // Sadece mobil projede çalıştır
  test.skip(({ isMobile }) => !isMobile, 'Bu test mobil projede çalışır');

  test('open drawer, navigate with arrows, close with Esc', async ({ page }) => {
    // Pre-populate localStorage with history items BEFORE page loads
    await page.addInitScript(() => {
      const key = 'sicilius.searchHistory.v2';
      const now = Date.now();
      const items = [
        { id: '1', query: 'Acme AŞ', createdAt: now - 3000, pinned: true },
        { id: '2', query: 'John Doe', createdAt: now - 2000, pinned: false },
        { id: '3', query: 'Beta Ltd', createdAt: now - 1000, pinned: false },
      ];
      window.localStorage.setItem(key, JSON.stringify(items));
    });

    await page.goto(DASHBOARD_PATH);

    // Ensure input is ready and submit a search to guarantee at least one history item
    await expect(page.getByTestId('search-input')).toBeVisible();
    await page.getByTestId('search-input').fill('Acme Test');
    await page.keyboard.press('Enter');

    // Ensure button is present
    await expect(page.getByTestId('mobile-history-button')).toBeVisible();

    // Open drawer
    await page.getByTestId('mobile-history-button').click();

    const dialog = page.getByRole('dialog', { name: 'Geçmiş' });
    await expect(dialog).toBeVisible();

    const items = dialog.locator('[data-history-item] button[data-role="select"]');
    await expect(items.first()).toBeVisible();

    // Focus first selectable item
    await items.first().focus();
    await expect(items.first()).toBeFocused();

    // ArrowDown should move focus to next item (wraps if needed)
    await page.keyboard.press('ArrowDown');
    const count = await items.count();
    if (count > 1) {
      await expect(items.nth(1)).toBeFocused();
    } else {
      await expect(items.first()).toBeFocused();
    }

    // Close with Escape
    await page.keyboard.press('Escape');
    await expect(dialog).toBeHidden();
  });
});
