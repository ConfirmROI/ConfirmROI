<script setup>
import { Check } from 'lucide-vue-next'
import { RouterLink } from 'vue-router'

const tiers = [
  {
    name: 'Starter',
    price: '$9',
    period: '/seat/mo',
    seats: 'Up to 25',
    readonlySeats: '200',
    teams: 'Up to 10',
    hierarchy: '2 levels',
    support: 'Email',
    highlight: false,
  },
  {
    name: 'Growth',
    price: '$19',
    period: '/seat/mo',
    seats: 'Up to 100',
    readonlySeats: '1000',
    teams: 'Unlimited',
    hierarchy: '5 levels',
    sso: 'Google',
    audit: 'Yes',
    support: 'Priority email',
    highlight: false,
  },
  {
    name: 'Enterprise',
    price: 'Contact us',
    period: '',
    seats: 'Unlimited',
    readonlySeats: 'Unlimited',
    teams: 'Unlimited',
    hierarchy: 'Unlimited',
    sso: 'Google + Okta/SAML',
    audit: 'Yes',
    scheduled: 'Yes',
    support: 'Dedicated',
    highlight: false,
  },
]

const features = [
  { key: 'seats', label: 'Seats' },
  { key: 'readonlySeats', label: 'Read-only seats' },
  { key: 'teams', label: 'Teams' },
  { key: 'hierarchy', label: 'Hierarchy levels' },
  { key: 'sso', label: 'SSO' },
  { key: 'audit', label: 'Audit trail' },
  { key: 'scheduled', label: 'Scheduled reports' },
  { key: 'support', label: 'Support' },
]
</script>

<template>
  <section class="py-20 lg:py-28 bg-primary-950">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="text-center max-w-2xl mx-auto">
        <h2 class="text-3xl sm:text-4xl font-bold text-white">
          Simple, per-seat pricing.
        </h2>
        <p class="mt-4 text-lg text-slate-300">
          Self-host for free, or let us run it for you.
          Paid tiers add collaboration, multi-team dashboards, and enterprise features.
        </p>
      </div>

      <div class="mt-12 grid md:grid-cols-3 gap-6 lg:gap-8">
        <div
          v-for="tier in tiers"
          :key="tier.name"
          class="rounded-2xl border p-6 lg:p-8 flex flex-col"
          :class="tier.highlight
            ? 'border-primary-300 ring-2 ring-primary-200 shadow-lg bg-white'
            : 'border-slate-200 bg-white'"
        >

          <h3 class="text-xl font-bold text-primary-950">{{ tier.name }}</h3>
          <div class="mt-2 flex items-baseline gap-1">
            <span class="text-3xl font-extrabold text-primary-950">{{ tier.price }}</span>
            <span class="text-sm text-slate-500">{{ tier.period }}</span>
          </div>

          <ul class="mt-6 space-y-3 flex-1">
            <li
              v-for="feat in features"
              :key="feat.key"
              class="flex items-start gap-2 text-sm"
            >
              <Check v-if="tier[feat.key]" class="w-4 h-4 text-accent-600 mt-0.5 flex-shrink-0" />
              <span v-else class="w-4 h-4 mt-0.5 flex-shrink-0 text-slate-300">&nbsp;</span>
              <span class="text-slate-600">
                <span class="font-medium text-slate-700">{{ feat.label }}:</span>
                {{ tier[feat.key] || '✖️' }}
              </span>
            </li>
          </ul>

          <RouterLink
            :to="{ path: '/register', query: { plan: tier.name } }"
            class="mt-8 inline-flex items-center justify-center px-6 py-3 rounded-xl font-semibold transition-colors"
            :class="tier.highlight
              ? 'bg-primary-600 text-white hover:bg-primary-700'
              : 'bg-slate-100 text-primary-700 hover:bg-slate-200'"
          >
            Get Started
          </RouterLink>
        </div>
      </div>

    </div>
  </section>
</template>
