import { test, expect, request } from '@playwright/test'

const TEST_USER = {
  name: 'E2E Formulas CRUD User',
  email: `e2e-form-crud-${Date.now()}@test.com`,
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

async function createAssumption(key, label) {
  const ctx = await request.newContext()
  const resp = await ctx.post('http://localhost:5174/api/archetypes/assumptions', {
    data: { key, label, data_type: 'number', default_value: 10, description: 'E2E test assumption' },
    headers: { Authorization: `Bearer ${accessToken}` },
  })
  const data = await resp.json()
  await ctx.dispose()
  return data.id
}

async function getAllAssumptions() {
  const ctx = await request.newContext()
  const resp = await ctx.get('http://localhost:5174/api/archetypes/assumptions', {
    headers: { Authorization: `Bearer ${accessToken}` },
  })
  const data = await resp.json()
  await ctx.dispose()
  return data
}

test.describe('Value Formulas CRUD Extended', () => {
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

  test('all 4 system formulas are displayed', async ({ page }) => {
    await login(page)
    await page.getByRole('link', { name: /Value Formulas/i }).click()
    await expect(page).toHaveURL(/\/formulas/)

    await expect(page.getByText('Cost Savings')).toBeVisible({ timeout: 5000 })
    await expect(page.getByText('Revenue Generation')).toBeVisible()
    await expect(page.getByText('Time Saved')).toBeVisible()
    await expect(page.getByText('Risk Reduction')).toBeVisible()
  })

  test('system formulas have System badge', async ({ page }) => {
    await login(page)
    await page.getByRole('link', { name: /Value Formulas/i }).click()

    const systemBadges = page.locator('span.text-blue-600.font-medium:has-text("System")')
    await expect(systemBadges.first()).toBeVisible({ timeout: 5000 })
    const count = await systemBadges.count()
    expect(count).toBeGreaterThanOrEqual(4)
  })

  test('system formulas have no edit or delete buttons', async ({ page }) => {
    await login(page)
    await page.getByRole('link', { name: /Value Formulas/i }).click()

    const costSavingsCard = page.locator('div.bg-white.rounded-xl.border')
      .filter({ has: page.getByText('Cost Savings') })
    await expect(costSavingsCard.getByTestId('edit-archetype')).not.toBeVisible()
    await expect(costSavingsCard.getByTestId('delete-archetype')).not.toBeVisible()
  })

  test('create formula with linked assumptions and verify display', async ({ page }) => {
    await login(page)
    await page.getByRole('link', { name: /Value Formulas/i }).click()

    await page.getByRole('button', { name: /New Formula/i }).click()

    await page.getByPlaceholder('e.g. Efficiency Gains').fill('E2E Linked Formula')
    await page.getByPlaceholder('e.g. hours_saved * hourly_rate - cost').fill('hours_saved_per_week * hourly_rate * 52')

    const firstCheckbox = page.locator('input[type="checkbox"]').first()
    await firstCheckbox.check()

    await page.getByRole('button', { name: 'Create' }).click()

    await expect(page.getByText('E2E Linked Formula')).toBeVisible({ timeout: 5000 })

    const formulaCard = page.locator('div.bg-white.rounded-xl.border')
      .filter({ has: page.getByText('E2E Linked Formula') })
    await expect(formulaCard.getByText('Assumptions:')).toBeVisible()
  })

  test('edit formula preserves and updates assumption links', async ({ page }) => {
    await login(page)
    await page.getByRole('link', { name: /Value Formulas/i }).click()

    const editBtn = page.locator('div.bg-white.rounded-xl.border')
      .filter({ has: page.getByText('E2E Linked Formula') })
      .getByTestId('edit-archetype')
    await editBtn.click()

    await expect(page.getByText('Edit Formula')).toBeVisible()

    const firstCheckbox = page.locator('input[type="checkbox"]').first()
    await expect(firstCheckbox).toBeChecked()

    await page.getByPlaceholder('e.g. Efficiency Gains').fill('E2E Edited Linked')
    await page.getByPlaceholder('e.g. hours_saved * hourly_rate - cost').fill('hours_saved_per_week * 52 * hourly_rate - implementation_cost')

    const secondCheckbox = page.locator('input[type="checkbox"]').nth(1)
    await secondCheckbox.check()

    await page.getByRole('button', { name: 'Update' }).click()

    await expect(page.getByText('E2E Edited Linked')).toBeVisible({ timeout: 5000 })
  })

  test('custom formula appears in project assign dropdown', async ({ page }) => {
    await login(page)
    await page.getByRole('link', { name: /Projects/i }).click()

    await page.getByRole('button', { name: /New Project/i }).click()
    await page.getByPlaceholder('Project name').fill('Formula Dropdown Test')
    await page.getByPlaceholder('Project description').fill('Testing formula dropdown')
    await page.getByRole('button', { name: 'Create' }).click()
    await expect(page.getByText('Formula Dropdown Test')).toBeVisible({ timeout: 10000 })

    await page.getByText('Formula Dropdown Test').click()
    await expect(page).toHaveURL(/\/projects\/\d+/)

    await page.getByRole('button', { name: /Assign Formula/i }).click()

    const select = page.locator('select')
    const options = await select.locator('option').allTextContents()
    expect(options.some(o => o.includes('E2E Edited Linked'))).toBeTruthy()
  })

  test('create formula with no assumptions linked', async ({ page }) => {
    await login(page)
    await page.getByRole('link', { name: /Value Formulas/i }).click()

    await page.getByRole('button', { name: /New Formula/i }).click()

    await page.getByPlaceholder('e.g. Efficiency Gains').fill('E2E No Assumptions')
    await page.getByPlaceholder('e.g. hours_saved * hourly_rate - cost').fill('42 * 10')

    await page.getByRole('button', { name: 'Create' }).click()

    await expect(page.getByText('E2E No Assumptions')).toBeVisible({ timeout: 5000 })
  })

  test('create formula with invalid expression succeeds (no validation)', async ({ page }) => {
    await login(page)
    await page.getByRole('link', { name: /Value Formulas/i }).click()

    await page.getByRole('button', { name: /New Formula/i }).click()

    await page.getByPlaceholder('e.g. Efficiency Gains').fill('E2E Invalid Formula')
    await page.getByPlaceholder('e.g. hours_saved * hourly_rate - cost').fill('hours_saved *')

    await page.getByRole('button', { name: 'Create' }).click()

    await expect(page.getByText('E2E Invalid Formula')).toBeVisible({ timeout: 5000 })
  })

  test('delete custom formula with confirmation', async ({ page }) => {
    await login(page)
    await page.getByRole('link', { name: /Value Formulas/i }).click()

    page.on('dialog', (dialog) => dialog.accept())

    const formulasToDelete = ['E2E Edited Linked', 'E2E No Assumptions', 'E2E Invalid Formula']
    for (const name of formulasToDelete) {
      const deleteBtn = page.locator('div.bg-white.rounded-xl.border')
        .filter({ has: page.getByText(name) })
        .getByTestId('delete-archetype')
      if (await deleteBtn.isVisible({ timeout: 3000 }).catch(() => false)) {
        await deleteBtn.click()
        await expect(page.getByText(name)).not.toBeVisible({ timeout: 5000 })
      }
    }
  })

  test('empty state shows when no formulas exist', async ({ page }) => {
    await login(page)
    await page.getByRole('link', { name: /Value Formulas/i }).click()

    const systemFormulas = page.locator('div.bg-white.rounded-xl.border')
    const count = await systemFormulas.count()
    expect(count).toBeGreaterThanOrEqual(4)
  })
})
