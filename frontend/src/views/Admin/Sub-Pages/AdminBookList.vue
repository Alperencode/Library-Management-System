<template>
  <div class="admin-books-container">
    <h2 class="mb-4">Book List</h2>

    <input v-model="searchQuery" @keyup.enter="onSearchEnter" class="search-input"
      placeholder="Search by title, author, publisher..." />

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
          <tr v-for="(book, index) in books" :key="book.id" class="fade-in-row"
            :style="{ animationDelay: `${index * 80}ms` }">
            <td>
              <img :src="book.cover_image || defaultCover" alt="Cover" class="book-cover" />
            </td>
            <router-link :to="`/admin/books/${book.id}`" class="book-link book-title">
              {{ book.title || book.name }}
            </router-link>
            <td class="ellipsis">{{ book.authors?.join(', ') || 'Unknown' }}</td>
            <td class="ellipsis">{{ book.publisher || 'Unknown' }}</td>
            <td>
              <span :class="book.borrowed ? 'taken' : 'available'">
                {{ book.borrowed ? 'Taken' : 'Available' }}
              </span>
            </td>
            <td>
              <span v-if="usernames[book.currently_borrowed_by]">
                <a :href="`/admin/users/${book.currently_borrowed_by}`" class="user-link">
                  {{ usernames[book.currently_borrowed_by] }}
                </a>
              </span>
              <span v-else-if="book.currently_borrowed_by">Loading...</span>
              <span v-else>-</span>
            </td>
            <td>
              <button class="edit-btn">Edit</button>
              <button class="delete-btn" @click="confirmDelete(book)">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-else class="no-books">No books found.</div>

    <div class="pagination">
      <button :disabled="page === 1" @click="changePage(page - 1)">‹</button>
      <button v-for="p in lastPage" :key="p" @click="changePage(p)" :class="{ active: p === page }">
        {{ p }}
      </button>
      <button :disabled="page === lastPage" @click="changePage(page + 1)">›</button>
    </div>

    <div v-if="showModal" class="modal-overlay">
      <div class="confirm-modal">
        <h3>Confirm Book Deletion</h3>
        <p>This will remove the book from all users and the entire system. Are you sure?</p>
        <div class="modal-actions">
          <button class="confirm-btn" @click="deleteBook(bookToDelete.id)">Yes, Delete</button>
          <button class="cancel-btn" @click="showModal = false">Cancel</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, reactive } from 'vue'
import api from '@/api/axios'
import defaultCover from '@/assets/images/default-cover.png'
import { useToast } from 'vue-toastification'

const books = ref([])
const searchQuery = ref('')
const page = ref(1)
const limit = 10
const lastPage = ref(1)
const usernames = reactive({})
const toast = useToast()

const showModal = ref(false)
const bookToDelete = ref(null)

watch(
  () => books.value,
  async (newBooks) => {
    for (const book of newBooks) {
      const userId = book.currently_borrowed_by
      if (userId && !usernames[userId]) {
        try {
          const res = await api.get(`/admin/users/${userId}`)
          usernames[userId] = res.data.admin?.username || res.data.user?.username || '(Unknown)'
        } catch {
          usernames[userId] = '(Error)'
        }
      }
    }
  },
  { immediate: true }
)

const fetchBooks = async () => {
  try {
    const response = await api.get('/books', {
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

const confirmDelete = (book) => {
  bookToDelete.value = book
  showModal.value = true
}

const deleteBook = async (bookId) => {
  try {
    await api.delete(`/admin/book/${bookId}`)
    toast.success('Book deleted successfully.')
    showModal.value = false
    fetchBooks()
  } catch (err) {
    toast.error('Failed to delete book.')
    console.error(err)
  }
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

.user-link {
  text-decoration: none;
  color: #2980b9;
}

.user-link:hover {
  text-decoration: underline;
}

.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}

.confirm-modal {
  background: #fff;
  padding: 24px;
  border-radius: 10px;
  width: 90%;
  max-width: 400px;
  box-shadow: 0 5px 30px rgba(0, 0, 0, 0.2);
}

.confirm-modal h3 {
  margin: 0 0 15px;
  font-size: 20px;
}

.confirm-modal p {
  margin: 0 0 20px;
  color: #555;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.confirm-btn {
  padding: 8px 16px;
  background: #c0392b;
  color: #fff;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}

.cancel-btn {
  padding: 8px 16px;
  background: #bdc3c7;
  color: #333;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}
</style>
