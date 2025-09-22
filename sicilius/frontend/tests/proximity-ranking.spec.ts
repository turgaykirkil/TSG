import { test, expect } from '@playwright/test';

const DASHBOARD_PATH = '/dashboard';
const QUERY = '496712 ankara';

// Auth bypass
test.beforeEach(async ({ context, baseURL, page }) => {
  if (baseURL) {
    await context.addCookies([{ name: 'auth_token', value: 'e2e', url: baseURL }]);
  }

  // Mock backend response only for our specific mixed query
  const encoded = encodeURIComponent(QUERY);
  await page.route('**/api/v1/search/all*', async (route) => {
    const url = route.request().url();
    if (url.includes(`q=${encoded}`)) {
      const body = {
        companies: [
          {
            id: 'near-1',
            unvan: 'Ankara Yakın Eşleşme Ltd. Şti.',
            sicil_no: '496712',
            address: 'Ankara Çankaya',
            sicil_mudurluk: 'Ankara Ticaret Sicil Müdürlüğü',
            match_strength: 99,
          },
          {
            id: 'far-1',
            unvan: 'Uzak Eşleşme A.Ş.',
            sicil_no: '496712',
            address: 'İzmir Bayraklı',
            sicil_mudurluk: 'İzmir Ticaret Sicil Müdürlüğü',
            match_strength: 72,
          },
        ],
        persons: [],
        history: [],
        total_matches: 2,
        limit: 20,
        next_cursor: null,
        next_offset: null,
      };
      await route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(body) });
    } else {
      await route.continue();
    }
  });
});

test('Proximity ranking brings the near match to the top', async ({ page }) => {
  await page.goto(DASHBOARD_PATH);

  await expect(page.getByTestId('search-input')).toBeVisible();
  await page.getByTestId('search-input').fill(QUERY);
  await page.keyboard.press('Enter');

  const firstRow = page.getByTestId('company-row-0');
  await expect(firstRow).toBeVisible();
  await expect(firstRow.getByRole('cell').first()).toContainText('Ankara Yakın Eşleşme');
  await expect(firstRow.getByTestId('near-badge')).toBeVisible();

  // Second row should be the far match
  const secondRow = page.getByTestId('company-row-1');
  await expect(secondRow.getByRole('cell').first()).toContainText('Uzak Eşleşme');
  await expect(secondRow.getByTestId('near-badge')).toHaveCount(0);
});
