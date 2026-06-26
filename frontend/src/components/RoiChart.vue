<script setup>
import { computed } from 'vue'
import { Bar } from 'vue-chartjs'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js'

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend)

const props = defineProps({
  projects: { type: Array, default: () => [] },
  roiResults: { type: Object, default: () => ({}) },
  breakdown: { type: Object, default: () => ({}) },
})

const ARCHETYPE_COLORS = {
  'Direct Savings': '#84cc16',
  'Avoided-Loss': '#e11d48',
  'Toil Reduction': '#06b6d4',
  'Velocity Multiplier': '#8b5cf6',
  'Enabler / Option Value': '#d4d480',
  'Reputation Shield': '#f97316',
  'Support / KTLO': '#2f5c28',
  'Cost Savings': '#84cc16',
  'Risk Reduction': '#e11d48',
  'Time Saved': '#06b6d4',
  'Revenue Generation': '#d4d480',
  'Unknown': '#9ca3af',
}

function archetypeColor(name) {
  return ARCHETYPE_COLORS[name] || ARCHETYPE_COLORS['Unknown']
}

const chartData = computed(() => {
  const labels = props.projects.map((p) => p.name)
  const allArchetypes = new Set()
  props.projects.forEach((p) => {
    const projectBreakdown = props.breakdown[p.id] || {}
    Object.keys(projectBreakdown).forEach((name) => allArchetypes.add(name))
  })
  const archetypes = Array.from(allArchetypes)
  const datasets = archetypes.map((name) => ({
    label: name,
    data: props.projects.map((p) => {
      const projectBreakdown = props.breakdown[p.id] || {}
      return projectBreakdown[name] || 0
    }),
    backgroundColor: archetypeColor(name),
    borderRadius: 4,
  }))
  return { labels, datasets }
})

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'bottom',
      labels: { usePointStyle: true, boxWidth: 10 },
    },
    tooltip: {
      callbacks: {
        label: (ctx) => `${ctx.dataset.label}: $${ctx.raw.toLocaleString()}`,
      },
    },
  },
  scales: {
    x: { stacked: true },
    y: {
      stacked: true,
      beginAtZero: true,
      ticks: {
        callback: (v) => `$${v.toLocaleString()}`,
      },
    },
  },
}
</script>

<template>
  <div v-if="projects.length" style="height: 320px">
    <Bar :data="chartData" :options="chartOptions" />
  </div>
  <div v-else class="flex items-center justify-center h-64 text-gray-400">
    No data to display yet.
  </div>
</template>
