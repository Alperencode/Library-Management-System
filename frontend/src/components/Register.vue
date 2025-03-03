<template>
    <div>
      <h2>Kayıt Ol</h2>
      <form @submit.prevent="register">
        <input type="text" v-model="name" placeholder="İsim" required />
        <input type="email" v-model="email" placeholder="Email" required />
        <input type="password" v-model="password" placeholder="Şifre" required />
        <button type="submit">Kayıt Ol</button>
      </form>
      <p v-if="message">{{ message }}</p>
    </div>
  </template>
  
  <script>
  import api from "../api";
  
  export default {
    data() {
      return {
        name: "",
        email: "",
        password: "",
        message: ""
      };
    },
    methods: {
      async register() {
        try {
          const response = await api.post("/register", {
            name: this.name,
            email: this.email,
            password: this.password
          });
  
          this.message = response.data.message;
        } catch (error) {
          console.error("Hata:", error.response);
          this.message = (error.response?.data?.message || "Bilinmeyen hata");
        }
      }
    }
  };
  </script>
  