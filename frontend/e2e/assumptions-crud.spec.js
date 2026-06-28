import { test, expect, request } from '@playwright/test'

const TEST_USER = {
  name: 'E2E Assumptions CRUD User',
  email: `e2e-assump-crud-${Date.now()}@test.com`,
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

async function createAssumptionViaAPI(key, label, dataType, defaultValue) {
  const ctx = await request.newContext()
  const resp = await ctx.post('http://localhost:5174/api/formulas/assumptions', {
    data: {
      key,
      label,
      data_type: dataType,
      default_value: defaultValue,
      description: 'E2E test assumption',
    },
    headers: { Authorization: `Bearer ${accessToken}` },
  })
  const data = await resp.json()
  await ctx.dispose()
  return data
}

test.describe('Assumptions CRUD Extended', () => {
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

  test('all 9 system assumptions are displayed', async ({ page }) => {
    await login(page)
    await page.getByRole('link', { name: /Assumptions/i }).click()
    await expect(page).toHaveURL(/\/assumptions/)
    await page.waitForLoadState('networkidle')

    const systemAssumptionKeys = [
      'monthly_cost_before',
      'monthly_cost_after',
      'years',
      'implementation_cost',
      'estimated_monthly_revenue',
      'hours_saved_per_week',
      'hourly_rate',
      'risk_probability',
      'risk_impact',
    ]

    for (const key of systemAssumptionKeys) {
      await expect(page.getByText(`(${key})`, { exact: true })).toBeVisible({ timeout: 5000 })
    }
  })

  test('system assumptions have System badge', async ({ page }) => {
    await login(page)
    await page.getByRole('link', { name: /Assumptions/i }).click()
    await page.waitForLoadState('networkidle')

    const systemBadges = page.locator('span.text-blue-600.font-medium:has-text("System")')
    await expect(systemBadges.first()).toBeVisible({ timeout: 5000 })
    const count = await systemBadges.count()
    expect(count).toBeGreaterThanOrEqual(9)
  })

  test('system assumptions can be edited but not deleted', async ({ page }) => {
    await login(page)
    await page.getByRole('link', { name: /Assumptions/i }).click()
    await page.waitForLoadState('networkidle')

    const monthlyCostCard = page.locator('div.flex.items-center.justify-between.p-4')
      .filter({ has: page.getByText('Monthly Cost Before', { exact: true }) })

    await expect(monthlyCostCard.getByTestId('edit-assumption')).toBeVisible()
    await expect(monthlyCostCard.getByTestId('delete-assumption')).not.toBeVisible()
  })

  test('create assumption with currency data type', async ({ page }) => {
    await login(page)
    await page.getByRole('link', { name: /Assumptions/i }).click()
    await page.waitForLoadState('networkidle')

    await page.getByRole('button', { name: /New Assumption/i }).click()
    await expect(page.getByText('Create Assumption')).toBeVisible()

    const createForm = page.locator('.bg-white.rounded-xl.border:has-text("Create Assumption")')
    await createForm.getByPlaceholder('e.g. hours_saved').fill('e2e_currency_key')
    await createForm.getByPlaceholder('e.g. Hours Saved').fill('E2E Currency Assumption')
    await createForm.locator('select').selectOption('currency')
    await createForm.locator('input[type="number"]').fill('5000')
    await createForm.getByPlaceholder('Optional description').fill('Currency type test')

    await createForm.getByRole('button', { name: 'Create' }).click()

    await expect(page.getByText('E2E Currency Assumption', { exact: true })).toBeVisible({ timeout: 10000 })
    const currencyCard = page.locator('div.flex.items-center.justify-between.p-4')
      .filter({ has: page.getByText('E2E Currency Assumption', { exact: true }) })
    await expect(currencyCard.locator('span.bg-gray-200')).toHaveText('currency')
  })

  test('create assumption with percentage data type', async ({ page }) => {
    await login(page)
    await page.getByRole('link', { name: /Assumptions/i }).click()
    await page.waitForLoadState('networkidle')

    await page.getByRole('button', { name: /New Assumption/i }).click()

    const createForm = page.locator('.bg-white.rounded-xl.border:has-text("Create Assumption")')
    await createForm.getByPlaceholder('e.g. hours_saved').fill('e2e_pct_key')
    await createForm.getByPlaceholder('e.g. Hours Saved').fill('E2E Percentage Assumption')
    await createForm.locator('select').selectOption('percentage')
    await createForm.locator('input[type="number"]').fill('75')
    await createForm.getByPlaceholder('Optional description').fill('Percentage type test')

    await createForm.getByRole('button', { name: 'Create' }).click()

    await expect(page.getByText('E2E Percentage Assumption', { exact: true })).toBeVisible({ timeout: 10000 })
    const pctCard = page.locator('div.flex.items-center.justify-between.p-4')
      .filter({ has: page.getByText('E2E Percentage Assumption', { exact: true }) })
    await expect(pctCard.locator('span.bg-gray-200')).toHaveText('percentage')
  })

  test('edit custom assumption default value', async ({ page }) => {
    await loginAndGetToken()
    await createAssumptionViaAPI('e2e_edit_default', 'Edit Default Test', 'number', 10)

    await login(page)
    await page.getByRole('link', { name: /Assumptions/i }).click()
    await page.waitForLoadState('networkidle')

    await expect(page.getByText('Edit Default Test', { exact: true })).toBeVisible({ timeout: 5000 })
    const editCard = page.locator('div.flex.items-center.justify-between.p-4')
      .filter({ has: page.getByText('Edit Default Test', { exact: true }) })
    await expect(editCard.getByText('Default: 10')).toBeVisible()

    const editBtn = editCard.getByTestId('edit-assumption')
    await editBtn.click()

    await expect(page.getByText('Edit Assumption')).toBeVisible()
    const editForm = page.locator('.bg-white.rounded-xl.border:has-text("Edit Assumption")')
    await editForm.locator('input[type="number"]').fill('42')
    await editForm.getByRole('button', { name: 'Update' }).click()

    await expect(editCard.getByText('Default: 42')).toBeVisible({ timeout: 5000 })
  })

  test('edit system assumption label', async ({ page }) => {
    await login(page)
    await page.getByRole('link', { name: /Assumptions/i }).click()
    await page.waitForLoadState('networkidle')

    const riskProbCard = page.locator('div.flex.items-center.justify-between.p-4')
      .filter({ has: page.getByText('(risk_probability)', { exact: true }) })

    await riskProbCard.getByTestId('edit-assumption').click()
    await expect(page.getByText('Edit Assumption')).toBeVisible()

    const editForm = page.locator('.bg-white.rounded-xl.border:has-text("Edit Assumption")')
    await editForm.getByPlaceholder('e.g. Hours Saved').fill('Risk Probability Edited')
    await editForm.getByRole('button', { name: 'Update' }).click()

    await expect(page.getByText('Risk Probability Edited', { exact: true })).toBeVisible({ timeout: 5000 })

    const editedCard = page.locator('div.flex.items-center.justify-between.p-4')
      .filter({ has: page.getByText('Risk Probability Edited', { exact: true }) })
    await expect(editedCard.getByTestId('delete-assumption')).not.toBeVisible()
  })

  test('new custom assumption appears in formula checkbox list', async ({ page }) => {
    await loginAndGetToken()
    await createAssumptionViaAPI('e2e_formula_link', 'Formula Link Test', 'number', 5)

    await login(page)
    await page.getByRole('link', { name: /Value Formulas/i }).click()
    await page.waitForLoadState('networkidle')

    await page.getByRole('button', { name: /New Formula/i }).click()

    const assumptionList = page.locator('.border.border-gray-200.rounded-lg.p-3')
    await expect(assumptionList.getByText('Formula Link Test')).toBeVisible({ timeout: 5000 })
    await expect(assumptionList.getByText('e2e_formula_link')).toBeVisible()
  })

  test('create assumption with duplicate key succeeds (no validation)', async ({ page }) => {
    await login(page)
    await page.getByRole('link', { name: /Assumptions/i }).click()
    await page.waitForLoadState('networkidle')

    await page.getByRole('button', { name: /New Assumption/i }).click()

    const createForm = page.locator('.bg-white.rounded-xl.border:has-text("Create Assumption")')
    await createForm.getByPlaceholder('e.g. hours_saved').fill('hours_saved_per_week')
    await createForm.getByPlaceholder('e.g. Hours Saved').fill('Duplicate Key Test')
    await createForm.getByRole('button', { name: 'Create' }).click()

    await expect(page.getByText('Duplicate Key Test', { exact: true })).toBeVisible({ timeout: 10000 })
  })

  test('delete custom assumption removes it from list', async ({ page }) => {
    await loginAndGetToken()
    const created = await createAssumptionViaAPI('e2e_delete_test', 'Delete Me Extended', 'number', 0)

    await login(page)
    await page.getByRole('link', { name: /Assumptions/i }).click()
    await page.waitForLoadState('networkidle')

    await expect(page.getByText('Delete Me Extended', { exact: true })).toBeVisible({ timeout: 5000 })

    page.on('dialog', (dialog) => dialog.accept())
    const deleteBtn = page.locator('div.flex.items-center.justify-between.p-4')
      .filter({ has: page.getByText('Delete Me Extended', { exact: true }) })
      .getByTestId('delete-assumption')
    await deleteBtn.click()

    await expect(page.getByText('Delete Me Extended', { exact: true })).not.toBeVisible({ timeout: 5000 })
  })

  test('cleanup: delete all custom assumptions created during tests', async ({ page }) => {
    await login(page)
    await page.getByRole('link', { name: /Assumptions/i }).click()
    await page.waitForLoadState('networkidle')

    page.on('dialog', (dialog) => dialog.accept())

    const customLabels = [
      'E2E Currency Assumption',
      'E2E Percentage Assumption',
      'Edit Default Test',
      'Formula Link Test',
      'Duplicate Key Test',
    ]

    for (const label of customLabels) {
      const card = page.locator('div.flex.items-center.justify-between.p-4')
        .filter({ has: page.getByText(label, { exact: true }) })
      const deleteBtn = card.getByTestId('delete-assumption')
      if (await deleteBtn.isVisible({ timeout: 3000 }).catch(() => false)) {
        await deleteBtn.click()
        await expect(page.getByText(label, { exact: true })).not.toBeVisible({ timeout: 5000 })
      }
    }
  })
})
