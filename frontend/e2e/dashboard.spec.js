import { test, expect } from '@playwright/test'

const TEST_USER = {
  name: 'E2E Dashboard User',
  email: `e2e-dash-${Date.now()}@test.com`,
  password: 'testpassword123',
}

test.describe('Dashboard', () => {
  test.beforeAll(async ({ browser }) => {
    const page = await browser.newPage()
    await page.goto('/register')
    await page.getByPlaceholder('John Doe').fill(TEST_USER.name)
    await page.getByPlaceholder('you@company.com').fill(TEST_USER.email)
    await page.getByPlaceholder('••••••••').fill(TEST_USER.password)
    await page.getByRole('button', { name: /Create account/i }).click()
    await page.waitForURL('**/dashboard', { timeout: 10000 })
    await page.close()
  })

  test('dashboard shows summary cards and navigation', async ({ page }) => {
    await page.goto('/login')
    await page.getByPlaceholder('you@company.com').fill(TEST_USER.email)
    await page.getByPlaceholder('••••••••').fill(TEST_USER.password)
    await page.getByRole('button', { name: /Sign in/i }).click()
    await page.waitForURL('**/dashboard', { timeout: 10000 })

    await expect(page.getByRole('heading', { name: 'Dashboard' })).toBeVisible()
    await expect(page.getByText('Total Projects')).toBeVisible()
    await expect(page.getByText('Total ROI')).toBeVisible()
    await expect(page.locator('aside').getByText('Value Formulas')).toBeVisible()
  })

  test('sidebar navigation works', async ({ page }) => {
    await page.goto('/login')
    await page.getByPlaceholder('you@company.com').fill(TEST_USER.email)
    await page.getByPlaceholder('••••••••').fill(TEST_USER.password)
    await page.getByRole('button', { name: /Sign in/i }).click()
    await page.waitForURL('**/dashboard', { timeout: 10000 })

    await page.getByRole('link', { name: /Projects/i }).click()
    await expect(page).toHaveURL(/\/projects/)

    await page.getByRole('link', { name: /Value Formulas/i }).click()
    await expect(page).toHaveURL(/\/formulas/)

    await page.goto('/dashboard')
    await expect(page).toHaveURL(/\/dashboard/)
  })

  test('sidebar does not show logout button', async ({ page }) => {
    await page.goto('/login')
    await page.getByPlaceholder('you@company.com').fill(TEST_USER.email)
    await page.getByPlaceholder('••••••••').fill(TEST_USER.password)
    await page.getByRole('button', { name: /Sign in/i }).click()
    await page.waitForURL('**/dashboard', { timeout: 10000 })

    await expect(page.locator('aside button:has(svg)')).toHaveCount(0)
  })
})
