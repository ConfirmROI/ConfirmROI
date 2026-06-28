<script setup>
import { ref, computed } from 'vue'
import {
  RefreshCw, Plus, Upload, Download, X, CheckCircle, AlertCircle,
  TrendingUp, FolderKanban, Calculator, LayoutDashboard,
  ArrowUp, GitBranch,
} from 'lucide-vue-next'
import RoiChart from './RoiChart.vue'
import ProjectCard from './ProjectCard.vue'

const activeTab = ref('jira')
const tabs = [
  { key: 'jira', label: 'Jira Import' },
  { key: 'csv', label: 'CSV Import' },
  { key: 'manual', label: 'Manual Creation' },
]

const assumptions = ref({
  hours_saved_per_week: 20,
  hourly_rate: 85,
  implementation_cost: 22000,
})

const formula = 'hours_saved_per_week * 52 * hourly_rate - implementation_cost'

const assumptionList = [
  { key: 'hours_saved_per_week', label: 'Hours Saved / Week' },
  { key: 'hourly_rate', label: 'Hourly Rate' },
  { key: 'implementation_cost', label: 'Implementation Cost' },
]

const annualRoi = computed(() => {
  const vars = {}
  for (const a of assumptionList) {
    vars[a.key] = parseFloat(assumptions.value[a.key]) || 0
  }
  try {
    const keys = Object.keys(vars)
    const values = keys.map(k => vars[k])
    const result = new Function(...keys, `return ${formula}`)(...values)
    return typeof result === 'number' && isFinite(result) ? result : null
  } catch {
    return null
  }
})

const roi3yr = computed(() => {
  if (annualRoi.value === null) return null
  const impl = parseFloat(assumptions.value.implementation_cost) || 0
  const gross = annualRoi.value + impl
  return gross * 3 - impl
})

const firstYearInvestment = computed(() => parseFloat(assumptions.value.implementation_cost) || 0)
const multiple1yr = computed(() =>
  firstYearInvestment.value > 0 && annualRoi.value !== null
    ? annualRoi.value / firstYearInvestment.value : null
)
const multiple3yr = computed(() =>
  firstYearInvestment.value > 0 && roi3yr.value !== null
    ? roi3yr.value / firstYearInvestment.value : null
)

function formatCurrency(val) {
  if (val === null || val === undefined) return '—'
  return '$' + Math.round(val).toLocaleString()
}

function formatMultiple(val) {
  if (val === null || val === undefined) return '—'
  return val.toFixed(1) + 'x'
}

const mockProjects = [
  { id: 1, name: 'CI/CD Pipeline Automation', description: 'Automate deployment pipelines to reduce manual toil', status: 'in_progress', start_date: '2024-01-15', end_date: '2024-06-30' },
  { id: 2, name: 'Cloud Cost Optimization', description: 'Right-size infrastructure and implement auto-scaling', status: 'planning', start_date: '2024-03-01', end_date: '' },
  { id: 3, name: 'Security Audit Tooling', description: 'Automated vulnerability scanning and remediation tracking', status: 'in_progress', start_date: '2024-02-01', end_date: '2024-08-15' },
  { id: 4, name: 'API Gateway Migration', description: 'Consolidate API management onto a unified gateway', status: 'completed', start_date: '2023-09-01', end_date: '2024-01-31' },
  { id: 5, name: 'Data Warehouse Modernization', description: 'Migrate to columnar storage for faster analytics', status: 'in_progress', start_date: '2024-01-01', end_date: '2024-12-31' },
  { id: 6, name: 'Developer Portal', description: 'Internal developer portal with service catalog and documentation', status: 'planning', start_date: '2024-04-01', end_date: '' },
]

const mockRoiResults = {
  1: 164000, 2: 92000, 3: 215000, 4: 78000, 5: 131000, 6: 45000,
}

const mockBreakdown = {
  1: { 'Cost Savings': 124000, 'Velocity Multiplier': 40000, 'Reputation Shield': 15000 },
  2: { 'Cost Savings': 192000 },
  3: { 'Risk Reduction': 105000, 'Reputation Shield': 20000 },
  4: { 'Velocity Multiplier': 48000, 'Cost Savings': 30000 },
  5: { 'Cost Savings': 81000, 'Velocity Multiplier': 50000, 'Risk Reduction': 10000 },
  6: { 'Velocity Multiplier': 45000 },
}

const mockTotalRoi = Object.values(mockRoiResults).reduce((s, v) => s + v, 0)
</script>

<template>
  <section id="workflow" class="py-20 lg:py-28 bg-white">
    <div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- Section header -->
      <div class="text-center max-w-2xl mx-auto mb-16">
        <h2 class="text-3xl sm:text-4xl font-bold text-primary-950">
          From project to ROI in five steps.
        </h2>
        <p class="mt-4 text-lg text-slate-600">
          See exactly how ConfirmROI turns your projects into defensible ROI estimates. Try the interactive demo below.
        </p>
      </div>

      <div class="space-y-20">
        <!-- =================== Step 1: Create a Project =================== -->
        <div class="relative">
          <div class="flex items-center gap-4 mb-3">
            <div class="flex items-center justify-center w-12 h-12 rounded-full bg-primary-600 text-white font-bold text-lg flex-shrink-0">1</div>
            <h3 class="text-2xl font-bold text-primary-950">Create a Project</h3>
          </div>
          <p class="text-slate-600 mb-6 ml-16">Start by importing or creating a project.</p>

          <div class="ml-16">
            <!-- Tab switcher -->
            <div class="flex gap-1 mb-4 border-b border-gray-200">
              <button
                v-for="tab in tabs"
                :key="tab.key"
                @click="activeTab = tab.key"
                :class="[
                  'px-4 py-2 text-sm font-medium transition-colors border-b-2 -mb-px',
                  activeTab === tab.key
                    ? 'border-primary-600 text-primary-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700'
                ]"
              >
                {{ tab.label }}
              </button>
            </div>

            <!-- Jira Import mock -->
            <div v-if="activeTab === 'jira'" class="bg-white rounded-xl border border-gray-200 p-6">
              <div class="flex items-center justify-between mb-4">
                <h4 class="font-semibold text-gray-900 flex items-center gap-2">
                  <RefreshCw class="w-5 h-5 text-primary-600" /> Jira Integration
                </h4>
                <button class="flex items-center gap-2 px-3 py-1.5 bg-primary-600 text-white rounded-lg text-sm opacity-90 cursor-default">
                  <Plus class="w-4 h-4" /> Connect
                </button>
              </div>
              <div class="space-y-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Jira Base URL</label>
                  <input value="https://yourteam.atlassian.net" readonly class="w-full px-4 py-2 border border-gray-300 rounded-lg bg-gray-50 text-gray-500" />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Email</label>
                  <input value="you@example.com" readonly class="w-full px-4 py-2 border border-gray-300 rounded-lg bg-gray-50 text-gray-500" />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">API Token</label>
                  <input type="password" value="••••••••••••••••" readonly class="w-full px-4 py-2 border border-gray-300 rounded-lg bg-gray-50 text-gray-500" />
                </div>
                <div class="flex gap-2">
                  <button class="px-4 py-2 bg-primary-600 text-white rounded-lg opacity-90 cursor-default">Connect</button>
                  <button class="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition">Cancel</button>
                </div>
              </div>
            </div>

            <!-- CSV Import mock -->
            <div v-if="activeTab === 'csv'" class="bg-white rounded-xl border border-gray-200 p-6">
              <div class="flex items-center justify-between mb-4">
                <h4 class="font-semibold text-gray-900">Import Projects from CSV</h4>
              </div>
              <p class="text-sm text-gray-500 mb-4">
                CSV must have a <code class="bg-gray-100 px-1 rounded">name</code> column. Optional columns:
                <code class="bg-gray-100 px-1 rounded">description</code>,
                <code class="bg-gray-100 px-1 rounded">status</code>,
                <code class="bg-gray-100 px-1 rounded">external_id</code>,
                <code class="bg-gray-100 px-1 rounded">start_date</code>,
                <code class="bg-gray-100 px-1 rounded">end_date</code>
              </p>
              <div class="flex items-center gap-3 mb-4">
                <label class="flex items-center gap-2 px-4 py-2 border border-gray-300 rounded-lg cursor-pointer hover:bg-gray-50 transition">
                  <Upload class="w-4 h-4" />
                  <span class="text-sm">Choose file</span>
                </label>
                <span class="text-sm text-gray-400">No file selected</span>
              </div>
              <button disabled class="px-4 py-2 bg-primary-600 text-white rounded-lg opacity-50 cursor-default">Import</button>
            </div>

            <!-- Manual Creation mock -->
            <div v-if="activeTab === 'manual'" class="bg-white rounded-xl border border-gray-200 p-6">
              <h4 class="font-semibold text-gray-900 mb-4">Create New Project</h4>
              <div class="space-y-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Name</label>
                  <input value="CI/CD Pipeline Automation" readonly class="w-full px-4 py-2 border border-gray-300 rounded-lg bg-gray-50 text-gray-700" />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Description</label>
                  <textarea rows="3" readonly class="w-full px-4 py-2 border border-gray-300 rounded-lg bg-gray-50 text-gray-500">Automate deployment pipelines to reduce manual toil and accelerate release cycles.</textarea>
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Status</label>
                  <select disabled class="w-full px-4 py-2 border border-gray-300 rounded-lg bg-gray-50 text-gray-700">
                    <option selected>Planning</option>
                  </select>
                </div>
                <div class="grid grid-cols-2 gap-4">
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Start Date</label>
                    <input type="text" value="2024-01-15" readonly class="w-full px-4 py-2 border border-gray-300 rounded-lg bg-gray-50 text-gray-500" />
                  </div>
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">End Date</label>
                    <input type="text" value="2024-06-30" readonly class="w-full px-4 py-2 border border-gray-300 rounded-lg bg-gray-50 text-gray-500" />
                  </div>
                </div>
                <div class="flex gap-2">
                  <button class="px-4 py-2 bg-primary-600 text-white rounded-lg opacity-90 cursor-default">Create</button>
                  <button class="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition">Cancel</button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- =================== Step 2: Value Formulas =================== -->
        <div class="relative">
          <div class="flex items-center gap-4 mb-3">
            <div class="flex items-center justify-center w-12 h-12 rounded-full bg-primary-600 text-white font-bold text-lg flex-shrink-0">2</div>
            <h3 class="text-2xl font-bold text-primary-950">Assign a Value Formula</h3>
          </div>
          <p class="text-slate-600 mb-6 ml-16">
              A <strong>Value Formula</strong> is a reusable expression that quantifies a project's worth in dollars.
              Instead of a hand-wavy "this will save us time," a formula produces a concrete number you can defend in a budget review.
              Start from a proven template (Cost Savings, Risk Reduction, Velocity Multiplier, and more)
              or write your own. Every formula is transparent and editable, so stakeholders can see exactly
              how the ROI was calculated.
          </p>

          <div class="ml-16">
            <div class="bg-white rounded-xl border border-gray-200 p-6">
              <div class="flex items-center justify-between mb-4">
                <h4 class="text-lg font-semibold text-gray-900">Value Formulas</h4>
                <button class="flex items-center gap-1 text-sm text-primary-600 hover:text-primary-700 font-medium cursor-default">
                  <Plus class="w-4 h-4" /> Assign Formula
                </button>
              </div>
              <div class="border border-gray-200 rounded-lg p-4">
                <div class="flex items-center justify-between mb-3">
                  <div>
                    <h5 class="font-semibold text-gray-900">Time Saved</h5>
                    <p class="text-sm text-gray-600 font-mono bg-gray-100 rounded-md px-3 py-2 mt-2">{{ formula }}</p>
                  </div>
                </div>
                <p class="text-xs font-medium text-gray-700 mb-2">Assumptions:</p>
                <div class="space-y-2">
                  <div v-for="a in assumptionList" :key="a.key" class="flex items-center gap-3">
                    <span class="text-sm text-gray-700 flex-1 transition font-medium">{{ a.label }}</span>
                    <input
                      :value="assumptions[a.key]"
                      readonly
                      class="w-32 px-3 py-1.5 border border-gray-200 rounded text-sm bg-gray-50 text-gray-500"
                    />
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- =================== Step 3: Collaborative Assumptions =================== -->
        <div class="relative">
          <div class="flex items-center gap-4 mb-3">
            <div class="flex items-center justify-center w-12 h-12 rounded-full bg-primary-600 text-white font-bold text-lg flex-shrink-0">3</div>
            <h3 class="text-2xl font-bold text-primary-950">Collaborative Assumptions</h3>
          </div>
          <p class="text-slate-600 mb-6 ml-16">
              <strong>Collaborative Assumptions</strong> are the editable variables that power every Value Formula.
              They're called "collaborative" because they're shared across your entire team: When someone
              updates an assumption with better data, every formula that references it recalculates instantly.
          </p>

          <div class="ml-16">
            <div class="bg-white rounded-xl border border-gray-200 p-6">
              <div class="space-y-2">
                <div v-for="a in assumptionList" :key="a.key" class="flex items-center gap-3">
                  <a
                    href="#workflow"
                    class="text-sm text-gray-700 flex-1 transition font-medium"
                    @click.prevent
                  >{{ a.label }}</a>
                  <input
                    v-model="assumptions[a.key]"
                    type="number"
                    step="any"
                    class="w-32 px-3 py-1.5 border border-gray-300 rounded text-sm focus:ring-2 focus:ring-primary-500 outline-none"
                  />
                </div>
              </div>
              <div class="mt-4 flex items-center gap-2 text-sm text-primary-600">
                <ArrowUp class="w-4 h-4 animate-bounce" />
                <span class="font-medium">Try it — change a value above and scroll down to see the ROI update live.</span>
              </div>
            </div>
          </div>
        </div>

        <!-- =================== Step 4: ROI Calculation (Live) =================== -->
        <div class="relative">
          <div class="flex items-center gap-4 mb-3">
            <div class="flex items-center justify-center w-12 h-12 rounded-full bg-primary-600 text-white font-bold text-lg flex-shrink-0">4</div>
            <h3 class="text-2xl font-bold text-primary-950">ROI Calculation</h3>
          </div>
          <p class="text-slate-600 mb-6 ml-16">Adjust any assumption and watch the project's ROI update instantly.</p>

          <div class="ml-16">
            <div class="bg-gradient-to-br from-primary-600 to-primary-700 rounded-xl p-6 text-white">
              <div class="flex items-center gap-2 mb-4">
                <TrendingUp class="w-5 h-5" />
                <h4 class="text-lg font-semibold">ROI Summary</h4>
              </div>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <!-- 1-Year -->
                <div class="border-r-0 md:border-r border-primary-500 pr-0 md:pr-6">
                  <p class="text-primary-200 text-xs font-medium uppercase tracking-wide mb-3">1-Year</p>
                  <div class="space-y-3">
                    <div>
                      <p class="text-primary-300 text-xs">ROI</p>
                      <p class="text-3xl font-bold">{{ formatCurrency(annualRoi) }}</p>
                    </div>
                    <div>
                      <p class="text-primary-300 text-xs">Multiple</p>
                      <p class="text-2xl font-semibold">{{ formatMultiple(multiple1yr) }}</p>
                    </div>
                    <div class="pt-2 border-t border-primary-500">
                      <p class="text-primary-300 text-xs">Total first year investment (includes development)</p>
                      <p class="text-lg font-medium text-primary-100">{{ formatCurrency(firstYearInvestment) }}</p>
                    </div>
                  </div>
                </div>
                <!-- 3-Year -->
                <div>
                  <p class="text-primary-200 text-xs font-medium uppercase tracking-wide mb-3">3-Year</p>
                  <div class="space-y-3">
                    <div>
                      <p class="text-primary-300 text-xs">ROI</p>
                      <p class="text-3xl font-bold">{{ formatCurrency(roi3yr) }}</p>
                    </div>
                    <div>
                      <p class="text-primary-300 text-xs">Multiple</p>
                      <p class="text-2xl font-semibold">{{ formatMultiple(multiple3yr) }}</p>
                    </div>
                    <div class="pt-2 border-t border-primary-500">
                      <p class="text-primary-300 text-xs">Total recurring annual investment</p>
                      <p class="text-lg font-medium text-primary-100">$0</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- =================== Step 5: Dashboard Visualization =================== -->
        <div class="relative">
          <div class="flex items-center gap-4 mb-3">
            <div class="flex items-center justify-center w-12 h-12 rounded-full bg-primary-600 text-white font-bold text-lg flex-shrink-0">5</div>
            <h3 class="text-2xl font-bold text-primary-950">Dashboard Visualization</h3>
          </div>
          <p class="text-slate-600 mb-6 ml-16">See ROI across all your projects at a glance.</p>

          <div class="ml-16">
            <!-- Summary cards -->
            <div class="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-8">
              <div class="bg-white rounded-xl border border-gray-200 p-5">
                <p class="text-sm text-gray-500 mb-1">Total Projects</p>
                <p class="text-2xl font-bold text-gray-900">{{ mockProjects.length }}</p>
              </div>
              <div class="bg-white rounded-xl border border-gray-200 p-5">
                <p class="text-sm text-gray-500 mb-1">Total ROI</p>
                <p class="text-2xl font-bold text-primary-600">${{ mockTotalRoi.toLocaleString() }}</p>
              </div>
              <div class="bg-white rounded-xl border border-gray-200 p-5">
                <p class="text-sm text-gray-500 mb-1">Value Formulas</p>
                <p class="text-2xl font-bold text-gray-900">4</p>
              </div>
            </div>

            <!-- ROI Chart -->
            <div class="bg-white rounded-xl border border-gray-200 p-6 mb-8">
              <h4 class="text-lg font-semibold text-gray-900 mb-4">ROI by Project — Value Formula Breakdown</h4>
              <RoiChart
                :projects="mockProjects"
                :roiResults="mockRoiResults"
                :breakdown="mockBreakdown"
              />
            </div>

          </div>
        </div>
      </div>
    </div>
  </section>
</template>
