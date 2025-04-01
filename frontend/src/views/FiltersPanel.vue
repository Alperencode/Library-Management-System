<template>
  <div class="filters-panel">
    <h3 style="margin-bottom: 8px">Filters</h3>
    <hr />
    <div class="filter-group">
      <div class="filter-item">
        <label>Category:</label>
        <select v-model="selectedCategory">
          <option value="">All</option>
          <option
            v-for="cat in categories"
            :key="cat.category"
            :value="cat.category"
          >
            {{ cat.category }}
          </option>
        </select>
      </div>
      <div class="filter-item">
        <label>Subcategory:</label>
        <select v-model="selectedSubcategory" :disabled="!selectedCategory">
          <option value="">All</option>
          <option
            v-for="sub in (categories.find(c => c.category === selectedCategory)?.subcategories || [])"
            :key="sub"
            :value="sub"
          >
            {{ sub }}
          </option>
        </select>
      </div>
      <div class="filter-item">
        <label>Language</label>
        <select v-model="selectedLanguage">
        </select>
      </div>
      <div class="checkbox-wrapper">
        <input type="checkbox" v-model="onlyAvailable" />
        <label>Book Not Taken</label>
      </div>

      <div class="filter-item">
        <label>Max Page Size</label>
        <input type="number" v-model="maxPageSize" placeholder="Enter number" />
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, defineEmits, watch } from 'vue'
import api from '@/api/axios'

const emit = defineEmits(['update:category', 'update:subcategory'])

const categories = ref([])
const selectedCategory = ref('')
const selectedSubcategory = ref('')

const fetchCategories = async () => {
  try {
    const res = await api.get('/books/search/categories')
    categories.value = res.data.categories
  } catch (err) {
    console.error('Failed to fetch categories:', err)
  }
}

onMounted(fetchCategories)

watch(selectedCategory, () => {
  selectedSubcategory.value = ''
  emit('update:category', selectedCategory.value)
})

watch(selectedSubcategory, () => {
  emit('update:subcategory', selectedSubcategory.value)
})
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
  color: #ffffff;
  font-size: 14px;
  transition: all 0.3s ease;
}

.filter-item select option {
  background-color: white;
  color: black;
}

.filter-item select option:hover {
  background-color: #f5a425 !important;
  color: white !important;
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