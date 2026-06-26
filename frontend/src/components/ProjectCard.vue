<script setup>
import { FolderKanban, TrendingUp } from 'lucide-vue-next'

defineProps({
  project: { type: Object, required: true },
  roi: { type: Number, default: null },
})
</script>

<template>
  <div
    class="bg-white rounded-xl border border-gray-200 p-5 hover:shadow-md transition cursor-pointer"
    @click="$emit('click')"
  >
    <div class="flex items-start justify-between mb-3">
      <div class="flex items-center gap-2">
        <div class="w-10 h-10 rounded-lg bg-primary-50 flex items-center justify-center">
          <FolderKanban class="w-5 h-5 text-primary-600" />
        </div>
        <div>
          <h3 class="font-semibold text-gray-900">{{ project.name }}</h3>
          <span class="text-xs text-gray-500 capitalize">{{ project.status }}</span>
        </div>
      </div>
    </div>
    <p class="text-sm text-gray-500 line-clamp-2 mb-3">{{ project.description || 'No description' }}</p>
    <div v-if="project.start_date || project.end_date" class="text-xs text-gray-400 mb-2">
      <span v-if="project.start_date">{{ project.start_date }}</span>
      <span v-if="project.start_date && project.end_date"> — </span>
      <span v-if="project.end_date">{{ project.end_date }}</span>
    </div>
    <div v-if="roi !== null" class="flex items-center gap-1 text-primary-600">
      <TrendingUp class="w-4 h-4" />
      <span class="font-semibold">${{ roi.toLocaleString() }}</span>
    </div>
  </div>
</template>
