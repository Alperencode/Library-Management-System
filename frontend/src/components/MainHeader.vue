<template>
  <header class="header-area header-sticky">
    <div class="container">
      <div class="row">
        <div class="col-12">
          <nav class="main-nav">
            <RouterLink to="/" class="logo">Library Management System</RouterLink>
            <ul class="nav">
              <li class="scroll-to-section"><RouterLink to="/" class="active">Home</RouterLink></li>
              <li><RouterLink to="/books">Books</RouterLink></li>
              <!--- <li class="scroll-to-section"><a href="#apply">Apply Now</a></li>
              <li class="has-sub">
                <a href="javascript:void(0)">Pages</a>
                <ul class="sub-menu">
                  <li><RouterLink to="/meetings">Upcoming Meetings</RouterLink></li>
                  <li><RouterLink to="/meeting-details">Meeting Details</RouterLink></li>
                </ul>
              </li>
              <li class="scroll-to-section"><a href="#courses">Courses</a></li>
              <li class="scroll-to-section"><a href="#contact">Contact Us</a></li>
              -->
              <li v-if="user" class="user-greeting">
                <RouterLink to="/user-page">
                  <span>Welcome, {{ user.username }}</span>
                </RouterLink>
              </li>
              <li v-if="user">
                <a href="javascript:void(0)" @click="logout">Logout</a>
              </li>
              <li v-if="!user"><RouterLink to="/login">Login</RouterLink></li>
              <li v-if="!user"><RouterLink to="/register">Register</RouterLink></li>
            </ul>
            <a class="menu-trigger"><span>Menu</span></a>
          </nav>
        </div>
      </div>
    </div>
  </header>
</template>

<script>
import { computed } from "vue";
import { useStore } from "vuex";
import { useRouter } from "vue-router";
import api from "@/api/axios";

export default {
  setup() {
    const store = useStore();
    const router = useRouter();
    const user = computed(() => store.state.user);

    const logout = async () => {
      await api.post("/logout");

      store.commit("logout");
      router.push("/login");
    };

    return {
      user,
      logout,
    };
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
</style>
