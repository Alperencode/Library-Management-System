<template>
  <div class="admin-layout d-flex">
    <aside class="admin-sidebar p-3 text-white">
      <h4 class="text-center mb-4">Admin Panel</h4>
      <ul class="nav flex-column">
        <li class="nav-item mb-2">
        <router-link to="/admin/dashboard" class="nav-link" active-class="active-link">
            Dashboard
        </router-link>
        </li>

        <li class="nav-item mb-2">
        <router-link to="/admin/books" class="nav-link" active-class="active-link">
            Book List
        </router-link>
        </li>

        <li class="nav-item mb-2">
        <router-link to="/admin/users" class="nav-link" active-class="active-link">
            User List
        </router-link>
        </li>

        <li class="nav-item mb-2">
        <router-link to="/admin/requests" class="nav-link" active-class="active-link">
            Request List
        </router-link>
        </li>

        <li class="nav-item mb-2">
        <router-link to="/admin/borrow" class="nav-link" active-class="active-link">
            Borrow Management
        </router-link>
        </li>

        <li class="nav-item mb-2">
        <router-link to="/admin/penalty" class="nav-link" active-class="active-link">
            Penalty Management
        </router-link>
        </li>

        <li class="nav-item mb-2">
        <router-link to="/admin/banned-users" class="nav-link" active-class="active-link">
            Banned User Management
        </router-link>
        </li>

        <li class="nav-item mb-2">
        <router-link to="/admin/add-book" class="nav-link" active-class="active-link">
            Add New Book
        </router-link>
        </li>
      </ul>
    </aside>

    <main class="admin-main flex-grow-1 p-4">
      <router-view />
    </main>
  </div>
</template>

<style scoped>

:root {
  --admin-orange: #d4881a;
  --sidebar-bg: #1e1e1e;
  --sidebar-hover: #302f2f;
  --active-bg: var(--admin-orange);
}

.admin-sidebar {
  width: 240px;
  min-height: 100vh;
  background-color: var(--sidebar-bg);
  color: white;
}

.nav-link {
  color: #ccc;
  font-size: 16px;
  padding: 8px 14px;
  border-radius: 6px;
  transition: all 0.2s ease;
  cursor: pointer;
}

.nav-link:hover {
  background-color: var(--sidebar-hover);
  color: var(--admin-orange);
}

.active-link {
  background-color: var(--active-bg);
  color: white !important;
}

.submenu {
  list-style: none;
  padding-left: 0;
  margin-top: 5px;
}

.admin-main {
    background-color: #f8f9fa;
  }

.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: all 0.3s ease;
}

.fade-slide-enter-from,
.fade-slide-leave-to {
  max-height: 0;
  opacity: 0;
  transform: translateY(-5px);
}

.fade-slide-enter-to,
.fade-slide-leave-from {
  max-height: 300px;
  opacity: 1;
  transform: translateY(0);
}

</style>
