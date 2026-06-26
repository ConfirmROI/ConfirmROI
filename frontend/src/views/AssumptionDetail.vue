<script setup>
import { ref, onMounted, reactive, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAssumptionsStore } from '../stores/assumptions'
import { useDashboardStore } from '../stores/dashboard'
import { useAuthStore } from '../stores/auth'
import { TrendingUp, LayoutDashboard, FolderKanban, Calculator, Lightbulb, Users, Menu, X, Pencil, ArrowLeft, Trash2, Link2, LogOut } from 'lucide-vue-next'
import AuditHistory from '../components/AuditHistory.vue'

const router = useRouter()
const route = useRoute()
const auth = useAuthStore()
const assumptionsStore = useAssumptionsStore()
const dashboardStore = useDashboardStore()

function logout() {
  auth.logout()
  router.push('/login')
}

const sidebarOpen = ref(false)
const isEditing = ref(false)
const assumption = ref(null)
const loading = ref(true)

const form = reactive({
  key: '',
  label: '',
  data_type: 'number',
  default_value: 0,
  description: '',
  change_reason: '',
})

const assumptionId = computed(() => parseInt(route.params.id))

onMounted(async () => {
  await assumptionsStore.fetchAssumptions()
  await dashboardStore.fetchUsage()
  loadAssumption()
})

function loadAssumption() {
  assumption.value = assumptionsStore.assumptions.find(a => a.id === assumptionId.value)
  loading.value = false
  if (assumption.value) {
    form.key = assumption.value.key
    form.label = assumption.value.label
    form.data_type = assumption.value.data_type
    form.default_value = assumption.value.default_value
    form.description = assumption.value.description || ''
    form.change_reason = ''
  }
}

function startEdit() {
  isEditing.value = true
}

function cancelEdit() {
  isEditing.value = false
  loadAssumption()
}

async function handleSave() {
  const data = {
    key: form.key,
    label: form.label,
    data_type: form.data_type,
    default_value: Number(form.default_value),
    description: form.description,
  }
  if (form.change_reason.trim()) {
    data.change_reason = form.change_reason.trim()
  }
  const updated = await assumptionsStore.updateAssumption(assumptionId.value, data)
  if (updated) {
    assumption.value = updated
    isEditing.value = false
  }
}

async function handleDelete() {
  if (confirm('Delete this assumption?')) {
    await assumptionsStore.deleteAssumption(assumptionId.value)
    router.push('/assumptions')
  }
}

function getUsage(id) {
  return dashboardStore.usageStats.assumptions[id] || { formula_count: 0, project_count: 0 }
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

      <div class="p-6 max-w-3xl mx-auto">
        <!-- Back link -->
        <button @click="router.push('/assumptions')" class="flex items-center gap-1 text-sm text-gray-500 hover:text-gray-700 mb-4 transition">
          <ArrowLeft class="w-4 h-4" /> Back to Assumptions
        </button>

        <div v-if="loading" class="text-center py-12 text-gray-500">
          Loading...
        </div>

        <div v-else-if="!assumption" class="text-center py-12 text-gray-500">
          Assumption not found.
        </div>

        <div v-else>
          <!-- Header -->
          <div class="flex items-center justify-between mb-6">
            <div>
              <h1 class="text-2xl font-bold text-gray-900">{{ assumption.label }}</h1>
              <div class="flex items-center gap-2 mt-1">
                <span class="text-xs font-mono text-gray-500">({{ assumption.key }})</span>
                <span class="text-xs px-2 py-0.5 rounded bg-gray-200 text-gray-600">{{ assumption.data_type }}</span>
                <span v-if="assumption.is_system" class="text-xs text-blue-600 font-medium">System</span>
              </div>
            </div>
            <div v-if="!isEditing" class="flex gap-2">
              <button @click="startEdit" data-testid="edit-assumption" class="flex items-center gap-1 px-3 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition">
                <Pencil class="w-4 h-4" /> Edit
              </button>
              <button v-if="!assumption.is_system" @click="handleDelete" data-testid="delete-assumption" class="flex items-center gap-1 px-3 py-2 border border-red-300 text-red-600 rounded-lg hover:bg-red-50 transition">
                <Trash2 class="w-4 h-4" /> Delete
              </button>
            </div>
          </div>

          <!-- Read view -->
          <div v-if="!isEditing" class="space-y-4">
            <div class="bg-white rounded-xl border border-gray-200 p-6">
              <dl class="space-y-3">
                <div>
                  <dt class="text-sm font-medium text-gray-500">Key</dt>
                  <dd class="text-sm text-gray-900 font-mono mt-1">{{ assumption.key }}</dd>
                </div>
                <div>
                  <dt class="text-sm font-medium text-gray-500">Label</dt>
                  <dd class="text-sm text-gray-900 mt-1">{{ assumption.label }}</dd>
                </div>
                <div>
                  <dt class="text-sm font-medium text-gray-500">Data Type</dt>
                  <dd class="text-sm text-gray-900 mt-1">{{ assumption.data_type }}</dd>
                </div>
                <div>
                  <dt class="text-sm font-medium text-gray-500">Default Value</dt>
                  <dd class="text-sm text-gray-900 mt-1">{{ assumption.default_value }}</dd>
                </div>
                <div v-if="assumption.description">
                  <dt class="text-sm font-medium text-gray-500">Description</dt>
                  <dd class="text-sm text-gray-900 mt-1">{{ assumption.description }}</dd>
                </div>
              </dl>
            </div>

            <!-- Usage links -->
            <div v-if="getUsage(assumption.id).formula_count > 0 || getUsage(assumption.id).project_count > 0" class="flex items-center gap-2">
              <button
                v-if="getUsage(assumption.id).formula_count > 0"
                @click="router.push('/formulas?assumption=' + assumption.id)"
                class="flex items-center gap-1 text-xs px-3 py-2 rounded-lg bg-primary-50 text-primary-700 hover:bg-primary-100 transition"
              >
                <Link2 class="w-3 h-3" /> {{ getUsage(assumption.id).formula_count }} formula{{ getUsage(assumption.id).formula_count > 1 ? 's' : '' }}
              </button>
              <button
                v-if="getUsage(assumption.id).project_count > 0"
                @click="router.push('/projects?assumption=' + assumption.id)"
                class="flex items-center gap-1 text-xs px-3 py-2 rounded-lg bg-primary-50 text-primary-700 hover:bg-primary-100 transition"
              >
                <Link2 class="w-3 h-3" /> {{ getUsage(assumption.id).project_count }} project{{ getUsage(assumption.id).project_count > 1 ? 's' : '' }}
              </button>
            </div>

            <!-- Audit History -->
            <AuditHistory entity-type="assumption" :entity-id="assumption.id" />
          </div>

          <!-- Edit view -->
          <div v-else class="bg-white rounded-xl border border-primary-200 p-6">
            <form @submit.prevent="handleSave" class="space-y-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Key</label>
                <input v-model="form.key" required class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 outline-none font-mono text-sm" />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Label</label>
                <input v-model="form.label" required class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 outline-none" />
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
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Reason for change <span class="text-gray-400 font-normal">(optional)</span></label>
                <textarea v-model="form.change_reason" rows="2" placeholder="Why are you making this change?" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 outline-none"></textarea>
              </div>
              <div class="flex gap-2">
                <button type="submit" class="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition">Save</button>
                <button type="button" @click="cancelEdit" class="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition">Cancel</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>
