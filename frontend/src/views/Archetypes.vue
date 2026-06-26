<script setup>
import { ref, onMounted, reactive, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useDashboardStore } from '../stores/dashboard'
import { useAssumptionsStore } from '../stores/assumptions'
import { useAuthStore } from '../stores/auth'
import { Plus, Trash2, Pencil, Calculator, TrendingUp, LayoutDashboard, FolderKanban, Lightbulb, Users, Menu, X, Link2, LogOut } from 'lucide-vue-next'

const router = useRouter()
const route = useRoute()
const auth = useAuthStore()
const dashboardStore = useDashboardStore()
const assumptionsStore = useAssumptionsStore()

function logout() {
  auth.logout()
  router.push('/login')
}

const sidebarOpen = ref(false)
const showCreate = ref(false)
const form = reactive({ name: '', description: '', formula: '', assumption_ids: [] })
const filterAssumptionId = ref(null)

onMounted(async () => {
  await dashboardStore.fetchArchetypes()
  await assumptionsStore.fetchAssumptions()
  await dashboardStore.fetchUsage()
  if (route.query.assumption) {
    filterAssumptionId.value = parseInt(route.query.assumption)
  }
})

const filteredArchetypes = computed(() => {
  if (!filterAssumptionId.value) return dashboardStore.archetypes
  return dashboardStore.archetypes.filter(a =>
    a.assumptions?.some(asm => asm.id === filterAssumptionId.value)
  )
})

function getArchetypeUsage(archetypeId) {
  return dashboardStore.usageStats.archetypes[archetypeId] || { project_count: 0 }
}

function clearFilter() {
  filterAssumptionId.value = null
  router.replace({ query: {} })
}

function resetForm() {
  form.name = ''
  form.description = ''
  form.formula = ''
  form.assumption_ids = []
}

function startCreate() {
  resetForm()
  showCreate.value = true
}

async function handleSubmit() {
  const payload = {
    name: form.name,
    description: form.description,
    formula: form.formula,
    assumption_ids: form.assumption_ids,
  }
  const created = await dashboardStore.createArchetype(payload)
  if (created) {
    showCreate.value = false
    resetForm()
  }
}

function toggleAssumption(id) {
  const idx = form.assumption_ids.indexOf(id)
  if (idx === -1) {
    form.assumption_ids.push(id)
  } else {
    form.assumption_ids.splice(idx, 1)
  }
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
          <div>
            <h1 class="text-2xl font-bold text-gray-900">Value Formulas</h1>
            <div v-if="filterAssumptionId" class="flex items-center gap-2 mt-2">
              <span class="text-sm text-gray-500">Filtered by assumption:</span>
              <span class="text-sm font-medium text-primary-700">{{ assumptionsStore.assumptions.find(a => a.id === filterAssumptionId)?.label }}</span>
              <button @click="clearFilter" class="text-xs text-red-500 hover:text-red-700">Clear</button>
            </div>
          </div>
          <button @click="startCreate" class="flex items-center gap-2 px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition">
            <Plus class="w-4 h-4" /> New Formula
          </button>
        </div>

        <!-- Create form -->
        <div v-if="showCreate" class="bg-white rounded-xl border border-gray-200 p-6 mb-6">
          <h3 class="font-semibold text-gray-900 mb-4">Create Custom Formula</h3>
          <form @submit.prevent="handleSubmit" class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Name</label>
              <input v-model="form.name" required placeholder="e.g. Efficiency Gains" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 outline-none" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Description</label>
              <textarea v-model="form.description" rows="2" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 outline-none"></textarea>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Formula</label>
              <input v-model="form.formula" required placeholder="e.g. hours_saved * hourly_rate - cost" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 outline-none font-mono text-sm" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Assumptions</label>
              <div class="space-y-1 max-h-48 overflow-y-auto border border-gray-200 rounded-lg p-3">
                <label
                  v-for="a in assumptionsStore.assumptions"
                  :key="a.id"
                  class="flex items-center gap-2 cursor-pointer hover:bg-gray-50 p-1 rounded"
                >
                  <input
                    type="checkbox"
                    :value="a.id"
                    :checked="form.assumption_ids.includes(a.id)"
                    @change="toggleAssumption(a.id)"
                    class="rounded border-gray-300"
                  />
                  <span class="text-sm text-gray-700">{{ a.label }}</span>
                  <span class="text-xs font-mono text-gray-400">({{ a.key }})</span>
                  <span v-if="a.is_system" class="text-xs text-blue-600">System</span>
                </label>
              </div>
              <p v-if="assumptionsStore.assumptions.length === 0" class="text-xs text-amber-600 mt-1">
                No assumptions available. Create some in the Assumptions page first.
              </p>
            </div>
            <div class="flex gap-2">
              <button type="submit" class="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition">Create</button>
              <button type="button" @click="showCreate = false; resetForm()" class="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition">Cancel</button>
            </div>
          </form>
        </div>

        <!-- Formula list -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div
            v-for="archetype in filteredArchetypes"
            :key="archetype.id"
            @click="router.push(`/formulas/${archetype.id}`)"
            class="bg-white rounded-xl border border-gray-200 p-5 hover:border-primary-300 hover:shadow-sm cursor-pointer transition"
          >
            <div class="flex items-start justify-between mb-2">
              <div class="flex items-center gap-2">
                <div class="w-10 h-10 rounded-lg bg-primary-50 flex items-center justify-center">
                  <Calculator class="w-5 h-5 text-primary-600" />
                </div>
                <div>
                  <h3 class="font-semibold text-gray-900">{{ archetype.name }}</h3>
                  <span v-if="archetype.is_system" class="text-xs text-blue-600 font-medium">System</span>
                  <span v-else class="text-xs text-gray-500 font-medium">Custom</span>
                </div>
              </div>
              <Pencil class="w-4 h-4 text-gray-300" />
            </div>
            <p class="text-sm text-gray-500 mb-2">{{ archetype.description }}</p>
            <p class="text-xs font-mono text-gray-600 bg-gray-50 px-3 py-2 rounded">{{ archetype.formula }}</p>
            <div v-if="archetype.assumptions?.length" class="mt-3">
              <p class="text-xs font-medium text-gray-700 mb-1">Assumptions:</p>
              <div class="flex flex-wrap gap-1">
                <span
                  v-for="a in archetype.assumptions"
                  :key="a.id"
                  class="text-xs px-2 py-1 bg-gray-100 rounded text-gray-600"
                >
                  {{ a.label }} ({{ a.key }})
                </span>
              </div>
            </div>
            <div v-if="getArchetypeUsage(archetype.id).project_count > 0" class="mt-3">
              <span class="flex items-center gap-1 text-xs px-2 py-1 rounded-lg bg-primary-50 text-primary-700">
                <Link2 class="w-3 h-3" /> {{ getArchetypeUsage(archetype.id).project_count }} project{{ getArchetypeUsage(archetype.id).project_count > 1 ? 's' : '' }}
              </span>
            </div>
          </div>
        </div>
        <div v-if="filteredArchetypes.length === 0" class="text-center py-12 text-gray-500">
          No formulas available.
        </div>
      </div>
    </main>
  </div>
</template>
