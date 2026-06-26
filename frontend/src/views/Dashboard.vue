<script setup>
import { ref, onMounted, computed, watch, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { useProjectsStore } from '../stores/projects'
import { useDashboardStore } from '../stores/dashboard'
import { useTeamsStore } from '../stores/teams'
import { TrendingUp, LayoutDashboard, FolderKanban, Calculator, Lightbulb, Users, Menu, X, Calendar, LogOut } from 'lucide-vue-next'
import RoiChart from '../components/RoiChart.vue'
import ProjectCard from '../components/ProjectCard.vue'

const router = useRouter()
const auth = useAuthStore()
const projectsStore = useProjectsStore()
const dashboardStore = useDashboardStore()
const teamsStore = useTeamsStore()

function logout() {
  auth.logout()
  router.push('/login')
}

const sidebarOpen = ref(false)
const selectedTeamId = ref(null)
const dateFilter = reactive({ start: '', end: '' })

const isPaid = computed(() => auth.userTier === 'paid')

const totalRoi = computed(() => {
  return Object.values(dashboardStore.projectRoi).reduce((sum, v) => sum + (v || 0), 0)
})

async function loadDashboard() {
  const dateRange = (dateFilter.start || dateFilter.end)
    ? { start: dateFilter.start || null, end: dateFilter.end || null }
    : null
  await projectsStore.fetchProjects(selectedTeamId.value, dateRange)
  await dashboardStore.fetchArchetypes()
  await dashboardStore.fetchProjectRoi(projectsStore.projects)
}

onMounted(async () => {
  await teamsStore.fetchTeams()
  const myTeams = teamsStore.teams.filter(t => t.manager_user_id === auth.user?.id)
  if (myTeams.length > 0) {
    selectedTeamId.value = myTeams[0].id
  } else {
    await loadDashboard()
  }
})

watch(selectedTeamId, async () => {
  await loadDashboard()
})

watch(() => [dateFilter.start, dateFilter.end], async () => {
  await loadDashboard()
})

function clearDateFilter() {
  dateFilter.start = ''
  dateFilter.end = ''
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
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
          <h1 class="text-2xl font-bold text-gray-900">Dashboard</h1>
          <div class="flex flex-wrap items-center gap-3">
            <div class="flex items-center gap-2">
              <Calendar class="w-5 h-5 text-gray-400 flex-shrink-0" />
              <input
                v-model="dateFilter.start"
                type="date"
                class="px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-primary-500 outline-none"
              />
              <span class="text-gray-400">to</span>
              <input
                v-model="dateFilter.end"
                type="date"
                class="px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-primary-500 outline-none"
              />
              <button v-if="dateFilter.start || dateFilter.end" @click="clearDateFilter" class="text-sm text-gray-500 hover:text-gray-700 px-2">
                Clear
              </button>
            </div>
            <select
              v-if="teamsStore.teams.length > 1"
              v-model="selectedTeamId"
              class="px-4 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-primary-500 outline-none"
            >
              <option :value="null">Org-wide (All Teams)</option>
              <option v-for="team in teamsStore.teams" :key="team.id" :value="team.id">{{ team.name }}</option>
            </select>
          </div>
        </div>

        <!-- Summary cards -->
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-8">
          <div class="bg-white rounded-xl border border-gray-200 p-5">
            <p class="text-sm text-gray-500 mb-1">Total Projects</p>
            <p class="text-2xl font-bold text-gray-900">{{ projectsStore.projectCount }}</p>
          </div>
          <div class="bg-white rounded-xl border border-gray-200 p-5">
            <p class="text-sm text-gray-500 mb-1">Total ROI</p>
            <p class="text-2xl font-bold text-primary-600">${{ totalRoi.toLocaleString() }}</p>
          </div>
          <div class="bg-white rounded-xl border border-gray-200 p-5">
            <p class="text-sm text-gray-500 mb-1">Archetypes</p>
            <p class="text-2xl font-bold text-gray-900">{{ dashboardStore.archetypes.length }}</p>
          </div>
        </div>

        <!-- ROI Chart -->
        <div class="bg-white rounded-xl border border-gray-200 p-6 mb-8">
          <h2 class="text-lg font-semibold text-gray-900 mb-4">ROI by Project — Value Formula Breakdown</h2>
          <RoiChart
            :projects="projectsStore.projects"
            :roiResults="dashboardStore.projectRoi"
            :breakdown="dashboardStore.projectRoiBreakdown"
          />
        </div>

        <!-- Project list -->
        <div>
          <div class="flex items-center justify-between mb-4">
            <h2 class="text-lg font-semibold text-gray-900">Recent Projects</h2>
            <router-link to="/projects" class="text-sm text-primary-600 hover:text-primary-700 font-medium">View all →</router-link>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            <ProjectCard
              v-for="project in projectsStore.projects.slice(0, 6)"
              :key="project.id"
              :project="project"
              :roi="dashboardStore.projectRoi[project.id]"
            />
          </div>
          <div v-if="projectsStore.projects.length === 0" class="text-center py-12 text-gray-500">
            No projects yet. Create your first project to get started.
          </div>
        </div>
      </div>
    </main>
  </div>
</template>
