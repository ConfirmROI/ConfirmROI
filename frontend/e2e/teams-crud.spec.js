import { test, expect } from '@playwright/test'

const TEST_USER = {
  name: 'E2E Teams CRUD User',
  email: `e2e-teams-crud-${Date.now()}@test.com`,
  password: 'testpassword123',
}

test.describe('Teams UI (Free Tier)', () => {
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

  async function login(page) {
    await page.goto('/login')
    await page.getByPlaceholder('you@company.com').fill(TEST_USER.email)
    await page.getByPlaceholder('••••••••').fill(TEST_USER.password)
    await page.getByRole('button', { name: /Sign in/i }).click()
    await page.waitForURL('**/dashboard', { timeout: 10000 })
  }

  test('free tier accessing /teams via direct URL redirects to dashboard', async ({ page }) => {
    await login(page)
    await page.goto('/teams')
    await page.waitForLoadState('networkidle')
    await expect(page).toHaveURL(/\/dashboard/)
  })

  test('free tier /teams redirect does not show Teams sidebar link', async ({ page }) => {
    await login(page)
    await page.goto('/teams')
    await page.waitForLoadState('networkidle')

    const teamsLink = page.locator('aside').getByRole('link', { name: 'Teams' })
    await expect(teamsLink).not.toBeVisible({ timeout: 10000 })
  })

  test('free tier sidebar hides Teams link on dashboard', async ({ page }) => {
    await login(page)
    await expect(page.getByRole('link', { name: 'Teams' })).not.toBeVisible()
  })

  test('free tier sidebar hides Teams link on formulas page', async ({ page }) => {
    await login(page)
    await page.getByRole('link', { name: /Value Formulas/i }).click()
    await expect(page).toHaveURL(/\/formulas/)

    const teamsLink = page.locator('aside').getByRole('link', { name: 'Teams' })
    await expect(teamsLink).not.toBeVisible()
  })

  test('free tier sidebar hides Teams link on assumptions page', async ({ page }) => {
    await login(page)
    await page.getByRole('link', { name: /Assumptions/i }).click()
    await expect(page).toHaveURL(/\/assumptions/)

    const teamsLink = page.locator('aside').getByRole('link', { name: 'Teams' })
    await expect(teamsLink).not.toBeVisible()
  })

  test('free tier sidebar hides Teams link on projects page', async ({ page }) => {
    await login(page)
    await page.getByRole('link', { name: /Projects/i }).click()
    await expect(page).toHaveURL(/\/projects/)

    const teamsLink = page.locator('aside').getByRole('link', { name: 'Teams' })
    await expect(teamsLink).not.toBeVisible()
  })
})
