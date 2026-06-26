<script setup>
import { ref, onMounted, reactive, computed, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { useProjectsStore } from '../stores/projects'
import { useDashboardStore } from '../stores/dashboard'
import apiClient from '../api/client'
import { Plus, Upload, Download, Search, TrendingUp, LayoutDashboard, FolderKanban, Calculator, Lightbulb, Users, Menu, X, Calendar, LayoutGrid, Table, Link2, LogOut } from 'lucide-vue-next'
import ProjectCard from '../components/ProjectCard.vue'
import CsvImport from '../components/CsvImport.vue'

const router = useRouter()
const route = useRoute()
const auth = useAuthStore()
const projectsStore = useProjectsStore()
const dashboardStore = useDashboardStore()

const showCreate = ref(false)
const showImport = ref(false)
const searchQuery = ref('')
const teams = ref([])
const selectedTeamId = ref('managed')
function logout() {
  auth.logout()
  router.push('/login')
}

const sidebarOpen = ref(false)
const filterFormulaId = ref(null)
const isPaid = computed(() => auth.userTier === 'paid')
const viewMode = computed({
  get: () => projectsStore.viewMode,
  set: (v) => { projectsStore.viewMode = v },
})

const form = reactive({ name: '', description: '', status: 'planning', start_date: '', end_date: '' })
const dateFilter = reactive({ start: '', end: '' })

onMounted(async () => {
  try {
    const resp = await apiClient.get('/projects/teams')
    teams.value = resp.data
  } catch {
    
  }
  if (route.query.formula) {
    filterFormulaId.value = parseInt(route.query.formula)
    await dashboardStore.fetchArchetypes()
  }
  await fetchProjects()
})

const filteredProjects = computed(() => {
  let list = projectsStore.projects
  if (searchQuery.value) {
    list = list.filter(p => p.name.toLowerCase().includes(searchQuery.value.toLowerCase()))
  }
  if (filterFormulaId.value && dashboardStore.archetypes.length) {
    const formulaArch = dashboardStore.archetypes.find(a => a.id === filterFormulaId.value)
    if (formulaArch) {
      // Can't filter by formula on client side without project_archetypes data
      // Show all projects but display a filter banner
    }
  }
  return list
})

function clearFormulaFilter() {
  filterFormulaId.value = null
  router.replace({ query: {} })
}

const filterFormulaName = computed(() => {
  if (!filterFormulaId.value) return null
  return dashboardStore.archetypes.find(a => a.id === filterFormulaId.value)?.name || null
})

async function fetchProjects() {
  const dateRange = (dateFilter.start || dateFilter.end)
    ? { start: dateFilter.start || null, end: dateFilter.end || null }
    : null
  const teamId = (selectedTeamId.value === 'managed' || selectedTeamId.value === 'all') ? null : selectedTeamId.value
  const managedOnly = selectedTeamId.value === 'managed'
  await projectsStore.fetchProjects(teamId, dateRange, projectsStore.viewMode === 'table', managedOnly)
}

watch(selectedTeamId, async () => {
  await fetchProjects()
})

function clearDateFilter() {
  dateFilter.start = ''
  dateFilter.end = ''
  fetchProjects()
}

async function handleCreate() {
  const teamId = (selectedTeamId.value === 'managed' || selectedTeamId.value === 'all')
    ? teams.value[0]?.id
    : selectedTeamId.value
  const project = await projectsStore.createProject({
    ...form,
    team_id: teamId,
    start_date: form.start_date || null,
    end_date: form.end_date || null,
  })
  if (project) {
    showCreate.value = false
    form.name = ''
    form.description = ''
    form.status = 'planning'
    form.start_date = ''
    form.end_date = ''
  }
}

async function handleExport() {
  const teamId = (selectedTeamId.value === 'managed' || selectedTeamId.value === 'all')
    ? teams.value[0]?.id
    : selectedTeamId.value
  if (!teamId) return
  try {
    const resp = await apiClient.get(`/projects/export?team_id=${teamId}`, { responseType: 'blob' })
    const url = window.URL.createObjectURL(new Blob([resp.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', `projects_team_${teamId}.csv`)
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)
  } catch {
    
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

      <div class="p-6 max-w-7xl mx-auto">
        <div class="flex items-center justify-between mb-6">
          <h1 class="text-2xl font-bold text-gray-900">Projects</h1>
          <div class="flex gap-2">
            <button @click="showImport = !showImport" class="flex items-center gap-2 px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition">
              <Upload class="w-4 h-4" /> Import CSV
            </button>
            <button @click="handleExport" class="flex items-center gap-2 px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition">
              <Download class="w-4 h-4" /> Export CSV
            </button>
            <button @click="showCreate = !showCreate" class="flex items-center gap-2 px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition">
              <Plus class="w-4 h-4" /> New Project
            </button>
          </div>
        </div>

        <!-- Search + Date filter -->
        <div class="flex flex-col sm:flex-row gap-3 mb-4">
          <div class="relative flex-1">
            <Search class="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
            <input
              v-model="searchQuery"
              placeholder="Search projects..."
              class="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 outline-none"
            />
          </div>
          <div class="flex items-center gap-2">
            <Calendar class="w-5 h-5 text-gray-400 flex-shrink-0" />
            <input
              v-model="dateFilter.start"
              type="date"
              @change="fetchProjects"
              class="px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-primary-500 outline-none"
              placeholder="Start date"
            />
            <span class="text-gray-400">to</span>
            <input
              v-model="dateFilter.end"
              type="date"
              @change="fetchProjects"
              class="px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-primary-500 outline-none"
              placeholder="End date"
            />
            <button v-if="dateFilter.start || dateFilter.end" @click="clearDateFilter" class="text-sm text-gray-500 hover:text-gray-700 px-2">
              Clear
            </button>
          </div>
        </div>

        <!-- CSV Import -->
        <CsvImport v-if="showImport" :teamId="(selectedTeamId === 'managed' || selectedTeamId === 'all') ? teams[0]?.id : selectedTeamId" @close="showImport = false" />

        <!-- Create form -->
        <div v-if="showCreate" class="bg-white rounded-xl border border-gray-200 p-6 mb-6">
          <h3 class="font-semibold text-gray-900 mb-4">Create New Project</h3>
          <form @submit.prevent="handleCreate" class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Name</label>
              <input v-model="form.name" required placeholder="Project name" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 outline-none" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Description</label>
              <textarea v-model="form.description" rows="3" placeholder="Project description" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 outline-none"></textarea>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Status</label>
              <select v-model="form.status" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 outline-none">
                <option value="planning">Planning</option>
                <option value="in_progress">In Progress</option>
                <option value="completed">Completed</option>
                <option value="cancelled">Cancelled</option>
              </select>
            </div>
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Start Date</label>
                <input v-model="form.start_date" type="date" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 outline-none" />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">End Date</label>
                <input v-model="form.end_date" type="date" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 outline-none" />
              </div>
            </div>
            <div class="flex gap-2">
              <button type="submit" class="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition">Create</button>
              <button type="button" @click="showCreate = false" class="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition">Cancel</button>
            </div>
          </form>
        </div>

        <!-- Formula filter banner -->
        <div v-if="filterFormulaName" class="flex items-center gap-2 mb-4 p-3 bg-primary-50 rounded-lg">
          <Link2 class="w-4 h-4 text-primary-600" />
          <span class="text-sm text-gray-600">Filtered by formula:</span>
          <span class="text-sm font-medium text-primary-700">{{ filterFormulaName }}</span>
          <button @click="clearFormulaFilter" class="text-xs text-red-500 hover:text-red-700 ml-auto">Clear filter</button>
        </div>

        <!-- Filters row -->
        <div class="flex flex-wrap items-center gap-3 mb-4">
          <select
            v-if="teams.length > 0"
            v-model="selectedTeamId"
            class="px-4 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-primary-500 outline-none"
          >
            <option value="managed">All Teams I Manage</option>
            <option v-if="isPaid" value="all">All Teams</option>
            <option v-for="team in teams" :key="team.id" :value="team.id">{{ team.name }}</option>
          </select>

          <!-- View toggle -->
          <div class="flex items-center gap-2 ml-auto">
          <button
            @click="viewMode = 'cards'; fetchProjects()"
            :class="[
              'flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-sm transition',
              viewMode === 'cards' ? 'bg-primary-600 text-white' : 'border border-gray-300 text-gray-700 hover:bg-gray-50'
            ]"
          >
            <LayoutGrid class="w-4 h-4" /> Cards
          </button>
          <button
            @click="viewMode = 'table'; fetchProjects()"
            :class="[
              'flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-sm transition',
              viewMode === 'table' ? 'bg-primary-600 text-white' : 'border border-gray-300 text-gray-700 hover:bg-gray-50'
            ]"
          >
            <Table class="w-4 h-4" /> Table
          </button>
          </div>
        </div>

        <!-- Card view -->
        <div v-if="viewMode === 'cards'" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <ProjectCard
            v-for="project in filteredProjects"
            :key="project.id"
            :project="project"
            @click="router.push(`/projects/${project.id}`)"
          />
        </div>

        <!-- Table view -->
        <div v-if="viewMode === 'table'" class="bg-white rounded-xl border border-gray-200 overflow-hidden">
          <table class="w-full">
            <thead>
              <tr class="border-b border-gray-200 bg-gray-50">
                <th class="text-left px-4 py-3 text-sm font-semibold text-gray-700">Title</th>
                <th class="text-left px-4 py-3 text-sm font-semibold text-gray-700">Status</th>
                <th class="text-right px-4 py-3 text-sm font-semibold text-gray-700">1-Year ROI</th>
                <th class="text-right px-4 py-3 text-sm font-semibold text-gray-700">3-Year ROI</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="project in filteredProjects"
                :key="project.id"
                @click="router.push(`/projects/${project.id}`)"
                class="border-b border-gray-100 hover:bg-gray-50 cursor-pointer transition"
              >
                <td class="px-4 py-3 text-sm font-medium text-gray-900">{{ project.name }}</td>
                <td class="px-4 py-3 text-sm text-gray-600 capitalize">{{ project.status }}</td>
                <td class="px-4 py-3 text-sm text-right font-semibold" :class="project.roi_1yr != null && project.roi_1yr > 0 ? 'text-primary-600' : 'text-gray-400'">
                  {{ project.roi_1yr != null ? '$' + project.roi_1yr.toLocaleString(undefined, { maximumFractionDigits: 0 }) : '—' }}
                </td>
                <td class="px-4 py-3 text-sm text-right font-semibold" :class="project.roi_3yr != null && project.roi_3yr > 0 ? 'text-primary-600' : 'text-gray-400'">
                  {{ project.roi_3yr != null ? '$' + project.roi_3yr.toLocaleString(undefined, { maximumFractionDigits: 0 }) : '—' }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <div v-if="filteredProjects.length === 0" class="text-center py-12 text-gray-500">
          No projects found.
        </div>
      </div>
    </main>
  </div>
</template>
