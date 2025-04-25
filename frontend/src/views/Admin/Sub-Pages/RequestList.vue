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
            <th>Author</th>
            <th>Publisher</th>
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
            <td>
              <router-link :to="`/admin/requests/${book.id}`" class="book-link">
                {{ book.title }}
              </router-link>
            </td>
            <td class="ellipsis">{{ book.authors?.join(', ') || 'Unknown' }}</td>
            <td class="ellipsis">{{ book.publisher || 'Unknown' }}</td>
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

    <button v-if="changedBooks.length" class="apply-btn" @click="applyChanges">Apply Changes</button>
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

const changedBooks = computed(() => requests.value.filter(b => b.changed))

const fetchRequests = async () => {
  try {
    const { data } = await api.get('/admin/requested-books', {
      params: {
        page: 1,
        limit: 100,
        q: searchQuery.value || undefined
      }
    })
    requests.value = data.requests.map(req => ({
      ...req,
      newStatus: req.status,
      changed: false
    }))
  } catch (err) {
    toast.error('Failed to fetch requests')
  }
}

const onSearchEnter = () => {
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

.apply-btn {
  position: fixed;
  bottom: 32px;
  right: 32px;
  background-color: #2ecc71;
  color: white;
  border: none;
  padding: 18px 36px;
  font-size: 24px;
  font-weight: 600;
  border-radius: 12px;
  cursor: pointer;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3);
  transition: all 0.2s ease;
  z-index: 1000;
}

.apply-btn:hover {
  background-color: #27ae60;
  transform: scale(1.07);
}

.search-input {
  width: 100%;
  padding: 10px;
  margin-bottom: 16px;
  border-radius: 6px;
  border: 1px solid #ccc;
}

.book-link {
  color: #2980b9;
  text-decoration: none;
  font-weight: 500;
}

.book-link:hover {
  text-decoration: underline;
}
</style>