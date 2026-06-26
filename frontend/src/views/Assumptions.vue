<script setup>
import { ref, onMounted, reactive } from 'vue'
import { useAssumptionsStore } from '../stores/assumptions'
import { useDashboardStore } from '../stores/dashboard'
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'
import { Plus, Trash2, TrendingUp, LayoutDashboard, FolderKanban, Calculator, Lightbulb, Users, Menu, X, Pencil, Link2, LogOut } from 'lucide-vue-next'

const router = useRouter()
const auth = useAuthStore()
const assumptionsStore = useAssumptionsStore()
const dashboardStore = useDashboardStore()

function logout() {
  auth.logout()
  router.push('/login')
}

const sidebarOpen = ref(false)
const showCreate = ref(false)

const form = reactive({
  key: '',
  label: '',
  data_type: 'number',
  default_value: 0,
  description: '',
})

onMounted(async () => {
  await assumptionsStore.fetchAssumptions()
  await dashboardStore.fetchUsage()
})

function resetForm() {
  form.key = ''
  form.label = ''
  form.data_type = 'number'
  form.default_value = 0
  form.description = ''
}

function startCreate() {
  resetForm()
  showCreate.value = true
}

async function handleSubmit() {
  const data = {
    key: form.key,
    label: form.label,
    data_type: form.data_type,
    default_value: Number(form.default_value),
    description: form.description,
  }
  const created = await assumptionsStore.createAssumption(data)
  if (created) {
    showCreate.value = false
    resetForm()
  }
}

function getUsage(assumptionId) {
  return dashboardStore.usageStats.assumptions[assumptionId] || { formula_count: 0, project_count: 0 }
}

</script>

<template>
  <div class="min-h-screen bg-gray-50 flex">
    <!-- Sidebar -->
    <aside
      :class="[
        'fixed inset-y-0 left-0 z-40 w-64 bg-white border-r border-gray-200 transform transition-transform flex flex-col lg:sticky lg:top-0 lg:h-screen lg:translate-x-0',
        sidebarOpen ? 'translate-x-0' : '-translate-x-full'
      ]"
    >
      <div class="flex items-center gap-2 px-6 py-4 border-b border-gray-200">
        <div class="w-8 h-8 rounded-lg bg-primary-600 flex items-center justify-center">
          <TrendingUp class="w-5 h-5 text-white" />
        </div>
        <span class="font-bold text-gray-900">ConfirmROI</span>
      </div>
      <nav class="p-4 space-y-1 flex-1 overflow-y-auto">
        <router-link to="/dashboard" class="flex items-center gap-3 px-3 py-2 rounded-lg text-gray-700 hover:bg-gray-100 transition" active-class="bg-primary-50 text-primary-700">
          <LayoutDashboard class="w-5 h-5" /> Dashboard
        </router-link>
        <router-link v-if="auth.userTier === 'paid'" to="/teams" class="flex items-center gap-3 px-3 py-2 rounded-lg text-gray-700 hover:bg-gray-100 transition" active-class="bg-primary-50 text-primary-700">
          <Users class="w-5 h-5" /> Teams
        </router-link>
        <router-link to="/projects" class="flex items-center gap-3 px-3 py-2 rounded-lg text-gray-700 hover:bg-gray-100 transition" active-class="bg-primary-50 text-primary-700">
          <FolderKanban class="w-5 h-5" /> Projects
        </router-link>
        <router-link to="/formulas" class="flex items-center gap-3 px-3 py-2 rounded-lg text-gray-700 hover:bg-gray-100 transition" active-class="bg-primary-50 text-primary-700">
          <Calculator class="w-5 h-5" /> Value Formulas
        </router-link>
        <router-link to="/assumptions" class="flex items-center gap-3 px-3 py-2 rounded-lg text-gray-700 hover:bg-gray-100 transition" active-class="bg-primary-50 text-primary-700">
          <Lightbulb class="w-5 h-5" /> Assumptions
        </router-link>
      </nav>
      <div v-if="auth.userTier === 'paid'" class="border-t border-gray-200 pt-4">
        <div class="px-3 py-2">
          <p class="text-sm font-medium text-gray-900">{{ auth.userName }}</p>
          <p class="text-xs text-gray-500 capitalize">{{ auth.userTier }} tier</p>
        </div>
        <button @click="logout" class="flex items-center gap-3 px-3 py-2 rounded-lg text-gray-700 hover:bg-gray-100 transition w-full">
          <LogOut class="w-5 h-5" /> Logout
        </button>
      </div>
    </aside>

    <!-- Mobile overlay -->
    <div v-if="sidebarOpen" @click="sidebarOpen = false" class="fixed inset-0 bg-black/30 z-30 lg:hidden" />

    <!-- Main content -->
    <main class="flex-1 lg:ml-0">
      <!-- Mobile header -->
      <div class="lg:hidden flex items-center justify-between px-4 py-3 bg-white border-b border-gray-200">
        <button @click="sidebarOpen = !sidebarOpen">
          <Menu v-if="!sidebarOpen" class="w-6 h-6 text-gray-600" />
          <X v-else class="w-6 h-6 text-gray-600" />
        </button>
        <span class="font-bold text-gray-900">ConfirmROI</span>
      </div>

      <div class="p-6 max-w-5xl mx-auto">
        <div class="flex items-center justify-between mb-6">
          <h1 class="text-2xl font-bold text-gray-900">Assumptions</h1>
          <button @click="startCreate" class="flex items-center gap-2 px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition">
            <Plus class="w-4 h-4" /> New Assumption
          </button>
        </div>

        <!-- Create form -->
        <div v-if="showCreate" class="bg-white rounded-xl border border-gray-200 p-6 mb-6">
          <h3 class="font-semibold text-gray-900 mb-4">Create Assumption</h3>
          <form @submit.prevent="handleSubmit" class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Key</label>
              <input v-model="form.key" required placeholder="e.g. hours_saved" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 outline-none font-mono text-sm" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Label</label>
              <input v-model="form.label" required placeholder="e.g. Hours Saved" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 outline-none" />
            </div>
            <div class="flex gap-4">
              <div class="flex-1">
                <label class="block text-sm font-medium text-gray-700 mb-1">Data Type</label>
                <select v-model="form.data_type" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 outline-none">
                  <option value="number">number</option>
                  <option value="currency">currency</option>
                  <option value="percentage">percentage</option>
                </select>
              </div>
              <div class="flex-1">
                <label class="block text-sm font-medium text-gray-700 mb-1">Default Value</label>
                <input v-model.number="form.default_value" type="number" step="any" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 outline-none" />
              </div>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Description</label>
              <textarea v-model="form.description" rows="2" placeholder="Optional description" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 outline-none"></textarea>
            </div>
            <div class="flex gap-2">
              <button type="submit" class="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition">Create</button>
              <button type="button" @click="showCreate = false; resetForm()" class="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition">Cancel</button>
            </div>
          </form>
        </div>

        <!-- Assumptions list -->
        <div class="space-y-2">
          <div
            v-for="a in assumptionsStore.assumptions"
            :key="a.id"
            @click="router.push(`/assumptions/${a.id}`)"
            class="flex items-center justify-between p-4 bg-white rounded-xl border border-gray-200 hover:border-primary-300 hover:shadow-sm cursor-pointer transition"
          >
            <div class="flex-1">
              <div class="flex items-center gap-2">
                <span class="font-medium text-gray-900">{{ a.label }}</span>
                <span class="text-xs font-mono text-gray-500">({{ a.key }})</span>
                <span class="text-xs px-2 py-0.5 rounded bg-gray-200 text-gray-600">{{ a.data_type }}</span>
                <span v-if="a.is_system" class="text-xs text-blue-600 font-medium">System</span>
              </div>
              <p v-if="a.description" class="text-xs text-gray-500 mt-1">{{ a.description }}</p>
              <p class="text-xs text-gray-400 mt-1">Default: {{ a.default_value }}</p>
              <div v-if="getUsage(a.id).formula_count > 0 || getUsage(a.id).project_count > 0" class="flex items-center gap-2 mt-2">
                <span
                  v-if="getUsage(a.id).formula_count > 0"
                  class="flex items-center gap-1 text-xs px-2 py-1 rounded-lg bg-primary-50 text-primary-700"
                >
                  <Link2 class="w-3 h-3" /> {{ getUsage(a.id).formula_count }} formula{{ getUsage(a.id).formula_count > 1 ? 's' : '' }}
                </span>
                <span
                  v-if="getUsage(a.id).project_count > 0"
                  class="flex items-center gap-1 text-xs px-2 py-1 rounded-lg bg-primary-50 text-primary-700"
                >
                  <Link2 class="w-3 h-3" /> {{ getUsage(a.id).project_count }} project{{ getUsage(a.id).project_count > 1 ? 's' : '' }}
                </span>
              </div>
            </div>
            <Pencil class="w-4 h-4 text-gray-300" />
          </div>
        </div>

        <div v-if="assumptionsStore.assumptions.length === 0" class="text-center py-12 text-gray-500">
          No assumptions available. Create one to get started.
        </div>
      </div>
    </main>
  </div>
</template>
