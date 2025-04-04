<template>
  <div>
    <section class="meetings-page" id="meetings">
      <div class="container">
        <div class="main-content">
          <div class="search-bar">
            <input class="input-line full-width" type="text" :value="searchQuery" @input="updateSearchQuery"
              @keyup.enter="performSearch" placeholder="Search by Author, Title, Publisher, ISBN..." />
          </div>
          <div v-if="books.length === 0 && searchPerformed" class="no-results">
            <p class="no-results-text">
              No books found for "{{ searchQuery }}"
            </p>
          </div>
          <div v-else>
            <div class="row grid">
              <div v-for="(book, index) in books" :key="index" class="meeting-item">
                <div class="meeting-box">
                  <div class="thumb">
                    <img :src="book.cover_image" :alt="book.title" class="book-thumbnail" />
                  </div>
                  <div class="down-content">
                    <h4 class="book-title">{{ book.title }}</h4>
                    <p class="text-ellipsis" :title="book.authors.join(', ')">
                      <strong>Author:</strong> {{ book.authors.join(', ') || 'Unknown' }}
                    </p>
                    <p class="text-ellipsis" :title="book.publisher">
                      <strong>Publisher:</strong> {{ book.publisher }}
                    </p>
                    <p
                      v-if="book.categories"
                      class="text-ellipsis"
                      :title="book.categories"
                    >
                      <strong>Categories:</strong> {{ book.categories }}
                    </p>
                    <button class="request-button" @click="requestBook(book)">
                      Request
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, watch } from "vue"
import api from "@/api/axios"
import defaultCover from "@/assets/images/default-cover.png"

const books = ref([])
const searchQuery = ref("")
const searchPerformed = ref(false)
const currentPage = ref(1)
const limit = ref(24)

const fetchBooks = async () => {
  if (!searchQuery.value.trim()) {
    books.value = []
    searchPerformed.value = false
    return
  }
  try {
    const res = await api.get("/google-books/search", {
      params: {
        q: searchQuery.value,
        page: currentPage.value,
        limit: limit.value,
      },
    })
    books.value = res.data.books.map((book) => {
      let categoriesString = ""
      if (Array.isArray(book.categories) && book.categories.length > 0) {
        categoriesString = book.categories
          .map((cat) => {
            let main = cat.category || "Unknown Category"
            if (cat.subcategory) {
              main += ` - ${cat.subcategory}`
            }
            return main
          })
          .join(", ")
      }
      return {
        id: book.id,
        title: book.title || "No Title",
        cover_image: book.cover_image || defaultCover,
        authors: book.authors || [],
        publisher: book.publisher || "Unknown",
        categories: categoriesString
      }
    })
    searchPerformed.value = true
  } catch (err) {
    books.value = []
    searchPerformed.value = true
  }
}

watch(searchQuery, () => {
  books.value = []
  searchPerformed.value = false
})

const performSearch = () => {
  currentPage.value = 1
  fetchBooks()
}

const updateSearchQuery = (event) => {
  searchQuery.value = event.target.value
}

const requestBook = (book) => {
  console.log(`Request sent for book: ${book.title} (ID: ${book.id})`)
}
</script>

<style scoped>
.meetings-page {
  display: flex;
  min-height: 100vh;
}

.main-content {
  flex: 1;
  padding: 24px;
  background-color: transparent;
}

.search-bar {
  margin: 40px 10px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.input-line {
  background: none;
  margin-bottom: 0;
  padding: 6px 10px;
  line-height: 2.4em;
  color: #fff;
  font-family: roboto;
  font-weight: 300;
  font-size: 1.2rem;
  border: none;
  border-bottom: 1px solid rgba(255, 255, 255, 0.65);
  transition: all 0.2s ease;
  width: 100%;
}

.input-line:focus {
  outline: none;
}

::placeholder {
  color: rgba(255, 255, 255, 0.65);
}

.no-results {
  color: #ffffff !important;
  padding: 20px;
  font-size: 18px;
  text-align: center;
  border-radius: 8px;
  font-weight: 600;
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
  text-align: left !important;
}

.book-title {
  text-align: center;
  overflow: hidden;
  margin-bottom: 8px;
}

.text-ellipsis {
  margin: 0 !important;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  display: block;
  width: 100%;
  max-width: 100%;
}


.status-badge.taken {
  background-color: #e74c3c;
}

.status-badge.available {
  background-color: #27ae60;
}

.request-button {
  width: 100%;
  padding: 8px;
  font-size: 14px;
  font-weight: bold;
  background-color: #3498db;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  margin-top: 10px;
  transition: 0.3s;
}

.request-button:hover {
  background-color: #2980b9;
}

.request-button:disabled {
  background-color: #bdc3c7;
  cursor: not-allowed;
}
</style>
