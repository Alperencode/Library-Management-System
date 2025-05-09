<template>
  <div class="admin-books-container">
    <h2 class="mb-4">Book List</h2>

    <input v-model="searchQuery" @keyup.enter="onSearchEnter" class="search-input"
      placeholder="Search by title, author, publisher..." />

    <div class="toggle-wrapper">
      <label class="toggle-switch">
        <input type="checkbox" v-model="borrowedOnly" @change="onSearchEnter" />
        <span class="slider"></span>
      </label>
      <span class="toggle-label">Show only borrowed books</span>

      <label class="toggle-switch">
        <input type="checkbox" v-model="recentlyAdded" @change="onSearchEnter" />
        <span class="slider"></span>
      </label>
      <span class="toggle-label">Sort by recently added</span>
    </div>

    <div v-if="books.length > 0" class="book-table-wrapper">
      <table class="book-table">
        <thead>
          <tr>
            <th style="width: 40px;">Cover</th>
            <th style="width: 160px;">Title</th>
            <th style="width: 60px;">Author</th>
            <th style="width: 60px;">Publisher</th>
            <th style="width: 40px;">Status</th>
            <th style="width: 60px;">Borrowed By</th>
            <th style="width: 50px;">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(book, index) in books" :key="book.id" class="fade-in-row"
            :style="{ animationDelay: `${index * 80}ms` }">
            <td>
              <img :src="book.cover_image || defaultCover" alt="Cover" class="book-cover" />
            </td>
            <td class="book-title-cell">
              <router-link :to="`/admin/books/${book.id}`" class="book-link book-title">
                {{ book.title || book.name }}
              </router-link>
            </td>
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
              <router-link :to="`/admin/edit-book/${book.id}`" class="edit-btn">
                Edit
              </router-link>
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
const borrowedOnly = ref(false)
const recentlyAdded = ref(false)

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
        q: searchQuery.value || undefined,
        borrowed_only: borrowedOnly.value || undefined,
        recently_added: recentlyAdded.value || undefined
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
.delete-btn,
.edit-btn:visited {
  display: inline-block;
  padding: 8px 16px;
  margin-right: 6px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  text-align: center;
  text-decoration: none;
}

.edit-btn {
  background-color: #2980b9;
  color: white;
}

.edit-btn:hover {
  background-color: #216aa0;
}

.delete-btn:hover {
  background-color: #a83226;
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

.book-title-cell {
  max-width: 180px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.book-link.book-title {
  font-weight: 600;
  color: #2980b9;
  text-decoration: none;
}

.book-link.book-title:hover {
  text-decoration: underline;
}

.book-table {
  width: 100%;
  border-collapse: collapse;
  table-layout: fixed;
}

.toggle-wrapper {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 16px;
  flex-wrap: wrap;
}

.toggle-switch {
  position: relative;
  display: inline-block;
  width: 44px;
  height: 24px;
}

.toggle-switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #ccc;
  border-radius: 24px;
  transition: 0.3s;
}

.slider:before {
  position: absolute;
  content: "";
  height: 18px;
  width: 18px;
  left: 3px;
  bottom: 3px;
  background-color: white;
  border-radius: 50%;
  transition: 0.3s;
}

.toggle-switch input:checked + .slider {
  background-color: #40916c;
}

.toggle-switch input:checked + .slider:before {
  transform: translateX(20px);
}

.toggle-label {
  font-size: 14px;
  color: #333;
  margin-right: 12px;
}
</style>
