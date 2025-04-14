<template>
  <div class="admin-books-container">
    <h2 class="mb-4">Book List</h2>

    <input
      v-model="searchQuery"
      @keyup.enter="onSearchEnter"
      class="search-input"
      placeholder="Search by title, author, publisher..."
    />

    <div v-if="books.length > 0" class="book-table-wrapper">
      <table class="book-table">
        <thead>
          <tr>
            <th>Cover</th>
            <th style="width: 180px;">Title</th>
            <th style="width: 160px;">Author</th>
            <th>Publisher</th>
            <th>Status</th>
            <th>Borrowed By</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="(book, index) in books"
            :key="book.id"
            class="fade-in-row"
            :style="{ animationDelay: `${index * 80}ms` }"
          >
            <td>
              <img :src="book.cover_image || defaultCover" alt="Cover" class="book-cover" />
            </td>
            <td>{{ book.title }}</td>
            <td class="ellipsis">{{ book.authors?.join(', ') || 'Unknown' }}</td>
            <td class="ellipsis">{{ book.publisher || 'Unknown' }}</td>
            <td>
              <span :class="book.borrowed ? 'taken' : 'available'">
                {{ book.borrowed ? 'Taken' : 'Available' }}
              </span>
            </td>
            <td>{{ book.currently_borrowed_by || '-' }}</td>
            <td>
              <button class="edit-btn">Edit</button>
              <button class="delete-btn">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-else class="no-books">No books found.</div>

    <div class="pagination">
      <button :disabled="page === 1" @click="changePage(page - 1)">‹</button>
      <button
        v-for="p in lastPage"
        :key="p"
        @click="changePage(p)"
        :class="{ active: p === page }"
      >
        {{ p }}
      </button>
      <button :disabled="page === lastPage" @click="changePage(page + 1)">›</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from '@/api/axios'
import defaultCover from '@/assets/images/default-cover.png'

const books = ref([])
const searchQuery = ref('')
const page = ref(1)
const limit = 10
const lastPage = ref(1)

const fetchBooks = async () => {
  try {
    const response = await axios.get('/books', {
      params: {
        page: page.value,
        limit,
        q: searchQuery.value || undefined
      }
    })

    books.value = response.data.books
    lastPage.value = response.data.last_page || 1
  } catch (err) {
    console.error('Error fetching books:', err)
  }
}

const changePage = (newPage) => {
  page.value = newPage
  fetchBooks()
}

const onSearchEnter = () => {
  page.value = 1
  fetchBooks()
}

onMounted(fetchBooks)
</script>

<style scoped>

.admin-books-container {
  padding: 24px;
}

.search-input {
  width: 100%;
  padding: 10px;
  margin-bottom: 16px;
  border-radius: 6px;
  border: 1px solid #ccc;
}

.book-table-wrapper {
  overflow-x: auto;
}

.book-table {
  width: 100%;
  border-collapse: collapse;
}

.book-table th,
.book-table td {
  padding: 10px;
  border-bottom: 1px solid #eee;
  text-align: left;
  vertical-align: middle;
}

.book-cover {
  width: 50px;
  height: 70px;
  object-fit: cover;
  border-radius: 4px;
}

.ellipsis {
  max-width: 160px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.available {
  color: green;
  font-weight: bold;
}

.taken {
  color: red;
  font-weight: bold;
}

.edit-btn,
.delete-btn {
  padding: 4px 8px;
  margin-right: 4px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 13px;
}
.edit-btn {
  background-color: #2980b9;
  color: white;
}
.delete-btn {
  background-color: #c0392b;
  color: white;
}

.no-books {
  text-align: center;
  margin-top: 40px;
  font-style: italic;
}

.pagination {
  display: flex;
  justify-content: center;
  margin-top: 20px;
  gap: 6px;
}
.pagination button {
  padding: 6px 12px;
  border: none;
  background-color: #f0f0f0;
  cursor: pointer;
  border-radius: 4px;
}
.pagination button.active {
  background-color: #d4881a;
  color: white;
  font-weight: bold;
}
.pagination button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.fade-in-row {
  animation: fadeUp 0.5s ease-out both;
}

@keyframes fadeUp {
  0% {
    opacity: 0;
    transform: translateY(20px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}

</style>
