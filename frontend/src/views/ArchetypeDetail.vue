<script setup>
import { ref, onMounted, reactive, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useDashboardStore } from '../stores/dashboard'
import { useAssumptionsStore } from '../stores/assumptions'
import { useAuthStore } from '../stores/auth'
import { Plus, Trash2, Pencil, Calculator, TrendingUp, LayoutDashboard, FolderKanban, Lightbulb, Users, Menu, X, ArrowLeft, Link2, LogOut } from 'lucide-vue-next'
import AuditHistory from '../components/AuditHistory.vue'

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
const isEditing = ref(false)
const archetype = ref(null)
const loading = ref(true)

const form = reactive({
  name: '',
  description: '',
  formula: '',
  assumption_ids: [],
  change_reason: '',
})

const archetypeId = computed(() => parseInt(route.params.id))

onMounted(async () => {
  await dashboardStore.fetchArchetypes()
  await assumptionsStore.fetchAssumptions()
  await dashboardStore.fetchUsage()
  loadArchetype()
})

function loadArchetype() {
  archetype.value = dashboardStore.archetypes.find(a => a.id === archetypeId.value)
  loading.value = false
  if (archetype.value) {
    form.name = archetype.value.name
    form.description = archetype.value.description || ''
    form.formula = archetype.value.formula || ''
    form.assumption_ids = (archetype.value.assumptions || []).map(a => a.id)
    form.change_reason = ''
  }
}

function startEdit() {
  isEditing.value = true
}

function cancelEdit() {
  isEditing.value = false
  loadArchetype()
}

async function handleSave() {
  const payload = {
    name: form.name,
    description: form.description,
    formula: form.formula,
    assumption_ids: form.assumption_ids,
  }
  if (form.change_reason.trim()) {
    payload.change_reason = form.change_reason.trim()
  }
  const updated = await dashboardStore.updateArchetype(archetypeId.value, payload)
  if (updated) {
    archetype.value = updated
    isEditing.value = false
  }
}

async function handleDelete() {
  if (confirm('Delete this formula?')) {
    await dashboardStore.deleteArchetype(archetypeId.value)
    router.push('/formulas')
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

function getArchetypeUsage(id) {
  return dashboardStore.usageStats.archetypes[id] || { project_count: 0 }
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
        <button @click="router.push('/formulas')" class="flex items-center gap-1 text-sm text-gray-500 hover:text-gray-700 mb-4 transition">
          <ArrowLeft class="w-4 h-4" /> Back to Value Formulas
        </button>

        <div v-if="loading" class="text-center py-12 text-gray-500">
          Loading...
        </div>

        <div v-else-if="!archetype" class="text-center py-12 text-gray-500">
          Formula not found.
        </div>

        <div v-else>
          <!-- Header -->
          <div class="flex items-center justify-between mb-6">
            <div class="flex items-center gap-3">
              <div class="w-10 h-10 rounded-lg bg-primary-50 flex items-center justify-center">
                <Calculator class="w-5 h-5 text-primary-600" />
              </div>
              <div>
                <h1 class="text-2xl font-bold text-gray-900">{{ archetype.name }}</h1>
                <span v-if="archetype.is_system" class="text-xs text-blue-600 font-medium">System</span>
                <span v-else class="text-xs text-gray-500 font-medium">Custom</span>
              </div>
            </div>
            <div v-if="!isEditing && !archetype.is_system" class="flex gap-2">
              <button @click="startEdit" data-testid="edit-archetype" class="flex items-center gap-1 px-3 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition">
                <Pencil class="w-4 h-4" /> Edit
              </button>
              <button @click="handleDelete" data-testid="delete-archetype" class="flex items-center gap-1 px-3 py-2 border border-red-300 text-red-600 rounded-lg hover:bg-red-50 transition">
                <Trash2 class="w-4 h-4" /> Delete
              </button>
            </div>
          </div>

          <!-- Read view -->
          <div v-if="!isEditing" class="space-y-4">
            <div class="bg-white rounded-xl border border-gray-200 p-6">
              <dl class="space-y-3">
                <div>
                  <dt class="text-sm font-medium text-gray-500">Description</dt>
                  <dd class="text-sm text-gray-900 mt-1">{{ archetype.description || '—' }}</dd>
                </div>
                <div>
                  <dt class="text-sm font-medium text-gray-500">Formula</dt>
                  <dd class="text-sm font-mono text-gray-900 bg-gray-50 px-3 py-2 rounded mt-1">{{ archetype.formula }}</dd>
                </div>
              </dl>
            </div>

            <!-- Assumptions -->
            <div v-if="archetype.assumptions?.length" class="bg-white rounded-xl border border-gray-200 p-6">
              <h3 class="text-sm font-medium text-gray-700 mb-2">Assumptions</h3>
              <div class="flex flex-wrap gap-1">
                <button
                  v-for="a in archetype.assumptions"
                  :key="a.id"
                  @click="router.push(`/assumptions/${a.id}`)"
                  class="text-xs px-2 py-1 bg-gray-100 rounded text-gray-600 hover:bg-gray-200 transition"
                >
                  {{ a.label }} ({{ a.key }})
                </button>
              </div>
            </div>

            <!-- Project usage -->
            <div v-if="getArchetypeUsage(archetype.id).project_count > 0">
              <button
                @click="router.push('/projects?formula=' + archetype.id)"
                class="flex items-center gap-1 text-xs px-3 py-2 rounded-lg bg-primary-50 text-primary-700 hover:bg-primary-100 transition"
              >
                <Link2 class="w-3 h-3" /> {{ getArchetypeUsage(archetype.id).project_count }} project{{ getArchetypeUsage(archetype.id).project_count > 1 ? 's' : '' }}
              </button>
            </div>

            <!-- Audit History -->
            <AuditHistory entity-type="archetype" :entity-id="archetype.id" />
          </div>

          <!-- Edit view -->
          <div v-else class="bg-white rounded-xl border border-primary-200 p-6">
            <form @submit.prevent="handleSave" class="space-y-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Name</label>
                <input v-model="form.name" required class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 outline-none" />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Description</label>
                <textarea v-model="form.description" rows="2" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 outline-none"></textarea>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Formula</label>
                <input v-model="form.formula" required class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 outline-none font-mono text-sm" />
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
