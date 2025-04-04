<template>
  <div class="filters-panel">
    <h3 style="margin-bottom: 8px">Categories</h3>
    <hr />
    <div class="filter-group">
      <div class="filter-item">
        <label>Categories</label>
        <section class="category-scroll-section">
          <ul class="category-list">
            <li
              @click="selectCategory('')"
              :class="{ active: selectedCategory === '' }"
            >
              All Categories
            </li>
            <li
              v-for="cat in categories"
              :key="cat.category"
              @click="selectCategory(cat.category)"
              :class="{ active: selectedCategory === cat.category }"
            >
              {{ cat.category }}
            </li>
          </ul>
        </section>
      </div>
      <div class="filter-item">
        <label>Subcategory</label>
        <select v-model="selectedSubcategory" :disabled="!selectedCategory">
          <option value="">All Subcategories</option>
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
        <h3 style="margin-bottom: 8px">Filters</h3>
        <hr />
        <div class="filter-item">
          <label>Language</label>
          <select v-model="selectedLanguage">
            <option :value="null">All Languages</option>
            <option
              v-for="lang in languages"
              :key="lang.Key"
              :value="lang.Key"
            >
              {{ lang.Language }}
            </option>
          </select>
        </div>
      </div>
      <hr />
      <div class="checkbox-wrapper">
        <label class="custom-checkbox">
          <input type="checkbox" v-model="onlyAvailable" />
          <span class="checkmark"></span>
          Available Only
        </label>
      </div>
      <hr />
      <div class="filter-item">
        <label>Max Page Size</label>
        <input type="number" min="1" v-model.number="localMaxPageCount" @input="$emit('update:maxPageCount', localMaxPageCount)" placeholder="Enter number" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, defineEmits, watch } from 'vue'
import api from '@/api/axios'

const emit = defineEmits(['update:category', 'update:subcategory', 'update:language', 'update:onlyAvailable',   'update:maxPageCount'])

const categories = ref([])
const selectedCategory = ref('')
const selectedSubcategory = ref('')
const languages = ref([])
const selectedLanguage = ref(null)
const onlyAvailable = ref(false)
const localMaxPageCount = ref(null)

const fetchCategories = async () => {
  try {
    const res = await api.get('/books/search/categories')
    categories.value = res.data.categories
  } catch (err) {
    console.error('Failed to fetch categories:', err)
  }
}

onMounted(fetchCategories)

onMounted(async () => {
  try {
    const res = await api.get('/books/search/languages')
    languages.value = res.data.languages
  } catch (err) {
    console.error('Language fetch failed:', err)
  }
})

watch(selectedCategory, () => {
  selectedSubcategory.value = ''
  emit('update:category', selectedCategory.value)
})

watch(selectedSubcategory, () => {
  emit('update:subcategory', selectedSubcategory.value)
})

watch(selectedLanguage, (newVal) => {
  emit('update:language', newVal)
})

watch(onlyAvailable, (val) => {
  emit('update:onlyAvailable', val)
})

watch(localMaxPageCount, (val) => {
  emit('update:maxPageCount', val)
})

const selectCategory = (category) => {
  selectedCategory.value = category
  selectedSubcategory.value = ''
  emit('update:category', category)
}

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


.category-scroll-section {
  max-height: 280px;
  overflow-y: auto;
  padding-right: 4px;
  margin-top: 6px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 6px;
  background-color: rgba(255, 255, 255, 0.03);
}

.category-list {
  list-style: none;
  padding: 8px;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.category-list li {
  padding: 6px 10px;
  border-radius: 4px;
  background-color: rgba(255, 255, 255, 0.06);
  color: white;
  cursor: pointer;
  transition: background-color 0.3s;
}

.category-list li:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.category-list li.active {
  background-color: #f5a425;
  color: black;
  font-weight: bold;
}

.category-scroll-section::-webkit-scrollbar {
  width: 8px;
}

.category-scroll-section::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 10px;
}

.category-scroll-section::-webkit-scrollbar-thumb {
  background-color: #f5a425;
  border-radius: 10px;
}

.category-scroll-section::-webkit-scrollbar-thumb:hover {
  background-color: #ffbb55;
}

.subcategory-scroll-section {
  max-height: 220px;
  overflow-y: auto;
  padding-right: 4px;
  margin-top: 6px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 6px;
  background-color: rgba(255, 255, 255, 0.03);
}

.subcategory-list {
  list-style: none;
  padding: 8px;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.subcategory-list li {
  padding: 6px 10px;
  border-radius: 4px;
  background-color: rgba(255, 255, 255, 0.06);
  color: white;
  cursor: pointer;
  transition: background-color 0.3s;
}

.subcategory-list li:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.subcategory-list li.active {
  background-color: #f5a425;
  color: black;
  font-weight: bold;
}

.subcategory-scroll-section::-webkit-scrollbar {
  width: 8px;
}

.subcategory-scroll-section::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 10px;
}

.subcategory-scroll-section::-webkit-scrollbar-thumb {
  background-color: #f5a425;
  border-radius: 10px;
}

.subcategory-scroll-section::-webkit-scrollbar-thumb:hover {
  background-color: #ffbb55;
}

</style>