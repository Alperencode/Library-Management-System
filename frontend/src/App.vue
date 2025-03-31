<template>
  <div id="app" class="layout">
    <MainHeader v-if="!hideLayout" />
    <main class="content">
      <router-view />
    </main>
    <MainFooter v-if="!hideLayout" />
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
