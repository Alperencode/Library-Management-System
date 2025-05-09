<template>
  <div class="request-list-container">
    <h2 class="mb-4">Requested Books</h2>

    <input v-model="searchQuery" @keyup.enter="onSearchEnter" class="search-input"
      placeholder="Search by title or ISBN..." />

    <div v-if="requests.length > 0" class="request-table-wrapper">
      <table class="request-table">
        <thead>
          <tr>
            <th>Cover</th>
            <th>Title</th>
            <th>Status</th>
            <th>Change Status</th>
            <th>Requested At</th>
            <th>Status Updated</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(book, index) in requests" :key="book.id" class="fade-in-row"
            :style="{ animationDelay: `${index * 80}ms` }">
            <td><img :src="book.cover_image || defaultCover" class="book-cover" /></td>
            <td class="truncate-title">
              <router-link :to="`/admin/requests/${book.id}`" class="book-link" :title="book.title">
                {{ book.title }}
              </router-link>
            </td>
            <td>
              <span :class="['status-label', statusColor(book.status)]">
                {{ book.status }}
              </span>
            </td>
            <td>
              <select v-model="book.newStatus" @change="markChanged(book)">
                <option value="Request Sent">Request Sent</option>
                <option value="Approved">Approved</option>
                <option value="Denied">Denied</option>
                <option value="Added">Added</option>
                <option value="On Hold">On Hold</option>
              </select>
            </td>
            <td>{{ formatDateWithoutTime(book.requested_at) }}</td>
            <td>{{ formatDateWithoutTime(book.status_updated_at) }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-else class="no-requests">No requested books found.</div>

    <div class="pagination" v-if="lastPage > 1">
      <button :disabled="page === 1" @click="changePage(page - 1)">‹</button>
      <button v-for="p in lastPage" :key="p" @click="changePage(p)" :class="{ active: p === page }">
        {{ p }}
      </button>
      <button :disabled="page === lastPage" @click="changePage(page + 1)">›</button>
    </div>

    <div class="apply-discard-buttons" v-if="changedBooks.length">
      <button class="discard-btn" @click="showDiscardModal = true">Discard</button>
      <button class="apply-btn" @click="showApplyModal = true">Apply Changes</button>
    </div>

    <div v-if="showDiscardModal" class="modal-overlay">
      <div class="confirm-modal">
        <h3>Discard All Changes?</h3>
        <p>Are you sure you want to discard changes?</p>
        <div class="modal-actions">
          <button class="confirm-btn" @click="discardChanges">Yes, Discard</button>
          <button class="cancel-btn" @click="showDiscardModal = false">Cancel</button>
        </div>
      </div>
    </div>

    <div v-if="showApplyModal" class="modal-overlay">
      <div class="confirm-modal">
        <h3>Apply All Changes?</h3>
        <p>
          Are you sure you want to apply the changes? <br />
          &ensp; • "Added" books will be included in the catalog and moved to Added tab. <br />
          &ensp; • "Denied" requests will be moved to Denied tab. <br />
          You can later delete denied requests from there.
        </p>
        <div class="modal-actions">
          <button class="confirm-btn" @click="confirmApplyChanges">Yes, Apply</button>
          <button class="cancel-btn" @click="showApplyModal = false">Cancel</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import defaultCover from '@/assets/images/default-cover.png'
import api from '@/api/axios'
import { useToast } from 'vue-toastification'
import { formatDateWithoutTime } from "@/utils/date"


const toast = useToast()
const requests = ref([])
const searchQuery = ref('')
const page = ref(1)
const limit = 10
const lastPage = ref(1)

const statusColor = (status) => {
  switch (status) {
    case 'Approved':
      return 'status-blue'
    case 'Denied':
      return 'status-red'
    case 'Added':
      return 'status-green'
    case 'On Hold':
      return 'status-orange'
    case 'Request Sent':
    default:
      return 'status-gray'
  }
}

const markChanged = (book) => {
  book.changed = book.status !== book.newStatus
}

const showDiscardModal = ref(false)
const showApplyModal = ref(false)

const discardChanges = () => {
  showDiscardModal.value = false
  fetchRequests()
  toast.info('Changes discarded')
}

const confirmApplyChanges = async () => {
  showApplyModal.value = false
  await applyChanges()
}

const changedBooks = computed(() => requests.value.filter(b => b.changed))

const fetchRequests = async () => {
  try {
    const { data } = await api.get('/admin/requested-books', {
      params: {
        page: page.value,
        limit,
        q: searchQuery.value || undefined
      }
    })
    requests.value = data.requests.map(req => ({
      ...req,
      newStatus: req.status,
      changed: false
    }))
    lastPage.value = data.last_page || 1
  } catch (err) {
    toast.error('Failed to fetch requests')
  }
}

const onSearchEnter = () => {
  page.value = 1
  fetchRequests()
}

const changePage = (newPage) => {
  page.value = newPage
  fetchRequests()
}

const applyChanges = async () => {
  for (const book of changedBooks.value) {
    try {
      if (book.newStatus === 'Added') {
        await api.post('/admin/add-book', {
          request_id: book.id
        })
      } else {
        await api.patch(`/admin/requested-books/${book.id}`, {
          status: book.newStatus
        })
      }
      toast.success(`Updated: ${book.title}`)
    } catch (err) {
      toast.error(`Failed to update: ${book.title}`)
    }
  }

  await fetchRequests()
}

onMounted(fetchRequests)
</script>

<style scoped>
.request-list-container {
  padding: 24px;
  position: relative;
}

.request-table-wrapper {
  overflow-x: auto;
  margin-top: 16px;
}

.request-table {
  width: 100%;
  border-collapse: collapse;
}

.request-table th,
.request-table td {
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

.status-label {
  padding: 4px 10px;
  border-radius: 6px;
  font-size: 13px;
  font-weight: 500;
}

.status-red {
  background-color: #ffe0e0;
  color: #c0392b;
}

.status-blue {
  background-color: #e0ecff;
  color: #2980b9;
}

.status-green {
  background-color: #e0f8e0;
  color: #27ae60;
}

.status-gray {
  background-color: #f0f0f0;
  color: #555;
}

.status-orange {
  background-color: #f39c12;
  color: #fff;
}

.no-requests {
  text-align: center;
  margin-top: 40px;
  font-style: italic;
}

.fade-in-row {
  animation: fadeUp 0.4s ease-out both;
}

@keyframes fadeUp {
  0% {
    opacity: 0;
    transform: translateY(15px);
  }

  100% {
    opacity: 1;
    transform: translateY(0);
  }
}

select {
  padding: 6px;
  border-radius: 4px;
  background-color: #f7f7f7;
  border: 1px solid #ccc;
}

.search-input {
  width: 100%;
  padding: 10px;
  margin-bottom: 16px;
  border-radius: 6px;
  border: 1px solid #ccc;
}


.book-link:hover {
  text-decoration: underline;
}

.apply-discard-buttons {
  position: fixed;
  bottom: 32px;
  right: 32px;
  display: flex;
  gap: 12px;
  z-index: 1000;
}

.apply-btn,
.discard-btn {
  padding: 18px 36px;
  font-size: 20px;
  font-weight: 600;
  border: none;
  border-radius: 12px;
  color: white;
  cursor: pointer;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3);
  transition: transform 0.2s ease;
}

.apply-btn {
  background-color: #2ecc71;
}

.apply-btn:hover {
  background-color: #27ae60;
  transform: scale(1.07);
}

.discard-btn {
  background-color: #e74c3c;
}

.discard-btn:hover {
  background-color: #c0392b;
  transform: scale(1.07);
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
  max-width: 600px;
  box-shadow: 0 5px 30px rgba(0, 0, 0, 0.2);
}

.confirm-modal h3 {
  margin: 0 0 15px;
  font-size: 20px;
}

.confirm-modal p {
  margin: 0 0 20px;
  color: #555;
  font-size: 15px;
  line-height: 1.4;
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


.truncate-title {
  max-width: 200px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.book-link {
  display: inline-block;
  max-width: 100%;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  color: #2980b9;
  text-decoration: none;
  font-weight: 500;
  vertical-align: middle;
}

.book-link:hover {
  text-decoration: underline;
}

.ellipsis {
  max-width: 160px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
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
</style>