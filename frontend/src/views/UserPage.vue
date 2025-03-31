<template>
  <div class="user-page" v-if="user">
    <MainHeader />

    <aside class="sidebar">
      <div class="username">{{ user.username }}</div>
      <nav class="menu">
        <ul>
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
            <button @click="logout">Logout</button>
          </li>
        </ul>
      </nav>
      <footer class="sidebar-footer">
        <p>Library Management System</p>
      </footer>
    </aside>

    <main class="content">
      <div class="page-content">
        <h2>Welcome, {{ user.username }}!</h2>
        <router-view></router-view>
      </div>
    </main>

    <MainFooter />
  </div>
</template>

<script>
import { useRouter } from "vue-router";
import { useStore, mapState } from "vuex";
import MainHeader from "@/components/MainHeader.vue";
import MainFooter from "@/components/MainFooter.vue";
import api from "@/api/axios";

export default {
  name: "UserPage",
  components: {
    MainHeader,
    MainFooter,
  },
  computed: {
    ...mapState({
      user: (state) => state.user,
    }),
  },
  setup() {
    const router = useRouter();
    const store = useStore();

    const logout = async () => {
      try {
        await api.post("/logout");
        store.commit("setUser", null);
        router.push("/");
      } catch (error) {
        console.error("Logout API request failed:", error);
      }
    };

    return { logout };
  },
};
</script>

<style scoped>
.user-page {
  display: flex;
  height: 100vh;
  background: #f4f4f4;
  background-image: url("@/assets/images/meetings-bg.jpg");
  background-size: cover;
  background-position: center;
}

.sidebar {
  width: 250px;
  background: linear-gradient(180deg, #222 0%, #444 100%);
  color: white;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 20px 0;
  position: fixed;
  top: 0;
  left: 0;
  bottom: 0;
  box-shadow: 2px 0 10px rgba(0, 0, 0, 0.2);
}

.username {
  text-align: center;
  font-size: 18px;
  font-weight: bold;
  padding: 12px;
  border-radius: 5px;
  background: rgba(255, 255, 255, 0.1);
  width: 80%;
  margin-bottom: 20px;
}

.menu {
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
  width: 100%;
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
  background: rgba(51, 51, 51, 0.8);
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

.sidebar-footer {
  width: 100%;
  background: #222;
  color: white;
  text-align: center;
  padding: 10px 0;
  position: fixed;
  bottom: 0;
  left: 0;
}

.content {
  flex: 1;
  margin-left: 250px;
  padding: 40px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.page-content {
  width: 80%;
  padding: 30px;
  background: white;
  border-radius: 12px;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
}

.page-content h2 {
  font-size: 28px;
  font-weight: bold;
  color: #333;
  margin-bottom: 15px;
  text-align: center;
}

.page-content p {
  font-size: 16px;
  color: #666;
  text-align: center;
}
</style>
