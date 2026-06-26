import { test, expect, request } from '@playwright/test'

const PAID_BASE = 'http://localhost:5175'

const TS = Date.now()

const TEST_USER = {
  name: 'Paid Tier User',
  email: `paid-${TS}@test.com`,
  password: 'testpassword123',
}

const TEAM_2_NAME = `E2E Paid Team 2 ${TS}`
const TEAM_RENAMED = `E2E Paid Renamed ${TS}`

test.describe('Paid tier registration', () => {
  test('can register on paid app and gets paid tier', async ({ page }) => {
    await page.goto(`${PAID_BASE}/register`)
    await page.getByPlaceholder('John Doe').fill(TEST_USER.name)
    await page.getByPlaceholder('you@company.com').fill(TEST_USER.email)
    await page.getByPlaceholder('••••••••').fill(TEST_USER.password)
    await page.getByRole('button', { name: /Create account/i }).click()
    await page.waitForURL('**/dashboard', { timeout: 10000 })

    // User should see "paid tier" in the sidebar
    await expect(page.getByText('paid tier', { exact: true })).toBeVisible()

    // Teams sidebar link should be visible for paid users
    await expect(page.getByRole('link', { name: 'Teams' })).toBeVisible()

    // Team filter dropdown should be visible on dashboard for paid users
    await expect(page.locator('select')).toBeVisible()
  })

  test('registered paid user has paid tier via API', async () => {
    const ctx = await request.newContext()
    const resp = await ctx.post('http://localhost:5200/api/auth/login', {
      data: { email: TEST_USER.email, password: TEST_USER.password },
    })
    expect(resp.ok()).toBeTruthy()
    const data = await resp.json()
    expect(data.user.tier).toBe('paid')
    await ctx.dispose()
  })

  test('paid user can create multiple teams', async ({ page }) => {
    // Login
    await page.goto(`${PAID_BASE}/login`)
    await page.getByPlaceholder('you@company.com').fill(TEST_USER.email)
    await page.getByPlaceholder('••••••••').fill(TEST_USER.password)
    await page.getByRole('button', { name: /Sign in/i }).click()
    await page.waitForURL('**/dashboard', { timeout: 10000 })

    // Navigate to Teams
    await page.getByRole('link', { name: 'Teams' }).click()
    await expect(page).toHaveURL(/\/teams/)

    // Should already have auto-created team
    await expect(page.getByText('Manager').first()).toBeVisible({ timeout: 5000 })

    // Create a second team
    await page.getByRole('button', { name: /New Team/i }).click()
    await page.getByPlaceholder('e.g. Engineering Team').fill(TEAM_2_NAME)
    await page.getByRole('button', { name: 'Create' }).click()

    await expect(page.getByText(TEAM_2_NAME)).toBeVisible({ timeout: 10000 })
  })

  test('paid user can edit a team', async ({ page }) => {
    await page.goto(`${PAID_BASE}/login`)
    await page.getByPlaceholder('you@company.com').fill(TEST_USER.email)
    await page.getByPlaceholder('••••••••').fill(TEST_USER.password)
    await page.getByRole('button', { name: /Sign in/i }).click()
    await page.waitForURL('**/dashboard', { timeout: 10000 })

    await page.getByRole('link', { name: 'Teams' }).click()
    await expect(page).toHaveURL(/\/teams/)

    // Edit the second team created in the previous test
    const editBtn = page.locator('div.bg-white.rounded-xl.border')
      .filter({ has: page.getByText(TEAM_2_NAME) })
      .getByTestId('edit-team')
    await editBtn.click()

    await expect(page.getByText('Edit Team')).toBeVisible()
    await page.getByPlaceholder('e.g. Engineering Team').fill(TEAM_RENAMED)
    await page.getByRole('button', { name: 'Update' }).click()

    await expect(page.getByText(TEAM_RENAMED)).toBeVisible({ timeout: 10000 })
  })

  test('paid user can delete a team', async ({ page }) => {
    await page.goto(`${PAID_BASE}/login`)
    await page.getByPlaceholder('you@company.com').fill(TEST_USER.email)
    await page.getByPlaceholder('••••••••').fill(TEST_USER.password)
    await page.getByRole('button', { name: /Sign in/i }).click()
    await page.waitForURL('**/dashboard', { timeout: 10000 })

    await page.getByRole('link', { name: 'Teams' }).click()
    await expect(page).toHaveURL(/\/teams/)

    page.on('dialog', (dialog) => dialog.accept())
    const deleteBtn = page.locator('div.bg-white.rounded-xl.border')
      .filter({ has: page.getByText(TEAM_RENAMED) })
      .getByTestId('delete-team')
    await deleteBtn.click()

    await expect(page.getByText(TEAM_RENAMED)).not.toBeVisible({ timeout: 10000 })
  })

  test('paid user can create a project', async ({ page }) => {
    await page.goto(`${PAID_BASE}/login`)
    await page.getByPlaceholder('you@company.com').fill(TEST_USER.email)
    await page.getByPlaceholder('••••••••').fill(TEST_USER.password)
    await page.getByRole('button', { name: /Sign in/i }).click()
    await page.waitForURL('**/dashboard', { timeout: 10000 })

    await page.getByRole('link', { name: 'Projects' }).click()
    await expect(page).toHaveURL(/\/projects/)

    await page.getByRole('button', { name: /New Project/i }).click()
    await page.getByPlaceholder('Project name').fill(`E2E Paid Project ${TS}`)
    await page.getByPlaceholder('Project description').fill('Created in paid tier')
    await page.getByRole('button', { name: 'Create' }).click()

    await expect(page.getByText(`E2E Paid Project ${TS}`)).toBeVisible({ timeout: 10000 })
  })

  test('paid user can assign formula to project', async ({ page }) => {
    await page.goto(`${PAID_BASE}/login`)
    await page.getByPlaceholder('you@company.com').fill(TEST_USER.email)
    await page.getByPlaceholder('••••••••').fill(TEST_USER.password)
    await page.getByRole('button', { name: /Sign in/i }).click()
    await page.waitForURL('**/dashboard', { timeout: 10000 })

    await page.getByRole('link', { name: 'Projects' }).click()
    await page.getByText(`E2E Paid Project ${TS}`).click()
    await expect(page).toHaveURL(/\/projects\/\d+/)

    await page.getByRole('button', { name: /Assign Formula/i }).click()
    await page.locator('select').selectOption({ index: 1 })
    await page.getByRole('button', { name: 'Assign', exact: true }).click()

    await expect(page.getByText(/1-Year ROI:/i)).toBeVisible({ timeout: 10000 })
  })
})
