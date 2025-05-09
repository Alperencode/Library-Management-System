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

          <div class="penalty-row" v-if="book.has_penalty">
            <div class="info-box info-small-box bg-red">
              <strong>Penalty:</strong> Yes
            </div>
            <button class="btn warning bg-orangeish" @click="notifyPenaltyUsers">Notify User</button>
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

function openDeleteModal(book) {
  bookToDelete.value = book
  showModal.value = true
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

.left-box {
  flex: 1;
  background-color: #dddddddc;
  padding: 1rem;
  border-radius: 10px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.book-image {
  width: 240px;
  height: 360px;
  object-fit: cover;
  border-radius: 6px;
}

.book-title {
  font-size: 1.4rem;
  font-weight: bold;
  text-align: center;
  margin-top: 1rem;
}

.right-box {
  flex: 2;
  background-color: #dddddddc;
  border-radius: 10px;
  padding: 2rem;
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
  font-size: 1.1rem;
}

.right-box p {
  font-size: 1.15rem;
  margin-bottom: 0.8rem;
}

.right-box p strong {
  font-size: 1.2rem;
  font-weight: 700;
}

.desc-box {
  margin-top: 2rem;
  background-color: #dddddddc;
  padding: 2rem;
  border-radius: 10px;
}

.desc-box h3 {
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: 0.8rem;
}

.desc-box p {
  font-size: 1.05rem;
  line-height: 1.8;
  white-space: pre-line;
}

.text-red {
  color: #f87171;
}

.text-green {
  color: #4ade80;
}

.left-box,
.right-box,
.desc-box,
.left-box *,
.right-box *,
.desc-box * {
  color: #000000 !important;
}

.info-box {
  padding: 0.75rem 1rem;
  border-radius: 8px;
  color: white;
  font-size: 0.9rem;
  font-weight: 500;
  margin-bottom: 0.5rem;
}

.bg-green {
  background-color: #16a34a;
}

.bg-red {
  background-color: #dc2626;
}

.book-image {
  width: 180px;
  height: 270px;
}

.button-row {
  display: flex;
  flex-wrap: wrap;
  gap: 0.6rem;
  margin-top: 0.5rem;
  justify-content: center;
}

.btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 500;
  letter-spacing: 0.5px;
  cursor: pointer;
  color: white;
  transition: all 0.2s ease-in-out;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.status-box {
  display: inline-block;
  padding: 0.4rem 0.8rem;
  font-size: 1rem;
  border-radius: 6px;
  margin-top: 0.5rem;
  width: fit-content;
  min-width: 140px;
  text-align: left;
  margin-top: 0.25rem;
}

.info-small-box {
  display: inline-block;
  padding: 0.4rem 0.8rem;
  font-size: 1rem;
  border-radius: 6px;
  width: fit-content;
  min-width: 140px;
  text-align: left;
  margin-top: 0.25rem;
}

.book-details {
  padding: 1rem;
  max-width: 600px;
  margin: auto;
  text-align: center;
}

.book-cover {
  width: 200px;
  height: auto;
  margin-bottom: 1rem;
}

.book-buttons {
  margin-top: 1.5rem;
}

.btn {
  margin: 0.5rem;
  padding: 0.75rem 1.5rem;
  background-color: #f5a425;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.btn:hover {
  background-color: #e48c12;
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
  color: #000;
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

.user-link {
  color: #2980b9 !important;
  text-decoration: none;
}

.user-link:hover {
  text-decoration: underline !important;
}

.bg-green {
  background-color: #28a745;
}

.bg-red {
  background-color: #df2336;
}

.penalty-row {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-top: 0.5rem;
}

.notify-btn {
  padding: 8px 16px;
  background-color: #f39c12;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
  transition: background-color 0.2s ease;
}

.notify-btn:hover {
  background-color: #d68910;
}

.btn-blue {
  background-color: #2980b9;
  color: white;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 500;
  letter-spacing: 0.5px;
  cursor: pointer;
  display: inline-block;
  text-align: center;
  text-decoration: none;
  transition: background-color 0.2s ease-in-out;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.btn-blue:hover {
  background-color: #216a94;
}

.btn-red {
  background-color: #c0392b;
  color: white;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 500;
  letter-spacing: 0.5px;
  cursor: pointer;
  display: inline-block;
  text-align: center;
  text-decoration: none;
  transition: background-color 0.2s ease-in-out;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.btn-red:hover {
  background-color: #962d22;
}

.btn {
  padding: 0.65rem 1.2rem;
  font-size: 1rem;
  font-weight: 500;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  text-align: center;
  display: inline-block;
  transition: background-color 0.2s ease;
  box-shadow: 0 3px 6px rgba(0, 0, 0, 0.1);
}

/* Button Types */
.primary {
  background-color: #2980b9;
  color: white;
}

.primary:hover {
  background-color: #216a94;
}

.danger {
  background-color: #d24242;
  color: white;
}

.danger:hover {
  background-color: #bb3c2e;
}

.warning {
  background-color: #f39c12;
  color: white;
}

.warning:hover {
  background-color: #d68910;
}

.disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.button-row {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 12px;
  justify-content: center;
}

.info-box {
  padding: 0.5rem 0.8rem;
  border-radius: 6px;
  font-size: 0.95rem;
  font-weight: 500;
  background-color: #f5f5f5;
  color: #333;
  border: 1px solid #ccc;
  margin-top: 8px;
}

.bg-green {
  background-color: #e6f4ea;
  color: #276749;
  border-color: #c6e6c3;
}

.bg-red {
  background-color: #ec6d66;
  color: #c53030;
  border-color: #b92030be;
}

.bg-orangeish {
  background-color: #f5c150;
  color: #e2ad3b;
  border-color: #c89526ce;
}

.edit-btn {
  background-color: #44adf7;
  color: #2980b9;
  border: 1px solid #1a8ad4ce;
}

.edit-btn:hover {
  background-color: #2f78b8bc;
}

.delete-btn {
  background-color: #f82525bf;
  color: #c0392b;
  border: 1px solid #c0392b;
}

.delete-btn:hover {
  background-color: #b21f1fc4;
}
</style>
