<template>
  <div id="app">
    <nav>
      <router-link to="/register">Kayıt Ol</router-link> |
      <router-link to="/login">Giriş Yap</router-link>
    </nav>
    <router-view></router-view>
  </div>
</template>

<script>
export default {
  name: "App"
};
</script>

<style scoped>
nav {
  text-align: center;
  margin-bottom: 20px;
}
</style>
