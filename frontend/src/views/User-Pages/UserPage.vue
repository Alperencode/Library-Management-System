<template>
  <div class="user-page" v-if="user">
    <aside class="sidebar">
      <router-link to="/user-page" class="username">
        Hi, {{ user.username }}!
      </router-link>
      <nav class="menu">
        <ul>
          <li v-for="item in menuItems" :key="item.path">
            <router-link :to="item.path" class="menu-link">
              {{ item.label }}
            </router-link>
          </li>
          <li>
            <button @click="logout" class="menu-link logout">Logout</button>
          </li>
        </ul>

      </nav>
    </aside>

    <main class="content">
      <div v-if="$route.path === '/user-page' || $route.path === '/user-page/'" class="page-content">
        <h2 class="dashboard-heading">Welcome, {{ user.username }}!</h2>

        <div class="dashboard-cards">
          <router-link to="/user-page/borrowed" class="card blue">
            Borrowed Books<br /><strong>{{ borrowedBooks.length }}</strong>
          </router-link>

          <router-link to="/user-page/overdue" class="card red">
            Overdue Books<br /><strong>{{ overdueBooks.length }}</strong>
          </router-link>

          <router-link to="/user-page/requested" class="card purple">
            Requested Books<br /><strong>{{ requestedBooks.length }}</strong>
          </router-link>

          <router-link to="/user-page/notify" class="card yellow">
            Notify Me<br /><strong>{{ notifyList.length }}</strong>
          </router-link>
        </div>

        <div class="alert-warning" v-if="overdueBooks.length > 0">
          You have <strong>{{ overdueBooks.length }}</strong> overdue book(s). Please return them as soon as possible.
        </div>

        <div v-if="topOverdueBooks.length" class="overdue-top-section">
          <h3 class="overdue-top-heading">Overdue Books (Top 3)</h3>
          <ul>
            <li class="overdue-top-item" v-for="book in topOverdueBooks" :key="book.id">
              <img :src="book.cover_image || defaultCover" class="thumbnail" alt="Cover" />
              <div class="info">
                <span class="title">
                  <router-link :to="`/books/${book.id}`" class="book-link">
                    {{ book.title }}
                  </router-link>
                </span>
                <span class="date"> &nbsp;&nbsp; Return Date was: {{ formatDateWithoutTime(book.return_date) }}</span>
              </div>
            </li>
          </ul>
        </div>
      </div>
      <router-view v-else />
    </main>
  </div>
</template>

<script setup>
import { useRouter, useRoute } from 'vue-router';
import api from '@/api/axios';
import { useAuth } from '@/composables/useAuth';
import { ref, onMounted, computed, watch } from 'vue';
import defaultCover from '@/assets/images/default-cover.png';
import { formatDateWithoutTime } from '@/utils/date';

const router = useRouter();
const route = useRoute();
const { user, setUser } = useAuth();

const borrowedBooks = ref([]);
const overdueBooks = ref([]);
const requestedBooks = ref([]);
const notifyList = ref([]);

const dataLoaded = ref(false);

const logout = async () => {
  await api.post("/logout");
  setUser(null);
  router.push("/login");
};

const menuItems = [
  { label: 'Account Management', path: '/user-page/account' },
  { label: 'Borrowed Books', path: '/user-page/borrowed' },
  { label: 'Requested Books', path: '/user-page/requested' },
  { label: 'Notify Me List', path: '/user-page/notify' },
  { label: 'Overdue Books', path: '/user-page/overdue' },
  { label: 'Borrow History', path: '/user-page/history' }
];

const fetchDashboardData = async () => {
  try {
    const [borrowed, overdue, requested, notify] = await Promise.all([
      api.get('/borrowed'),
      api.get('/borrowed/overdue-books'),
      api.get('/request-book'),
      api.get('/notify-me'),
    ]);

    borrowedBooks.value = borrowed.data.books;
    overdueBooks.value = overdue.data.books;
    requestedBooks.value = requested.data.books;
    notifyList.value = notify.data.books;
    dataLoaded.value = true;
  } catch (err) {
    console.error("Failed to fetch dashboard data:", err);
  }
};

onMounted(() => {
  if (route.path === '/user-page' || route.path === '/user-page/') {
    fetchDashboardData();
  }
});

watch(
  () => route.path,
  (newPath) => {
    if ((newPath === '/user-page' || newPath === '/user-page/') && !dataLoaded.value) {
      fetchDashboardData();
    }
  }
);

const topOverdueBooks = computed(() => {
  return overdueBooks.value
    .filter(book => book.return_date)
    .sort((a, b) => new Date(a.return_date) - new Date(b.return_date))
    .slice(0, 3);
});
</script>

<style scoped>
.user-page {
  display: flex;
  height: 100vh;
  background-blend-mode: overlay;
  background-size: cover;
  background-attachment: fixed;
}

.sidebar {
  width: 250px;
  margin-top: 3.5%;
  height: 93vh;
  background: rgba(0, 0, 0, 0.3);
  padding: 20px 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  overflow-y: auto;
}

.username {
  display: inline-block;
  width: 80%;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  text-align: center;
  font-size: 18px;
  font-weight: bold;
  padding: 12px;
  border-radius: 5px;
  background: rgba(255, 255, 255, 0.1);
  margin-bottom: 20px;
}

.menu-link {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 100%;
}

.menu ul {
  list-style: none;
  padding: 0;
  margin: 0;
  width: 110%;
}

.menu ul li {
  margin-bottom: 15px;
  width: 100%;
  display: flex;
  justify-content: center;
}

.menu ul li a,
.menu ul li button {
  color: white;
  text-decoration: none;
  display: block;
  padding: 12px 15px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  font-size: 16px;
  transition: all 0.3s ease-in-out;
  text-align: center;
  width: 80%;
  border: none;
  cursor: pointer;
}

.menu ul li a:hover,
.menu ul li button:hover {
  background: rgba(255, 165, 0, 0.8);
  color: #222;
}

.menu-link:hover {
  background: rgba(255, 255, 255, 0.25);
}

.menu-link.logout {
  background: rgba(255, 0, 0, 0.15);
}

.menu-link.logout:hover {
  background: rgba(255, 0, 0, 0.3);
}

.content {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
}

.page-content {
  background: rgba(255, 255, 255, 0.301);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
  padding: 40px;
  max-width: 900px;
  width: 100%;
  border: 1px solid rgba(255, 255, 255, 0.3);
}

h2 {
  text-align: center;
  font-size: 28px;
  font-weight: bold;
  color: #333;
  margin-bottom: 30px;
}

.dashboard-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
}

.card {
  padding: 1.2rem;
  border-radius: 16px;
  text-align: center;
  color: white;
  font-weight: 600;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  min-height: 100px;
  transition: transform 0.2s ease;
}

.card:hover {
  transform: scale(1.03);
}

.card.blue {
  background: #ffa500cc;
}

.card.red {
  background: #ffa500cc;
}

.card.purple {
  background: #ffa500cc;
}

.card.yellow {
  background: #ffa500cc;
}

.alert-warning {
  background-color: #fff1f2;
  border: 1px solid #fecdd3;
  color: #b91c1c;
  padding: 1rem;
  border-radius: 10px;
  margin-bottom: 2rem;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 10px;
}

.alert-warning::before {
  font-size: 1.4rem;
}

.recent-section {
  margin-top: 2rem;
}

.recent-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #f9fafb;
  padding: 1rem;
  margin-bottom: 0.75rem;
  border-radius: 10px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.06);
  transition: background 0.2s ease;
}

.recent-item:hover {
  background: #f3f4f6;
}

.recent-item .info {
  flex: 1;
}

.recent-item button {
  padding: 6px 12px;
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.85rem;
}

.recent-item button:hover {
  background: #2563eb;
}

.thumbnail {
  width: 60px;
  height: 80px;
  object-fit: cover;
  margin-right: 1rem;
  border-radius: 4px;
}

.info .title {
  font-weight: bold;
  font-size: 1rem;
  color: #111827;
}

.info .date {
  font-size: 0.9rem;
  color: #6b7280;
}

.dashboard-heading {
  text-align: center;
  font-size: 32px;
  font-weight: bold;
  background: white;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  animation: fadeInDown 0.5s ease-out;
}

@keyframes fadeInDown {
  0% {
    transform: translateY(-10px);
    opacity: 0;
  }

  100% {
    transform: translateY(0);
    opacity: 1;
  }
}

.overdue-top-section {
  margin-top: 2rem;
}

.overdue-top-heading {
  font-size: 20px;
  font-weight: 600;
  margin-bottom: 10px;
  color: #ffffff;
}

.overdue-top-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #f5f0f1;
  padding: 1rem;
  margin-bottom: 0.75rem;
  border-radius: 10px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.06);
  transition: background 0.2s ease;
}

.overdue-top-item:hover {
  background: #ffdada;
}

.overdue-top-item .info {
  flex: 1;
}

.overdue-top-item .title {
  font-weight: bold;
  font-size: 1rem;
  color: #000000;
}

.overdue-top-item .date {
  font-size: 0.9rem;
  color: #991b1b;
}

.book-link {
  color: inherit;
  text-decoration: none;
  font-weight: bold;
}

.book-link:hover {
  color: inherit;
  text-decoration: underline;
}

.username {
  display: inline-block;
  width: 80%;
  text-align: center;
  font-size: 18px;
  font-weight: bold;
  padding: 12px;
  border-radius: 5px;
  background: rgba(255, 255, 255, 0.1);
  margin-bottom: 20px;
  color: white;
  text-decoration: none;
  cursor: pointer;
  transition: background 0.2s ease;
}

.username:hover {
  background: rgba(255, 255, 255, 0.25);
}
</style>
