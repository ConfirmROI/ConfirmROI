import { test, expect } from '@playwright/test'

const TEST_USER = {
  name: 'E2E Test User',
  email: `e2e-${Date.now()}@test.com`,
  password: 'testpassword123',
}

test.describe('Authentication Flow', () => {
  test('register a new user', async ({ page }) => {
    await page.goto('/register')

    await expect(page.getByText('Create your account')).toBeVisible()

    await page.getByPlaceholder('John Doe').fill(TEST_USER.name)
    await page.getByPlaceholder('you@company.com').fill(TEST_USER.email)
    await page.getByPlaceholder('••••••••').fill(TEST_USER.password)
    await page.getByRole('button', { name: /Create account/i }).click()

    await page.waitForURL('**/dashboard', { timeout: 10000 })
    await expect(page).toHaveURL(/\/dashboard/)
  })

  test('login with existing user', async ({ page }) => {
    await page.goto('/login')

    await expect(page.getByText('Welcome back')).toBeVisible()

    await page.getByPlaceholder('you@company.com').fill(TEST_USER.email)
    await page.getByPlaceholder('••••••••').fill(TEST_USER.password)
    await page.getByRole('button', { name: /Sign in/i }).click()

    await page.waitForURL('**/dashboard', { timeout: 10000 })
    await expect(page).toHaveURL(/\/dashboard/)
  })

  test('login with invalid credentials shows error', async ({ page }) => {
    await page.goto('/login')

    await page.getByPlaceholder('you@company.com').fill('wrong@test.com')
    await page.getByPlaceholder('••••••••').fill('wrongpassword')
    await page.getByRole('button', { name: /Sign in/i }).click()

    await expect(page.getByText(/invalid|error|failed/i)).toBeVisible({ timeout: 5000 })
  })

  test('homepage displays landing page', async ({ page }) => {
    await page.goto('/')
    await expect(page).toHaveURL('/')
    await expect(page.getByRole('heading', { name: /Simple.*pricing/i })).toBeVisible()
  })

  test('register link navigates to register page', async ({ page }) => {
    await page.goto('/login')
    await page.getByRole('link', { name: /Register/i }).click()
    await expect(page).toHaveURL(/\/register/)
  })

  test('pricing tier Get Started shows plan selection on register', async ({ page }) => {
    await page.goto('/')
    await page.getByRole('link', { name: /Get Started/i }).first().click()
    await expect(page).toHaveURL(/\/register\?plan=/)
    await expect(page.getByText('Choose a plan to get started')).toBeVisible()
    await expect(page.getByRole('heading', { name: 'Starter' })).toBeVisible()
    await expect(page.getByRole('heading', { name: 'Growth' })).toBeVisible()
    await expect(page.getByRole('heading', { name: 'Enterprise' })).toBeVisible()
  })

  test('selecting a plan shows payment placeholder', async ({ page }) => {
    await page.goto('/register?plan=Growth')
    await expect(page.getByText('Payment integration coming soon')).toBeVisible()
    await expect(page.getByRole('heading', { name: 'Growth' })).toBeVisible()
    await expect(page.getByRole('button', { name: /Continue to Payment/i })).toBeDisabled()
  })
})
