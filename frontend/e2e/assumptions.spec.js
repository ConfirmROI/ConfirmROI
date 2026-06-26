import { test, expect, request } from '@playwright/test'

const TEST_USER = {
  name: 'E2E Assumptions User',
  email: `e2e-assump-${Date.now()}@test.com`,
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
    data: { key, label, data_type: 'number', default_value: 0, description: '' },
    headers: { Authorization: `Bearer ${accessToken}` },
  })
  const data = await resp.json()
  await ctx.dispose()
  return data.id
}

test.describe('Assumptions', () => {
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

  test('assumptions page shows system assumptions', async ({ page }) => {
    await login(page)
    await page.getByRole('link', { name: /Assumptions/i }).click()
    await expect(page).toHaveURL(/\/assumptions/)

    await expect(page.getByRole('heading', { name: 'Assumptions' })).toBeVisible()
    await expect(page.getByText('System').first()).toBeVisible({ timeout: 5000 })
  })

  test('create a new assumption via UI', async ({ page }) => {
    await login(page)
    await page.getByRole('link', { name: /Assumptions/i }).click()
    await expect(page).toHaveURL(/\/assumptions/)

    await page.getByRole('button', { name: /New Assumption/i }).click()
    await expect(page.getByText('Create Assumption')).toBeVisible()

    await page.getByPlaceholder('e.g. hours_saved').fill('ui_test_key')
    await page.getByPlaceholder('e.g. Hours Saved').fill('UI Test Assumption')
    await page.getByPlaceholder('Optional description').fill('Created via UI test')
    await page.getByRole('button', { name: 'Create' }).click()

    await expect(page.getByText('UI Test Assumption', { exact: true })).toBeVisible({ timeout: 10000 })
  })

  test('edit an assumption', async ({ page }) => {
    await loginAndGetToken()
    await createAssumption('edit_test', 'Edit Me')

    await login(page)
    await page.getByRole('link', { name: /Assumptions/i }).click()
    await expect(page).toHaveURL(/\/assumptions/)

    await expect(page.getByText('Edit Me', { exact: true })).toBeVisible({ timeout: 5000 })

    const editBtn = page.locator('div.flex.items-center.justify-between.p-4')
      .filter({ has: page.getByText('Edit Me', { exact: true }) })
      .getByTestId('edit-assumption')
    await editBtn.click()

    await expect(page.getByText('Edit Assumption')).toBeVisible()
    await page.getByPlaceholder('e.g. Hours Saved').fill('Edited Label')
    await page.getByRole('button', { name: 'Update' }).click()

    await expect(page.getByText('Edited Label', { exact: true })).toBeVisible({ timeout: 5000 })
  })

  test('delete an assumption', async ({ page }) => {
    await loginAndGetToken()
    await createAssumption('delete_test', 'Delete Me')

    await login(page)
    await page.getByRole('link', { name: /Assumptions/i }).click()
    await expect(page).toHaveURL(/\/assumptions/)

    await expect(page.getByText('Delete Me', { exact: true })).toBeVisible({ timeout: 5000 })

    page.on('dialog', (dialog) => dialog.accept())
    const deleteBtn = page.locator('div.flex.items-center.justify-between.p-4')
      .filter({ has: page.getByText('Delete Me', { exact: true }) })
      .getByTestId('delete-assumption')
    await deleteBtn.click()

    await expect(page.getByText('Delete Me', { exact: true })).not.toBeVisible({ timeout: 5000 })
  })
})
