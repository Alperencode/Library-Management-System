<template>
  <div id="app">
    <MainHeader v-if="!isAuthPage" />
    <router-view />
    <MainFooter v-if="!isAuthPage" />
  </div>
</template>

<script>
import MainHeader from "@/components/MainHeader.vue";
import MainFooter from "@/components/MainFooter.vue";
import { computed } from "vue";
import { useRoute } from "vue-router";

export default {
  components: {
    MainHeader,
    MainFooter,
  },
  setup() {
    const route = useRoute();
    const isAuthPage = computed(() => route.path === "/login" || route.path === "/register");
    return { isAuthPage };
  },
};
</script>

<style>
#app {
  overflow-x: hidden;
}

.router-container {
  overflow: hidden;
}
</style>
