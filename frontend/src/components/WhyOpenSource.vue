<script setup>
import { Eye, Server, Users, Scale, Star } from 'lucide-vue-next'

const bullets = [
  {
    icon: Eye,
    title: 'Transparent formulas',
    description: "Every formula’s ROI calculation is visible and editable",
  },
  {
    icon: Server,
    title: 'Self-host with Docker',
    description: 'Your project data stays on your infrastructure',
  },
  {
    icon: Users,
    title: 'Community-driven',
    description: 'Contribute new formulas, report issues, shape the roadmap',
  },
  {
    icon: Scale,
    title: 'MIT licensed',
    description: 'Use it freely, fork it, build on it',
  },
]
</script>

<template>
  <section class="py-20 lg:py-28" style="background: linear-gradient(to right, #3b82f6, #172554)">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="grid lg:grid-cols-2 gap-12 lg:gap-16 items-center">
        <!-- Left: Copy -->
        <div>
          <h2 class="text-3xl sm:text-4xl font-bold text-white">
            ROI tools shouldn’t be a black box.
          </h2>
          <p class="mt-6 text-lg text-slate-200 leading-relaxed">
            ConfirmROI is free and open source. That means you can self-host it, audit the formulas, contribute
            improvements, and trust that your ROI calculations are transparent — not locked behind a proprietary
            algorithm. No vendor lock-in. No surprise price hikes. Just clear, defensible ROI math you can stand
            behind.
          </p>

          <a
            href="https://github.com/confirmroi/confirmroi"
            class="mt-8 inline-flex items-center gap-2 px-6 py-3 rounded-xl bg-white text-slate-900 font-semibold hover:bg-slate-100 transition-colors shadow-sm"
          >
            <Star class="w-5 h-5" />
            Star on GitHub
          </a>
        </div>

        <!-- Right: Bullet cards -->
        <div class="grid sm:grid-cols-2 gap-4">
          <div
            v-for="bullet in bullets"
            :key="bullet.title"
            class="rounded-xl bg-white border border-slate-200 p-5 hover:shadow-md transition-shadow"
          >
            <div class="flex items-center justify-center w-10 h-10 rounded-lg bg-accent-50 mb-3">
              <component :is="bullet.icon" class="w-5 h-5 text-accent-600" />
            </div>
            <h3 class="font-semibold text-primary-950">{{ bullet.title }}</h3>
            <p class="mt-1 text-sm text-slate-600">{{ bullet.description }}</p>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
