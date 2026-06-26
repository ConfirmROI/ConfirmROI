import { test, expect, request } from '@playwright/test'

const TEST_USER = {
  name: 'E2E Projects User',
  email: `e2e-proj-${Date.now()}@test.com`,
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

test.describe('Projects', () => {
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

  test('create a new project', async ({ page }) => {
    await login(page)
    await page.getByRole('link', { name: /Projects/i }).click()
    await expect(page).toHaveURL(/\/projects/)

    await page.getByRole('button', { name: /New Project/i }).click()

    await expect(page.getByText('Create New Project')).toBeVisible()

    await page.getByPlaceholder('Project name').fill('E2E Test Project')
    await page.getByPlaceholder('Project description').fill('Created by Playwright')
    await page.getByRole('button', { name: 'Create' }).click()

    await expect(page.getByText('E2E Test Project')).toBeVisible({ timeout: 10000 })
  })

  test('search projects', async ({ page }) => {
    await login(page)
    await page.getByRole('link', { name: /Projects/i }).click()

    await page.getByPlaceholder('Search projects...').fill('E2E Test')
    await expect(page.getByText('E2E Test Project')).toBeVisible()

    await page.getByPlaceholder('Search projects...').fill('nonexistent')
    await expect(page.getByText('No projects found')).toBeVisible()
  })

  test('project detail page loads', async ({ page }) => {
    await login(page)
    await page.getByRole('link', { name: /Projects/i }).click()

    await page.getByText('E2E Test Project').click()
    await expect(page).toHaveURL(/\/projects\/\d+/)
    await expect(page.getByText('E2E Test Project')).toBeVisible()
    await expect(page.getByText('Value Formulas')).toBeVisible()
    await expect(page.getByText('No formulas assigned yet')).toBeVisible()
  })

  test('project detail back button', async ({ page }) => {
    await login(page)
    await page.getByRole('link', { name: /Projects/i }).click()
    await page.getByText('E2E Test Project').click()

    await page.getByText('Back to Projects').click()
    await expect(page).toHaveURL(/\/projects/)
  })

  test('edit a project', async ({ page }) => {
    await login(page)
    await page.getByRole('link', { name: /Projects/i }).click()
    await page.getByText('E2E Test Project').click()
    await expect(page).toHaveURL(/\/projects\/\d+/)

    await page.getByTestId('edit-project').click()
    await expect(page.getByText('Edit Project')).toBeVisible()

    await page.getByPlaceholder('Project name').fill('E2E Edited Project')
    await page.getByPlaceholder('Project description').fill('Updated by Playwright')
    await page.getByRole('button', { name: 'Update' }).click()

    await expect(page.getByText('E2E Edited Project')).toBeVisible({ timeout: 5000 })
    await expect(page.getByText('Updated by Playwright')).toBeVisible()
  })

  test('delete a project', async ({ page }) => {
    await login(page)
    await page.getByRole('link', { name: /Projects/i }).click()
    await page.getByText('E2E Edited Project').click()
    await expect(page).toHaveURL(/\/projects\/\d+/)

    page.on('dialog', (dialog) => dialog.accept())
    await page.getByTestId('delete-project').click()

    await expect(page).toHaveURL(/\/projects/, { timeout: 10000 })
    await expect(page.getByText('E2E Edited Project')).not.toBeVisible({ timeout: 5000 })
  })
})
