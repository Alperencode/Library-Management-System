<template>
  <div id="app" class="layout">
    <MainHeader v-if="!hideLayout && !isAdminRoute" />
    <main class="content">
      <router-view />
    </main>
    <MainFooter v-if="!hideLayout && !isAdminRoute" />
  </div>
</template>

<script>
import { onMounted, computed } from "vue";
import { useRoute } from "vue-router";
import { useAuth } from "@/composables/useAuth";
import MainHeader from "@/components/MainHeader.vue";
import MainFooter from "@/components/MainFooter.vue";
import axios from "axios";

export default {
  components: {
    MainHeader,
    MainFooter,
  },
  setup() {
    const route = useRoute();
    const { user, setUser } = useAuth();

    const isAdminRoute = computed(() => route.path.startsWith("/admin"));
    const hideLayout = computed(() => route.meta.hideLayout);

    onMounted(async () => {
      const savedUser = localStorage.getItem("user");
      if (!savedUser) return;

      const parsedUser = JSON.parse(savedUser);

      const protocol = window.location.protocol;
      const hostname = process.env.VUE_APP_API_HOST || window.location.hostname;
      const port = process.env.VUE_APP_API_PORT || 8000;
      const baseUrl = `${protocol}//${hostname}:${port}/api/v1`;

      const plain = axios.create({
        baseURL: baseUrl,
        withCredentials: true,
      });

      try {
        await plain.post("/refresh-token", {});
        setUser(parsedUser);
      } catch (err) {
        localStorage.removeItem("user");
        setUser(null);
      }
    });

    return { hideLayout, isAdminRoute, user };
  },
};
</script>

<style>

#app {
  background-image: url('@/assets/images/meetings-page-bg.jpg');
  background-position: center center;
  background-attachment: fixed;
  background-repeat: no-repeat;
  background-size: cover;
}

body {
  background-image: url('@/assets/images/meetings-page-bg.jpg');
  background-position: center center;
  background-attachment: fixed;
  background-repeat: no-repeat;
  background-size: cover;
  margin: 0;
  padding: 0;
}

.content {
  padding-top: 73px;
}
</style>
