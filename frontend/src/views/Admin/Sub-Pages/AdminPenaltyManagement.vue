<template>
  <div class="admin-users-container">
    <h2 class="mb-4">User Penalty Management</h2>

    <input v-model="searchQuery" @keyup.enter="onSearchEnter" class="search-input"
      placeholder="Search by username or email..." />


    <div class="toggle-wrapper">
      <label class="toggle-switch">
        <input type="checkbox" v-model="onlyWithPenalties" @change="onSearchEnter" />
        <span class="slider"></span>
      </label>
      <span class="toggle-label">Show only users with penalties</span>
    </div>

    <div v-if="users.length > 0" class="user-table-wrapper">
      <table class="user-table">
        <thead>
          <tr>
            <th>Username</th>
            <th>E-mail</th>
            <th>Borrow Count</th>
            <th>Penalty Fee</th>
            <th>Notify User</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(user, index) in users" :key="user.id" class="fade-in-row" :style="{ animationDelay: `${index * 80}ms` }">
            <td>
              <router-link :to="`/admin/users/${user.id}`" class="user-link">
                {{ user.username }}
              </router-link>
            </td>
            <td>{{ user.email }}</td>
            <td>{{ user.borrow_count }}</td>
            <td>₺{{ user.penalty_fee?.toFixed(2) || '0.00' }}</td>
            <td>
              <button class="notify-btn" @click="notifyUser(user.id)">
                Notify
              </button>
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
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/api/axios'
import { useToast } from 'vue-toastification'

const toast = useToast()

const users = ref([])
const searchQuery = ref('')
const page = ref(1)
const limit = 10
const lastPage = ref(1)
const onlyWithPenalties = ref(false)


const selectedUserId = ref(null)
const showModal = ref(false)

const fetchUsers = async () => {
  try {
    const response = await api.get('/admin/users', {
      params: {
        page: page.value,
        limit,
        q: searchQuery.value || undefined,
        only_with_penalties: onlyWithPenalties.value || undefined
      }
    })
    users.value = response.data.users
    lastPage.value = response.data.last_page || 1
  } catch (error) {
    const msg = error?.response?.data?.message || "Failed to fetch users."
    toast.error(msg)
    users.value = []
  }
}

onMounted(fetchUsers)

const onSearchEnter = () => {
  page.value = 1
  fetchUsers()
}

const changePage = (newPage) => {
  page.value = newPage
  fetchUsers()
}

const notifyUser = async (userId) => {
  const user = users.value.find(u => u.id === userId)
  if (!user) {
    toast.error("User not found in the list.")
    return
  }

  if (!user.penalty_fee || user.penalty_fee === 0) {
    toast.warning("User has no penalty fee to notify.")
    return
  }

  try {
    const { data } = await api.post(`/admin/notify/${userId}`)
    if (data.code === "Success") {
      toast.success(data.message)
    }
  } catch (error) {
    const msg = error?.response?.data?.message || "Failed to notify user."
    toast.error(msg)
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
    }
  } catch (error) {
    const msg = error?.response?.data?.message || "Failed to ban user."
    toast.error(msg)
  }
}

const unbanUser = async (userId) => {
  try {
    const { data } = await api.post(`/admin/unban/${userId}`)
    if (data.code === "Success") {
      toast.success(data.message)
      fetchUsers()
    }
  } catch (error) {
    const msg = error?.response?.data?.message || "Failed to unban user."
    toast.error(msg)
  }
}
</script>

<style scoped>
.admin-users-container {
  padding: 24px;
}

.search-input {
  width: 100%;
  padding: 10px;
  margin-bottom: 16px;
  border-radius: 6px;
  border: 1px solid #ccc;
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

.unban-btn {
  padding: 6px 12px;
  background-color: #27ae60;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.notify-btn {
  padding: 6px 12px;
  background-color: #f39c12;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.user-link {
  color: #2980b9;
  text-decoration: none;
}

.user-link:hover {
  text-decoration: underline;
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

.toggle-wrapper {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 16px;
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
