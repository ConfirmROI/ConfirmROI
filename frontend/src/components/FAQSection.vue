<script setup>
import { ref } from 'vue'
import { ChevronDown } from 'lucide-vue-next'

const faqs = [
  {
    q: 'Is the free version actually usable for real work?',
    a: "Yes. The free version is a complete, fully functional tool for a single manager to calculate and visualize ROI for their team. No trial limitations, no feature crippleware. It’s open source — you own it.",
  },
  {
    q: "What’s the difference between system and custom value formulas?",
    a: 'System formulas are pre-built templates (Cost Savings, Revenue Generation, Time Saved, Risk Reduction) with proven formulas. Custom formulas let you define your own formula and assumptions for any type of value you want to measure.',
  },
  {
    q: 'How does the Jira integration work?',
    a: 'Connect your Jira instance via API token. ConfirmROI pulls all available project data — issues, epics, story points, and status. You can also import via CSV or enter projects manually.',
  },
  {
    q: 'Can I contribute to the open-source project?',
    a: 'Absolutely. ConfirmROI is open source and we welcome contributions — new formulas, bug fixes, features, documentation. Check out our GitHub.',
  },
  {
    q: 'Can I self-host the paid version?',
    a: 'The paid version is available as a managed SaaS service. If you need on-prem deployment for the paid features, contact us about enterprise licensing.',
  },
  {
    q: 'Do I need to talk to a salesperson?',
    a: 'No. Pick a plan, enter your payment info, and get started immediately. No sales calls required.',
  },
]

const openIndex = ref(0)

function toggle(i) {
  openIndex.value = openIndex.value === i ? -1 : i
}
</script>

<template>
  <section class="py-20 lg:py-28 bg-primary-50">
    <div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="text-center">
        <h2 class="text-3xl sm:text-4xl font-bold text-primary-950">
          Frequently Asked Questions
        </h2>
      </div>

      <div class="mt-12 space-y-3">
        <div
          v-for="(faq, i) in faqs"
          :key="i"
          class="rounded-xl bg-white border border-slate-200 overflow-hidden"
        >
          <button
            class="w-full flex items-center justify-between px-5 py-4 text-left hover:bg-slate-50 transition-colors"
            @click="toggle(i)"
          >
            <span class="font-semibold text-primary-950 pr-4">{{ faq.q }}</span>
            <ChevronDown
              class="w-5 h-5 text-slate-400 flex-shrink-0 transition-transform"
              :class="{ 'rotate-180': openIndex === i }"
            />
          </button>
          <div
            v-show="openIndex === i"
            class="px-5 pb-4 text-slate-600 leading-relaxed"
          >
            {{ faq.a }}
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
