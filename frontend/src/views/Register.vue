<script setup>
import { ref, reactive, computed, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { TrendingUp, Mail, Lock, User, ArrowRight, Check, ArrowLeft } from 'lucide-vue-next'

const router = useRouter()
const route = useRoute()
const auth = useAuthStore()

const isPaid = import.meta.env.VITE_IS_PAID === 'true'
const showPlans = computed(() => isPaid || !!route.query.plan)

const plans = [
  {
    name: 'Starter',
    price: '$9',
    period: '/seat/mo',
    seats: 'Up to 25',
    teams: 'Up to 10',
    features: ['Up to 25 seats', 'Up to 10 teams', '2 hierarchy levels', 'Email support'],
  },
  {
    name: 'Growth',
    price: '$19',
    period: '/seat/mo',
    seats: 'Up to 100',
    teams: 'Unlimited',
    features: ['Up to 100 seats', 'Unlimited teams', '5 hierarchy levels', 'Google SSO', 'Audit trail', 'Priority email support'],
  },
  {
    name: 'Enterprise',
    price: 'Contact us',
    period: '',
    features: ['Unlimited seats', 'Unlimited teams', 'Unlimited hierarchy', 'Google + Okta/SAML SSO', 'Audit trail', 'Scheduled reports', 'Dedicated support'],
  },
]

const selectedPlan = ref(route.query.plan || null)

watch(() => route.query.plan, (newPlan) => {
  selectedPlan.value = newPlan || selectedPlan.value
})

const selectedPlanObj = computed(() => {
  return plans.find(p => p.name === selectedPlan.value) || null
})

const form = reactive({ name: '', email: '', password: '' })
const errorMsg = ref('')

function selectPlan(name) {
  selectedPlan.value = name
}

function goBackToPlans() {
  selectedPlan.value = null
}

async function handleSubmit() {
  errorMsg.value = ''
  const success = await auth.register(form.email, form.password, form.name)
  if (success) {
    router.push('/dashboard')
  } else {
    errorMsg.value = auth.error || 'Registration failed'
  }
}
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 px-4 py-12">
    <div class="max-w-md w-full">
      <div class="text-center mb-8">
        <div class="inline-flex items-center justify-center w-14 h-14 rounded-xl bg-primary-600 mb-4">
          <TrendingUp class="w-7 h-7 text-white" />
        </div>
        <h1 class="text-2xl font-bold text-gray-900">Create your account</h1>
        <p class="text-gray-500 mt-1">Start measuring ROI with ConfirmROI</p>
      </div>

      <!-- Paid version: Plan selection step -->
      <template v-if="showPlans && !selectedPlan">
        <p class="text-center text-sm text-gray-600 mb-6">
          Choose a plan to get started. You'll complete payment on the next step.
        </p>

        <div class="space-y-4">
          <div
            v-for="plan in plans"
            :key="plan.name"
            class="border border-gray-200 rounded-xl p-5 bg-white hover:border-primary-400 hover:ring-1 hover:ring-primary-300 cursor-pointer transition"
            @click="selectPlan(plan.name)"
          >
            <div class="flex items-center justify-between mb-2">
              <h3 class="text-lg font-bold text-gray-900">{{ plan.name }}</h3>
              <div class="flex items-baseline gap-1">
                <span class="text-2xl font-extrabold text-primary-600">{{ plan.price }}</span>
                <span class="text-sm text-gray-500">{{ plan.period }}</span>
              </div>
            </div>
            <ul class="space-y-1.5">
              <li
                v-for="feat in plan.features"
                :key="feat"
                class="flex items-start gap-2 text-sm text-gray-600"
              >
                <Check class="w-4 h-4 text-accent-600 mt-0.5 flex-shrink-0" />
                {{ feat }}
              </li>
            </ul>
          </div>
        </div>

        <p class="text-center text-sm text-gray-500 mt-6">
          Already have an account?
          <router-link to="/login" class="text-primary-600 hover:text-primary-700 font-medium">Sign in</router-link>
        </p>
      </template>

      <!-- Paid version: Payment placeholder step -->
      <template v-else-if="showPlans && selectedPlan">
        <div v-if="errorMsg" class="bg-red-50 border border-red-200 text-red-700 rounded-lg px-4 py-3 mb-4 text-sm">
          {{ errorMsg }}
        </div>

        <!-- Selected plan summary -->
        <div class="bg-white border border-gray-200 rounded-xl p-5 mb-6">
          <div class="flex items-center justify-between mb-3">
            <div>
              <h3 class="text-lg font-bold text-gray-900">{{ selectedPlanObj.name }}</h3>
              <p class="text-sm text-gray-500">{{ selectedPlanObj.price }}{{ selectedPlanObj.period }}</p>
            </div>
            <button @click="goBackToPlans" class="text-sm text-primary-600 hover:text-primary-700 font-medium flex items-center gap-1">
              <ArrowLeft class="w-4 h-4" /> Change plan
            </button>
          </div>
          <ul class="space-y-1.5">
            <li
              v-for="feat in selectedPlanObj.features"
              :key="feat"
              class="flex items-start gap-2 text-sm text-gray-600"
            >
              <Check class="w-4 h-4 text-accent-600 mt-0.5 flex-shrink-0" />
              {{ feat }}
            </li>
          </ul>
        </div>

        <!-- Account details form -->
        <form @submit.prevent="handleSubmit" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Name</label>
            <div class="relative">
              <User class="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
              <input
                v-model="form.name"
                type="text"
                required
                placeholder="John Doe"
                class="w-full pl-10 pr-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 outline-none transition"
              />
            </div>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Email</label>
            <div class="relative">
              <Mail class="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
              <input
                v-model="form.email"
                type="email"
                required
                placeholder="you@company.com"
                class="w-full pl-10 pr-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 outline-none transition"
              />
            </div>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Password</label>
            <div class="relative">
              <Lock class="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
              <input
                v-model="form.password"
                type="password"
                required
                minlength="6"
                placeholder="••••••••"
                class="w-full pl-10 pr-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 outline-none transition"
              />
            </div>
          </div>

          <!-- Payment placeholder button -->
          <div class="pt-2">
            <div class="bg-gray-100 border border-dashed border-gray-300 rounded-lg p-4 text-center">
              <p class="text-sm text-gray-500 mb-3">Payment integration coming soon</p>
              <button
                type="button"
                disabled
                class="w-full flex items-center justify-center gap-2 bg-gray-300 text-gray-500 font-medium py-2.5 rounded-lg cursor-not-allowed"
              >
                Continue to Payment
                <ArrowRight class="w-4 h-4" />
              </button>
            </div>
          </div>
        </form>

        <p class="text-center text-sm text-gray-500 mt-6">
          Already have an account?
          <router-link to="/login" class="text-primary-600 hover:text-primary-700 font-medium">Sign in</router-link>
        </p>
      </template>

      <!-- Free version: Direct registration form (no plan selection) -->
      <template v-else>
        <div v-if="errorMsg" class="bg-red-50 border border-red-200 text-red-700 rounded-lg px-4 py-3 mb-4 text-sm">
          {{ errorMsg }}
        </div>

        <form @submit.prevent="handleSubmit" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Name</label>
            <div class="relative">
              <User class="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
              <input
                v-model="form.name"
                type="text"
                required
                placeholder="John Doe"
                class="w-full pl-10 pr-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 outline-none transition"
              />
            </div>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Email</label>
            <div class="relative">
              <Mail class="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
              <input
                v-model="form.email"
                type="email"
                required
                placeholder="you@company.com"
                class="w-full pl-10 pr-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 outline-none transition"
              />
            </div>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Password</label>
            <div class="relative">
              <Lock class="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
              <input
                v-model="form.password"
                type="password"
                required
                minlength="6"
                placeholder="••••••••"
                class="w-full pl-10 pr-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 outline-none transition"
              />
            </div>
          </div>

          <button
            type="submit"
            :disabled="auth.loading"
            class="w-full flex items-center justify-center gap-2 bg-primary-600 hover:bg-primary-700 text-white font-medium py-2.5 rounded-lg transition disabled:opacity-50"
          >
            <span v-if="auth.loading">Creating account...</span>
            <template v-else>
              Create account
              <ArrowRight class="w-4 h-4" />
            </template>
          </button>
        </form>

        <p class="text-center text-sm text-gray-500 mt-6">
          Already have an account?
          <router-link to="/login" class="text-primary-600 hover:text-primary-700 font-medium">Sign in</router-link>
        </p>
      </template>
    </div>
  </div>
</template>
