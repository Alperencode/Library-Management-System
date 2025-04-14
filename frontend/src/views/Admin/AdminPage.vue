<template>
  <div class="admin-layout">
    <aside class="admin-sidebar">
      <h4 class="text-center mb-4">Admin Panel</h4>
      <ul class="nav flex-column">
        <li
          v-for="(item, index) in adminMenuItems"
          :key="index"
          class="nav-item mb-2"
        >
          <router-link
            :to="item.path"
            class="nav-link"
            active-class="active-link"
            exact-active-class="active-link"
          >
            {{ item.label }}
          </router-link>
        </li>
      </ul>
    </aside>
    <main class="admin-main">
      <router-view />
    </main>
  </div>
</template>

<script setup>
const adminMenuItems = [
  { label: "Dashboard", path: "/admin/dashboard" },
  { label: "Book List", path: "/admin/books" },
  { label: "User List", path: "/admin/users" },
  { label: "Request List", path: "/admin/requests" },
  { label: "Borrow Management", path: "/admin/borrow" },
  { label: "Penalty Management", path: "/admin/penalty" },
  { label: "Banned User Management", path: "/admin/banned-users" },
  { label: "Add New Book", path: "/admin/add-book" },
];
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

</style>
