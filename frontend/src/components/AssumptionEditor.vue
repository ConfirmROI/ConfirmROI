<script setup>
import { ref, watch, computed } from 'vue'
import { TrendingUp } from 'lucide-vue-next'
import { useCostsStore } from '../stores/costs'

let isEditing = false

const props = defineProps({
  projectArchetype: { type: Object, required: true },
  projectId: { type: Number, default: null },
})

const emit = defineEmits(['update'])

const costsStore = useCostsStore()

const localValues = ref({})

watch(
  () => props.projectArchetype,
  (pa) => {
    if (isEditing) return
    if (pa?.assumption_values) {
      for (const av of pa.assumption_values) {
        localValues.value[av.assumption_id] = av.value
      }
    }
  },
  { immediate: true }
)

const liveGrossAnnual = computed(() => {
  const pa = props.projectArchetype
  if (!pa?.archetype?.formula || !pa?.assumption_values) return null
  const vars = {}
  for (const av of pa.assumption_values) {
    const key = av.assumption?.key
    if (!key) continue
    vars[key] = parseFloat(localValues.value[av.assumption_id]) || 0
  }
  // Set implementation_cost to 0 so formula gives gross annual value
  if ('implementation_cost' in vars) vars['implementation_cost'] = 0
  try {
    const keys = Object.keys(vars)
    const values = keys.map(k => vars[k])
    const result = new Function(...keys, `return ${pa.archetype.formula}`)(...values)
    return typeof result === 'number' && isFinite(result) ? result : null
  } catch {
    return null
  }
})

const costBreakdown = computed(() => {
  const costs = costsStore.costs || []
  const breakdown = { one_time: 0, recurring_monthly: 0, recurring_annual: 0 }
  for (const c of costs) {
    const ct = c.cost_type || 'one_time'
    if (ct in breakdown) breakdown[ct] += c.amount || 0
  }
  return breakdown
})

const liveRoi = computed(() => {
  if (liveGrossAnnual.value === null) return null
  const c = costBreakdown.value
  const recurring = c.recurring_monthly * 12 + c.recurring_annual
  return liveGrossAnnual.value - c.one_time - recurring
})

watch(
  () => props.projectId,
  async (id) => {
    if (id) await costsStore.fetchCosts(id)
  },
  { immediate: true }
)

const liveRoi3yr = computed(() => {
  if (liveGrossAnnual.value === null) return null
  const c = costBreakdown.value
  const recurring = c.recurring_monthly * 12 + c.recurring_annual
  return liveGrossAnnual.value * 3 - c.one_time - recurring * 3
})

function onInput(assumptionId, value) {
  isEditing = true
  const parsed = parseFloat(value)
  emit('update', assumptionId, isNaN(parsed) ? 0 : parsed)
}

function onBlur() {
  isEditing = false
}
</script>

<template>
  <div v-if="projectArchetype?.assumption_values?.length" class="space-y-2">
    <p class="text-xs font-medium text-gray-700 mb-2">Assumptions:</p>
    <div v-for="av in projectArchetype.assumption_values" :key="av.id" class="flex items-center gap-3">
      <router-link
        :to="`/assumptions`"
        class="text-sm text-primary-600 flex-1 underline hover:text-primary-700 hover:no-underline transition font-medium"
        @click.stop
      >{{ av.assumption?.label || av.assumption?.key }}</router-link>
      <input
        v-if="av.assumption?.key === 'implementation_cost'"
        :value="costsStore.totalCost.toLocaleString(undefined, { maximumFractionDigits: 2 })"
        disabled
        class="w-32 px-3 py-1.5 border border-gray-200 rounded text-sm bg-gray-50 text-gray-500"
      />
      <input
        v-else
        v-model="localValues[av.assumption_id]"
        type="number"
        step="any"
        @input="onInput(av.assumption_id, localValues[av.assumption_id])"
        @blur="onBlur"
        class="w-32 px-3 py-1.5 border border-gray-300 rounded text-sm focus:ring-2 focus:ring-primary-500 outline-none"
      />
    </div>
    <div v-if="liveRoi !== null" class="mt-3 p-3 bg-primary-50 rounded-lg space-y-1">
      <div class="flex items-center gap-2">
        <TrendingUp class="w-5 h-5 text-primary-600" />
        <span class="font-semibold text-primary-700">1-Year ROI: ${{ liveRoi.toLocaleString(undefined, { maximumFractionDigits: 2 }) }}</span>
      </div>
      <div v-if="liveRoi3yr !== null" class="flex items-center gap-2 pl-7">
        <span class="font-semibold text-primary-600">3-Year ROI: ${{ liveRoi3yr.toLocaleString(undefined, { maximumFractionDigits: 2 }) }}</span>
      </div>
    </div>
  </div>
  <div v-else class="text-sm text-gray-400">No editable assumptions for this formula.</div>
</template>
