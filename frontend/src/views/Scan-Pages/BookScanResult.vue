<template>
  <div class="content-wrapper">
    <main>
      <div v-if="book" class="book-flexbox">
        <div class="left-box">
          <img :src="book.cover_image || defaultCover" alt="Cover Image" class="book-image" />
          <div class="book-title">{{ book.title }}</div>
          <div class="book-buttons">
            <button v-if="showReturnButton" @click="returnBook" class="btn" :disabled="actionBlocked">
              Return
            </button>

            <button v-if="showExtendButton" @click="extendReturn" class="btn" :disabled="actionBlocked">
              Extend
            </button>

            <button v-else-if="showNotifyButton" @click="notifyMe" class="btn" :disabled="isAlreadyInNotifyList">
              {{ isAlreadyInNotifyList ? 'Already in Notify List' : 'Notify Me' }}
            </button>

            <button v-else-if="showBorrowButton" @click="borrowBook" class="btn">Borrow</button>
          </div>
        </div>

        <div class="right-box">
          <p><strong>Author:</strong> {{ book.authors?.join(', ') }}</p>
          <p><strong>Publisher:</strong> {{ book.publisher }}</p>
          <p><strong>Category: </strong>
            <span v-if="book.categories?.length">
              {{ book.categories[0]?.category }} / {{ book.categories[0]?.subcategory }}
            </span>
            <span v-else>Not specified</span>
          </p>
          <p><strong>Language:</strong> {{ book.language }}</p>
          <p><strong>Page Count:</strong> {{ book.page_count }}</p>
          <p><strong>ISBN:</strong> {{ book.isbn }}</p>
          <div v-if="isMine" class="info-box info-small-box bg-redish">
            <strong>Penalty:</strong> {{ penaltyAmount }} ₺
          </div>

          <div v-else class="info-box status-box" :class="book.borrowed ? 'bg-red' : 'bg-green'">
            <strong>Status:</strong> {{ book.borrowed ? 'Taken' : 'Available' }}
          </div>

          <div class="info-box info-small-box bg-redish">
            <strong>Borrow Count:</strong> {{ book.borrow_count || 0 }}
          </div>

          <div v-if="book.borrowed && book.return_date" class="info-box info-small-box bg-blue">
            <strong>Return Date:</strong> {{ formatDate(book.return_date) }}
          </div>
          <div v-if="penaltyAmount > 0" class="info-box info-small-box"
            style="background-color: #b91c1c; color: white; margin-top: 0.5rem;">
            <strong>Warning:</strong> You have exceeded the return date,
            please contact the library staff to return it.
          </div>
        </div>
      </div>
      <div class="desc-box" v-if="book">
        <h3>Description</h3>
        <p v-html="book.description || 'No description available.'"></p>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '@/api/axios'
import defaultCover from '@/assets/images/default-cover.png'
import { formatDate } from "@/utils/date"
import { useToast } from 'vue-toastification'

const router = useRouter()
const route = useRoute()
const toast = useToast()

const user = ref(null)
const savedUser = localStorage.getItem("user")
if (savedUser) user.value = JSON.parse(savedUser)

const book = ref(null)
const actionBlocked = ref(false)

const isMine = computed(() => book.value?.currently_borrowed_by === user.value?.id)
const isBorrowedByAnother = computed(() =>
  book.value?.borrowed && book.value.currently_borrowed_by && book.value.currently_borrowed_by !== user.value.id
)

const isAlreadyInNotifyList = computed(() =>
  Array.isArray(book.value?.notify_me_list) &&
  book.value.notify_me_list.includes(user.value.id)
)

const showReturnButton = computed(() => isMine.value)
const showExtendButton = computed(() => isMine.value)
const showNotifyButton = computed(() => isBorrowedByAnother.value)
const showBorrowButton = computed(() => book.value && !book.value.borrowed)

onMounted(async () => {
  try {
    const res = await api.get(`/scan-book/${route.params.id}`)
    book.value = res.data.book
  } catch {
    router.push("/")
  }
})

async function borrowBook() {
  if (!book.value?._id) return
  try {
    const res = await api.post(`/borrow/${book.value._id}`)
    toast.success(res.data.message)
    setTimeout(() => router.push("/"), 1000)
  } catch (err) {
    console.error(err)
  }
}

async function extendReturn() {
  try {
    const res = await api.post(`/extend-return/${book.value._id}`)
    toast.success(res.data.message)
    setTimeout(() => router.push("/"), 1000)
  } catch (err) {
    if (err.response?.data?.message?.includes("penalty")) {
      actionBlocked.value = true
    }
  }
}

async function returnBook() {
  try {
    const res = await api.post(`/return/${book.value._id}`)
    toast.success(res.data.message)
    setTimeout(() => router.push("/"), 1000)
  } catch (err) {
    if (err.response?.data?.message?.includes("penalty")) {
      actionBlocked.value = true
    }
  }
}

async function notifyMe() {
  if (!book.value?._id) {
    toast.error('Book ID is not available')
    return
  }
  try {
    const res = await api.post(`/notify-me/${book.value._id}`)
    toast.success(res.data.message)
    book.value.notify_me_list = book.value.notify_me_list || []
    book.value.notify_me_list.push(user.value.id)
  } catch (err) {
    console.error("Notification failed:", err)
  }
}
</script>

<style scoped>
.content-wrapper {
  color: white;
  min-height: 100vh;
  padding-top: 150px;
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
  }
}

.left-box {
  flex: 1;
  background-color: #ffffffdc;
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
  background-color: #ffffffdc;
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
  background-color: #ffffffdc;
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

.bg-blue {
  background-color: #189fd0;
}

.bg-redish {
  background-color: #e35521;
}

.book-image {
  width: 180px;
  height: 270px;
}

.button-row {
  display: flex;
  flex-wrap: wrap;
  gap: 0.6rem;
  margin-top: 1.5rem;
  justify-content: center;
}

.btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-size: 1.1rem;
  font-weight: 600;
  letter-spacing: 0.5px;
  cursor: pointer;
  color: white;
  transition: all 0.2s ease-in-out;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.btn:hover {
  transform: scale(1.05);
  opacity: 0.9;
}

.btn.blue {
  background-color: #d48d29;
}

.btn.blue:hover {
  background-color: #d48d29;
}

.btn.yellow {
  background-color: #eab308;
  color: black;
}

.btn.yellow:hover {
  background-color: #ca8a04;
}

.btn.green {
  background-color: #d48d29;
}

.btn.green:hover {
  background-color: #d48d29;
}

.btn.gray {
  background-color: #6b7280;
}

.btn.gray:hover {
  background-color: #4b5563;
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
  text-align: center;
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
</style>