<template>
  <header class="header-area header-sticky">
    <div class="container">
      <div class="row">
        <div class="col-12">
          <nav class="main-nav">
            <RouterLink to="/" class="logo">Library Management System</RouterLink>
            <ul class="nav">
              <li class="scroll-to-section">
                <RouterLink to="/" class="active">Home</RouterLink>
              </li>

              <li :class="{ 'has-sub': user }">
                <RouterLink to="/books">Books</RouterLink>
                <ul v-if="user" class="sub-menu">
                  <li>
                    <RouterLink to="/books">Books</RouterLink>
                  </li>
                  <li>
                    <RouterLink to="/scan-book">Scan a Book</RouterLink>
                  </li>
                  <li>
                    <RouterLink to="/request-book">Request a Book</RouterLink>
                  </li>
                </ul>
              </li>

              <li v-if="user" :class="{ 'has-sub': user }">
                <RouterLink to="/user-page">Welcome, {{ user.username }}</RouterLink>
                <ul class="sub-menu">
                  <li>
                    <RouterLink to="/user-page/account">Account Management</RouterLink>
                  </li>
                  <li>
                    <RouterLink to="/user-page/borrowed">Borrowed Books</RouterLink>
                  </li>
                  <li>
                    <RouterLink to="/user-page/requested">Requested Books</RouterLink>
                  </li>
                  <li>
                    <RouterLink to="/user-page/notify">Notify Me List</RouterLink>
                  </li>
                  <li>
                    <RouterLink to="/user-page/history">Borrow History</RouterLink>
                  </li>
                  <li>
                    <RouterLink to="/user-page/overdue">Overdue Books</RouterLink>
                  </li>
                </ul>
              </li>

              <li v-if="admin" class="has-sub">
                <RouterLink to="/admin">Welcome, {{ admin.username }}</RouterLink>
                <ul class="sub-menu">
                  <li>
                    <RouterLink to="/admin/dashboard">Dashboard</RouterLink>
                  </li>
                  <li>
                    <RouterLink to="/admin/books">Books</RouterLink>
                  </li>
                  <li>
                    <RouterLink to="/admin/users">Users</RouterLink>
                  </li>
                  <li>
                    <RouterLink to="/admin/requests">Requests</RouterLink>
                  </li>
                  <li>
                    <RouterLink to="/admin/borrow">Borrow Management</RouterLink>
                  </li>
                  <li>
                    <RouterLink to="/admin/penalty">Penalty Management</RouterLink>
                  </li>
                  <li>
                    <RouterLink to="/admin/banned-users">Banned Users</RouterLink>
                  </li>
                </ul>
              </li>

              <li v-if="user || admin">
                <a href="javascript:void(0)" @click="logout">Logout</a>
              </li>
              <li v-if="!user && !admin">
                <RouterLink to="/login">Login</RouterLink>
              </li>
              <li v-if="!user && !admin">
                <RouterLink to="/register">Register</RouterLink>
              </li>
            </ul>
            <a class="menu-trigger"><span>Menu</span></a>
          </nav>
        </div>
      </div>
    </div>
  </header>
</template>

<script>
import { useRouter } from "vue-router";
import api from "@/api/axios";
import { useAuth } from '@/composables/useAuth'

export default {
  setup() {
    const { user, admin, setUser, setAdmin } = useAuth()
    const router = useRouter()

    const logout = async () => {
      await api.post("/logout")
      setUser(null)
      setAdmin(null)
      router.push("/login")
    }

    return { user, admin, logout }
  },
};
</script>

<style scoped>
.user-greeting {
  font-size: 17px;
  font-weight: bold;
  color: #f5a425;
  opacity: 0.8;
  display: flex;
  align-items: center;
  padding: 0 15px;
}

nav .nav li.has-sub {
  position: relative;
}

nav .nav li.has-sub .sub-menu {
  position: absolute;
  top: 100%;
  left: 0;
  z-index: 1000;
  background-color: white;
  padding: 10px 0;
  min-width: 200px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

nav .nav li.has-sub .sub-menu li a {
  color: #1f1f1f;
  text-transform: uppercase;
  padding: 10px 20px;
  display: block;
  font-weight: 500;
  font-size: 13px;
  white-space: nowrap;
  transition: background 0.2s, color 0.2s;
}

nav .nav li.has-sub .sub-menu li a:hover {
  background-color: #f5a425;
  color: white;
}
</style>
