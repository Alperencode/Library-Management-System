<template>
    <div class="filters-panel">
      <h2 class="section-title">Filters</h2>
      <hr class="divider" />
      <div class="filter-group">
        <div class="filter-item">
            <label for="language">Language</label>
            <select id="language" v-model="filters.language">
            </select>
        </div>
        <div class="checkbox-wrapper">
            <input type="checkbox" id="bookNotTaken" v-model="filters.bookNotTaken" />
            <label for="bookNotTaken">Book Not Taken</label>
        </div>
        <div class="filter-item">
            <label for="maxPageSize">Max Page Size</label>
            <input type="number" id="maxPageSize" v-model="filters.maxPageSize" min="1" />
        </div>
        </div>
      <hr class="divider" />  
      <h3 class="section-title">Categories</h3>
      <ul class="category-list">
        <li
          v-for="category in categories"
          :key="category"
          @click="selectCategory(category)"
          :class="{ active: filters.selectedCategory === category }"
        >
          {{ category }}
        </li>
      </ul>
    </div>
  </template>
  
  <script setup>
  import { reactive } from 'vue'
  
  const filters = reactive({
    language: '',
    bookNotTaken: false,
    maxPageSize: '',
  })

  const categories = ['Science', 'Fiction', 'History', 'Biography']
  
  </script>
  
  <style scoped>

.filters-panel {
  color: white;
}
  .filter-group {
  display: flex;
  flex-direction: column;
  gap: 20px;
  color: white;
}

.filter-item {
  display: flex;
  flex-direction: column;
  color: white;
  font-size: 15px;
  font-weight: 500;
}

.filter-item label {
  margin-bottom: 6px;
  color: white;
}

.filter-item select,
.filter-item input[type="number"] {
  padding: 8px 12px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 6px;
  background-color: rgba(255, 255, 255, 0.08);
  color: white;
  font-size: 14px;
  transition: all 0.3s ease;
}

.filter-item select:focus,
.filter-item input[type="number"]:focus {
  border-color: #f5a425;
  background-color: rgba(255, 255, 255, 0.12);
  outline: none;
}

.checkbox-wrapper {
  display: flex;
  align-items: center;
  gap: 10px;
  color: white;
  font-size: 14px;
}

.checkbox-wrapper input[type="checkbox"] {
  width: 16px;
  height: 16px;
  accent-color: #f5a425;
}

input[type="number"] {
  padding: 8px 12px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 6px;
  background-color: rgba(255, 255, 255, 0.08);
  color: white;
  font-size: 14px;
  transition: border-color 0.3s ease, background-color 0.3s ease;

  box-sizing: border-box;
  opacity: 0.6;
  height: auto;
  margin: 0;
}

input[type="number"]:focus {
  border-color: #f5a425;
  background-color: rgba(255, 255, 255, 0.12);
  outline: none;
}

  </style>
  