<script setup>
import { ref } from 'vue'
import { useProjectsStore } from '../stores/projects'
import { Upload, X, CheckCircle, AlertCircle } from 'lucide-vue-next'

const props = defineProps({
  teamId: { type: [Number, String], default: null },
})

const emit = defineEmits(['close'])

const projectsStore = useProjectsStore()
const fileInput = ref(null)
const csvContent = ref('')
const fileName = ref('')
const result = ref(null)
const error = ref('')

function handleFileSelect(event) {
  const file = event.target.files[0]
  if (!file) return
  fileName.value = file.name
  const reader = new FileReader()
  reader.onload = (e) => {
    csvContent.value = e.target.result
  }
  reader.readAsText(file)
}

async function handleImport() {
  if (!csvContent.value) {
    error.value = 'Please select a CSV file'
    return
  }
  error.value = ''
  result.value = null

  const teamId = props.teamId
  if (!teamId) {
    error.value = 'No team selected. Please create a team first.'
    return
  }
  const res = await projectsStore.importCsv(teamId, csvContent.value)
  if (res) {
    result.value = res
  } else {
    error.value = projectsStore.error || 'Import failed'
  }
}
</script>

<template>
  <div class="bg-white rounded-xl border border-gray-200 p-6 mb-6">
    <div class="flex items-center justify-between mb-4">
      <h3 class="font-semibold text-gray-900">Import Projects from CSV</h3>
      <button @click="emit('close')" class="text-gray-400 hover:text-gray-600">
        <X class="w-5 h-5" />
      </button>
    </div>

    <p class="text-sm text-gray-500 mb-4">
      CSV must have a <code class="bg-gray-100 px-1 rounded">name</code> column. Optional columns:
      <code class="bg-gray-100 px-1 rounded">description</code>,
      <code class="bg-gray-100 px-1 rounded">status</code>,
      <code class="bg-gray-100 px-1 rounded">external_id</code>,
      <code class="bg-gray-100 px-1 rounded">start_date</code>,
      <code class="bg-gray-100 px-1 rounded">end_date</code>
    </p>

    <div class="flex items-center gap-3 mb-4">
      <label class="flex items-center gap-2 px-4 py-2 border border-gray-300 rounded-lg cursor-pointer hover:bg-gray-50 transition">
        <Upload class="w-4 h-4" />
        <span class="text-sm">Choose file</span>
        <input ref="fileInput" type="file" accept=".csv" @change="handleFileSelect" class="hidden" />
      </label>
      <span v-if="fileName" class="text-sm text-gray-600">{{ fileName }}</span>
    </div>

    <div v-if="error" class="flex items-center gap-2 text-red-600 text-sm mb-3">
      <AlertCircle class="w-4 h-4" /> {{ error }}
    </div>

    <div v-if="result" class="flex items-center gap-2 text-green-600 text-sm mb-3">
      <CheckCircle class="w-4 h-4" />
      Imported {{ result.imported }} project(s)
      <span v-if="result.errors.length" class="text-red-500">({{ result.errors.length }} error(s))</span>
    </div>

    <button
      @click="handleImport"
      :disabled="!csvContent"
      class="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:opacity-50 transition"
    >
      Import
    </button>
  </div>
</template>
