<template>
  <div id="app">
    <MainHeader />
    <router-view />
    <MainFooter />
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

    return { hideLayout };
  },
};
</script>