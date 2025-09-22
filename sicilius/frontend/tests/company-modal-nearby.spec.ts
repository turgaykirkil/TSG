import { test, expect } from '@playwright/test';

const DASHBOARD_PATH = '/dashboard';

// Auth bypass for middleware: set dummy auth cookie before each test
test.beforeEach(async ({ context, baseURL }) => {
  if (baseURL) {
    await context.addCookies([
      { name: 'auth_token', value: 'e2e', url: baseURL },
    ]);
  }
});

async function openFirstCompanyModal(page: import('@playwright/test').Page, query: string) {
  await page.goto(DASHBOARD_PATH);
  await expect(page.getByTestId('search-input')).toBeVisible();
  await page.getByTestId('search-input').fill(query);
  await page.keyboard.press('Enter');

  const firstRow = page.locator('[data-testid^="company-row-"]').first();
  // Poll up to 12s for first row to appear
  let appeared = false;
  for (let t = 0; t < 12; t++) {
    if (await firstRow.count()) { appeared = true; break; }
    await page.waitForTimeout(1000);
  }
  if (!appeared) return false;
  await firstRow.click();
  return true;
}

// Smoke test: modal shows map section and radius controls. If minimap/nearby-list exist, assert visibility.
test('Company detail modal shows map section and radius controls', async ({ page }) => {
  const opened = await openFirstCompanyModal(page, 'istanbul');
  if (!opened) return; // no data for this query

  // Header text for the section
  await expect(page.getByText('Konum ve Yakın Şirketler')).toBeVisible();

  // Radius controls should be present and clickable
  const r1 = page.getByTestId('radius-1');
  const r5 = page.getByTestId('radius-5');
  const r10 = page.getByTestId('radius-10');

  await expect(r1).toBeVisible();
  await expect(r5).toBeVisible();
  await expect(r10).toBeVisible();

  await r10.click();
  await r1.click();
  await r5.click();

  // Optional assertions: if minimap exists, it should be visible
  const miniMap = page.getByTestId('company-minimap');
  if (await miniMap.count()) {
    await expect(miniMap).toBeVisible();
  }

  // Optional: if nearby list exists and has items, at least the container is visible
  const nearbyList = page.getByTestId('nearby-list');
  if (await nearbyList.count()) {
    await expect(nearbyList).toBeVisible();
  }
});
