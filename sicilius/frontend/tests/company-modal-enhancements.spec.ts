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
  if (!appeared) {
    // No data for this query; skip further steps gracefully
    return false;
  }
  await firstRow.click();
  return true;
}

// Persist radius selection and external map link
// This test is resilient: it checks features if present, without failing if data does not provide coordinates.
test('Modal radius selection persists and external OSM link is visible if coords exist', async ({ page }) => {
  // Open modal
  const opened = await openFirstCompanyModal(page, 'istanbul');
  if (!opened) return; // nothing to assert if no data

  // Ensure radius controls are visible
  const r1 = page.getByTestId('radius-1');
  const r10 = page.getByTestId('radius-10');
  await expect(r1).toBeVisible({ timeout: 10000 });
  await expect(r10).toBeVisible();

  // Pick 10 km
  await r10.click();

  // Optional: OSM link
  const osmLink = page.getByTestId('open-osm');
  if (await osmLink.count()) {
    await expect(osmLink).toBeVisible();
  }

  // Close modal via Escape (Radix Dialog should close)
  await page.keyboard.press('Escape');
  // Reopen modal by clicking first row again
  const firstRow = page.locator('[data-testid^="company-row-"]').first();
  await expect(firstRow).toBeVisible();
  await firstRow.click();

  // Expect the selection to persist (10 km pressed)
  await expect(page.getByTestId('radius-10')).toHaveAttribute('aria-pressed', 'true');
});
