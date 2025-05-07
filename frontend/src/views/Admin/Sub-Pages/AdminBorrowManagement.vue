<template>
  <div class="admin-borrow-container">
    <h2>Borrowed Books</h2>

    <input v-model="searchQuery" @keyup.enter="onSearchEnter" class="search-input"
      placeholder="Search by username, title, author, publisher, or ISBN..." />

    <div v-if="borrowedBooks.length > 0" class="book-table-wrapper">
      <table class="book-table">
        <thead>
          <tr>
            <th>Cover</th>
            <th>Title</th>
            <th>Borrowed By</th>
            <th>Days Left</th>
            <th>Penalty Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(book, index) in borrowedBooks" :key="book.id" class="fade-in-row"
            :style="{ animationDelay: `${index * 80}ms` }">
            <td>
              <img :src="book.cover_image || defaultCover" alt="Cover" class="book-cover" />
            </td>
            <router-link :to="`/admin/books/${book.id}`" class="book-link book-title">
              {{ book.title || book.name }}
            </router-link>
            <td>
              <span v-if="usernames[book.currently_borrowed_by]">
                <a :href="`/admin/users/${book.currently_borrowed_by}`" class="user-link">
                  {{ usernames[book.currently_borrowed_by] }}
                </a>
              </span>
              <span v-else-if="book.currently_borrowed_by">Loading...</span>
              <span v-else>-</span>
            </td>
            <td>{{ getDaysLeft(book.return_date) }} days</td>
            <td>
              <span :class="getPenaltyClass(book)">
                {{ getPenaltyStatus(book) }}
              </span>
            </td>
            <td>
              <button class="extend-btn" @click="openExtendModal(book.id)">Extend</button>
              <router-link :to="`/admin/edit-book/${book.id}`" class="edit-btn">Edit</router-link>
              <button class="delete-btn" @click="adminReturnBook(book.id)">Return</button>
            </td>
          </tr>
        </tbody>
      </table>

      <div v-if="showExtendModal" class="modal-overlay">
        <div class="confirm-modal">
          <h3>Extend Return Date</h3>
          <p>How many days would you like to extend?</p>
          <input v-model.number="extraDays" type="number" min="1" class="days-input" />
          <div class="modal-actions">
            <button class="confirm-btn" @click="confirmExtend">Confirm</button>
            <button class="cancel-btn" @click="showExtendModal = false">Cancel</button>
          </div>
        </div>
      </div>
    </div>

    <div v-else class="no-books">No borrowed books found.</div>

    <div class="pagination" v-if="lastPage > 1">
      <button :disabled="page === 1" @click="changePage(page - 1)">‹</button>
      <button v-for="p in lastPage" :key="p" @click="changePage(p)" :class="{ active: p === page }">
        {{ p }}
      </button>
      <button :disabled="page === lastPage" @click="changePage(page + 1)">›</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, reactive, watch } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/api/axios'
import { useToast } from 'vue-toastification'
import defaultCover from '@/assets/images/default-cover.png'

const toast = useToast()
const router = useRouter()
const borrowedBooks = ref([])
const usernames = reactive({})
const searchQuery = ref('')
const page = ref(1)
const lastPage = ref(1)
const limit = 10

const showExtendModal = ref(false)
const selectedBookId = ref(null)
const extraDays = ref(7)

const openExtendModal = (bookId) => {
  selectedBookId.value = bookId
  extraDays.value = 7
  showExtendModal.value = true
}

const confirmExtend = async () => {
  try {
    await api.post(`/admin/borrowed-books/extend/${selectedBookId.value}`, { extra_days: extraDays.value })
    toast.success(`Return date extended by ${extraDays.value} days`)
    showExtendModal.value = false
    await fetchBorrowedBooks()
  } catch (error) {
    toast.error('Failed to extend return date')
  }
}

const fetchBorrowedBooks = async () => {
  try {
    const { data } = await api.get('/admin/borrowed-books', {
      params: {
        page: page.value,
        limit,
        q: searchQuery.value || undefined,
      }
    })
    borrowedBooks.value = data.books
    lastPage.value = data.last_page || 1
  } catch (error) {
    toast.error('Failed to fetch borrowed books')
  }
}

watch(
  () => borrowedBooks.value,
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

const getDaysLeft = (returnDate) => {
  if (!returnDate) return 'N/A'
  const returnDateObj = new Date(returnDate)
  const today = new Date()
  const diffTime = returnDateObj - today
  return Math.ceil(diffTime / (1000 * 60 * 60 * 24))
}

const getPenaltyStatus = (book) => {
  const daysLeft = getDaysLeft(book.return_date)
  return daysLeft < 0 ? "Overdue" : "No Penalty"
}

const getPenaltyClass = (book) => {
  const daysLeft = getDaysLeft(book.return_date)
  return daysLeft < 0 ? "overdue-penalty" : "no-penalty"
}


const adminReturnBook = async (bookId) => {
  try {
    await api.post(`/admin/borrowed-books/return/${bookId}`)
    toast.success('Book returned successfully')
    await fetchBorrowedBooks()
  } catch (error) {
    toast.error('Failed to return book')
  }
}

const goToEditPage = (bookId) => {
  router.push(`/admin/borrow/${bookId}`)
}

const onSearchEnter = () => {
  page.value = 1
  fetchBorrowedBooks()
}

const changePage = (newPage) => {
  page.value = newPage
  fetchBorrowedBooks()
}

onMounted(fetchBorrowedBooks)
</script>

<style scoped>
.admin-borrow-container {
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
  margin-top: 20px;
}

.book-table {
  width: 100%;
  border-collapse: collapse;
}

.book-table th,
.book-table td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #eee;
}

.book-cover {
  width: 50px;
  height: 70px;
  object-fit: cover;
  border-radius: 4px;
}

.no-penalty {
  color: green;
  font-weight: bold;
}

.overdue-penalty {
  color: red;
  font-weight: bold;
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

.extend-btn,
.edit-btn,
.delete-btn {
  padding: 6px 12px;
  margin-right: 6px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 13px;
}

.extend-btn {
  background-color: #f39c12;
  color: white;
}

.edit-btn {
  background-color: #3498db;
  color: white;
}

.delete-btn {
  background-color: #e74c3c;
  color: white;
}

.no-books {
  text-align: center;
  font-style: italic;
  margin-top: 40px;
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

.user-link {
  text-decoration: none;
  color: #2980b9;
}

.user-link:hover {
  text-decoration: underline;
}

.ellipsis {
  max-width: 160px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.days-input {
  width: 100%;
  padding: 10px;
  margin: 12px 0;
  border-radius: 6px;
  border: 1px solid #ccc;
  font-size: 16px;
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
  margin: 0 0 12px;
  color: #555;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.confirm-btn {
  padding: 8px 16px;
  background: #27ae60;
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