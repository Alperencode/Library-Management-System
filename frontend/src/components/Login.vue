<template>
    <div>
      <h2>Giriş Yap</h2>
      <input v-model="email" type="email" placeholder="Email">
      <input v-model="password" type="password" placeholder="Şifre">
      <button @click="login">Giriş Yap</button>
      <p v-if="errorMessage" style="color: red;">{{ errorMessage }}</p>
    </div>
  </template>
  
  <script>
  import api from "../api";
  
  export default {
    data() {
      return {
        email: "",
        password: "",
        errorMessage: "",
      };
    },
    methods: {
      async login() {
        try {
          const response = await api.post("/login", {
            email: this.email,
            password: this.password,
          });
          console.log(response.data);
  
          localStorage.setItem("access_token", response.data.access_token);
  
          
          this.$router.push("/dashboard");
        } catch (error) {
          console.error("Hata:", error.response ? error.response.data : error);
          this.errorMessage =(error.response?.data?.message || "Bilinmeyen hata");
        }
      },
    },
  };
  </script>
  