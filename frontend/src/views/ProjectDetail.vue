<script setup>
import { ref, onMounted, onUnmounted, computed, reactive } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useProjectsStore } from '../stores/projects'
import { useDashboardStore } from '../stores/dashboard'
import { useCostsStore } from '../stores/costs'
import { ArrowLeft, Plus, TrendingUp, Pencil, Trash2, ExternalLink } from 'lucide-vue-next'
import AssumptionEditor from '../components/AssumptionEditor.vue'
import CostTracker from '../components/CostTracker.vue'

const route = useRoute()
const router = useRouter()
const projectsStore = useProjectsStore()
const dashboardStore = useDashboardStore()
const costsStore = useCostsStore()

const project = ref(null)
const projectArchetypes = ref([])
const showAssign = ref(false)
const showEdit = ref(false)
const selectedArchetypeId = ref(null)
const editForm = reactive({ name: '', description: '', status: 'planning', start_date: '', end_date: '' })
const saveState = ref({}) // { [paId]: 'saving' | 'saved' | null }

const projectId = computed(() => parseInt(route.params.id))

onMounted(async () => {
  project.value = await projectsStore.fetchProject(projectId.value)
  await loadProjectArchetypes()
  await dashboardStore.fetchArchetypes()
  await costsStore.fetchCosts(projectId.value)
  await loadRoiData()
})

async function loadRoiData() {
  for (const pa of projectArchetypes.value) {
    await dashboardStore.getLatestRoi(projectId.value, pa.id)
  }
}

const roiSummary = computed(() => {
  const costs = costsStore.costs || []
  const costBreakdown = { one_time: 0, recurring_monthly: 0, recurring_annual: 0 }
  for (const c of costs) {
    const ct = c.cost_type || 'one_time'
    if (ct in costBreakdown) costBreakdown[ct] += c.amount || 0
  }
  const oneTime = costBreakdown.one_time
  const recurringAnnual = costBreakdown.recurring_monthly * 12 + costBreakdown.recurring_annual
  const firstYearInvestment = oneTime + recurringAnnual
  const threeYearInvestment = oneTime + recurringAnnual * 3

  let grossAnnual = 0
  let hasData = false
  for (const pa of projectArchetypes.value) {
    if (!pa?.formula?.formula || !pa?.assumption_values) continue
    const vars = {}
    for (const av of pa.assumption_values) {
      const key = av.assumption?.key
      if (!key) continue
      vars[key] = parseFloat(av.value) || 0
    }
    if ('implementation_cost' in vars) vars['implementation_cost'] = 0
    try {
      const keys = Object.keys(vars)
      const values = keys.map(k => vars[k])
      const result = new Function(...keys, `return ${pa.formula.formula}`)(...values)
      if (typeof result === 'number' && isFinite(result)) {
        grossAnnual += result
        hasData = true
      }
    } catch {
      // skip invalid formulas
    }
  }

  const roi1yr = grossAnnual - firstYearInvestment
  const roi3yr = grossAnnual * 3 - threeYearInvestment
  const multiple1yr = firstYearInvestment > 0 ? roi1yr / firstYearInvestment : null
  const multiple3yr = threeYearInvestment > 0 ? roi3yr / threeYearInvestment : null
  return { roi1yr, roi3yr, firstYearInvestment, recurringAnnual, multiple1yr, multiple3yr, hasData }
})

function formatCurrency(val) {
  if (val === null || val === undefined) return '—'
  return '$' + Math.round(val).toLocaleString()
}

function formatMultiple(val) {
  if (val === null || val === undefined) return '—'
  return val.toFixed(1) + 'x'
}

async function loadProjectArchetypes() {
  projectArchetypes.value = await dashboardStore.fetchProjectArchetypes(projectId.value) || []
}

async function handleUnassign(paId) {
  if (!confirm('Remove this value formula from the project?')) return
  const ok = await dashboardStore.unassignArchetype(projectId.value, paId)
  if (ok) {
    await loadProjectArchetypes()
    await loadRoiData()
  }
}

async function handleAssign() {
  if (!selectedArchetypeId.value) return
  await dashboardStore.assignArchetype(projectId.value, selectedArchetypeId.value)
  await loadProjectArchetypes()
  await loadRoiData()
  showAssign.value = false
  selectedArchetypeId.value = null
}

const debounceTimers = {}

async function handleAssumptionUpdate(paId, assumptionId, value) {
  clearTimeout(debounceTimers[`${paId}-${assumptionId}`])
  debounceTimers[`${paId}-${assumptionId}`] = setTimeout(async () => {
    saveState.value[paId] = 'saving'
    await dashboardStore.updateAssumptionValue(projectId.value, paId, assumptionId, value)
    await dashboardStore.calculateRoi(projectId.value, paId)
    saveState.value[paId] = 'saved'
    setTimeout(() => { saveState.value[paId] = null }, 2000)
  }, 600)
}

onUnmounted(() => {
  for (const key of Object.keys(debounceTimers)) {
    clearTimeout(debounceTimers[key])
  }
})

function startEdit() {
  if (!project.value) return
  editForm.name = project.value.name || ''
  editForm.description = project.value.description || ''
  editForm.status = project.value.status || 'planning'
  editForm.start_date = project.value.start_date || ''
  editForm.end_date = project.value.end_date || ''
  showEdit.value = true
}

async function handleEdit() {
  const updated = await projectsStore.updateProject(projectId.value, { ...editForm })
  if (updated) {
    project.value = updated
    showEdit.value = false
  }
}

async function handleDelete() {
  if (confirm('Delete this project?')) {
    const ok = await projectsStore.deleteProject(projectId.value)
    if (ok) router.push('/projects')
  }
}
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <div class="max-w-5xl mx-auto p-6">
      <button @click="router.push('/projects')" class="flex items-center gap-1 text-gray-500 hover:text-gray-700 mb-4">
        <ArrowLeft class="w-4 h-4" /> Back to Projects
      </button>

      <div v-if="project" class="mb-8">
        <div class="flex items-start justify-between">
          <div>
            <h1 class="text-2xl font-bold text-gray-900">{{ project.name }}</h1>
            <p class="text-gray-500 mt-1">{{ project.description || 'No description' }}</p>
            <div class="flex gap-3 mt-3">
              <span class="px-3 py-1 text-xs font-medium rounded-full bg-gray-100 text-gray-700 capitalize">{{ project.status }}</span>
              <span v-if="project.external_source" class="px-3 py-1 text-xs font-medium rounded-full bg-blue-50 text-blue-700 capitalize">{{ project.external_source }}</span>
              <span v-if="project.start_date" class="px-3 py-1 text-xs font-medium rounded-full bg-green-50 text-green-700">{{ project.start_date }}</span>
              <span v-if="project.end_date" class="px-3 py-1 text-xs font-medium rounded-full bg-orange-50 text-orange-700">{{ project.end_date }}</span>
            </div>
          </div>
          <div class="flex gap-2">
            <button @click="startEdit" data-testid="edit-project" class="flex items-center gap-1 px-3 py-1.5 text-sm border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition">
              <Pencil class="w-4 h-4" /> Edit
            </button>
            <button @click="handleDelete" data-testid="delete-project" class="flex items-center gap-1 px-3 py-1.5 text-sm border border-red-300 rounded-lg text-red-600 hover:bg-red-50 transition">
              <Trash2 class="w-4 h-4" /> Delete
            </button>
          </div>
        </div>
      </div>

      <!-- Edit form -->
      <div v-if="showEdit" class="bg-white rounded-xl border border-gray-200 p-6 mb-6">
        <h3 class="font-semibold text-gray-900 mb-4">Edit Project</h3>
        <form @submit.prevent="handleEdit" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Name</label>
            <input v-model="editForm.name" required placeholder="Project name" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 outline-none" />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Description</label>
            <textarea v-model="editForm.description" rows="3" placeholder="Project description" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 outline-none"></textarea>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Status</label>
            <select v-model="editForm.status" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 outline-none">
              <option value="planning">Planning</option>
              <option value="in_progress">In Progress</option>
              <option value="completed">Completed</option>
              <option value="cancelled">Cancelled</option>
            </select>
          </div>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Start Date</label>
              <input v-model="editForm.start_date" type="date" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 outline-none" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">End Date</label>
              <input v-model="editForm.end_date" type="date" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 outline-none" />
            </div>
          </div>
          <div class="flex gap-2">
            <button type="submit" class="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition">Update</button>
            <button type="button" @click="showEdit = false" class="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition">Cancel</button>
          </div>
        </form>
      </div>

      <!-- ROI Summary section -->
      <div v-if="roiSummary.hasData" class="bg-gradient-to-br from-primary-600 to-primary-700 rounded-xl p-6 mb-6 text-white">
        <div class="flex items-center gap-2 mb-4">
          <TrendingUp class="w-5 h-5" />
          <h2 class="text-lg font-semibold">ROI Summary</h2>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <!-- 1-Year column -->
          <div class="border-r-0 md:border-r border-primary-500 pr-0 md:pr-6">
            <p class="text-primary-200 text-xs font-medium uppercase tracking-wide mb-3">1-Year</p>
            <div class="space-y-3">
              <div>
                <p class="text-primary-300 text-xs">ROI</p>
                <p class="text-3xl font-bold">{{ formatCurrency(roiSummary.roi1yr) }}</p>
              </div>
              <div>
                <p class="text-primary-300 text-xs">Multiple</p>
                <p class="text-2xl font-semibold">{{ formatMultiple(roiSummary.multiple1yr) }}</p>
              </div>
              <div class="pt-2 border-t border-primary-500">
                <p class="text-primary-300 text-xs">Total first year investment (includes development)</p>
                <p class="text-lg font-medium text-primary-100">{{ formatCurrency(roiSummary.firstYearInvestment) }}</p>
              </div>
            </div>
          </div>
          <!-- 3-Year column -->
          <div>
            <p class="text-primary-200 text-xs font-medium uppercase tracking-wide mb-3">3-Year</p>
            <div class="space-y-3">
              <div>
                <p class="text-primary-300 text-xs">ROI</p>
                <p class="text-3xl font-bold">{{ formatCurrency(roiSummary.roi3yr) }}</p>
              </div>
              <div>
                <p class="text-primary-300 text-xs">Multiple</p>
                <p class="text-2xl font-semibold">{{ formatMultiple(roiSummary.multiple3yr) }}</p>
              </div>
              <div class="pt-2 border-t border-primary-500">
                <p class="text-primary-300 text-xs">Total recurring annual investment</p>
                <p class="text-lg font-medium text-primary-100">{{ formatCurrency(roiSummary.recurringAnnual) }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Value Formulas section -->
      <div class="bg-white rounded-xl border border-gray-200 p-6 mb-6">
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-lg font-semibold text-gray-900">Value Formulas</h2>
          <button @click="showAssign = !showAssign" class="flex items-center gap-1 text-sm text-primary-600 hover:text-primary-700 font-medium">
            <Plus class="w-4 h-4" /> Assign Formula
          </button>
        </div>

        <!-- Assign form -->
        <div v-if="showAssign" class="mb-4 p-4 bg-gray-50 rounded-lg">
          <select v-model="selectedArchetypeId" class="w-full px-4 py-2 border border-gray-300 rounded-lg mb-2">
            <option value="" disabled>Select a formula...</option>
            <option v-for="a in dashboardStore.archetypes" :key="a.id" :value="a.id">{{ a.name }}</option>
          </select>
          <button @click="handleAssign" :disabled="!selectedArchetypeId" class="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:opacity-50 transition">Assign</button>
        </div>

        <!-- Project archetype cards -->
        <div v-if="projectArchetypes.length" class="space-y-4">
          <div v-for="pa in projectArchetypes" :key="pa.id" class="border border-gray-200 rounded-lg p-4">
            <div class="flex items-center justify-between mb-3">
              <div>
                <h3 class="font-semibold text-gray-900">
                  <router-link :to="`/formulas`" class="hover:text-primary-600 transition" @click.stop>{{ pa.formula?.name || 'Value Formula' }}</router-link>
                </h3>
                <p class="text-sm text-gray-600 font-mono bg-gray-100 rounded-md px-3 py-2 mt-2">{{ pa.formula?.formula }}</p>
              </div>
              <div class="flex items-center gap-3">
                <router-link
                  :to="`/formulas`"
                  class="flex items-center gap-1 text-xs text-primary-600 hover:text-primary-700 transition"
                  @click.stop
                >
                  <ExternalLink class="w-3 h-3" /> View formula
                </router-link>
                <button
                  @click.stop="handleUnassign(pa.id)"
                  data-testid="remove-formula"
                  class="flex items-center gap-1 text-xs text-red-500 hover:text-red-700 transition"
                >
                  <Trash2 class="w-3 h-3" /> Remove
                </button>
              </div>
            </div>

            <!-- Assumption editor with live ROI -->
            <AssumptionEditor
              :project-archetype="pa"
              :project-id="projectId"
              @update="(assumptionId, value) => handleAssumptionUpdate(pa.id, assumptionId, value)"
            />
            <div v-if="saveState[pa.id]" class="mt-2 text-xs flex items-center gap-1">
              <span v-if="saveState[pa.id] === 'saving'" class="text-gray-500 animate-pulse">Saving...</span>
              <span v-else-if="saveState[pa.id] === 'saved'" class="text-green-600">✓ Saved</span>
            </div>
          </div>
        </div>
        <div v-else class="text-center py-8 text-gray-500">
          No formulas assigned yet. Assign one to start calculating ROI.
        </div>
      </div>

      <!-- Investment (Costs) section -->
      <div class="bg-white rounded-xl border border-gray-200 p-6 mb-6">
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-lg font-semibold text-gray-900">Investment (Costs)</h2>
        </div>
        <CostTracker :project-id="projectId" />
      </div>
    </div>
  </div>
</template>
