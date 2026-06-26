# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: formulas-crud.spec.js >> Value Formulas CRUD Extended >> edit formula preserves and updates assumption links
- Location: e2e/formulas-crud.spec.js:116:3

# Error details

```
Test timeout of 30000ms exceeded.
```

```
Error: locator.click: Test timeout of 30000ms exceeded.
Call log:
  - waiting for locator('div.bg-white.rounded-xl.border').filter({ has: getByText('E2E Linked Formula') }).getByTestId('edit-archetype')

```

# Page snapshot

```yaml
- generic [ref=e3]:
  - complementary [ref=e4]:
    - generic [ref=e5]:
      - img [ref=e7]
      - generic [ref=e10]: ConfirmROI
    - navigation [ref=e11]:
      - link "Dashboard" [ref=e12] [cursor=pointer]:
        - /url: /dashboard
        - img [ref=e13]
        - text: Dashboard
      - link "Projects" [ref=e18] [cursor=pointer]:
        - /url: /projects
        - img [ref=e19]
        - text: Projects
      - link "Value Formulas" [ref=e21] [cursor=pointer]:
        - /url: /formulas
        - img [ref=e22]
        - text: Value Formulas
      - link "Assumptions" [ref=e24] [cursor=pointer]:
        - /url: /assumptions
        - img [ref=e25]
        - text: Assumptions
    - generic [ref=e28]:
      - generic [ref=e29]:
        - paragraph [ref=e30]: E2E Formulas CRUD User
        - paragraph [ref=e31]: free tier
      - button [ref=e32] [cursor=pointer]:
        - img [ref=e33]
  - main [ref=e36]:
    - generic [ref=e37]:
      - generic [ref=e38]:
        - heading "Value Formulas" [level=1] [ref=e40]
        - button "New Formula" [ref=e41] [cursor=pointer]:
          - img [ref=e42]
          - text: New Formula
      - generic [ref=e43]:
        - generic [ref=e44] [cursor=pointer]:
          - generic [ref=e45]:
            - generic [ref=e46]:
              - img [ref=e48]
              - generic [ref=e50]:
                - heading "Cost Savings" [level=3] [ref=e51]
                - text: System
            - img [ref=e52]
          - paragraph [ref=e55]: Calculate annual ROI from reducing monthly operational costs.
          - paragraph [ref=e56]: (monthly_cost_before - monthly_cost_after) * 12 - implementation_cost
          - generic [ref=e57]:
            - paragraph [ref=e58]: "Assumptions:"
            - generic [ref=e59]:
              - generic [ref=e60]: Monthly Cost Before (monthly_cost_before)
              - generic [ref=e61]: Monthly Cost After (monthly_cost_after)
              - generic [ref=e62]: Implementation Cost (implementation_cost)
        - generic [ref=e63] [cursor=pointer]:
          - generic [ref=e64]:
            - generic [ref=e65]:
              - img [ref=e67]
              - generic [ref=e69]:
                - heading "Revenue Generation" [level=3] [ref=e70]
                - text: System
            - img [ref=e71]
          - paragraph [ref=e74]: Calculate annual ROI from generating new revenue.
          - paragraph [ref=e75]: estimated_monthly_revenue * 12 - implementation_cost
          - generic [ref=e76]:
            - paragraph [ref=e77]: "Assumptions:"
            - generic [ref=e78]:
              - generic [ref=e79]: Estimated Monthly Revenue (estimated_monthly_revenue)
              - generic [ref=e80]: Implementation Cost (implementation_cost)
        - generic [ref=e81] [cursor=pointer]:
          - generic [ref=e82]:
            - generic [ref=e83]:
              - img [ref=e85]
              - generic [ref=e87]:
                - heading "Time Saved" [level=3] [ref=e88]
                - text: System
            - img [ref=e89]
          - paragraph [ref=e92]: Calculate annual ROI from time savings converted to dollar value.
          - paragraph [ref=e93]: hours_saved_per_week * 52 * hourly_rate - implementation_cost
          - generic [ref=e94]:
            - paragraph [ref=e95]: "Assumptions:"
            - generic [ref=e96]:
              - generic [ref=e97]: Hours Saved Per Week (hours_saved_per_week)
              - generic [ref=e98]: Hourly Rate (hourly_rate)
              - generic [ref=e99]: Implementation Cost (implementation_cost)
        - generic [ref=e100] [cursor=pointer]:
          - generic [ref=e101]:
            - generic [ref=e102]:
              - img [ref=e104]
              - generic [ref=e106]:
                - heading "Risk Reduction" [level=3] [ref=e107]
                - text: System
            - img [ref=e108]
          - paragraph [ref=e111]: Calculate annual ROI from reducing risk probability and impact.
          - paragraph [ref=e112]: risk_probability * risk_impact - implementation_cost
          - generic [ref=e113]:
            - paragraph [ref=e114]: "Assumptions:"
            - generic [ref=e115]:
              - generic [ref=e116]: Risk Probability (risk_probability)
              - generic [ref=e117]: Risk Impact ($) (risk_impact)
              - generic [ref=e118]: Implementation Cost (implementation_cost)
        - generic [ref=e119] [cursor=pointer]:
          - generic [ref=e120]:
            - generic [ref=e121]:
              - img [ref=e123]
              - generic [ref=e125]:
                - heading "Velocity Multiplier" [level=3] [ref=e126]
                - text: System
            - img [ref=e127]
          - paragraph [ref=e130]: Structural improvements that compound across many engineers' delivery speed, valued as a fraction of their total cost.
          - paragraph [ref=e131]: ic_count * uplift_pct * eng_cost * realization * ramp_factor * attribution
          - generic [ref=e132]:
            - paragraph [ref=e133]: "Assumptions:"
            - generic [ref=e134]:
              - generic [ref=e135]: IC Count (ic_count)
              - generic [ref=e136]: Uplift % (uplift_pct)
              - generic [ref=e137]: Engineer Cost (eng_cost)
              - generic [ref=e138]: Realization (realization)
              - generic [ref=e139]: Ramp Factor (ramp_factor)
              - generic [ref=e140]: Attribution (attribution)
        - generic [ref=e141] [cursor=pointer]:
          - generic [ref=e142]:
            - generic [ref=e143]:
              - img [ref=e145]
              - generic [ref=e147]:
                - heading "Enabler / Option Value" [level=3] [ref=e148]
                - text: System
            - img [ref=e149]
          - paragraph [ref=e152]: No direct cash value — the initiative unlocks downstream projects that do. Value is attributed upstream.
          - paragraph [ref=e153]: downstream_npv_total * enabler_attr / horizon_years
          - generic [ref=e154]:
            - paragraph [ref=e155]: "Assumptions:"
            - generic [ref=e156]:
              - generic [ref=e157]: Downstream NPV Total (downstream_npv_total)
              - generic [ref=e158]: Enabler Attribution (enabler_attr)
              - generic [ref=e159]: Horizon Years (horizon_years)
        - generic [ref=e160] [cursor=pointer]:
          - generic [ref=e161]:
            - generic [ref=e162]:
              - img [ref=e164]
              - generic [ref=e166]:
                - heading "Reputation Shield" [level=3] [ref=e167]
                - text: System
            - img [ref=e168]
          - paragraph [ref=e171]: Reducing incident frequency to avoid erosion of partner and dealer trust — churn and deal-flow loss that follows reliability failures.
          - paragraph [ref=e172]: delta_incidents_per_year * p_partner_impact * (p_churn * avg_partner_arr + p_vol_reduction * avg_vol_reduction_rev) * realization
          - generic [ref=e173]:
            - paragraph [ref=e174]: "Assumptions:"
            - generic [ref=e175]:
              - generic [ref=e176]: Incident Reduction (per year) (delta_incidents_per_year)
              - generic [ref=e177]: Partner Impact Probability (p_partner_impact)
              - generic [ref=e178]: Partner Churn Probability (p_churn)
              - generic [ref=e179]: Average Partner ARR (avg_partner_arr)
              - generic [ref=e180]: Volume Reduction Probability (p_vol_reduction)
              - generic [ref=e181]: Average Volume Reduction Revenue (avg_vol_reduction_rev)
              - generic [ref=e182]: Realization (realization)
        - generic [ref=e183] [cursor=pointer]:
          - generic [ref=e184]:
            - generic [ref=e185]:
              - img [ref=e187]
              - generic [ref=e189]:
                - heading "Support / KTLO" [level=3] [ref=e190]
                - text: System
            - img [ref=e191]
          - paragraph [ref=e194]: A deliberate capacity allocation decision, not a value-generation initiative. Cost = Opportunity, net ROI is zero by design.
          - paragraph [ref=e195]: team_cost * (capacity / headcount)
          - generic [ref=e196]:
            - paragraph [ref=e197]: "Assumptions:"
            - generic [ref=e198]:
              - generic [ref=e199]: Team Cost (team_cost)
              - generic [ref=e200]: Allocated Capacity (capacity)
              - generic [ref=e201]: Team Headcount (headcount)
        - generic [ref=e202] [cursor=pointer]:
          - generic [ref=e203]:
            - generic [ref=e204]:
              - img [ref=e206]
              - generic [ref=e208]:
                - heading "E2E Linked Formula" [level=3] [ref=e209]
                - text: Custom
            - img [ref=e210]
          - paragraph
          - paragraph [ref=e213]: hours_saved_per_week * hourly_rate * 52
          - generic [ref=e214]:
            - paragraph [ref=e215]: "Assumptions:"
            - generic [ref=e217]: Monthly Cost Before (monthly_cost_before)
```

# Test source

```ts
  23  |   const resp = await ctx.post('http://localhost:5174/api/archetypes/assumptions', {
  24  |     data: { key, label, data_type: 'number', default_value: 10, description: 'E2E test assumption' },
  25  |     headers: { Authorization: `Bearer ${accessToken}` },
  26  |   })
  27  |   const data = await resp.json()
  28  |   await ctx.dispose()
  29  |   return data.id
  30  | }
  31  | 
  32  | async function getAllAssumptions() {
  33  |   const ctx = await request.newContext()
  34  |   const resp = await ctx.get('http://localhost:5174/api/archetypes/assumptions', {
  35  |     headers: { Authorization: `Bearer ${accessToken}` },
  36  |   })
  37  |   const data = await resp.json()
  38  |   await ctx.dispose()
  39  |   return data
  40  | }
  41  | 
  42  | test.describe('Value Formulas CRUD Extended', () => {
  43  |   test.beforeAll(async ({ browser }) => {
  44  |     const page = await browser.newPage()
  45  |     await page.goto('/register')
  46  |     await page.getByPlaceholder('John Doe').fill(TEST_USER.name)
  47  |     await page.getByPlaceholder('you@company.com').fill(TEST_USER.email)
  48  |     await page.getByPlaceholder('••••••••').fill(TEST_USER.password)
  49  |     await page.getByRole('button', { name: /Create account/i }).click()
  50  |     await page.waitForURL('**/dashboard', { timeout: 10000 })
  51  |     await page.close()
  52  | 
  53  |     await loginAndGetToken()
  54  |   })
  55  | 
  56  |   async function login(page) {
  57  |     await page.goto('/login')
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
> 123 |     await editBtn.click()
      |                   ^ Error: locator.click: Test timeout of 30000ms exceeded.
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
  158 |     expect(options.some(o => o.includes('E2E Edited Linked'))).toBeTruthy()
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