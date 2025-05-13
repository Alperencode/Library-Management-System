<template>
  <div>
    <section class="meetings-page" id="meetings">
      <div class="container">
        <div class="main-content">
          <h2 class="request-title">Request a Book</h2>
          <p class="request-subtitle">Looking for a book? Start typing to search by title, author, publisher, or ISBN.</p>
          <div class="search-bar">
            <input class="input-line full-width" type="text" :value="searchQuery" @input="updateSearchQuery"
              @keyup.enter="performSearch" placeholder="Search by Author, Title, Publisher, ISBN..." />
          </div>
          <div v-if="books.length === 0 && searchPerformed" class="no-results">
            <p class="no-results-text">
              No books found for "{{ searchQuery }}"
            </p>
          </div>
          <div v-if="previousRequests.length > 0 && !searchPerformed" class="previous-requests">
            <div class="requests-header">
              <h3 class="previous-title">Your Previous Requests</h3>
              <span class="see-more" @click="goToRequested">See more →</span>
            </div>
            <ul>
              <li v-for="(book, index) in previousRequests.slice(0, 8)" :key="index">
                <span class="truncate-text">
                  <strong>{{ book.title }}</strong> by {{ book.authors.join(', ') || 'Unknown' }}
                </span>
              </li>
            </ul>
          </div>
          <div v-if="books.length > 0">
            <div class="row grid">
              <div v-for="(book, index) in books" :key="index" class="meeting-item">
                <div class="meeting-box">
                  <div class="thumb">
                    <img :src="book.cover_image" :alt="book.title" class="book-thumbnail" />
                  </div>
                  <div class="down-content">
                    <h4 class="book-title">{{ book.title }}</h4>
                    <p class="text-ellipsis" :title="book.authors.join(', ')">
                      <strong>Author:</strong>
                      {{ book.authors.join(", ") || "Unknown" }}
                    </p>
                    <p class="text-ellipsis" :title="book.publisher">
                      <strong>Publisher:</strong> {{ book.publisher }}
                    </p>
                    <p v-if="book.categories" class="text-ellipsis" :title="book.categories">
                      <strong>Categories:</strong> {{ book.categories }}
                    </p>
                    <button class="request-button" @click="requestBook(book)" :disabled="requestedBookIds.has(book.id)">
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
import { ref, watch, onMounted } from "vue"
import api from "@/api/axios"
import defaultCover from "@/assets/images/default-cover.png"
import { useToast } from 'vue-toastification'
import { useRouter } from "vue-router";
const router = useRouter();

const goToRequested = () => {
  router.push("/user-page/requested");
};

const books = ref([])
const searchQuery = ref("")
const searchPerformed = ref(false)
const currentPage = ref(1)
const limit = ref(24)
const toast = useToast()
const previousRequests = ref([])

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
        isbn: book.isbn || null,
        authors: book.authors || [],
        publisher: book.publisher || "Unknown",
        categories: categoriesString || "Not specified",
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

const requestedBookIds = ref(new Set())

const fetchRequestedBooks = async () => {
  try {
    const res = await api.get("/request-book")
    const ids = res.data.books.map((book) => book.id)
    requestedBookIds.value = new Set(ids)
    previousRequests.value = res.data.books
  } catch (err) {
    console.warn("Could not fetch requested books")
  }
}

onMounted(fetchRequestedBooks)

const requestBook = async (book) => {
  try {
    const payload = {
      id: book.id,
      title: book.title,
      authors: book.authors,
      isbn: book.isbn,
      publisher: book.publisher,
      cover_image: book.cover_image,
    }

    const res = await api.post("/request-book", payload)
    requestedBookIds.value.add(book.id)
    toast.success(res.data.message)
  } catch (err) {
    console.error("Failed to request the book:", err)
  }
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
  justify-content: center;
}


.meeting-item {
  flex: 0 0 calc(25% - 20px);
  max-width: calc(25% - 20px);
  min-width: 220px;
  box-sizing: border-box;
}


@media (max-width: 1024px) {
  .meeting-item {
    flex: 0 0 calc(50% - 20px);
    max-width: calc(50% - 20px);
  }
}

@media (max-width: 600px) {
  .meeting-item {
    flex: 0 0 100%;
    max-width: 100%;
  }
}


.meeting-box {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  height: 500px;
  width: 280px;
  padding: 10px;
  border-radius: 8px;
  background-color: white;
  border: 1px solid #ccc;
  box-sizing: border-box;
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
  background-color: #ffa500cc;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  margin-top: 10px;
  transition: 0.3s;
}

.request-button:hover {
  background-color: #dd9000cc;
}

.request-button:disabled {
  background-color: #bdc3c7;
  cursor: not-allowed;
}

.request-title {
  font-size: 28px;
  margin-bottom: 10px;
  color: white;
}

.request-subtitle {
  font-size: 16px;
  margin-bottom: 30px;
  color: white;
}
.previous-requests {
  margin-top: 40px;
  color: white;
}

.previous-requests h3 {
  font-size: 20px;
  margin-bottom: 12px;
  color: #ffb03b;
}

.previous-requests ul {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  padding: 0;
}

.previous-requests li {
  list-style: none;
  background: rgba(255,255,255,0.1);
  padding: 12px 16px;
  border-radius: 10px;
  color: #fff;
  min-width: 220px;
  max-width: 300px;
  font-size: 14px;
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2;
  overflow: hidden;
  text-overflow: ellipsis;
}

.truncate-text {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
}

.requests-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.previous-title {
  font-size: 20px;
  color: #ffb03b;
  margin: 0;
}

.see-more {
  font-size: 14px;
  color: #ffb03b;
  cursor: pointer;
  transition: text-decoration 0.2s ease;
}

.see-more:hover {
  text-decoration: underline;
}

</style>
