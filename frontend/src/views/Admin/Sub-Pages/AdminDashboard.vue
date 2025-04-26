<template>
  <div class="admin-dashboard">
    <div class="admin-info-card" v-if="adminInfo">
      <p class="admin-welcome">Welcome, <strong>{{ adminInfo.username }}</strong>!</p>
    </div>

    <div class="quick-actions">
      <button @click="goToAddBook">Add New Book</button>
      <button @click="openAdminModal">Add Admin</button>
    </div>

    <div class="stats-container">
      <div class="stat-card">
        <h3>Total Books</h3>
        <p>{{ animatedStats.total_books_count }}</p>
      </div>
      <div class="stat-card">
        <h3>Available Books</h3>
        <p>{{ animatedStats.available_books_count }}</p>
      </div>
      <div class="stat-card">
        <h3>Borrowed Books</h3>
        <p>{{ animatedStats.borrowed_books_count }}</p>
      </div>
      <div class="stat-card">
        <h3>Penalty Books</h3>
        <p>{{ animatedStats.penalty_books_count }}</p>
      </div>
      <div class="stat-card">
        <h3>Total Users</h3>
        <p>{{ animatedStats.total_users_count }}</p>
      </div>
      <div class="stat-card">
        <h3>Penalty Users</h3>
        <p>{{ animatedStats.penalty_users_count }}</p>
      </div>
    </div>

    <div class="chart-wrapper">
      <div class="chart-row">
        <div class="chart-container">
          <h3>Books Availability</h3>
          <canvas ref="pieChartRef"></canvas>
        </div>

        <div class="chart-container">
          <h3>Penalty Overview</h3>
          <canvas ref="barChartRef"></canvas>
        </div>

        <div class="chart-container">
          <h3>Books Distribution</h3>
          <canvas ref="booksChartRef"></canvas>
        </div>
      </div>

      <div class="chart-row">
        <div class="chart-container">
          <h3>Users Overview</h3>
          <canvas ref="usersChartRef"></canvas>
        </div>

        <div class="chart-container">
          <h3>Books Summary</h3>
          <canvas ref="booksSummaryChartRef"></canvas>
        </div>
      </div>
    </div>

    <div class="progress-container">
      <h3>Borrowed Books Usage</h3>
      <div class="progress-bar">
        <div class="progress-fill"
          :style="{ width: (stats.borrowed_books_count / stats.total_books_count * 100) + '%' }"></div>
      </div>
      <p>{{ ((stats.borrowed_books_count / stats.total_books_count) * 100).toFixed(1) }}% of books are borrowed</p>
    </div>

    <div class="recent-users">
      <h3 class="section-title">Banned Users</h3>
      <div v-if="bannedUsers && bannedUsers.length === 0" class="no-users">
        No banned users found.
      </div>
      <div v-else class="user-list">
        <div v-for="user in bannedUsers" :key="user.id" class="user-card">
          <div class="user-info">
            <div class="user-name">{{ user.username }}</div>
            <div class="user-email">({{ user.email }})</div>
          </div>
          <div class="view-details" @click="goToUserDetail(user.id)">User Details</div>
        </div>
      </div>
    </div>

    <div v-if="showAdminModal" class="modal-overlay">
      <div class="modal-content">
        <button class="close-button" @click="closeAdminModal">×</button>
        <h3>Add New Admin</h3>
        <form @submit.prevent="submitNewAdmin">
          <input v-model="newAdmin.username" placeholder="Username" required />
          <input v-model="newAdmin.email" placeholder="Email" type="email" required />
          <input v-model="newAdmin.password" placeholder="Password" type="password" required />
          <div class="modal-actions">
            <button type="submit">Create</button>
            <button type="button" @click="closeAdminModal">Cancel</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { Chart, registerables } from 'chart.js';
import { useRouter } from 'vue-router';
import api from '@/api/axios';
import { useToast } from 'vue-toastification';


Chart.register(...registerables);

const stats = ref({
  borrowed_books_count: 0,
  penalty_books_count: 0,
  penalty_users_count: 0,
  total_books_count: 0,
  available_books_count: 0,
  total_users_count: 0,
});

const animatedStats = ref({
  total_books_count: 0,
  available_books_count: 0,
  borrowed_books_count: 0,
  penalty_books_count: 0,
  total_users_count: 0,
  penalty_users_count: 0,
});

const bannedUsers = ref([]);
const pieChartRef = ref(null);
const barChartRef = ref(null);
const booksChartRef = ref(null);
const usersChartRef = ref(null);
const booksSummaryChartRef = ref(null);
const router = useRouter();
const toast = useToast();

const adminInfo = ref(null);

const fetchAdminInfo = async () => {
  try {
    const response = await api.get('/admin/me');
    adminInfo.value = response.data.admin;
  } catch (error) {
    console.error('Failed to fetch admin info:', error);
  }
};

const showAdminModal = ref(false);
const newAdmin = ref({
  username: '',
  email: '',
  password: ''
});

const openAdminModal = () => {
  showAdminModal.value = true;
};

const closeAdminModal = () => {
  showAdminModal.value = false;
  newAdmin.value = { username: '', email: '', password: '' };
};

const goToUserDetail = (userId) => {
  router.push(`/admin/users/${userId}`);
};

const submitNewAdmin = async () => {
  try {
    await api.post('/admin/register-admin', {
      username: newAdmin.value.username,
      email: newAdmin.value.email,
      password: newAdmin.value.password,
    });
    toast.success(`Admin '${newAdmin.value.username}' created successfully!`);
    closeAdminModal();
  } catch (error) {
    console.error('Failed to create admin:', error);
  }
};

const animateStat = (key, target) => {
  const duration = 1000;
  const startTime = performance.now();

  const animate = (time) => {
    const elapsed = time - startTime;
    const progress = Math.min(elapsed / duration, 1);
    animatedStats.value[key] = Math.floor(progress * target);

    if (progress < 1) {
      requestAnimationFrame(animate);
    } else {
      animatedStats.value[key] = target;
    }
  };

  requestAnimationFrame(animate);
};

const fetchDashboardData = async () => {
  try {
    const response = await api.get('/admin/dashboard');
    stats.value = response.data;

    animateStat('total_books_count', stats.value.total_books_count);
    animateStat('available_books_count', stats.value.available_books_count);
    animateStat('borrowed_books_count', stats.value.borrowed_books_count);
    animateStat('penalty_books_count', stats.value.penalty_books_count);
    animateStat('total_users_count', stats.value.total_users_count);
    animateStat('penalty_users_count', stats.value.penalty_users_count);

    createCharts();
  } catch (error) {
    console.error('Failed to fetch dashboard stats:', error);
  }
};

const fetchBannedUsers = async () => {
  try {
    const response = await api.get('/admin/users?page=1&limit=10');
    bannedUsers.value = (response.data.users || []).filter(user => user.banned);
  } catch (error) {
    console.error('Failed to fetch banned users:', error);
  }
};

const createCharts = () => {
  if (pieChartRef.value) {
    new Chart(pieChartRef.value, {
      type: 'pie',
      data: {
        labels: ['Available', 'Borrowed'],
        datasets: [{
          label: 'Book Availability',
          data: [
            stats.value.available_books_count,
            stats.value.borrowed_books_count
          ],
          backgroundColor: ['#4caf50', '#f44336'],
        }]
      },
      options: {
        plugins: {
          legend: {
            display: true,
            position: 'bottom',
          },
        },
        animation: {
          animateScale: true,
          animateRotate: true,
        }
      }
    });
  }

  if (barChartRef.value) {
    new Chart(barChartRef.value, {
      type: 'bar',
      data: {
        labels: ['Penalty Books', 'Penalty Users'],
        datasets: [{
          label: 'Penalties',
          data: [
            stats.value.penalty_books_count,
            stats.value.penalty_users_count
          ],
          backgroundColor: ['#ff9800', '#ff5722'],
        }]
      },
      options: {
        plugins: {
          legend: {
            display: true,
            position: 'bottom',
          },
        },
        animation: {
          animateScale: true,
          animateRotate: true,
        }
      }
    });
  }

  if (booksChartRef.value) {
    new Chart(booksChartRef.value, {
      type: 'bar',
      data: {
        labels: ['Total Books', 'Available Books', 'Borrowed Books'],
        datasets: [{
          label: 'Books Distribution',
          data: [
            stats.value.total_books_count,
            stats.value.available_books_count,
            stats.value.borrowed_books_count
          ],
          backgroundColor: ['#2196f3', '#4caf50', '#f44336'],
        }]
      },
      options: {
        plugins: {
          legend: {
            display: true,
            position: 'bottom',
          },
        },
        animation: {
          animateScale: true,
          animateRotate: true,
        }
      }
    });
  }

  if (usersChartRef.value) {
    new Chart(usersChartRef.value, {
      type: 'pie',
      data: {
        labels: ['Total Users', 'Penalty Users'],
        datasets: [{
          label: 'Users Overview',
          data: [
            stats.value.total_users_count,
            stats.value.penalty_users_count
          ],
          backgroundColor: ['#2196f3', '#ff5722'],
        }]
      },
      options: {
        plugins: {
          legend: {
            display: true,
            position: 'bottom',
          },
        },
        animation: {
          animateScale: true,
          animateRotate: true,
        }
      }
    });
  }

  if (booksSummaryChartRef.value) {
    new Chart(booksSummaryChartRef.value, {
      type: 'doughnut',
      data: {
        labels: ['Available Books', 'Borrowed Books', 'Total Books'],
        datasets: [{
          label: 'Books Summary',
          data: [
            stats.value.available_books_count,
            stats.value.borrowed_books_count,
            stats.value.total_books_count
          ],
          backgroundColor: ['#4caf50', '#f44336', '#2196f3'],
        }]
      },
      options: {
        plugins: {
          legend: {
            display: true,
            position: 'bottom',
          },
        },
        animation: {
          animateScale: true,
          animateRotate: true,
        }
      }
    });
  }
};

const goToAddBook = () => {
  router.push('/admin/add-book');
};

onMounted(() => {
  fetchDashboardData();
  fetchBannedUsers();
  fetchAdminInfo();
});
</script>

<style scoped>
.admin-dashboard {
  padding: 24px;
}

.welcome-text {
  font-size: 28px;
  margin-bottom: 24px;
}

.quick-actions {
  display: flex;
  gap: 15px;
  margin-bottom: 24px;
}

.quick-actions button {
  background-color: #4caf50;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.quick-actions button:hover {
  background-color: #388e3c;
}

.stats-container {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  margin-bottom: 40px;
}

.stat-card {
  background: #fff;
  border-radius: 8px;
  padding: 20px;
  flex: 1 1 200px;
  text-align: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s, box-shadow 0.3s;
}

.stat-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.stat-card:nth-child(1) {
  background: #e3f2fd;
}

.stat-card:nth-child(2) {
  background: #e8f5e9;
}

.stat-card:nth-child(3) {
  background: #fff3e0;
}

.stat-card:nth-child(4) {
  background: #ffebee;
}

.stat-card:nth-child(5) {
  background: #ede7f6;
}

.stat-card:nth-child(6) {
  background: #e5f2f5;
}

.chart-wrapper {
  display: flex;
  flex-direction: column;
  gap: 20px;
  align-items: center;
}

.chart-row {
  display: flex;
  gap: 20px;
  flex-wrap: wrap;
  justify-content: center;
}

.chart-container {
  width: 400px;
  min-height: 420px;
  background: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}


.chart-container h3 {
  margin-bottom: 16px;
}

.progress-container {
  margin-top: 20px;
}

.progress-bar {
  width: 100%;
  background-color: #eee;
  border-radius: 8px;
  overflow: hidden;
  height: 20px;
}

.progress-fill {
  height: 100%;
  background-color: #4caf50;
}

.recent-users {
  margin-top: 40px;
}

.section-title {
  font-size: 24px;
  margin-bottom: 20px;
  font-weight: bold;
}

.user-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.user-card {
  width: 500px;
  max-width: 90%;
  background: #ffffff;
  padding: 10px 16px;
  border-radius: 10px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: transform 0.2s, box-shadow 0.2s;
}

.user-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
}

.user-info {
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.user-name {
  font-size: 16px;
  font-weight: 600;
}

.user-email {
  font-size: 12px;
  color: #777;
  margin-top: 2px;
}

.view-details {
  color: #4caf50;
  font-weight: 600;
  cursor: pointer;
  padding: 6px 12px;
  border-radius: 8px;
  transition: background-color 0.3s, color 0.3s;
}

.view-details:hover {
  background-color: #e8f5e9;
  color: #388e3c;
}

.admin-info-card {
  background-color: #e8f5e9;
  padding: 16px 24px;
  border-radius: 10px;
  margin-bottom: 20px;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  width: 300px;
}

.admin-welcome {
  font-size: 18px;
  margin: 0;
  color: #2e7d32;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.4);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 999;
}

.modal-content {
  background: #ffffff;
  padding: 40px 30px;
  border-radius: 14px;
  width: 380px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  display: flex;
  flex-direction: column;
  gap: 20px;
  animation: fadeIn 0.3s ease-out;
}

.modal-content h3 {
  margin: 0;
  font-size: 24px;
  text-align: center;
  color: #333;
}

.modal-content input {
  padding: 12px 16px;
  border: 1px solid #ccc;
  border-radius: 8px;
  font-size: 16px;
  outline: none;
  transition: border-color 0.3s;
}

.modal-content form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}


.modal-content input:focus {
  border-color: #4caf50;
}

.modal-actions {
  display: flex;
  justify-content: space-between;
  gap: 16px;
  margin-top: 10px;
}

.modal-actions button {
  flex: 1;
  padding: 12px 0;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.3s;
}

.modal-actions button:first-child {
  background-color: #4caf50;
  color: white;
}

.modal-actions button:first-child:hover {
  background-color: #43a047;
}

.modal-actions button:last-child {
  background-color: #e53935;
  color: white;
}

.modal-actions button:last-child:hover {
  background-color: #d32f2f;
}

.close-button {
  position: absolute;
  top: 12px;
  right: 16px;
  background: none;
  border: none;
  font-size: 24px;
  font-weight: bold;
  color: #999;
  cursor: pointer;
  transition: color 0.3s;
}

.close-button:hover {
  color: #e53935;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: scale(0.9);
  }

  to {
    opacity: 1;
    transform: scale(1);
  }
}
</style>