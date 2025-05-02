<template>
  <div class="admin-users-container">
    <h2 class="mb-4">Banned User</h2>

    <input v-model="searchQuery" @keyup.enter="onSearchEnter" class="search-input"
      placeholder="Search banned user by username or email..." />

    <div v-if="bannedUsers.length > 0" class="user-table-wrapper">
      <table class="user-table">
        <thead>
          <tr>
            <th>Username</th>
            <th>E-mail</th>
            <th>Borrow Count</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in bannedUsers" :key="user.id">
            <td>
              <router-link :to="`/admin/users/${user.id}`" class="user-link">
                {{ user.username }}
              </router-link>
            </td>
            <td>{{ user.email }}</td>
            <td>{{ user.borrow_count }}</td>
            <td>
              <button class="unban-btn" @click="unbanUser(user.id)">
                Un-ban User
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-else class="no-users">No banned users found.</div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/api/axios'
import { useToast } from 'vue-toastification'

const toast = useToast()

const bannedUsers = ref([])
const searchQuery = ref('')

const fetchBannedUsers = async () => {
  try {
    const response = await api.get('/admin/users', {
      params: {
        page: 1,
        limit: 100,
        q: searchQuery.value || undefined
      }
    })
    bannedUsers.value = response.data.users.filter(user => user.banned)
  } catch (err) {
    bannedUsers.value = []
  }
}

const onSearchEnter = () => {
  fetchBannedUsers()
}

const unbanUser = async (userId) => {
    const { data } = await api.post(`/admin/unban/${userId}`)
    if (data.code === 'Success') {
      toast.success(data.message)
      fetchBannedUsers()
    }
}

onMounted(fetchBannedUsers)
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

.unban-btn {
  padding: 6px 12px;
  background-color: #27ae60;
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
</style>
