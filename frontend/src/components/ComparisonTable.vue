<script setup>
import { Check, X, ArrowRight } from 'lucide-vue-next'
import { RouterLink } from 'vue-router'

const rows = [
  { feature: 'Price', free: 'Free, open source', paid: 'Per-seat subscription' },
  { feature: 'Hosting', free: 'Self-hosted (Docker)', paid: 'Managed cloud' },
  { feature: 'Users', free: 'Single user', paid: 'Organization-wide' },
  { feature: 'Teams', free: '1 team', paid: 'Multiple teams per manager' },
  { feature: 'Hierarchy & Rollups', free: null, paid: 'Multiple levels' },
  { feature: 'Project import', free: 'CSV, Jira API, manual', paid: 'Same' },
  { feature: 'Value formulas', free: 'System + custom', paid: 'Same + org-wide sharing' },
  { feature: 'Value assumptions', free: 'Editable per project', paid: 'Editable + collaborative with audit trail' },
  { feature: 'ROI calculation', free: 'Per-project', paid: 'Per-project + rollup aggregation' },
  { feature: 'Dashboard', free: 'Single team view', paid: 'Multi-team, rollup, custom views' },
  { feature: 'Collaboration', free: null, paid: 'Multiple managers, shared assumptions, comments' },
  { feature: 'SSO', free: null, paid: 'Yes' },
  { feature: 'Export', free: 'CSV', paid: 'CSV + PDF + scheduled reports' },
  { feature: 'Support', free: 'Community', paid: 'Email + priority' },
  { feature: 'License', free: 'MIT', paid: 'Commercial' },
]
</script>

<template>
  <section id="pricing" class="py-20 lg:py-28 bg-primary-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- Heading -->
      <div class="text-center max-w-2xl mx-auto">
        <h2 class="text-3xl sm:text-4xl font-bold text-primary-950">
          Self-host or let us manage it.
        </h2>
        <p class="mt-4 text-lg text-slate-600">
          The free version is fully functional for a single manager and team. The paid version adds
          organization-wide collaboration, hierarchical rollups, and enterprise features.
        </p>
      </div>

      <!-- Comparison table -->
      <div class="mt-12 overflow-x-auto max-w-4xl mx-auto">
        <table class="w-full border-collapse bg-white rounded-xl overflow-hidden shadow-md border-2 border-slate-300">
          <thead>
            <tr class="border-b-2 border-slate-300 bg-slate-100">
              <th class="text-left py-4 px-4 text-base font-bold text-slate-700 uppercase tracking-wide border-r border-slate-300">Feature</th>
              <th class="text-center py-4 px-4 text-base font-extrabold text-primary-900 uppercase tracking-wide bg-primary-100 border-r border-slate-300">
                Free (OSS)
              </th>
              <th class="text-center py-4 px-4 text-base font-extrabold text-slate-800 uppercase tracking-wide bg-slate-200">
                Paid (SaaS)
              </th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="(row, i) in rows"
              :key="i"
              class="border-b border-slate-200 hover:bg-slate-50 transition-colors"
            >
              <td class="py-4 px-4 text-base font-bold text-slate-800 border-r border-slate-200">{{ row.feature }}</td>
              <td class="py-4 px-4 text-center text-base text-slate-700 bg-primary-50 border-r border-slate-200">
                <span v-if="row.free === null" class="inline-flex"><X class="w-5 h-5 text-slate-400" /></span>
                <span v-else class="inline-flex items-center gap-1.5 font-medium">
                  <Check class="w-5 h-5 text-accent-600" />
                  {{ row.free }}
                </span>
              </td>
              <td class="py-4 px-4 text-center text-base text-slate-700 font-medium bg-white">
                <span v-if="row.paid === null" class="inline-flex"><X class="w-5 h-5 text-slate-400" /></span>
                <span v-else class="inline-flex items-center gap-1.5">
                  <Check class="w-5 h-5 text-accent-600" />
                  {{ row.paid }}
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- CTAs below table -->
      <div class="mt-10 grid sm:grid-cols-2 gap-4 max-w-lg mx-auto">
        <a
          href="https://github.com/ConfirmROI/ConfirmROI"
          class="inline-flex items-center justify-center gap-2 px-6 py-3.5 rounded-xl bg-accent-600 text-white font-bold hover:bg-accent-700 transition-colors shadow-sm"
        >
          Self-Host Free
          <ArrowRight class="w-4 h-4" />
        </a>
        <RouterLink
          to="/register"
          class="inline-flex items-center justify-center gap-2 px-6 py-3.5 rounded-xl bg-primary-600 text-white font-bold hover:bg-primary-700 transition-colors shadow-sm"
        >
          Let us manage it
          <ArrowRight class="w-4 h-4" />
        </RouterLink>
      </div>
    </div>
  </section>
</template>
