<template>
  <div class="admin-users-container">
    <h2 class="mb-4">User List</h2>

    <input v-model="searchQuery" @keyup.enter="onSearchEnter" class="search-input"
      placeholder="Search by username or email..." />

    <div v-if="users.length > 0" class="user-table-wrapper">
      <table class="user-table">
        <thead>
          <tr>
            <th>Username</th>
            <th>E-mail</th>
            <th>Borrow Count</th>
            <th>Penalty Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(user, index) in users" :key="user.id" class="fade-in-row"
            :style="{ animationDelay: `${index * 80}ms` }">
            <td>
              <router-link :to="`/admin/users/${user.id}`" class="user-link">
                {{ user.username }}
              </router-link>
            </td>
            <td>{{ user.email }}</td>
            <td>{{ user.borrow_count }}</td>
            <td>
              <span :class="user.has_penalty ? 'penalty' : 'no-penalty'">
                {{ user.has_penalty ? 'Has Penalty' : 'No Penalty' }}
              </span>
            </td>
            <td>
              <button v-if="!user.banned" class="ban-btn" @click="banUser(user.id)">
                Ban User
              </button>

              <button v-else class="unban-btn" @click="unbanUser(user.id)">
                Un-ban User
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-else class="no-users">No users found.</div>

    <div class="pagination">
      <button :disabled="page === 1" @click="changePage(page - 1)">‹</button>
      <button v-for="p in lastPage" :key="p" @click="changePage(p)" :class="{ active: p === page }">
        {{ p }}
      </button>
      <button :disabled="page === lastPage" @click="changePage(page + 1)">›</button>
    </div>

    <div v-if="showModal" class="modal-overlay">
      <div class="confirm-modal">
        <h3>Force Ban User?</h3>
        <p>
          This user has active borrowed books. Hard banning will remove their books
          from the library system. Are you sure you want to continue?
        </p>

        <div class="modal-actions">
          <button class="details-btn" @click="viewUserBooks">View User’s Books</button>
          <button class="confirm-btn" @click="hardBanUser">Yes, Hard Ban</button>
          <button class="cancel-btn" @click="showModal = false">Cancel</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { ref, onMounted } from 'vue'
import api from '@/api/axios'
import { useToast } from 'vue-toastification'

const toast = useToast()
const router = useRouter()

const showModal = ref(false)
const selectedUserId = ref(null)

const users = ref([])
const searchQuery = ref('')
const page = ref(1)
const limit = 10
const lastPage = ref(1)

const fetchUsers = async () => {
  try {
    const response = await api.get('/admin/users', {
      params: {
        page: page.value,
        limit,
        q: searchQuery.value || undefined
      }
    })
    users.value = response.data.users
    lastPage.value = response.data.last_page || 1
  } catch (err) {
    console.error('Failed to fetch users:', err)
    users.value = []
  }
}

const onSearchEnter = () => {
  page.value = 1
  fetchUsers()
}

const changePage = (newPage) => {
  page.value = newPage
  fetchUsers()
}

const viewUserBooks = () => {
  if (selectedUserId.value) {
    router.push(`/admin/users/${selectedUserId.value}`)
    showModal.value = false
  }
}

const banUser = async (userId) => {
  try {
    const { data } = await api.post(`/admin/ban/${userId}`)

    if (data.code === "Success") {
      toast.success(data.message)
      fetchUsers()
    } else if (data.code === "NeedAction") {
      selectedUserId.value = userId
      showModal.value = true
    } else {
      toast.error(data.message || "Unexpected response")
    }
  } catch (err) {
    toast.error(err.response?.data?.message || "Failed to ban user")
  }
}

const hardBanUser = async () => {
  try {
    const response = await api.post(`/admin/hard-ban/${selectedUserId.value}`)
    if (response.data.code === "Success") {
      toast.success(response.data.message)
      showModal.value = false
      fetchUsers()
    }
  } catch (err) {
    toast.error(err.response?.data?.message || "Failed to hard-ban user")
  }
}

const unbanUser = async (userId) => {
  try {
    const { data } = await api.post(`/admin/unban/${userId}`)
    if (data.code === "Success") {
      toast.success(data.message)
      fetchUsers()
    } else {
      toast.error(data.message || "Unexpected response")
    }
  } catch (err) {
    toast.error(err.response?.data?.message || "Failed to un-ban user")
  }
}

onMounted(fetchUsers)
</script>

<style scoped>
.admin-users-container {
  padding: 24px;
}

.user-table-wrapper {
  margin-top: 16px;
}

.user-table {
  width: 100%;
  border-collapse: collapse;
}

.user-table th,
.user-table td {
  padding: 12px;
  border-bottom: 1px solid #eee;
  text-align: left;
}

.ban-btn {
  padding: 6px 12px;
  background-color: #e74c3c;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.penalty {
  color: red;
  font-weight: bold;
}

.no-penalty {
  color: green;
  font-weight: normal;
}

.no-users {
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

.details-btn {
  padding: 8px 16px;
  background: #2980b9;
  color: #fff;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}

.unban-btn {
  padding: 6px 12px;
  background: #27ae60;
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.user-link {
  text-decoration: none;
  color: #2980b9;
}

.user-link:hover {
  text-decoration: underline;
}

.search-input {
  width: 100%;
  padding: 10px;
  margin-bottom: 16px;
  border-radius: 6px;
  border: 1px solid #ccc;
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