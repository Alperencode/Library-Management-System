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

export default {
  components: {
    MainHeader,
    MainFooter,
  },
  setup() {
    const route = useRoute();
    const { fetchUser } = useAuth();

    onMounted(() => {
      fetchUser();
    });

    const hideLayout = computed(() => route.meta.hideLayout);

    return { hideLayout };
  },
};
</script>