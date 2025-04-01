<template>
  <div>
    <MainHeader />
    <section class="meetings-page" id="meetings">
      <div class="container two-column-layout">
        <div class="sidebar">
          <FiltersPanel
            @update:category="selectedCategory = $event"
            @update:subcategory="selectedSubcategory = $event"
            @update:language="selectedLanguage = $event"
            @update:onlyAvailable="onlyAvailable = $event"
            @update:maxPageCount="maxPageCount = $event"
          />
        </div>
        <div class="main-content">
          <SearchBar v-model="searchQuery" @order="orderBy" />
          <div v-if="paginatedBooks.length === 0" class="no-results">
            <p class="no-results-text">
              No books found for "{{ searchQuery }}"
            </p>
          </div>
          <div v-else>
            <div class="row grid">
              <div
                v-for="(book, index) in paginatedBooks"
                :key="index"
                class="meeting-item"
                :ref="el => setBooksRef(book.title, el)"
              >
                <div class="meeting-box">
                  <div class="thumb">
                    <router-link :to="book.link">
                      <img
                        :src="book.image"
                        :alt="book.title"
                        class="book-thumbnail"
                      />
                    </router-link>
                  </div>
                  <div class="down-content">
                    <router-link :to="book.link">
                      <h4 class="book-title">{{ book.title }}</h4>
                    </router-link>
                    <p class="text-ellipsis" :title="book.authors.join(', ')">
                      <strong>Author:</strong> {{ book.authors.join(', ') || 'Unknown' }}
                    </p>
                    <p class="text-ellipsis" :title="book.publisher">
                      <strong>Publisher:</strong> {{ book.publisher }}
                    </p>
                    <p>
                      <strong>Status:</strong>
                      <span
                        :class="book.borrowed ? 'status-badge taken' : 'status-badge available'"
                      >
                        {{ book.borrowed ? 'Taken' : 'Available' }}
                      </span>
                    </p>
                  </div>
                </div>
              </div>
            </div>
            <PaginationControl
              :currentPage="currentPage"
              :lastPage="lastPage"
              @update:currentPage="handlePageChange"
            />
          </div>    
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import MainHeader from '@/components/MainHeader.vue'
import FiltersPanel from './FiltersPanel.vue'
import SearchBar from './SearchBar.vue'
import PaginationControl from './PaginationControl.vue'
import api from '@/api/axios'
import defaultCover from '@/assets/images/default-cover.png'

const books = ref([])
const limit = ref(24)
const lastPage = ref(1)
const searchQuery = ref('')
const currentPage = ref(Number(localStorage.getItem('currentPage')) || 1)
const selectedCategory = ref('')
const selectedSubcategory = ref('')
const selectedLanguage = ref(null)
const onlyAvailable = ref(false)
const maxPageCount = ref(null)
const mostBorrowed = ref(false)
const recentlyAdded = ref(false)
const order = ref(null)

const BooksRefs = ref({})
const setBooksRef = (title, el) => {
  BooksRefs.value[title] = el
}

const fetchBooks = async () => {
  try {
    const res = await api.get('/books', {
      params: {
        page: currentPage.value,
        limit: limit.value,
        q: searchQuery.value || undefined,
        category: selectedCategory.value || undefined,
        subcategory: selectedSubcategory.value || undefined,
        language: selectedLanguage.value || undefined,
        available_only: onlyAvailable.value,
        max_page_count: maxPageCount.value || undefined,
        most_borrowed: mostBorrowed.value,
        recently_added: recentlyAdded.value,
      },
    })
    books.value = res.data.books.map(book => ({
      id: book.id,
      title: book.title || 'No Title',
      image: book.cover_image || defaultCover,
      link: `/book/${book.id}`,
      authors: book.authors || [],
      publisher: book.publisher || 'Unknown',
      borrowed: book.borrowed || false,
    }))
    lastPage.value = res.data.last_page || 1
  } catch (err) {
    console.error('Books could not be retrieved:', err)
  }
}

onMounted(fetchBooks)
watch([order, selectedCategory, selectedSubcategory, onlyAvailable, maxPageCount], async () => {
  currentPage.value = 1
  await fetchBooks()
})

const handlePageChange = (newPage) => {
  currentPage.value = newPage
  localStorage.setItem('currentPage', newPage)
  fetchBooks()
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

const paginatedBooks = books

const orderBy = (type) => {
  mostBorrowed.value = false;
  recentlyAdded.value = false;

  if (type === 'az') {
    books.value.sort((a, b) => a.title.localeCompare(b.title));
  } else if (type === 'za') {
    books.value.sort((a, b) => b.title.localeCompare(a.title));
  } else if (type === 'most') {
    mostBorrowed.value = true;
    fetchBooks();
  } else if (type === 'recent') {
    recentlyAdded.value = true;
    fetchBooks();
  }
};

watch(searchQuery, async () => {
  currentPage.value = 1
  await fetchBooks()
})

watch(selectedLanguage, () => fetchBooks())

</script>

<style scoped>
.meetings-page {
  display: flex;
  min-height: 100vh;
}

.two-column-layout {
  display: flex;
  flex: 1;
}

.sidebar {
  width: 320px;
  background-color: rgba(255, 255, 255, 0.02);
  backdrop-filter: blur(5px);
  -webkit-backdrop-filter: blur(5px);
  box-shadow: 2px 0 8px rgba(0, 0, 0, 0.05);
  border-right: 1px solid rgba(0, 0, 0, 0.05);
  border-top: 1px solid rgba(0, 0, 0, 0.02);
  padding: 16px;
  position: sticky;
  top: 0;
  align-self: flex-start;
  height: 100vh;
  overflow-y: auto;
  padding-top: 50px;
  margin-top: 15px;
}

.main-content {
  flex: 1;
  padding: 24px;
  background-color: transparent;
}

.no-results {
  color: #ffffff !important;
  padding: 20px;
  font-size: 18px;
  text-align: center;
  border-radius: 8px;
  font-weight: 600;
  z-index: 1000;
  position: relative;
}
.no-results-text {
  color: rgb(226, 226, 226) !important;
  font-size: 15px;
  font-weight: bold;
  text-shadow: 1px 1px 3px black;
}

.grid {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  margin-top: 20px;
}

.meeting-item {
  width: 100%;
}
@media (min-width: 768px) {
  .meeting-item {
    width: calc(33.333% - 20px);
  }
}

.meeting-box {
  border: 1px solid #ccc;
  padding: 10px;
  border-radius: 8px;
  background-color: white;
  height: 100%;
  min-height: 100px;
}

.thumb {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 180px;
  background-color: #ffffff;
  padding: 8px;
  overflow: hidden;
  border-radius: 8px;
}

.book-thumbnail {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}
.down-content {
  text-align: left;
  padding: 10px;
}

.down-content h4 {
  margin-bottom: 8px;
}

.down-content p {
  margin: 4px 0;
  font-size: 14px;
}

.book-title {
  text-align: center;
  margin-bottom: 8px;
}

.text-ellipsis {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  display: block;
  width: 100%;
  max-width: 100%;
}

.status-badge {
  display: inline-block;
  padding: 4px 10px;
  font-size: 14px;
  font-weight: 600;
  border-radius: 6px;
  margin-left: 6px;
  color: white;
  min-width: 80px;
  text-align: center;
}

.status-badge.taken {
  background-color: #e74c3c;
}

.status-badge.available {
  background-color: #27ae60;
}

.sidebar::-webkit-scrollbar {
  width: 8px;
}

.sidebar::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 10px;
}

.sidebar::-webkit-scrollbar-thumb {
  background-color: #f5a425;
  border-radius: 10px;
}

.sidebar::-webkit-scrollbar-thumb:hover {
  background-color: #ffbb55;
}

</style>
