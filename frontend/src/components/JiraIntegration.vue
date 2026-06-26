<script setup>
import { ref, onMounted } from 'vue'
import apiClient from '../api/client'
import { Plus, Trash2, Download, RefreshCw, AlertCircle, CheckCircle, X } from 'lucide-vue-next'

const props = defineProps({
  teamId: { type: Number, default: null },
})

const connection = ref(null)
const showForm = ref(false)
const form = ref({ base_url: '', api_token: '', email: '' })
const error = ref('')
const success = ref('')
const importResult = ref(null)
const loading = ref(false)

onMounted(async () => {
  await fetchConnection()
})

async function fetchConnection() {
  if (!props.teamId) return
  try {
    const resp = await apiClient.get(`/teams/${props.teamId}/jira`)
    connection.value = resp.data
  } catch {
    connection.value = null
  }
}

async function createConnection() {
  error.value = ''
  success.value = ''
  if (!form.value.base_url || !form.value.api_token || !form.value.email) {
    error.value = 'All fields are required'
    return
  }
  loading.value = true
  try {
    await apiClient.post(`/teams/${props.teamId}/jira`, form.value)
    await fetchConnection()
    showForm.value = false
    form.value = { base_url: '', api_token: '', email: '' }
    success.value = 'Jira connection created successfully'
  } catch (err) {
    error.value = err.response?.data?.error || 'Failed to create connection'
  } finally {
    loading.value = false
  }
}

async function deleteConnection() {
  if (!confirm('Remove Jira connection?')) return
  error.value = ''
  try {
    await apiClient.delete(`/teams/${props.teamId}/jira`)
    connection.value = null
    success.value = 'Jira connection removed'
  } catch (err) {
    error.value = err.response?.data?.error || 'Failed to remove connection'
  }
}

async function importProjects() {
  if (!confirm('Import all projects from Jira?')) return
  error.value = ''
  success.value = ''
  importResult.value = null
  loading.value = true
  try {
    const resp = await apiClient.post(`/teams/${props.teamId}/jira/import`)
    importResult.value = resp.data
    if (importResult.value.imported > 0) {
      success.value = `Imported ${importResult.value.imported} project(s) from Jira`
    } else if (importResult.value.errors.length === 0) {
      success.value = 'No new projects to import (all already exist)'
    }
  } catch (err) {
    error.value = err.response?.data?.error || 'Failed to import from Jira'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="bg-white rounded-xl border border-gray-200 p-6 mb-6">
    <div class="flex items-center justify-between mb-4">
      <h3 class="font-semibold text-gray-900 flex items-center gap-2">
        <RefreshCw class="w-5 h-5 text-primary-600" /> Jira Integration
      </h3>
      <button v-if="!connection && !showForm" @click="showForm = true" class="flex items-center gap-2 px-3 py-1.5 bg-primary-600 text-white rounded-lg text-sm hover:bg-primary-700 transition">
        <Plus class="w-4 h-4" /> Connect
      </button>
      <button v-if="connection" @click="deleteConnection" class="flex items-center gap-2 px-3 py-1.5 border border-red-300 text-red-600 rounded-lg text-sm hover:bg-red-50 transition">
        <Trash2 class="w-4 h-4" /> Disconnect
      </button>
    </div>

    <div v-if="error" class="flex items-center gap-2 text-red-600 text-sm mb-3">
      <AlertCircle class="w-4 h-4" /> {{ error }}
    </div>
    <div v-if="success" class="flex items-center gap-2 text-green-600 text-sm mb-3">
      <CheckCircle class="w-4 h-4" /> {{ success }}
    </div>
    <div v-if="importResult?.errors?.length" class="text-red-500 text-sm mb-3">
      <p v-for="(e, i) in importResult.errors" :key="i">{{ e }}</p>
    </div>

    <!-- Connection status -->
    <div v-if="connection" class="space-y-3">
      <div class="flex items-center gap-2 text-sm text-gray-600">
        <CheckCircle class="w-4 h-4 text-green-500" />
        Connected to <span class="font-medium text-gray-900">{{ connection.base_url }}</span>
      </div>
      <button @click="importProjects" :disabled="loading" class="flex items-center gap-2 px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 disabled:opacity-50 transition">
        <Download class="w-4 h-4" /> Import Projects from Jira
      </button>
    </div>

    <!-- Connection form -->
    <div v-if="showForm && !connection" class="space-y-4">
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Jira Base URL</label>
        <input v-model="form.base_url" placeholder="https://yourteam.atlassian.net" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 outline-none" />
      </div>
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Email</label>
        <input v-model="form.email" type="email" placeholder="you@example.com" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 outline-none" />
      </div>
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">API Token</label>
        <input v-model="form.api_token" type="password" placeholder="Your Jira API token" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 outline-none" />
      </div>
      <div class="flex gap-2">
        <button @click="createConnection" :disabled="loading" class="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:opacity-50 transition">
          {{ loading ? 'Connecting...' : 'Connect' }}
        </button>
        <button @click="showForm = false; error = ''" class="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition">
          Cancel
        </button>
      </div>
    </div>

    <!-- Not connected state -->
    <div v-if="!connection && !showForm" class="text-sm text-gray-500">
      No Jira connection configured. Click "Connect" to link your Jira instance and import projects.
    </div>
  </div>
</template>
