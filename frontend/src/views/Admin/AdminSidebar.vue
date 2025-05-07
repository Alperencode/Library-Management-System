<template>
  <div class="admin-layout">
    <aside class="admin-sidebar">
      <router-link to="/admin/dashboard" class="admin-panel-link">Admin Panel</router-link>
      <ul class="nav flex-column">
        <li v-for="(item, index) in adminMenuItems" :key="index" class="nav-item mb-2">
          <template v-if="item.label === 'Request List'">
            <div class="nav-link" @click="goToRequestsAndToggle(index)">
              {{ item.label }}
            </div>
            <transition name="submenu-slide">
              <ul v-if="activeSubmenu === index" class="submenu">
                <li>
                  <router-link to="/admin/requests/added" class="nav-link" active-class="active-link"
                    exact-active-class="active-link">
                    Added Requests
                  </router-link>
                </li>
                <li>
                  <router-link to="/admin/requests/denied" class="nav-link" active-class="active-link"
                    exact-active-class="active-link">
                    Denied Requests
                  </router-link>
                </li>
              </ul>
            </transition>
          </template>
          <template v-else>
            <router-link :to="item.path" class="nav-link" active-class="active-link" exact-active-class="active-link">
              {{ item.label }}
            </router-link>
          </template>
        </li>
      </ul>
      <div class="logout-container">
        <router-link to="/" class="nav-link">View the Home Page</router-link>
        <a class="nav-link logout-link" @click="logout">Logout</a>
      </div>
    </aside>
    <main class="admin-main">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/api/axios'
import { useAuth } from '@/composables/useAuth'

const router = useRouter()
const { setUser, setAdmin } = useAuth()
const activeSubmenu = ref(null)

const goToRequestsAndToggle = (index) => {
  router.push('/admin/requests')
  activeSubmenu.value = activeSubmenu.value === index ? null : index
}

const adminMenuItems = [
  { label: "Dashboard", path: "/admin/dashboard" },
  { label: "Book List", path: "/admin/books" },
  { label: "User List", path: "/admin/users" },
  { label: "Request List", path: "/admin/requests", expandable: true },
  { label: "Borrow Management", path: "/admin/borrow" },
  { label: "Penalty Management", path: "/admin/penalty" },
  { label: "Banned User Management", path: "/admin/banned-users" },
  { label: "Add New Book", path: "/admin/add-book" },
]

const logout = async () => {
  try {
    await api.post('/logout')
    setUser(null)
    setAdmin(null)
    router.push('/login')
  } catch (error) {
    console.error('Logout failed:', error)
  }
}
</script>

<style scoped>
:root {
  --admin-orange: #d4881a;
  --sidebar-bg: #1e1e1e;
  --sidebar-hover: #302f2f;
  --active-bg: var(--admin-orange);
}

.admin-layout {
  min-height: 100vh;
}

.admin-sidebar {
  position: fixed;
  top: 0;
  left: 0;
  width: 240px;
  height: 100vh;
  background-color: var(--sidebar-bg);
  color: white;
  padding: 24px 16px;
  overflow-y: auto;
  z-index: 1000;
  margin-top: 30px;
}

.admin-panel-link {
  display: block;
  text-align: center;
  font-size: 20px;
  font-weight: bold;
  color: white;
  margin-bottom: 24px;
  text-decoration: none;
}

.admin-panel-link:hover {
  color: var(--admin-orange);
}

.nav-link {
  color: #ccc;
  font-size: 16px;
  padding: 8px 14px;
  border-radius: 6px;
  transition: all 0.2s ease;
  cursor: pointer;
  display: block;
  text-decoration: none;
}

.nav-link:hover {
  background-color: var(--sidebar-hover);
  color: var(--admin-orange);
}

.active-link {
  background-color: var(--active-bg);
  color: white !important;
  font-weight: bold;
}

.admin-main {
  margin-left: 240px;
  background-color: #f8f9fa;
  padding: 32px 24px 30px 24px;
  min-height: 100vh;
  box-sizing: border-box;
  margin-top: -85px;
}

.logout-container {
  padding-top: 16px;
  border-top: 1px solid #333;
}

.logout-link {
  color: #ccc;
  font-size: 16px;
  padding: 8px 14px;
  border-radius: 6px;
  transition: all 0.2s ease;
  text-decoration: none;
  display: block;
}

.logout-link:hover {
  background-color: var(--sidebar-hover);
  color: var(--admin-orange);
}

.submenu {
  margin-left: 16px;
  margin-top: 4px;
}

.submenu .nav-link {
  font-size: 14px;
  padding: 6px 12px;
}

.submenu-slide-enter-active,
.submenu-slide-leave-active {
  transition: all 0.3s ease;
}

.submenu-slide-enter-from,
.submenu-slide-leave-to {
  opacity: 0;
  max-height: 0;
  transform: translateY(-5px);
  overflow: hidden;
}

.submenu-slide-enter-to,
.submenu-slide-leave-from {
  opacity: 1;
  max-height: 200px;
  transform: translateY(0);
}
</style>
