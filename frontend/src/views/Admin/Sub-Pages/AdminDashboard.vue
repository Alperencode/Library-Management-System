<template>
  <div class="admin-dashboard">

    <h2 class="welcome-text">Welcome, Admin!</h2>

    <div class="quick-actions">
      <button @click="goToAddBook">Add New Book</button>
      <button @click="goToUserList">Manage Users</button>
    </div>

    <div class="stats-container">
      <div class="stat-card">
        <h3>Total Books</h3>
        <p>{{ stats.total_books_count }}</p>
      </div>
      <div class="stat-card">
        <h3>Available Books</h3>
        <p>{{ stats.available_books_count }}</p>
      </div>
      <div class="stat-card">
        <h3>Borrowed Books</h3>
        <p>{{ stats.borrowed_books_count }}</p>
      </div>
      <div class="stat-card">
        <h3>Penalty Books</h3>
        <p>{{ stats.penalty_books_count }}</p>
      </div>
      <div class="stat-card">
        <h3>Total Users</h3>
        <p>{{ stats.total_users_count }}</p>
      </div>
      <div class="stat-card">
        <h3>Penalty Users</h3>
        <p>{{ stats.penalty_users_count }}</p>
      </div>
    </div>

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

    <div class="chart-container">
      <h3>Users Overview</h3>
      <canvas ref="usersChartRef"></canvas>
    </div>

    <div class="chart-container">
      <h3>Books Summary</h3>
      <canvas ref="booksSummaryChartRef"></canvas>
    </div>

    <div class="progress-container">
      <h3>Borrowed Books Usage</h3>
      <div class="progress-bar">
        <div class="progress-fill"
          :style="{ width: (stats.borrowed_books_count / stats.total_books_count * 100) + '%' }"></div>
      </div>
      <p>{{ ((stats.borrowed_books_count / stats.total_books_count) * 100).toFixed(1) }}% of books are borrowed</p>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { Chart, registerables } from 'chart.js';
import { useRouter } from 'vue-router';
import api from '@/api/axios';

Chart.register(...registerables);

const stats = ref({
  borrowed_books_count: 0,
  penalty_books_count: 0,
  penalty_users_count: 0,
  total_books_count: 0,
  available_books_count: 0,
  total_users_count: 0,
});

const pieChartRef = ref(null);
const barChartRef = ref(null);
const booksChartRef = ref(null);
const usersChartRef = ref(null);
const booksSummaryChartRef = ref(null);
const router = useRouter();

const fetchDashboardData = async () => {
  try {
    const response = await api.get('/admin/dashboard');
    stats.value = response.data;
    createCharts();
  } catch (error) {
    console.error('Failed to fetch dashboard stats:', error);
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

const goToUserList = () => {
  router.push('/admin/users');
};

onMounted(() => {
  fetchDashboardData();
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

.chart-container {
  margin-bottom: 40px;
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
</style>