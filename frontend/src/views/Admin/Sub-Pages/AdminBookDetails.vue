<template>
  <div class="content-wrapper">
    <main>
      <div v-if="book" class="book-flexbox">
        <div class="left-box">
          <img :src="book.cover_image || defaultCover" alt="Cover Image" class="book-image" />
          <div class="book-title">{{ book.title }}</div>
          <div class="button-row">
            <button class="btn edit-btn" @click="editBook">Edit</button>
            <button class="btn delete-btn" @click="openDeleteModal(book)">Delete</button>
          </div>
          <div class="info-box status-box" :class="book.borrowed ? 'bg-red' : 'bg-green'">
            <strong>Status:</strong> {{ book.borrowed ? 'Taken' : 'Available' }}
          </div>
          <div class="info-box info-small-box bg-orangeish">
            <strong>Borrow Count:</strong> {{ book.borrow_count || 0 }}
          </div>

          <div v-if="book.borrowed" class="penalty-row borrowed-row">
            <button class="btn extend-btn" @click="openExtendModal(book.id)">Extend</button>
            <button class="btn delete-btn" @click="adminReturnBook(book.id)">Return</button>
          </div>
        </div>

        <div class="right-box">
          <p><strong>Author: </strong> {{ book.authors?.join(', ') }}</p>
          <p><strong>Publisher: </strong> {{ book.publisher }}</p>
          <p><strong>Categories: </strong>
            <span v-if="book.categories?.length">
              {{book.categories.map(c => c.subcategory ? `${c.category} / ${c.subcategory}` : c.category).join(', ')}}
            </span>
            <span v-else>Not specified</span>
          </p>
          <p><strong>Language: </strong> {{ book.language }}</p>
          <p><strong>Page Count: </strong> {{ book.page_count }}</p>
          <p><strong>ISBN: </strong> {{ book.isbn }}</p>
          <p><strong>Added At: </strong> {{ formatDate(book.added_at) }}</p>

          <p v-if="notifyUsers.length">
            <strong>Waiting Users: </strong>
            <span>
              <template v-for="(user, index) in notifyUsers" :key="user.id">
                <router-link :to="`/admin/users/${user.id}`" class="user-link">
                  {{ user.username }}
                </router-link>
                <span v-if="index < notifyUsers.length - 1">, </span>
              </template>
            </span>
          </p>

          <p><strong>Last Borrowed By: </strong>
            <router-link v-if="book.last_borrowed_by && lastBorrowerUsername"
              :to="`/admin/users/${book.last_borrowed_by}`" class="user-link">
              {{ lastBorrowerUsername }}
            </router-link>
            <span v-else>-</span>
          </p>

          <p><strong>Currently Borrowed By: </strong>
            <router-link v-if="book.currently_borrowed_by && currentBorrowerUsername"
              :to="`/admin/users/${book.currently_borrowed_by}`" class="user-link">
              {{ currentBorrowerUsername }}
            </router-link>
            <span v-else>-</span>
          </p>

          <div class="penalty-row penalty-actions" v-if="book.has_penalty">
            <div class="info-box info-small-box bg-red">
              <strong>Penalty:</strong> Yes
            </div>
            <button class="btn warning" @click="notifyPenaltyUsers">Notify User</button>
          </div>
        </div>
      </div>

      <div class="desc-box" v-if="book">
        <h3>Description</h3>
        <p v-html="book.description || 'No description available.'"></p>
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
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '@/api/axios'
import defaultCover from '@/assets/images/default-cover.png'
import { formatDate } from '@/utils/date'
import { useToast } from 'vue-toastification'

const route = useRoute()
const router = useRouter()
const toast = useToast()

const book = ref(null)
const showModal = ref(false)
const bookToDelete = ref(null)

const lastBorrowerUsername = ref('')
const currentBorrowerUsername = ref('')
const notifyUsers = ref([])

const showExtendModal = ref(false)
const extraDays = ref(7)
const selectedBookId = ref(null)

function openDeleteModal(book) {
  bookToDelete.value = book
  showModal.value = true
}

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
    const res = await api.get(`/books/${route.params.id}`)
    book.value = { id: res.data.book._id, ...res.data.book }
  } catch (error) {
    toast.error('Failed to extend return date')
  }
}

const adminReturnBook = async (bookId) => {
  try {
    await api.post(`/admin/borrowed-books/return/${bookId}`)
    toast.success('Book returned successfully')
    const res = await api.get(`/books/${route.params.id}`)
    book.value = { id: res.data.book._id, ...res.data.book }
  } catch (error) {
    toast.error('Failed to return book')
  }
}

async function deleteBook(id) {
  try {
    const res = await api.delete(`/admin/book/${id}`)
    toast.success(res.data.message || "Book deleted successfully.")
    router.push('/admin/books')
  } catch (err) {
    console.error("Delete error:", err)
    toast.error("Failed to delete the book.")
  } finally {
    showModal.value = false
  }
}

function editBook() {
  if (book.value?.id) {
    router.push(`/admin/edit-book/${book.value.id}`)
  } else {
    toast.warning("Book ID is not available.")
  }
}

async function notifyPenaltyUsers() {
  try {
    const userId = book.value.currently_borrowed_by
    const bookId = book.value.id

    if (!userId || !bookId) {
      toast.warning("Book or user ID is missing.")
      return
    }

    const { data } = await api.post(`/admin/notify/${userId}/book/${bookId}`)
    if (data.code === "Success") {
      toast.success(data.message)
    }
  } catch (error) {
    const msg = error?.response?.data?.message || "Failed to notify user."
    toast.error(msg)
  }
}

onMounted(async () => {
  const res = await api.get(`/books/${route.params.id}`)
  book.value = {
    id: res.data.book._id,
    ...res.data.book
  }

  if (book.value.last_borrowed_by) {
    try {
      const resUser = await api.get(`/admin/users/${book.value.last_borrowed_by}`)
      lastBorrowerUsername.value =
        resUser.data.user?.username || resUser.data.admin?.username || '(Unknown)'
    } catch {
      lastBorrowerUsername.value = '(Error)'
    }
  }

  if (book.value.currently_borrowed_by) {
    try {
      const resUser = await api.get(`/admin/users/${book.value.currently_borrowed_by}`)
      currentBorrowerUsername.value =
        resUser.data.user?.username || resUser.data.admin?.username || '(Unknown)'
    } catch {
      currentBorrowerUsername.value = '(Error)'
    }
  }

  const list = book.value.notify_me_list || []
  for (const userId of list) {
    try {
      const resUser = await api.get(`/admin/users/${userId}`)
      notifyUsers.value.push({
        id: userId,
        username: resUser.data.user?.username || resUser.data.admin?.username || '(Unknown)'
      })
    } catch {
      notifyUsers.value.push({ id: userId, username: '(Error)' })
    }
  }
})
</script>

<style scoped>
.content-wrapper {
  color: white;
  min-height: 100vh;
  padding-top: 40px;
  padding-bottom: 100px;
}

main {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

.book-flexbox {
  display: flex;
  flex-direction: column;
  gap: 2rem;
  margin-bottom: 2rem;
}

@media (min-width: 768px) {
  .book-flexbox {
    flex-direction: row;
    align-items: stretch;
  }
}

.left-box,
.right-box,
.desc-box {
  background-color: #dddddddc;
  border-radius: 10px;
}

.left-box {
  flex: 1;
  padding: 1rem;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.right-box {
  flex: 2;
  padding: 2rem;
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
  font-size: 1.1rem;
}

.desc-box {
  margin-top: 2rem;
  padding: 2rem;
}

.book-title {
  font-size: 1.4rem;
  font-weight: bold;
  text-align: center;
  margin-top: 1rem;
}

.book-image {
  width: 240px;
  height: 360px;
  object-fit: cover;
  border-radius: 6px;
}

.book-cover {
  width: 200px;
  height: auto;
  margin-bottom: 1rem;
}

.right-box p {
  font-size: 1.15rem;
  margin-bottom: 0.8rem;
}

.right-box p strong {
  font-size: 1.2rem;
  font-weight: 700;
}

.desc-box p {
  font-size: 1.05rem;
  line-height: 1.8;
  white-space: pre-line;
}

.left-box *,
.right-box *,
.desc-box * {
  color: #000 !important;
}

.btn {
  margin: 0.5rem;
  padding: 0.65rem 1.2rem;
  font-size: 1rem;
  font-weight: 500;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  display: inline-block;
  text-align: center;
  transition: background-color 0.2s ease;
  box-shadow: 0 3px 6px rgba(0, 0, 0, 0.1);
  color: white;
}

.btn:hover {
  opacity: 0.9;
}

.edit-btn {
  background-color: #44adf7;
  color: #2980b9;
  border: 1px solid #1a8ad4ce;
}

.edit-btn:hover {
  background-color: #2f78b8bc;
}

.extend-btn {
  background-color: #f7ac44;
  color: #f7ac44;
  border: 1px solid #e98c09d7;
}

.extend-btn:hover {
  background-color: #2f78b8bc;
}


.delete-btn {
  background-color: #dc1c1cd0;
  color: #c0392b;
  border: 1px solid #c0392b;
}

.delete-btn:hover {
  background-color: #b21f1fc4;
}

.primary {
  background-color: #2980b9;
}

.danger {
  background-color: #d24242;
}

.warning {
  background-color: #f39c12;
}

.primary:hover {
  background-color: #216a94;
}

.danger:hover {
  background-color: #bb3c2e;
}

.warning:hover {
  background-color: #d68910;
}

.info-box,
.info-small-box {
  padding: 0.75rem 1rem;
  border-radius: 8px;
  font-size: 0.9rem;
  font-weight: 500;
  margin-bottom: 0.5rem;
  color: white;
}

.status-box {
  display: inline-block;
  padding: 0.4rem 0.8rem;
  border-radius: 6px;
  min-width: 140px;
  margin-top: 0.25rem;
  width: fit-content;
}

/* Colors */
.bg-green {
  background-color: #e6f4ea;
  color: #276749;
  border-color: #c6e6c3;
}

.bg-red {
  background-color: #ff2727a5;
  color: #bb2323;
  border-color: #d90016f9;
}

.bg-orangeish {
  background-color: #f5c150;
  color: #e2ad3b;
  border-color: #c89526ce;
}

.button-row,
.borrowed-action-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 12px;
  justify-content: center;
}

.penalty-row,
.borrowed-actions {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-top: 0.5rem;
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
  font-size: 20px;
  color: #000;
}

.confirm-modal p {
  color: #555;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.confirm-btn,
.cancel-btn {
  padding: 8px 16px;
  border-radius: 6px;
  border: none;
  cursor: pointer;
}

.confirm-btn {
  background: #c0392b;
  color: #fff;
}

.cancel-btn {
  background: #bdc3c7;
  color: #333;
}

.days-input {
  width: 100%;
  padding: 10px;
  margin: 12px 0;
  border-radius: 6px;
  border: 1px solid #ccc;
  font-size: 16px;
}

.user-link {
  color: #2980b9 !important;
  text-decoration: none;
}

.user-link:hover {
  text-decoration: underline !important;
}

.penalty-row.penalty-actions {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-top: 0.5rem;
}

.info-box.info-small-box {
  margin: 0;
  display: flex;
  align-items: center;
}
</style>
