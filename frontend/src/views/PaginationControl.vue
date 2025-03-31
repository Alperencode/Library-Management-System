<template>
  <div class="pagination">
    <ul>
      <li
        v-for="n in props.totalPages"
        :key="n"
        :class="{ active: props.currentPage === n }"
      >
        <a href="#" @click.prevent="emit('update:currentPage', n)">{{ n }}</a>
      </li>
    </ul>
  </div>
</template>

<script setup>
const props = defineProps({
  totalPages: Number,
  currentPage: Number,
});
const emit = defineEmits(['update:currentPage']);
</script>

  <style scoped>
  .pagination ul {
  list-style: none;
  display: flex;
  gap: 8px;
  justify-content: center;
  margin-top: 30px;
  padding: 0;
}

.pagination li a {
  display: inline-block;
  padding: 8px 14px;
  border-radius: 10px;
  background: #fff;
  color: #f5a425;
  border: 2px solid #f5a425;
  font-weight: 600;
  font-size: 14px;
  text-decoration: none;
  transition: all 0.2s ease;
}

.pagination li a:hover {
  background: #f5a425;
  color: white;
}

.pagination li.active a {
  background: #f5a425;
  color: white;
  border-color: #f5a425;
}
  </style>
  