<script setup>
import { ref } from 'vue'
import { RouterLink } from 'vue-router'
import { Menu, X, TrendingUp } from 'lucide-vue-next'

const mobileOpen = ref(false)

const navLinks = [
  { label: 'Features', href: '#value-formulas' },
  { label: 'How It Works', href: '#how-it-works' },
  { label: 'Pricing', href: '#pricing' },
  { label: 'Docs', to: '/docs' },
]

function closeMobile() {
  mobileOpen.value = false
}
</script>

<template>
  <nav class="sticky top-0 z-50 bg-white/90 backdrop-blur-md border-b border-slate-200">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-center justify-between h-16">
        <!-- Logo -->
        <a href="/" class="flex items-center gap-2 font-bold text-xl text-primary-900">
          <span class="flex items-center justify-center w-8 h-8 rounded-lg bg-primary-900">
            <TrendingUp class="w-5 h-5 text-accent-400" />
          </span>
          ConfirmROI
        </a>

        <!-- Desktop nav -->
        <div class="hidden md:flex items-center gap-8">
          <a
            v-for="link in navLinks.filter(l => l.href)"
            :key="link.href"
            :href="link.href"
            class="text-sm font-medium text-slate-600 hover:text-primary-700 transition-colors"
          >
            {{ link.label }}
          </a>
          <RouterLink
            v-for="link in navLinks.filter(l => l.to)"
            :key="link.to"
            :to="link.to"
            class="text-sm font-medium text-slate-600 hover:text-primary-700 transition-colors"
          >
            {{ link.label }}
          </RouterLink>
        </div>

        <!-- Desktop CTAs -->
        <div class="hidden md:flex items-center gap-4">
          <RouterLink to="/login" class="text-sm font-medium text-slate-600 hover:text-primary-700 transition-colors">
            Sign In
          </RouterLink>
          <RouterLink
            to="/register"
            class="inline-flex items-center px-4 py-2 rounded-lg bg-primary-600 text-white text-sm font-semibold hover:bg-primary-700 transition-colors shadow-sm"
          >
            Get Started Free
          </RouterLink>
        </div>

        <!-- Mobile toggle -->
        <button
          class="md:hidden p-2 text-slate-600 hover:text-primary-700"
          @click="mobileOpen = !mobileOpen"
        >
          <Menu v-if="!mobileOpen" class="w-6 h-6" />
          <X v-else class="w-6 h-6" />
        </button>
      </div>
    </div>

    <!-- Mobile menu -->
    <div v-if="mobileOpen" class="md:hidden border-t border-slate-200 bg-white">
      <div class="px-4 py-4 space-y-3">
        <a
          v-for="link in navLinks.filter(l => l.href)"
          :key="link.href"
          :href="link.href"
          class="block text-sm font-medium text-slate-600 hover:text-primary-700"
          @click="closeMobile"
        >
          {{ link.label }}
        </a>
        <RouterLink
          v-for="link in navLinks.filter(l => l.to)"
          :key="link.to"
          :to="link.to"
          class="block text-sm font-medium text-slate-600 hover:text-primary-700"
          @click="closeMobile"
        >
          {{ link.label }}
        </RouterLink>
        <hr class="border-slate-200" />
        <RouterLink to="/login" class="block text-sm font-medium text-slate-600 hover:text-primary-700" @click="closeMobile">
          Sign In
        </RouterLink>
        <RouterLink
          to="/register"
          class="block text-center px-4 py-2 rounded-lg bg-primary-600 text-white text-sm font-semibold"
          @click="closeMobile"
        >
          Get Started Free
        </RouterLink>
      </div>
    </div>
  </nav>
</template>
