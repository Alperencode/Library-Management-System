<template>
  <div class="page-content">
    <h1>404 - Page Not Found</h1>
    <p style="color: white">
      The page you are looking for does not exist or may have been removed.
    </p>
    <div v-if="admin">
    <router-link to="/admin" class="go-home"> Return to Admin Page</router-link>
    </div>
    <div v-if="!admin">
    <router-link to="/" class="go-home"> Return to Home Page</router-link>
    </div>
  </div>
</template>

<script>
import { useAuth } from '@/composables/useAuth'

export default {
  setup() {
    const { user, admin } = useAuth()

    return { user, admin }
  },
};
</script>

<style scoped>
html,
body {
  margin: 0;
  padding: 0;
  height: 100%;
}

.page-content {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 0 30px;
  color: white;
  text-align: center;
}

.go-home {
  display: inline-block;
  margin-top: 20px;
  padding: 10px 20px;
  background-color: #d48d29;
  color: white;
  text-decoration: none;
  border-radius: 5px;
  transition: background-color 0.3s ease;
}

.go-home:hover {
  background-color: #eab308;
}
</style>