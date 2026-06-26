import { test, expect, request } from '@playwright/test'

const TEST_USER = {
  name: 'E2E Teams User',
  email: `e2e-teams-${Date.now()}@test.com`,
  password: 'testpassword123',
}

let accessToken = ''

async function loginAndGetToken() {
  const ctx = await request.newContext()
  const resp = await ctx.post('http://localhost:5174/api/auth/login', {
    data: { email: TEST_USER.email, password: TEST_USER.password },
  })
  const data = await resp.json()
  accessToken = data.access_token
  await ctx.dispose()
}

test.describe('Teams & Auto-creation (Free Tier)', () => {
  test.beforeAll(async ({ browser }) => {
    const page = await browser.newPage()
    await page.goto('/register')
    await page.getByPlaceholder('John Doe').fill(TEST_USER.name)
    await page.getByPlaceholder('you@company.com').fill(TEST_USER.email)
    await page.getByPlaceholder('••••••••').fill(TEST_USER.password)
    await page.getByRole('button', { name: /Create account/i }).click()
    await page.waitForURL('**/dashboard', { timeout: 10000 })
    await page.close()

    await loginAndGetToken()
  })

  async function login(page) {
    await page.goto('/login')
    await page.getByPlaceholder('you@company.com').fill(TEST_USER.email)
    await page.getByPlaceholder('••••••••').fill(TEST_USER.password)
    await page.getByRole('button', { name: /Sign in/i }).click()
    await page.waitForURL('**/dashboard', { timeout: 10000 })
  }

  test('free tier does not show Teams sidebar link', async ({ page }) => {
    await login(page)
    await expect(page.getByRole('link', { name: 'Teams' })).not.toBeVisible()
  })

  test('free tier teams API returns 404', async () => {
    const ctx = await request.newContext()
    const resp = await ctx.get('http://localhost:5174/api/teams', {
      headers: { Authorization: `Bearer ${accessToken}` },
    })
    expect(resp.status()).toBe(404)
    await ctx.dispose()
  })

  test('can create project without manually creating a team', async ({ page }) => {
    await login(page)
    await page.getByRole('link', { name: /Projects/i }).click()
    await expect(page).toHaveURL(/\/projects/)

    await page.getByRole('button', { name: /New Project/i }).click()
    await expect(page.getByText('Create New Project')).toBeVisible()

    await page.getByPlaceholder('Project name').fill('Auto Team Project')
    await page.getByPlaceholder('Project description').fill('Created without manual team creation')
    await page.getByRole('button', { name: 'Create' }).click()

    await expect(page.getByText('Auto Team Project')).toBeVisible({ timeout: 10000 })
  })
})
