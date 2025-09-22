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
// Mobil geçmiş çekmecesi testi mobile-history.spec.ts dosyasına taşındı
