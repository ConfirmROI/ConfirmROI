<script setup>
import { Download, Layers, BarChart3 } from 'lucide-vue-next'

const steps = [
  {
    icon: Download,
    title: 'Import Your Projects',
    description: "Connect Jira, upload a CSV, or enter projects manually. We pull in everything available — issues, epics, story points, status.",
  },
  {
    icon: Layers,
    title: 'Apply Value Formulas',
    description: "Choose from proven templates like Cost Savings, Revenue Generation, or Time Saved. Or build your own with custom formulas. Every formula uses editable assumptions, so you can refine the values as you learn more.",
  },
  {
    icon: BarChart3,
    title: 'Visualize & Share',
    description: "See all your project ROIs on a dashboard. Compare, prioritize, and export. Your estimates get more accurate every time you update an assumption.",
  },
]
</script>

<template>
  <section id="how-it-works" class="py-20 lg:py-28 bg-primary-950">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="text-center max-w-2xl mx-auto">
        <h2 class="text-3xl sm:text-4xl font-bold text-white">
          Three steps to defensible ROI estimates.
        </h2>
      </div>

      <div class="mt-16 grid md:grid-cols-3 gap-8 lg:gap-12 relative">
        <!-- Connecting line -->
        <div class="hidden md:block absolute top-12 left-[16.67%] right-[16.67%] h-0.5 bg-gradient-to-r from-primary-400 via-primary-300 to-primary-400"></div>

        <div
          v-for="(step, i) in steps"
          :key="i"
          class="relative flex flex-col items-center text-center"
        >
          <div class="relative z-10 flex items-center justify-center w-24 h-24 rounded-2xl bg-white border-2 border-primary-200 shadow-sm">
            <component :is="step.icon" class="w-10 h-10 text-primary-600" />
          </div>
          <h3 class="mt-6 text-xl font-semibold text-white">
            {{ step.title }}
          </h3>
          <p class="mt-3 text-slate-300 leading-relaxed">
            {{ step.description }}
          </p>
        </div>
      </div>
    </div>
  </section>
</template>
