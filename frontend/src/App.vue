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
import api from "@/api/axios";


export default {
  components: {
    MainHeader,
    MainFooter,
  },
  setup() {
    const route = useRoute();
    const { fetchUser } = useAuth();
    const isAdminRoute = computed(() => route.path.startsWith('/admin'))

    onMounted(async () => {
      try {
        await fetchUser();
      } catch (error) {
        await api.post('/refresh-token', {}, { withCredentials: true });
        await fetchUser();
        console.log("failed to fetch the user")
      }
    });

    const hideLayout = computed(() => route.meta.hideLayout);

    return { hideLayout, isAdminRoute };
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
