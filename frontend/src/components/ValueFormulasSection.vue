<script setup>
import { ref } from 'vue'
import { Calculator, RefreshCw, GitBranch, ShieldCheck, TrendingUp } from 'lucide-vue-next'

const examples = [
  {
    icon: Calculator,
    title: 'Time Saved',
    formula: 'hours_saved_per_week * 52 * hourly_rate - implementation_cost',
    assumptions: [
      { key: 'hours_saved_per_week', label: 'Hours Saved / Week', value: ref(40) },
      { key: 'hourly_rate', label: 'Hourly Rate', value: ref(85) },
      { key: 'implementation_cost', label: 'Implementation Cost', value: ref(22000) },
    ],
  },
  {
    icon: ShieldCheck,
    title: 'Risk Reduction',
    formula: 'risk_probability * risk_impact - implementation_cost',
    assumptions: [
      { key: 'risk_probability', label: 'Risk Probability', value: ref(0.45) },
      { key: 'risk_impact', label: 'Risk Impact', value: ref(500000) },
      { key: 'implementation_cost', label: 'Implementation Cost', value: ref(80000) },
    ],
  },
]

function computeRoi(example) {
  const vars = {}
  for (const a of example.assumptions) {
    vars[a.key] = parseFloat(a.value.value) || 0
  }
  try {
    const keys = Object.keys(vars)
    const values = keys.map(k => vars[k])
    const result = new Function(...keys, `return ${example.formula}`)(...values)
    return typeof result === 'number' && isFinite(result) ? result : null
  } catch {
    return null
  }
}

function formatCurrency(val) {
  if (val === null || val === undefined) return '—'
  return '$' + Math.round(val).toLocaleString()
}


const features = [
  {
    icon: GitBranch,
    title: 'Shared assumptions',
    description: 'One assumption, like hourly rate, feeds every formula that references it. Update it once, and every project using that assumption recalculates automatically.',
  },
  {
    icon: RefreshCw,
    title: 'Always improvable',
    description: 'When an assumption gets challenged in a review, swap in better data. The new value propagates to all dependent formulas instantly — no spreadsheets to chase down.',
  },
]
</script>

<template>
  <section id="value-formulas" class="py-20 lg:py-28 bg-primary-50" style="background: linear-gradient(to top, white, #CCDDFF)">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="grid lg:grid-cols-2 gap-12 lg:gap-16 items-center">
        <!-- Left: Narrative -->
        <div>
          <h2 class="text-3xl sm:text-4xl font-bold text-primary-950">
            Your gut says go. Your spreadsheet should explain why.
          </h2>
          <p class="mt-6 text-lg text-slate-600 leading-relaxed">
            The ROI for some projects is easy to quantify: “increases sales by 10%” or “adds $100,000 through a new product line.”
          </p>
          <p class="mt-4 text-lg text-slate-600 leading-relaxed">
            But what about the project that helps five other teams move faster? Or the one that reduces the risk of a
            costly outage?
          </p>
          <p class="mt-4 text-lg text-slate-600 leading-relaxed">
            That’s where <strong class="text-primary-900">Value Formulas</strong> come in. Each formula is built from
            <strong class="text-primary-900">Collaborative Assumptions</strong>, editable variables that capture the
            real drivers of value for your specific situation. Start with a proven template or build your own from
            scratch.
          </p>

          <div class="mt-8 space-y-5">
            <div
              v-for="feature in features"
              :key="feature.title"
              class="flex gap-4"
            >
              <div class="flex-shrink-0 flex items-center justify-center w-10 h-10 rounded-lg bg-primary-50">
                <component :is="feature.icon" class="w-5 h-5 text-primary-600" />
              </div>
              <div>
                <h3 class="font-semibold text-primary-950">{{ feature.title }}</h3>
                <p class="mt-1 text-sm text-slate-600 leading-relaxed">{{ feature.description }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Right: Formula visual -->
        <div class="space-y-4">
          <div
            v-for="(example, i) in examples"
            :key="i"
            class="border border-gray-200 rounded-lg bg-white p-4"
          >
            <div class="flex items-center justify-between mb-3">
              <div>
                <h3 class="font-semibold text-gray-900">{{ example.title }}</h3>
                <p class="text-sm text-gray-600 font-mono bg-gray-100 rounded-md px-3 py-2 mt-2">{{ example.formula }}</p>
              </div>
            </div>

            <p class="text-xs font-medium text-gray-700 mb-2">Assumptions:</p>
            <div class="space-y-2">
              <div
                v-for="assumption in example.assumptions"
                :key="assumption.key"
                class="flex items-center gap-3"
              >
                <span class="text-sm text-gray-700 flex-1">{{ assumption.label }}</span>
                <input
                  v-model="assumption.value.value"
                  type="number"
                  :step="assumption.key === 'risk_probability' ? 0.01 : 'any'"
                  class="w-32 px-3 py-1.5 border border-gray-300 rounded text-sm focus:ring-2 focus:ring-primary-500 outline-none"
                />
              </div>
            </div>

            <div class="mt-3 p-3 bg-primary-50 rounded-lg space-y-1">
              <div class="flex items-center gap-2">
                <TrendingUp class="w-5 h-5 text-primary-600" />
                <span class="font-semibold text-primary-700">Annual ROI: {{ formatCurrency(computeRoi(example)) }}</span>
              </div>
              <div class="flex items-center gap-2 pl-7">
                <span class="font-semibold text-primary-600">3-Year ROI: {{ formatCurrency(computeRoi(example) !== null ? computeRoi(example) * 3 : null) }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
