# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: formulas-crud.spec.js >> Value Formulas CRUD Extended >> custom formula appears in project assign dropdown
- Location: e2e/formulas-crud.spec.js:141:3

# Error details

```
Error: expect(received).toBeTruthy()

Received: false
```

# Page snapshot

```yaml
- generic [ref=e4]:
  - button "Back to Projects" [ref=e5] [cursor=pointer]:
    - img [ref=e6]
    - text: Back to Projects
  - generic [ref=e9]:
    - generic [ref=e10]:
      - heading "Formula Dropdown Test" [level=1] [ref=e11]
      - paragraph [ref=e12]: Testing formula dropdown
      - generic [ref=e13]:
        - generic [ref=e14]: planning
        - generic [ref=e15]: manual
    - generic [ref=e16]:
      - button "Edit" [ref=e17] [cursor=pointer]:
        - img [ref=e18]
        - text: Edit
      - button "Delete" [ref=e21] [cursor=pointer]:
        - img [ref=e22]
        - text: Delete
  - generic [ref=e25]:
    - generic [ref=e26]:
      - heading "Value Formulas" [level=2] [ref=e27]
      - button "Assign Formula" [active] [ref=e28] [cursor=pointer]:
        - img [ref=e29]
        - text: Assign Formula
    - generic [ref=e30]:
      - combobox [ref=e31]:
        - option "Select a formula..." [disabled]
        - option "Cost Savings"
        - option "Revenue Generation"
        - option "Time Saved"
        - option "Risk Reduction"
        - option "Velocity Multiplier"
        - option "Enabler / Option Value"
        - option "Reputation Shield"
        - option "Support / KTLO"
      - button "Assign" [disabled] [ref=e32]
    - generic [ref=e33]: No formulas assigned yet. Assign one to start calculating ROI.
  - generic [ref=e34]:
    - heading "Investment (Costs)" [level=2] [ref=e36]
    - generic [ref=e37]:
      - generic [ref=e38]:
        - generic [ref=e39]:
          - img [ref=e41]
          - generic [ref=e43]:
            - paragraph [ref=e44]: Total Investment
            - paragraph [ref=e45]: $0
        - button "Add Cost" [ref=e46] [cursor=pointer]:
          - img [ref=e47]
          - text: Add Cost
      - generic [ref=e49]:
        - generic [ref=e50]:
          - generic [ref=e51]:
            - generic [ref=e52]: Development
            - generic [ref=e53]: Estimate
          - button [ref=e54] [cursor=pointer]:
            - img [ref=e55]
        - generic [ref=e58]:
          - generic [ref=e59]:
            - generic [ref=e60]: Person-Weeks
            - spinbutton [ref=e61]: "0"
            - generic [ref=e62]: "@ $3,500/wk"
          - generic [ref=e63]:
            - generic [ref=e64]: Computed Cost
            - generic [ref=e65]: $0
```

# Test source

```ts
  58  |     await page.getByPlaceholder('you@company.com').fill(TEST_USER.email)
  59  |     await page.getByPlaceholder('••••••••').fill(TEST_USER.password)
  60  |     await page.getByRole('button', { name: /Sign in/i }).click()
  61  |     await page.waitForURL('**/dashboard', { timeout: 10000 })
  62  |   }
  63  | 
  64  |   test('all 4 system formulas are displayed', async ({ page }) => {
  65  |     await login(page)
  66  |     await page.getByRole('link', { name: /Value Formulas/i }).click()
  67  |     await expect(page).toHaveURL(/\/formulas/)
  68  | 
  69  |     await expect(page.getByText('Cost Savings')).toBeVisible({ timeout: 5000 })
  70  |     await expect(page.getByText('Revenue Generation')).toBeVisible()
  71  |     await expect(page.getByText('Time Saved')).toBeVisible()
  72  |     await expect(page.getByText('Risk Reduction')).toBeVisible()
  73  |   })
  74  | 
  75  |   test('system formulas have System badge', async ({ page }) => {
  76  |     await login(page)
  77  |     await page.getByRole('link', { name: /Value Formulas/i }).click()
  78  | 
  79  |     const systemBadges = page.locator('span.text-blue-600.font-medium:has-text("System")')
  80  |     await expect(systemBadges.first()).toBeVisible({ timeout: 5000 })
  81  |     const count = await systemBadges.count()
  82  |     expect(count).toBeGreaterThanOrEqual(4)
  83  |   })
  84  | 
  85  |   test('system formulas have no edit or delete buttons', async ({ page }) => {
  86  |     await login(page)
  87  |     await page.getByRole('link', { name: /Value Formulas/i }).click()
  88  | 
  89  |     const costSavingsCard = page.locator('div.bg-white.rounded-xl.border')
  90  |       .filter({ has: page.getByText('Cost Savings') })
  91  |     await expect(costSavingsCard.getByTestId('edit-archetype')).not.toBeVisible()
  92  |     await expect(costSavingsCard.getByTestId('delete-archetype')).not.toBeVisible()
  93  |   })
  94  | 
  95  |   test('create formula with linked assumptions and verify display', async ({ page }) => {
  96  |     await login(page)
  97  |     await page.getByRole('link', { name: /Value Formulas/i }).click()
  98  | 
  99  |     await page.getByRole('button', { name: /New Formula/i }).click()
  100 | 
  101 |     await page.getByPlaceholder('e.g. Efficiency Gains').fill('E2E Linked Formula')
  102 |     await page.getByPlaceholder('e.g. hours_saved * hourly_rate - cost').fill('hours_saved_per_week * hourly_rate * 52')
  103 | 
  104 |     const firstCheckbox = page.locator('input[type="checkbox"]').first()
  105 |     await firstCheckbox.check()
  106 | 
  107 |     await page.getByRole('button', { name: 'Create' }).click()
  108 | 
  109 |     await expect(page.getByText('E2E Linked Formula')).toBeVisible({ timeout: 5000 })
  110 | 
  111 |     const formulaCard = page.locator('div.bg-white.rounded-xl.border')
  112 |       .filter({ has: page.getByText('E2E Linked Formula') })
  113 |     await expect(formulaCard.getByText('Assumptions:')).toBeVisible()
  114 |   })
  115 | 
  116 |   test('edit formula preserves and updates assumption links', async ({ page }) => {
  117 |     await login(page)
  118 |     await page.getByRole('link', { name: /Value Formulas/i }).click()
  119 | 
  120 |     const editBtn = page.locator('div.bg-white.rounded-xl.border')
  121 |       .filter({ has: page.getByText('E2E Linked Formula') })
  122 |       .getByTestId('edit-archetype')
  123 |     await editBtn.click()
  124 | 
  125 |     await expect(page.getByText('Edit Formula')).toBeVisible()
  126 | 
  127 |     const firstCheckbox = page.locator('input[type="checkbox"]').first()
  128 |     await expect(firstCheckbox).toBeChecked()
  129 | 
  130 |     await page.getByPlaceholder('e.g. Efficiency Gains').fill('E2E Edited Linked')
  131 |     await page.getByPlaceholder('e.g. hours_saved * hourly_rate - cost').fill('hours_saved_per_week * 52 * hourly_rate - implementation_cost')
  132 | 
  133 |     const secondCheckbox = page.locator('input[type="checkbox"]').nth(1)
  134 |     await secondCheckbox.check()
  135 | 
  136 |     await page.getByRole('button', { name: 'Update' }).click()
  137 | 
  138 |     await expect(page.getByText('E2E Edited Linked')).toBeVisible({ timeout: 5000 })
  139 |   })
  140 | 
  141 |   test('custom formula appears in project assign dropdown', async ({ page }) => {
  142 |     await login(page)
  143 |     await page.getByRole('link', { name: /Projects/i }).click()
  144 | 
  145 |     await page.getByRole('button', { name: /New Project/i }).click()
  146 |     await page.getByPlaceholder('Project name').fill('Formula Dropdown Test')
  147 |     await page.getByPlaceholder('Project description').fill('Testing formula dropdown')
  148 |     await page.getByRole('button', { name: 'Create' }).click()
  149 |     await expect(page.getByText('Formula Dropdown Test')).toBeVisible({ timeout: 10000 })
  150 | 
  151 |     await page.getByText('Formula Dropdown Test').click()
  152 |     await expect(page).toHaveURL(/\/projects\/\d+/)
  153 | 
  154 |     await page.getByRole('button', { name: /Assign Formula/i }).click()
  155 | 
  156 |     const select = page.locator('select')
  157 |     const options = await select.locator('option').allTextContents()
> 158 |     expect(options.some(o => o.includes('E2E Edited Linked'))).toBeTruthy()
      |                                                                ^ Error: expect(received).toBeTruthy()
  159 |   })
  160 | 
  161 |   test('create formula with no assumptions linked', async ({ page }) => {
  162 |     await login(page)
  163 |     await page.getByRole('link', { name: /Value Formulas/i }).click()
  164 | 
  165 |     await page.getByRole('button', { name: /New Formula/i }).click()
  166 | 
  167 |     await page.getByPlaceholder('e.g. Efficiency Gains').fill('E2E No Assumptions')
  168 |     await page.getByPlaceholder('e.g. hours_saved * hourly_rate - cost').fill('42 * 10')
  169 | 
  170 |     await page.getByRole('button', { name: 'Create' }).click()
  171 | 
  172 |     await expect(page.getByText('E2E No Assumptions')).toBeVisible({ timeout: 5000 })
  173 |   })
  174 | 
  175 |   test('create formula with invalid expression succeeds (no validation)', async ({ page }) => {
  176 |     await login(page)
  177 |     await page.getByRole('link', { name: /Value Formulas/i }).click()
  178 | 
  179 |     await page.getByRole('button', { name: /New Formula/i }).click()
  180 | 
  181 |     await page.getByPlaceholder('e.g. Efficiency Gains').fill('E2E Invalid Formula')
  182 |     await page.getByPlaceholder('e.g. hours_saved * hourly_rate - cost').fill('hours_saved *')
  183 | 
  184 |     await page.getByRole('button', { name: 'Create' }).click()
  185 | 
  186 |     await expect(page.getByText('E2E Invalid Formula')).toBeVisible({ timeout: 5000 })
  187 |   })
  188 | 
  189 |   test('delete custom formula with confirmation', async ({ page }) => {
  190 |     await login(page)
  191 |     await page.getByRole('link', { name: /Value Formulas/i }).click()
  192 | 
  193 |     page.on('dialog', (dialog) => dialog.accept())
  194 | 
  195 |     const formulasToDelete = ['E2E Edited Linked', 'E2E No Assumptions', 'E2E Invalid Formula']
  196 |     for (const name of formulasToDelete) {
  197 |       const deleteBtn = page.locator('div.bg-white.rounded-xl.border')
  198 |         .filter({ has: page.getByText(name) })
  199 |         .getByTestId('delete-archetype')
  200 |       if (await deleteBtn.isVisible({ timeout: 3000 }).catch(() => false)) {
  201 |         await deleteBtn.click()
  202 |         await expect(page.getByText(name)).not.toBeVisible({ timeout: 5000 })
  203 |       }
  204 |     }
  205 |   })
  206 | 
  207 |   test('empty state shows when no formulas exist', async ({ page }) => {
  208 |     await login(page)
  209 |     await page.getByRole('link', { name: /Value Formulas/i }).click()
  210 | 
  211 |     const systemFormulas = page.locator('div.bg-white.rounded-xl.border')
  212 |     const count = await systemFormulas.count()
  213 |     expect(count).toBeGreaterThanOrEqual(4)
  214 |   })
  215 | })
  216 | 
```