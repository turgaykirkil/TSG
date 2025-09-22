import { test, expect } from '@playwright/test';

const DASHBOARD_PATH = '/dashboard';
const QUERY_MIXED = '496712 ankara';

// Auth bypass for middleware
test.beforeEach(async ({ context, baseURL }) => {
  if (baseURL) {
    await context.addCookies([
      { name: 'auth_token', value: 'e2e', url: baseURL },
    ]);
  }
});

test('Mixed query does not cause infinite fetch and at most one next-page fetch', async ({ page }) => {
  const encoded = encodeURIComponent(QUERY_MIXED);
  let reqCount = 0;
  page.on('request', (req) => {
    const url = req.url();
    if (url.includes('/api/v1/search/all') && url.includes(`q=${encoded}`)) {
      reqCount += 1;
    }
  });

  await page.goto(DASHBOARD_PATH);
  await expect(page.getByTestId('search-input')).toBeVisible();
  await page.getByTestId('search-input').fill(QUERY_MIXED);
  await page.keyboard.press('Enter');

  // Wait a bit for initial request and render
  await page.waitForTimeout(1500);
  expect(reqCount).toBeGreaterThanOrEqual(1);

  const sentinel = page.getByTestId('infinite-sentinel');
  const hasSentinel = await sentinel.isVisible().catch(() => false);

  const before = reqCount;
  if (hasSentinel) {
    await sentinel.scrollIntoViewIfNeeded();
    await page.waitForTimeout(1500);
    const delta = reqCount - before;
    expect(delta).toBeLessThanOrEqual(1);
  } else {
    // No sentinel -> there should be no further /all requests caused by bottom scrolling
    await page.evaluate(() => {
      try { window.scrollTo(0, document.body.scrollHeight); } catch {}
    });
    await page.waitForTimeout(1500);
    const delta = reqCount - before;
    expect(delta).toBe(0);
  }
});
