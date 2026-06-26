<script setup>
defineProps({
  sections: {
    type: Array,
    required: true,
  },
  title: {
    type: String,
    default: 'Contents',
  },
})
</script>

<template>
  <aside class="hidden lg:block">
    <nav class="sticky top-24 space-y-1">
      <p class="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-3">{{ title }}</p>
      <a
        v-for="s in sections"
        :key="s.id"
        :href="`#${s.id}`"
        class="block text-sm text-gray-600 hover:text-primary-700 transition-colors py-1.5"
      >
        {{ s.label }}
      </a>
    </nav>
  </aside>
</template>
