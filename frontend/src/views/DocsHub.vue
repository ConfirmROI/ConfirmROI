<script setup>
import NavBar from '../components/NavBar.vue'
import SiteFooter from '../components/SiteFooter.vue'
import { TrendingUp, Server, Cloud, ArrowRight } from 'lucide-vue-next'
</script>

<template>
  <div class="min-h-screen bg-white">
    <NavBar />

    <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
      <div class="text-center mb-12">
        <h1 class="text-4xl font-bold text-gray-900 mb-3">Documentation</h1>
        <p class="text-lg text-gray-500">Choose the guide that matches how you use ConfirmROI.</p>
      </div>

      <div class="grid md:grid-cols-2 gap-6 lg:gap-8">
        <!-- Free / Open Source -->
        <router-link
          to="/docs/free"
          class="group rounded-2xl border-2 border-slate-200 p-8 hover:border-primary-300 hover:shadow-lg transition-all"
        >
          <div class="flex items-center gap-3 mb-4">
            <div class="w-12 h-12 rounded-xl bg-primary-50 flex items-center justify-center">
              <Server class="w-6 h-6 text-primary-600" />
            </div>
            <div>
              <h2 class="text-xl font-bold text-gray-900">Free (Open Source)</h2>
              <p class="text-sm text-gray-500">Self-hosted, single team</p>
            </div>
          </div>
          <p class="text-gray-600 text-sm mb-4">
            Everything you need to self-host ConfirmROI and track ROI for your engineering initiatives.
            Covers all 8 system formulas, 26 assumptions, cost tracking, CSV import, and deployment.
          </p>
          <span class="inline-flex items-center gap-1 text-sm font-semibold text-primary-600 group-hover:text-primary-700">
            Read the guide
            <ArrowRight class="w-4 h-4" />
          </span>
        </router-link>

        <!-- Paid / Hosted SaaS -->
        <router-link
          to="/docs/paid"
          class="group rounded-2xl border-2 border-slate-200 p-8 hover:border-primary-300 hover:shadow-lg transition-all"
        >
          <div class="flex items-center gap-3 mb-4">
            <div class="w-12 h-12 rounded-xl bg-accent-50 flex items-center justify-center">
              <Cloud class="w-6 h-6 text-accent-600" />
            </div>
            <div>
              <h2 class="text-xl font-bold text-gray-900">Paid (Hosted SaaS)</h2>
              <p class="text-sm text-gray-500">Managed, multi-team, enterprise</p>
            </div>
          </div>
          <p class="text-gray-600 text-sm mb-4">
            Guide for the managed platform: multi-team dashboards, hierarchical rollups, audit trails,
            SSO, scheduled reports, and enterprise features. Includes pricing and plan details.
          </p>
          <span class="inline-flex items-center gap-1 text-sm font-semibold text-accent-600 group-hover:text-accent-700">
            Read the guide
            <ArrowRight class="w-4 h-4" />
          </span>
        </router-link>
      </div>

      <div class="mt-12 border-t border-gray-200 pt-8">
        <div class="flex items-center gap-2 text-gray-500">
          <TrendingUp class="w-5 h-5" />
          <span class="text-sm">ConfirmROI is open-source software licensed under MIT. <a href="https://github.com/confirmroi/confirmroi" class="text-primary-600 hover:underline">View on GitHub</a></span>
        </div>
      </div>
    </div>

    <SiteFooter />
  </div>
</template>
