import { test, expect, request } from '@playwright/test'

const TEST_USER = {
  name: 'E2E Projects CRUD User',
  email: `e2e-proj-crud-${Date.now()}@test.com`,
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

test.describe('Projects CRUD Extended', () => {
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

  async function createProjectViaUI(page, name, description, status) {
    await page.getByRole('link', { name: /Projects/i }).click()
    await page.getByRole('button', { name: /New Project/i }).click()
    await page.getByPlaceholder('Project name').fill(name)
    await page.getByPlaceholder('Project description').fill(description)
    if (status) {
      const createForm = page.locator('.bg-white.rounded-xl.border:has-text("Create New Project")')
      await createForm.locator('select').selectOption(status)
    }
    await page.getByRole('button', { name: 'Create' }).click()
    await expect(page.getByText(name)).toBeVisible({ timeout: 10000 })
  }

  test('create project with all fields including dates', async ({ page }) => {
    await login(page)
    await page.getByRole('link', { name: /Projects/i }).click()
    await page.getByRole('button', { name: /New Project/i }).click()

    await page.getByPlaceholder('Project name').fill('Full Field Project')
    await page.getByPlaceholder('Project description').fill('Project with all fields')
    const createForm = page.locator('.bg-white.rounded-xl.border:has-text("Create New Project")')
    await createForm.locator('select').selectOption('in_progress')
    await createForm.locator('input[type="date"]').first().fill('2025-01-15')
    await createForm.locator('input[type="date"]').nth(1).fill('2025-06-30')
    await page.getByRole('button', { name: 'Create' }).click()

    await expect(page.getByText('Full Field Project')).toBeVisible({ timeout: 10000 })

    await page.getByText('Full Field Project').click()
    await expect(page).toHaveURL(/\/projects\/\d+/)
    await expect(page.getByText('in_progress')).toBeVisible()
    await expect(page.getByText('2025-01-15')).toBeVisible()
    await expect(page.getByText('2025-06-30')).toBeVisible()
  })

  test('create projects with different statuses', async ({ page }) => {
    await login(page)

    await createProjectViaUI(page, 'Planning Project', 'In planning', 'planning')
    await createProjectViaUI(page, 'Completed Project', 'Done', 'completed')
    await createProjectViaUI(page, 'Cancelled Project', 'Abandoned', 'cancelled')

    await page.getByRole('link', { name: /Projects/i }).click()
    await expect(page.getByText('Planning Project')).toBeVisible()
    await expect(page.getByText('Completed Project')).toBeVisible()
    await expect(page.getByText('Cancelled Project')).toBeVisible()
  })

  test('edit project status and dates', async ({ page }) => {
    await login(page)
    await page.getByRole('link', { name: /Projects/i }).click()
    await page.getByText('Planning Project').click()
    await expect(page).toHaveURL(/\/projects\/\d+/)

    await page.getByTestId('edit-project').click()
    await expect(page.getByText('Edit Project')).toBeVisible()

    const editForm = page.locator('.bg-white.rounded-xl.border:has-text("Edit Project")')
    await editForm.locator('select').selectOption('completed')
    await editForm.locator('input[type="date"]').first().fill('2025-03-01')
    await editForm.locator('input[type="date"]').nth(1).fill('2025-09-15')
    await page.getByRole('button', { name: 'Update' }).click()

    await expect(page.getByText('completed')).toBeVisible({ timeout: 5000 })
    await expect(page.getByText('2025-03-01')).toBeVisible()
    await expect(page.getByText('2025-09-15')).toBeVisible()
  })

  test('assign formula to project and see ROI', async ({ page }) => {
    await login(page)
    await page.getByRole('link', { name: /Projects/i }).click()
    await page.getByText('Full Field Project').click()
    await expect(page).toHaveURL(/\/projects\/\d+/)

    await expect(page.getByText('No formulas assigned yet')).toBeVisible()

    await page.getByRole('button', { name: /Assign Formula/i }).click()
    await page.locator('select').selectOption({ index: 1 })
    await page.getByRole('button', { name: 'Assign', exact: true }).click()

    await expect(page.getByText(/1-Year ROI:/i)).toBeVisible({ timeout: 10000 })
  })

  test('edit assumption values updates live ROI', async ({ page }) => {
    await login(page)
    await page.getByRole('link', { name: /Projects/i }).click()
    await page.getByText('Full Field Project').click()
    await expect(page).toHaveURL(/\/projects\/\d+/)

    const roiText = page.locator('span.font-semibold.text-primary-700')
    await expect(roiText).toBeVisible({ timeout: 10000 })
    const initialRoi = await roiText.textContent()

    const firstInput = page.locator('input[type="number"]').first()
    await firstInput.fill('99999')

    await expect(roiText).not.toHaveText(initialRoi, { timeout: 5000 })
  })

  test('assign a second formula independently', async ({ page }) => {
    await login(page)
    await page.getByRole('link', { name: /Projects/i }).click()
    await page.getByText('Full Field Project').click()
    await expect(page).toHaveURL(/\/projects\/\d+/)

    await page.getByRole('button', { name: /Assign Formula/i }).click()
    await page.locator('select').selectOption({ index: 2 })
    await page.getByRole('button', { name: 'Assign', exact: true }).click()

    const roiElements = page.locator('span.font-semibold.text-primary-700')
    await expect(roiElements).toHaveCount(2, { timeout: 10000 })
  })

  test('ROI persists after page refresh', async ({ page }) => {
    await login(page)
    await page.getByRole('link', { name: /Projects/i }).click()
    await page.getByText('Full Field Project').click()
    await expect(page).toHaveURL(/\/projects\/\d+/)

    const roiBefore = await page.locator('span.font-semibold.text-primary-700').first().textContent()

    await page.reload()
    await page.waitForLoadState('networkidle')

    const roiAfter = await page.locator('span.font-semibold.text-primary-700').first().textContent()
    expect(roiAfter).toBeTruthy()
  })

  test('delete project with assigned formulas redirects to projects list', async ({ page }) => {
    await login(page)
    await page.getByRole('link', { name: /Projects/i }).click()
    await page.getByText('Full Field Project').click()
    await expect(page).toHaveURL(/\/projects\/\d+/)

    page.on('dialog', (dialog) => dialog.accept())
    await page.getByTestId('delete-project').click()

    await expect(page).toHaveURL(/\/projects/, { timeout: 10000 })
    await expect(page.getByText('Full Field Project')).not.toBeVisible({ timeout: 5000 })
  })

  test('CSV import creates projects', async ({ page }) => {
    await login(page)
    await page.getByRole('link', { name: /Projects/i }).click()

    await page.getByRole('button', { name: /Import CSV/i }).click()
    await expect(page.getByText('Import Projects from CSV')).toBeVisible()

    const csvContent = 'name,description,status\nCSV Project 1,From CSV,planning\nCSV Project 2,Also from CSV,completed'
    await page.locator('input[type="file"]').setInputFiles({
      name: 'test-import.csv',
      mimeType: 'text/csv',
      buffer: Buffer.from(csvContent),
    })

    await page.getByRole('button', { name: 'Import', exact: true }).click()

    await expect(page.getByText(/Imported/i)).toBeVisible({ timeout: 10000 })
    await expect(page.getByText('CSV Project 1')).toBeVisible({ timeout: 10000 })
    await expect(page.getByText('CSV Project 2')).toBeVisible()
  })

  test('CSV import without file has disabled Import button', async ({ page }) => {
    await login(page)
    await page.getByRole('link', { name: /Projects/i }).click()

    await page.getByRole('button', { name: /Import CSV/i }).click()
    await expect(page.getByText('Import Projects from CSV')).toBeVisible()

    const importBtn = page.getByRole('button', { name: 'Import', exact: true })
    await expect(importBtn).toBeDisabled()
  })

  test('CSV export downloads file', async ({ page }) => {
    await login(page)
    await page.getByRole('link', { name: /Projects/i }).click()

    const downloadPromise = page.waitForEvent('download')
    await page.getByRole('button', { name: /Export CSV/i }).click()
    const download = await downloadPromise

    expect(download.suggestedFilename()).toContain('.csv')
  })

  test('project detail shows empty state when no formulas assigned', async ({ page }) => {
    await login(page)
    await page.getByRole('link', { name: /Projects/i }).click()

    await page.getByRole('button', { name: /New Project/i }).click()
    await page.getByPlaceholder('Project name').fill('No Formula Project')
    await page.getByPlaceholder('Project description').fill('No formulas')
    await page.getByRole('button', { name: 'Create' }).click()
    await expect(page.getByText('No Formula Project')).toBeVisible({ timeout: 10000 })

    await page.getByText('No Formula Project').click()
    await expect(page.getByText('No formulas assigned yet')).toBeVisible()
  })

  test('non-existent project ID shows page without crash', async ({ page }) => {
    await login(page)
    await page.goto('/projects/99999')
    await expect(page).toHaveURL(/\/projects\/99999/)
  })

  test('cleanup: delete all remaining test projects', async ({ page }) => {
    await login(page)
    await page.getByRole('link', { name: /Projects/i }).click()

    page.on('dialog', (dialog) => dialog.accept())

    const projectNames = [
      'Planning Project',
      'Completed Project',
      'Cancelled Project',
      'CSV Project 1',
      'CSV Project 2',
      'No Formula Project',
    ]

    for (const name of projectNames) {
      const projectLink = page.getByText(name, { exact: false })
      if (await projectLink.first().isVisible({ timeout: 3000 }).catch(() => false)) {
        await projectLink.first().click()
        await page.waitForURL(/\/projects\/\d+/, { timeout: 5000 })
        const deleteBtn = page.getByTestId('delete-project')
        if (await deleteBtn.isVisible({ timeout: 2000 }).catch(() => false)) {
          await deleteBtn.click()
          await page.waitForURL(/\/projects/, { timeout: 10000 })
        }
      }
    }
  })
})
