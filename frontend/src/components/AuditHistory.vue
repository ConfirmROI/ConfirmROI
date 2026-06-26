<script setup>
import { ref, watch } from 'vue'
import { History, ChevronDown, ChevronUp } from 'lucide-vue-next'
import apiClient from '../api/client'

const props = defineProps({
  entityType: { type: String, required: true },
  entityId: { type: Number, required: true },
})

const entries = ref([])
const loading = ref(false)
const expanded = ref(false)

async function fetchHistory() {
  loading.value = true
  try {
    const resp = await apiClient.get('/audit', {
      params: { entity_type: props.entityType, entity_id: props.entityId },
    })
    entries.value = resp.data
  } catch {
    entries.value = []
  } finally {
    loading.value = false
  }
}

watch(expanded, (val) => {
  if (val && entries.value.length === 0 && !loading.value) {
    fetchHistory()
  }
})

function toggle() {
  expanded.value = !expanded.value
}

function formatDate(isoStr) {
  if (!isoStr) return ''
  const d = new Date(isoStr)
  return d.toLocaleDateString(undefined, {
    month: 'short', day: 'numeric', year: 'numeric',
    hour: '2-digit', minute: '2-digit',
  })
}

function actionColor(action) {
  if (action === 'create') return 'text-green-600 bg-green-50'
  if (action === 'update') return 'text-blue-600 bg-blue-50'
  if (action === 'delete') return 'text-red-600 bg-red-50'
  return 'text-gray-600 bg-gray-50'
}
</script>

<template>
  <div class="mt-3">
    <button
      @click="toggle"
      class="flex items-center gap-1.5 text-xs text-gray-500 hover:text-gray-700 transition"
      :data-testid="`audit-history-toggle-${entityType}-${entityId}`"
    >
      <History class="w-3.5 h-3.5" />
      <span>Change History</span>
      <ChevronDown v-if="!expanded" class="w-3 h-3" />
      <ChevronUp v-else class="w-3 h-3" />
    </button>

    <div v-if="expanded" class="mt-3 space-y-2">
      <div v-if="loading" class="text-xs text-gray-400 animate-pulse">Loading history...</div>

      <div v-else-if="entries.length === 0" class="text-xs text-gray-400">
        No changes recorded yet.
      </div>

      <div v-else class="space-y-2">
        <div
          v-for="entry in entries"
          :key="entry.id"
          class="border border-gray-100 rounded-lg p-3 bg-gray-50/50"
        >
          <div class="flex items-center gap-2 flex-wrap">
            <span
              class="text-xs font-medium px-2 py-0.5 rounded capitalize"
              :class="actionColor(entry.action)"
            >{{ entry.action }}</span>
            <span class="text-xs text-gray-600 font-medium">{{ entry.user_name || 'Unknown' }}</span>
            <span class="text-xs text-gray-400">{{ formatDate(entry.created_at) }}</span>
          </div>

          <div v-if="entry.change_reason" class="mt-2 text-xs text-gray-700">
            <span class="font-medium">Why: </span>{{ entry.change_reason }}
          </div>

          <div v-if="entry.changes" class="mt-2 space-y-1">
            <div
              v-for="(change, field) in entry.changes"
              :key="field"
              class="text-xs text-gray-500 flex items-center gap-1.5"
            >
              <span class="font-mono font-medium text-gray-600">{{ field }}:</span>
              <span class="line-through text-gray-400">{{ change.old ?? '—' }}</span>
              <span class="text-gray-400">→</span>
              <span class="text-gray-700">{{ change.new ?? '—' }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
