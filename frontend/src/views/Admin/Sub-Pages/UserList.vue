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
          <tr v-for="(user) in users" :key="user.id">
            <td>{{ user.username }}</td>
            <td>{{ user.email }}</td>
            <td>{{ user.borrow_count }}</td>
            <td>
              <span :class="user.penalty_status ? 'penalty' : 'no-penalty'">
                {{ user.penalty_status ? 'Penalty' : 'No Penalty' }}
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
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const users = ref([])

const exampleUsers = [
  { id: 1, username: 'user1', email: 'user1@example.com', borrow_count: 5, penalty_status: true },
  { id: 2, username: 'user2', email: 'user2@example.com', borrow_count: 2, penalty_status: false },
  { id: 3, username: 'user3', email: 'user3@example.com', borrow_count: 8, penalty_status: true },
  { id: 4, username: 'user4', email: 'user4@example.com', borrow_count: 1, penalty_status: false },
]

onMounted(() => {
  users.value = exampleUsers
})

const banUser = (userId) => {
  console.log(`User with ID: ${userId} is banned.`)
  // API call to fetch users
}
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

</style>
