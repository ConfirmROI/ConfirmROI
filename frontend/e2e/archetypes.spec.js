import { test, expect } from '@playwright/test'

const TEST_USER = {
  name: 'E2E Formulas User',
  email: `e2e-form-${Date.now()}@test.com`,
  password: 'testpassword123',
}

test.describe('Value Formulas', () => {
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

  test('formulas page shows system formulas', async ({ page }) => {
    await login(page)
    await page.getByRole('link', { name: /Value Formulas/i }).click()
    await expect(page).toHaveURL(/\/formulas/)

    await expect(page.getByRole('heading', { name: 'Value Formulas' })).toBeVisible()
    await expect(page.getByText('System').first()).toBeVisible({ timeout: 5000 })
  })

  test('create custom formula', async ({ page }) => {
    await login(page)
    await page.getByRole('link', { name: /Value Formulas/i }).click()

    await page.getByRole('button', { name: /New Formula/i }).click()
    await expect(page.getByText('Create Custom Formula')).toBeVisible()

    await page.getByPlaceholder('e.g. Efficiency Gains').fill('E2E Custom Formula')
    await page.getByPlaceholder('e.g. hours_saved * hourly_rate - cost').fill('hours * rate')
    await page.getByRole('button', { name: 'Create' }).click()

    await expect(page.getByText('E2E Custom Formula')).toBeVisible({ timeout: 5000 })
    await expect(page.getByText('Custom').first()).toBeVisible()
  })

  test('create formula with assumptions', async ({ page }) => {
    await login(page)
    await page.getByRole('link', { name: /Value Formulas/i }).click()

    await page.getByRole('button', { name: /New Formula/i }).click()

    await page.getByPlaceholder('e.g. Efficiency Gains').fill('E2E With Assumptions')
    await page.getByPlaceholder('e.g. hours_saved * hourly_rate - cost').fill('years * implementation_cost')

    await page.locator('input[type="checkbox"]').first().check()

    await page.getByRole('button', { name: 'Create' }).click()

    await expect(page.getByText('E2E With Assumptions')).toBeVisible({ timeout: 5000 })
  })

  test('edit a custom formula', async ({ page }) => {
    await login(page)
    await page.getByRole('link', { name: /Value Formulas/i }).click()

    // Find the custom formula created in an earlier test and edit it
    const editBtn = page.locator('div.bg-white.rounded-xl.border')
      .filter({ has: page.getByText('E2E Custom Formula') })
      .getByTestId('edit-archetype')
    await editBtn.click()

    await expect(page.getByText('Edit Formula')).toBeVisible()
    await page.getByPlaceholder('e.g. Efficiency Gains').fill('E2E Edited Formula')
    await page.getByPlaceholder('e.g. hours_saved * hourly_rate - cost').fill('rate * 2')
    await page.getByRole('button', { name: 'Update' }).click()

    await expect(page.getByText('E2E Edited Formula')).toBeVisible({ timeout: 5000 })
  })

  test('delete a custom formula', async ({ page }) => {
    await login(page)
    await page.getByRole('link', { name: /Value Formulas/i }).click()

    page.on('dialog', (dialog) => dialog.accept())
    const deleteBtn = page.locator('div.bg-white.rounded-xl.border')
      .filter({ has: page.getByText('E2E Edited Formula') })
      .getByTestId('delete-archetype')
    await deleteBtn.click()

    await expect(page.getByText('E2E Edited Formula')).not.toBeVisible({ timeout: 5000 })
  })
})
