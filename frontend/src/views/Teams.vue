<script setup>
import { ref, onMounted, reactive, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useTeamsStore } from '../stores/teams'
import { useAuthStore } from '../stores/auth'
import { Plus, Trash2, Pencil, TrendingUp, LayoutDashboard, FolderKanban, Calculator, Lightbulb, Users, Menu, X, LogOut } from 'lucide-vue-next'
import JiraIntegration from '../components/JiraIntegration.vue'

const router = useRouter()
const auth = useAuthStore()
const teamsStore = useTeamsStore()

function logout() {
  auth.logout()
  router.push('/login')
}

const sidebarOpen = ref(false)
const showCreate = ref(false)
const editingId = ref(null)
const form = reactive({ name: '', avg_labor_cost_per_week: null })

const isPaid = computed(() => auth.userTier === 'paid')

onMounted(async () => {
  await teamsStore.fetchTeams()
})

function resetForm() {
  form.name = ''
  form.avg_labor_cost_per_week = null
  editingId.value = null
}

function startCreate() {
  resetForm()
  showCreate.value = true
}

function startEdit(team) {
  editingId.value = team.id
  form.name = team.name
  form.avg_labor_cost_per_week = team.avg_labor_cost_per_week || null
  showCreate.value = true
}

async function handleSubmit() {
  const payload = { name: form.name }
  if (form.avg_labor_cost_per_week !== null) {
    payload.avg_labor_cost_per_week = form.avg_labor_cost_per_week
  }
  if (editingId.value) {
    await teamsStore.updateTeam(editingId.value, payload)
  } else {
    await teamsStore.createTeam(payload)
  }
  showCreate.value = false
  resetForm()
}

async function handleDelete(id) {
  if (confirm('Delete this team? All projects in this team will also be deleted.')) {
    await teamsStore.deleteTeam(id)
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
          <h1 class="text-2xl font-bold text-gray-900">Teams</h1>
          <button @click="startCreate" class="flex items-center gap-2 px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition">
            <Plus class="w-4 h-4" /> New Team
          </button>
        </div>

        <!-- Create/Edit form -->
        <div v-if="showCreate" class="bg-white rounded-xl border border-gray-200 p-6 mb-6">
          <h3 class="font-semibold text-gray-900 mb-4">{{ editingId ? 'Edit Team' : 'Create Team' }}</h3>
          <form @submit.prevent="handleSubmit" class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Team Name</label>
              <input v-model="form.name" required placeholder="e.g. Engineering Team" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 outline-none" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Avg Labor Cost / Person-Week ($)</label>
              <input v-model.number="form.avg_labor_cost_per_week" type="number" step="any" placeholder="e.g. 3500 (optional)" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 outline-none" />
              <p class="text-xs text-gray-400 mt-1">Used to auto-compute development costs. Falls back to org default if unset.</p>
            </div>
            <div class="flex gap-2">
              <button type="submit" class="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition">{{ editingId ? 'Update' : 'Create' }}</button>
              <button type="button" @click="showCreate = false; resetForm()" class="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition">Cancel</button>
            </div>
          </form>
        </div>

        <!-- Teams list -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div v-for="team in teamsStore.teams" :key="team.id" class="bg-white rounded-xl border border-gray-200 p-5">
            <div class="flex items-start justify-between mb-2">
              <div class="flex items-center gap-2">
                <div class="w-10 h-10 rounded-lg bg-primary-50 flex items-center justify-center">
                  <Users class="w-5 h-5 text-primary-600" />
                </div>
                <div>
                  <h3 class="font-semibold text-gray-900">{{ team.name }}</h3>
                  <span v-if="team.manager_user_id === auth.user?.id" class="text-xs text-primary-600 font-medium">Manager</span>
                  <span v-else class="text-xs text-gray-500 font-medium">Managed by {{ team.manager_name || 'Unknown' }}</span>
                </div>
              </div>
              <div v-if="team.manager_user_id === auth.user?.id" class="flex gap-2">
                <button @click="startEdit(team)" data-testid="edit-team" class="text-gray-400 hover:text-primary-600 transition">
                  <Pencil class="w-4 h-4" />
                </button>
                <button @click="handleDelete(team.id)" data-testid="delete-team" class="text-red-400 hover:text-red-600 transition">
                  <Trash2 class="w-4 h-4" />
                </button>
              </div>
            </div>
            <p class="text-xs text-gray-400 mt-2">Created {{ team.created_at ? new Date(team.created_at).toLocaleDateString() : '' }}</p>
            <p v-if="team.avg_labor_cost_per_week" class="text-xs text-gray-500 mt-1">
              Labor rate: ${{ team.avg_labor_cost_per_week.toLocaleString() }}/person-week
            </p>
            <JiraIntegration v-if="team.manager_user_id === auth.user?.id" :teamId="team.id" />
          </div>
        </div>

        <div v-if="teamsStore.teams.length === 0" class="text-center py-12 text-gray-500">
          No teams found.
        </div>
      </div>
    </main>
  </div>
</template>
