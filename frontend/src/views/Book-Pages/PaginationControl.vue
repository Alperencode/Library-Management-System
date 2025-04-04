<template>
  <div class="pagination">
    <button @click="prevPage" :disabled="currentPage === 1">‹</button>
    <button
      v-for="page in visiblePages"
      :key="page"
      :class="{ active: page === currentPage }"
      @click="goToPage(page)"
    >
      {{ page }}
    </button>
    <button @click="nextPage" :disabled="currentPage === lastPage">›</button>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  currentPage: Number,
  lastPage: Number
})

const emit = defineEmits(['update:currentPage'])

const goToPage = (page) => {
  if (page >= 1 && page <= props.lastPage) {
    emit('update:currentPage', page)
  }
}

const prevPage = () => {
  if (props.currentPage > 1) {
    emit('update:currentPage', props.currentPage - 1)
  }
}

const nextPage = () => {
  if (props.currentPage < props.lastPage) {
    emit('update:currentPage', props.currentPage + 1)
  }
}

const visiblePages = computed(() => {
  const pages = []
  const start = Math.max(1, props.currentPage - 1)
  const end = Math.min(start + 2, props.lastPage)

  for (let i = start; i <= end; i++) {
    pages.push(i)
  }

  return pages
})
</script>

<style scoped>
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 10px;
  margin-top: 24px;
  flex-wrap: wrap;
}

button {
  padding: 10px 16px;
  font-size: 14px;
  font-weight: 600;
  border: none;
  border-radius: 12px;
  min-width: 4px;
  background-color: #f2f2f2;
  color: #333;
  cursor: pointer;
  transition: all 0.2s ease;
  margin: 0 6px;
}

button:hover:not(:disabled) {
  background-color: #ffb03b;
}

button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

button.active {
  background-color: #ffb03b;
  color: #fff;
}
</style>
