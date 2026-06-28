<script setup>
import { TrendingUp } from 'lucide-vue-next'

const columns = [
  {
    title: 'Product',
    links: [
      { label: 'Features', href: '#value-formulas' },
      { label: 'Pricing', href: '#pricing' },
      { label: 'Changelog', href: '#' },
      { label: 'Roadmap', href: '#' },
    ],
  },
  {
    title: 'Resources',
    links: [
      { label: 'Docs', href: '/docs' },
      { label: 'GitHub', href: 'https://github.com/confirmroi/confirmroi' },
      { label: 'Blog', href: '#' },
      { label: 'Community', href: '#' },
    ],
  },
  {
    title: 'Company',
    links: [
      { label: 'About', href: '#' },
      { label: 'Contact', href: '#' },
      { label: 'Privacy', href: '#' },
      { label: 'Terms', href: '#' },
    ],
  },
]
</script>

<template>
  <footer class="bg-primary-950 text-slate-300">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
      <div class="grid lg:grid-cols-5 gap-8 lg:gap-12">
        <!-- Logo + tagline -->
        <div class="lg:col-span-2">
          <a href="/" class="flex items-center gap-2 font-bold text-xl text-white">
            <span class="flex items-center justify-center w-8 h-8 rounded-lg bg-primary-800">
              <TrendingUp class="w-5 h-5 text-accent-400" />
            </span>
            ConfirmROI
          </a>
          <p class="mt-4 text-sm text-slate-400 max-w-xs">
            Stop guessing. Start proving your ROI.
          </p>
        </div>

        <!-- Link columns -->
        <div
          v-for="col in columns"
          :key="col.title"
          class="space-y-3"
        >
          <h4 class="text-sm font-semibold text-white uppercase tracking-wide">{{ col.title }}</h4>
          <ul class="space-y-2">
            <li v-for="link in col.links" :key="link.label">
              <a :href="link.href" class="text-sm text-slate-400 hover:text-white transition-colors">
                {{ link.label }}
              </a>
            </li>
          </ul>
        </div>
      </div>

      <!-- Bottom bar -->
      <div class="mt-12 pt-8 border-t border-primary-800 flex flex-col sm:flex-row items-center justify-between gap-4">
        <p class="text-sm text-slate-400">
          &copy; {{ new Date().getFullYear() }} ConfirmROI. MIT licensed.
        </p>
      </div>
    </div>
  </footer>
</template>
