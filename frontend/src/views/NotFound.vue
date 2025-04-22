<template>
  <div class="page-content">
    <h1>404 - Page Not Found</h1>
    <p style="color: white">
      The page you are looking for does not exist or may have been removed.
    </p>
    <router-link to="/" class="go-home">Go to Home Page</router-link>
  </div>
</template>

<script>
export default {
  name: "NotFound",
};
</script>

<style scoped>
html,
body {
  margin: 0;
  padding: 0;
  height: 100%;
  overflow: hidden;
}

.page-content {
  height: 86.5vh;
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
