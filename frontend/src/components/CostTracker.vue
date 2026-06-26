<script setup>
import { ref, computed, watch } from 'vue'
import { Plus, Trash2, ChevronDown, ChevronRight, DollarSign } from 'lucide-vue-next'
import { useCostsStore } from '../stores/costs'

const props = defineProps({
  projectId: { type: Number, required: true },
})

const costsStore = useCostsStore()

const showAdvanced = ref(false)
const showAddForm = ref(false)
const newCost = ref({
  category: 'infrastructure',
  description: '',
  person_weeks: null,
  amount: null,
  cost_type: 'one_time',
  incurred_date: '',
  is_estimate: true,
})

const costs = computed(() => costsStore.costs)
const totalCost = computed(() => costsStore.totalCost)

watch(
  () => props.projectId,
  async (id) => {
    if (id) await costsStore.fetchCosts(id)
  },
  { immediate: true }
)

const categoryLabels = {
  development: 'Development',
  infrastructure: 'Infrastructure',
  vendor: 'Vendor',
  other: 'Other',
}

const categoryColors = {
  development: 'bg-blue-50 text-blue-700',
  infrastructure: 'bg-purple-50 text-purple-700',
  vendor: 'bg-orange-50 text-orange-700',
  other: 'bg-gray-100 text-gray-700',
}

function formatCurrency(val) {
  if (val === null || val === undefined) return '$0'
  return '$' + Number(val).toLocaleString(undefined, { maximumFractionDigits: 2 })
}

async function updatePersonWeeks(cost) {
  await costsStore.updateCost(props.projectId, cost.id, {
    person_weeks: cost.person_weeks,
  })
}

async function updateAmount(cost) {
  await costsStore.updateCost(props.projectId, cost.id, {
    amount: cost.amount,
  })
}

async function updateDescription(cost) {
  await costsStore.updateCost(props.projectId, cost.id, {
    description: cost.description,
  })
}

async function deleteCost(cost) {
  if (confirm(`Delete "${categoryLabels[cost.category]}" cost entry?`)) {
    await costsStore.deleteCost(props.projectId, cost.id)
  }
}

async function addCost() {
  const data = {
    category: newCost.value.category,
    description: newCost.value.description || null,
  }
  if (newCost.value.category === 'development' && newCost.value.person_weeks) {
    data.person_weeks = newCost.value.person_weeks
  } else if (newCost.value.amount) {
    data.amount = newCost.value.amount
  } else {
    data.amount = 0
  }
  if (showAdvanced.value) {
    data.cost_type = newCost.value.cost_type
    data.incurred_date = newCost.value.incurred_date || null
    data.is_estimate = newCost.value.is_estimate
  }
  await costsStore.createCost(props.projectId, data)
  showAddForm.value = false
  newCost.value = {
    category: 'infrastructure',
    description: '',
    person_weeks: null,
    amount: null,
    cost_type: 'one_time',
    incurred_date: '',
    is_estimate: true,
  }
}
</script>

<template>
  <div>
    <!-- Total Investment summary -->
    <div class="flex items-center justify-between mb-4">
      <div class="flex items-center gap-2">
        <div class="w-10 h-10 rounded-lg bg-primary-50 flex items-center justify-center">
          <DollarSign class="w-5 h-5 text-primary-600" />
        </div>
        <div>
          <p class="text-sm text-gray-500">Total Investment</p>
          <p class="text-2xl font-bold text-gray-900">{{ formatCurrency(totalCost) }}</p>
        </div>
      </div>
      <button
        @click="showAddForm = !showAddForm"
        class="flex items-center gap-1 text-sm text-primary-600 hover:text-primary-700 font-medium"
      >
        <Plus class="w-4 h-4" /> Add Cost
      </button>
    </div>

    <!-- Add cost form -->
    <div v-if="showAddForm" class="mb-4 p-4 bg-gray-50 rounded-lg space-y-3">
      <div class="grid grid-cols-2 gap-3">
        <div>
          <label class="block text-xs font-medium text-gray-600 mb-1">Category</label>
          <select v-model="newCost.category" class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-primary-500 outline-none">
            <option value="development">Development</option>
            <option value="infrastructure">Infrastructure</option>
            <option value="vendor">Vendor</option>
            <option value="other">Other</option>
          </select>
        </div>
        <div>
          <label class="block text-xs font-medium text-gray-600 mb-1">Description</label>
          <input v-model="newCost.description" placeholder="e.g. AWS hosting" class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-primary-500 outline-none" />
        </div>
      </div>
      <div v-if="newCost.category === 'development'" class="grid grid-cols-2 gap-3">
        <div>
          <label class="block text-xs font-medium text-gray-600 mb-1">Person-Weeks</label>
          <input v-model.number="newCost.person_weeks" type="number" step="any" placeholder="e.g. 12" class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-primary-500 outline-none" />
        </div>
        <div class="flex items-end">
          <p class="text-xs text-gray-400">Amount auto-calculated from labor rate</p>
        </div>
      </div>
      <div v-else class="grid grid-cols-2 gap-3">
        <div>
          <label class="block text-xs font-medium text-gray-600 mb-1">Amount ($)</label>
          <input v-model.number="newCost.amount" type="number" step="any" placeholder="e.g. 5000" class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-primary-500 outline-none" />
        </div>
      </div>

      <!-- Advanced fields toggle -->
      <button @click="showAdvanced = !showAdvanced" class="flex items-center gap-1 text-xs text-gray-500 hover:text-gray-700">
        <ChevronDown v-if="!showAdvanced" class="w-3 h-3" />
        <ChevronRight v-else class="w-3 h-3" />
        Show advanced fields
      </button>
      <div v-if="showAdvanced" class="grid grid-cols-3 gap-3 p-3 bg-white rounded-lg border border-gray-200">
        <div>
          <label class="block text-xs font-medium text-gray-600 mb-1">Cost Type</label>
          <select v-model="newCost.cost_type" class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-primary-500 outline-none">
            <option value="one_time">One-time</option>
            <option value="recurring_monthly">Recurring (monthly)</option>
            <option value="recurring_annual">Recurring (annual)</option>
          </select>
        </div>
        <div>
          <label class="block text-xs font-medium text-gray-600 mb-1">Incurred Date</label>
          <input v-model="newCost.incurred_date" type="date" class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-primary-500 outline-none" />
        </div>
        <div>
          <label class="block text-xs font-medium text-gray-600 mb-1">Estimate?</label>
          <select v-model="newCost.is_estimate" class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-primary-500 outline-none">
            <option :value="true">Estimate</option>
            <option :value="false">Actual</option>
          </select>
        </div>
      </div>

      <div class="flex gap-2">
        <button @click="addCost" class="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition text-sm">Add</button>
        <button @click="showAddForm = false" class="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition text-sm">Cancel</button>
      </div>
    </div>

    <!-- Cost entries list -->
    <div v-if="costs.length" class="space-y-3">
      <div v-for="cost in costs" :key="cost.id" class="border border-gray-200 rounded-lg p-4">
        <div class="flex items-start justify-between mb-2">
          <div class="flex items-center gap-2">
            <span :class="['px-2 py-0.5 text-xs font-medium rounded-full', categoryColors[cost.category]]">
              {{ categoryLabels[cost.category] }}
            </span>
            <span v-if="cost.is_estimate" class="px-2 py-0.5 text-xs font-medium rounded-full bg-yellow-50 text-yellow-700">Estimate</span>
            <span v-else class="px-2 py-0.5 text-xs font-medium rounded-full bg-green-50 text-green-700">Actual</span>
          </div>
          <button @click="deleteCost(cost)" class="text-gray-400 hover:text-red-500 transition">
            <Trash2 class="w-4 h-4" />
          </button>
        </div>

        <!-- Development: person-weeks input -->
        <div v-if="cost.category === 'development'" class="space-y-2">
          <div class="flex items-center gap-3">
            <label class="text-sm text-gray-600 w-32">Person-Weeks</label>
            <input
              v-model.number="cost.person_weeks"
              type="number"
              step="any"
              @change="updatePersonWeeks(cost)"
              class="w-32 px-3 py-1.5 border border-gray-300 rounded text-sm focus:ring-2 focus:ring-primary-500 outline-none"
            />
            <span class="text-sm text-gray-400">
              @ {{ formatCurrency(cost.effective_rate) }}/wk
            </span>
          </div>
          <div class="flex items-center gap-3">
            <label class="text-sm text-gray-600 w-32">Computed Cost</label>
            <span class="text-sm font-semibold text-gray-900">{{ formatCurrency(cost.amount) }}</span>
          </div>
        </div>

        <!-- Non-development: direct amount input -->
        <div v-else class="space-y-2">
          <div class="flex items-center gap-3">
            <label class="text-sm text-gray-600 w-32">Description</label>
            <input
              v-model="cost.description"
              @change="updateDescription(cost)"
              placeholder="Add description..."
              class="flex-1 px-3 py-1.5 border border-gray-300 rounded text-sm focus:ring-2 focus:ring-primary-500 outline-none"
            />
          </div>
          <div class="flex items-center gap-3">
            <label class="text-sm text-gray-600 w-32">Amount</label>
            <input
              v-model.number="cost.amount"
              type="number"
              step="any"
              @change="updateAmount(cost)"
              class="w-32 px-3 py-1.5 border border-gray-300 rounded text-sm focus:ring-2 focus:ring-primary-500 outline-none"
            />
          </div>
        </div>

        <!-- Advanced fields (read-only display for existing entries) -->
        <div v-if="cost.cost_type !== 'one_time' || cost.incurred_date" class="mt-2 flex gap-3 text-xs text-gray-400">
          <span v-if="cost.cost_type !== 'one_time'">{{ cost.cost_type.replace('_', ' ') }}</span>
          <span v-if="cost.incurred_date">{{ cost.incurred_date }}</span>
        </div>
      </div>
    </div>
    <div v-else class="text-center py-6 text-gray-500 text-sm">
      No costs recorded yet.
    </div>
  </div>
</template>
