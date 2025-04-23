<template>
  <div class="admin-users-container">
    <h2 class="mb-4">User List</h2>

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
          <tr v-for="user in users" :key="user.id">
            <td>{{ user.username }}</td>
            <td>{{ user.email }}</td>
            <td>{{ user.borrow_count }}</td>
            <td>
              <span :class="user.has_penalty ? 'penalty' : 'no-penalty'">
                {{ user.has_penalty ? 'Has Penalty' : 'No Penalty' }}
              </span>
            </td>
            <td>
              <button class="ban-btn" @click="banUser(user.id)">Ban the User</button>
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

const users = ref([])
const page = ref(1)
const limit = 10
const lastPage = ref(1)

const fetchUsers = async () => {
  try {
    const response = await api.get('/admin/users', {
      params: {
        page: page.value,
        limit
      }
    })
    users.value = response.data.users
    lastPage.value = response.data.last_page || 1
  } catch (err) {
    console.error('Failed to fetch users:', err)
    users.value = []
  }
}

const changePage = (newPage) => {
  page.value = newPage
  fetchUsers()
}

const banUser = (userId) => {
  console.log(`User with ID: ${userId} is banned.`)
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
</style>