<script setup>
import { ArrowRight, ShieldCheck, Gift, Server, TrendingUp, LayoutDashboard, FolderKanban, Calculator, Lightbulb, Users } from 'lucide-vue-next'
import { RouterLink } from 'vue-router'
</script>

<template>
  <section class="relative overflow-hidden bg-primary-50">
    <!-- Decorative background -->
    <div class="absolute inset-0 -z-10">
      <div class="absolute top-0 left-1/2 -translate-x-1/2 w-[800px] h-[400px] bg-primary-200/40 rounded-full blur-3xl"></div>
      <div class="absolute top-40 right-0 w-[400px] h-[300px] bg-accent-200/20 rounded-full blur-3xl"></div>
    </div>

    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20 lg:py-28">
      <div class="grid lg:grid-cols-2 gap-12 lg:gap-16 items-center">
        <!-- Left: Copy -->
        <div>
          <h1 class="text-4xl sm:text-5xl lg:text-6xl font-extrabold text-primary-950 leading-tight tracking-tight">
            Stop guessing.<br />
            Start proving your ROI.
          </h1>
          <p class="mt-6 text-lg text-slate-600 leading-relaxed max-w-xl">            
            Not every project’s impact can be derived from a single, tidy line item. When the value is 
            multifaceted (losses avoided, risks mitigated, productivity gained across teams) ConfirmROI helps you make 
            the case with numbers instead of intuition.
          </p>

          <!-- CTAs -->
          <div class="mt-8 flex flex-col sm:flex-row gap-4">
            <a
              href="https://github.com/ConfirmROI/ConfirmROI"
              class="inline-flex items-center justify-center gap-2 px-6 py-3 rounded-xl bg-primary-600 text-white font-semibold hover:bg-primary-700 transition-colors shadow-sm"
            >
              Self-Host Free
              <ArrowRight class="w-4 h-4" />
            </a>
            <a
              href="#pricing"
              class="inline-flex items-center justify-center gap-2 px-6 py-3 rounded-xl bg-white text-primary-700 font-semibold border border-slate-300 hover:border-primary-400 hover:bg-primary-50 transition-colors"
            >
              Let us manage it
            </a>
          </div>

          <!-- Trust badges -->
          <div class="mt-8 flex flex-wrap gap-x-6 gap-y-2">
            <span class="inline-flex items-center gap-1.5 text-sm text-slate-600">
              <Gift class="w-4 h-4 text-accent-600" />
              Free &amp; Open Source
            </span>
            <span class="inline-flex items-center gap-1.5 text-sm text-slate-600">
              <Server class="w-4 h-4 text-accent-600" />
              Self-Host in Minutes with Docker
            </span>
            <span class="inline-flex items-center gap-1.5 text-sm text-slate-600">
              <ShieldCheck class="w-4 h-4 text-accent-600" />
              No signup wall
            </span>
          </div>
        </div>

        <!-- Right: Hero visual (dashboard mockup) -->
        <div class="relative">
          <div class="rounded-2xl border border-slate-200 bg-gray-50 shadow-2xl shadow-primary-900/10 overflow-hidden">
            <!-- Window chrome -->
            <div class="flex items-center gap-2 px-4 py-3 border-b border-slate-200 bg-white">
              <span class="w-3 h-3 rounded-full bg-red-400"></span>
              <span class="w-3 h-3 rounded-full bg-yellow-400"></span>
              <span class="w-3 h-3 rounded-full bg-green-400"></span>
              <span class="ml-3 text-xs text-slate-400 font-medium"></span>
            </div>

            <!-- Dashboard layout -->
            <div class="flex">
              <!-- Sidebar -->
              <div class="hidden sm:flex flex-col w-44 bg-white border-r border-gray-200 py-4 px-3 shrink-0">
                <div class="flex items-center gap-2 px-2 mb-4">
                  <div class="w-7 h-7 rounded-lg bg-primary-600 flex items-center justify-center">
                    <TrendingUp class="w-4 h-4 text-white" />
                  </div>
                  <span class="font-bold text-gray-900 text-sm">ConfirmROI</span>
                </div>
                <nav class="space-y-1">
                  <div class="flex items-center gap-2 px-2 py-1.5 rounded-lg bg-primary-50 text-primary-700 text-xs font-medium">
                    <LayoutDashboard class="w-4 h-4" /> Dashboard
                  </div>
                  <div class="flex items-center gap-2 px-2 py-1.5 rounded-lg text-gray-600 text-xs">
                    <Users class="w-4 h-4" /> Teams
                  </div>
                  <div class="flex items-center gap-2 px-2 py-1.5 rounded-lg text-gray-600 text-xs">
                    <FolderKanban class="w-4 h-4" /> Projects
                  </div>
                  <div class="flex items-center gap-2 px-2 py-1.5 rounded-lg text-gray-600 text-xs">
                    <Calculator class="w-4 h-4" /> Value Formulas
                  </div>
                  <div class="flex items-center gap-2 px-2 py-1.5 rounded-lg text-gray-600 text-xs">
                    <Lightbulb class="w-4 h-4" /> Assumptions
                  </div>
                </nav>
                <div class="mt-auto pt-4 border-t border-gray-200">
                  <p class="text-xs font-medium text-gray-900">Sarah Chen</p>
                </div>
              </div>

              <!-- Main content -->
              <div class="flex-1 p-4 space-y-4 overflow-hidden">
                <!-- Header -->
                <div class="flex items-center justify-between">
                  <h2 class="text-base font-bold text-gray-900">Dashboard</h2>
                  <span class="border border-gray-200 rounded px-2 py-1 text-xs text-gray-500 bg-white">Engineering</span>
                </div>

                <!-- Summary cards -->
                <div class="grid grid-cols-3 gap-3">
                  <div class="bg-white rounded-xl border border-gray-200 p-3">
                    <p class="text-xs text-gray-500 mb-0.5">Total Projects</p>
                    <p class="text-lg font-bold text-gray-900">12</p>
                  </div>
                  <div class="bg-white rounded-xl border border-gray-200 p-3">
                    <p class="text-xs text-gray-500 mb-0.5">Total ROI</p>
                    <p class="text-lg font-bold text-primary-600">$2.4M</p>
                  </div>
                  <div class="bg-white rounded-xl border border-gray-200 p-3">
                    <p class="text-xs text-gray-500 mb-0.5">Value Formulas</p>
                    <p class="text-lg font-bold text-gray-900">8</p>
                  </div>
                </div>

                <!-- Bar chart mockup -->
                <div class="bg-white rounded-xl border border-gray-200 p-4">
                  <p class="text-sm font-semibold text-gray-900 mb-3">ROI by Project — Value Formula Breakdown</p>
                  <div class="flex items-stretch gap-2 h-32">
                    <div class="flex-1 min-w-0 flex flex-col items-center gap-1 h-full">
                      <div class="w-full flex flex-col justify-end flex-1">
                        <div class="w-full rounded-t" style="background: #84cc16; height: 35%"></div>
                      </div>
                      <span class="text-[9px] text-gray-400 truncate w-full text-center">CI/CD</span>
                    </div>
                    <div class="flex-1 min-w-0 flex flex-col items-center gap-1 h-full">
                      <div class="w-full flex flex-col justify-end flex-1">
                        <div class="w-full rounded-t" style="background: #d4d480; height: 45%"></div>
                      </div>
                      <span class="text-[9px] text-gray-400 truncate w-full text-center">Portal</span>
                    </div>
                    <div class="flex-1 min-w-0 flex flex-col items-center gap-1 h-full">
                      <div class="w-full flex flex-col justify-end flex-1">
                        <div class="w-full rounded-t" style="background: #06b6d4; height: 55%"></div>
                      </div>
                      <span class="text-[9px] text-gray-400 truncate w-full text-center">QA Suite</span>
                    </div>
                    <div class="flex-1 min-w-0 flex flex-col items-center gap-1 h-full">
                      <div class="w-full flex flex-col justify-end flex-1">
                        <div class="w-full rounded-t" style="background: #e11d48; height: 70%"></div>
                      </div>
                      <span class="text-[9px] text-gray-400 truncate w-full text-center">SOC2</span>
                    </div>
                    <div class="flex-1 min-w-0 flex flex-col items-center gap-1 h-full">
                      <div class="w-full flex flex-col justify-end flex-1">
                        <div class="w-full rounded-t" style="background: #8b5cf6; height: 90%"></div>
                      </div>
                      <span class="text-[9px] text-gray-400 truncate w-full text-center">TypeScript</span>
                    </div>
                    <div class="flex-1 min-w-0 flex flex-col items-center gap-1 h-full">
                      <div class="w-full flex flex-col justify-end flex-1">
                        <div class="w-full rounded-t" style="background: #f97316; height: 60%"></div>
                      </div>
                      <span class="text-[9px] text-gray-400 truncate w-full text-center">P1 Incidents</span>
                    </div>
                    <div class="flex-1 min-w-0 flex flex-col items-center gap-1 h-full">
                      <div class="w-full flex flex-col justify-end flex-1">
                        <div class="w-full rounded-t" style="background: #2f5c28; height: 40%"></div>
                      </div>
                      <span class="text-[9px] text-gray-400 truncate w-full text-center">Legacy</span>
                    </div>
                    <div class="flex-1 min-w-0 flex flex-col items-center gap-1 h-full">
                      <div class="w-full flex flex-col justify-end flex-1">
                        <div class="w-full rounded-t" style="background: #d4d480; height: 50%"></div>
                      </div>
                      <span class="text-[9px] text-gray-400 truncate w-full text-center">Zero-Trust</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
