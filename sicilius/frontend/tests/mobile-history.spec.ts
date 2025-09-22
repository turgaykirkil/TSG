import { test, expect } from '@playwright/test';

const DASHBOARD_PATH = '/dashboard';

// Sadece mobil projede çalıştır
test.skip(({ isMobile }) => !isMobile, 'Bu test mobil projede çalışır');

// Auth bypass for middleware
test.beforeEach(async ({ context, baseURL }) => {
  if (baseURL) {
    await context.addCookies([
      { name: 'auth_token', value: 'e2e', url: baseURL },
    ]);
  }
});

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
