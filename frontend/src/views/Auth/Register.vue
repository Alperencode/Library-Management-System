<template>
    <MainHeader />
    <div class="bold-line"></div>
    <div class="container">
      <div class="window">
        <div class="overlay"></div>
        <div class="content">
          <h2 class="title">Sign Up</h2>
          <div class="input-fields">
            <input type="text" v-model="username" placeholder="Username" class="input-line full-width" />
            <input type="email" v-model="email" placeholder="Email" class="input-line full-width" />
            <input type="password" v-model="password" placeholder="Password" class="input-line full-width" />
          </div>
          <button class="ghost-round full-width" @click="register">Create Account</button>
  
          <div class="alert-container" v-if="message">
            <div :class="alertClass">
              <span v-if="messageType === 'success'" class="success-icon"></span>
              <span v-if="messageType === 'error'" class="error-icon"></span>
            </div>
            <p :class="{ 'success-text': messageType === 'success', 'error-text': messageType === 'error' }">{{ message }}</p>
          </div>
        </div>
      </div>
    </div>
    <MainFooter />
  </template>
  
  <script>
  import axios from "axios";
  import MainHeader from "@/components/MainHeader.vue";
  import MainFooter from "@/components/MainFooter.vue";
  
  export default {
    name: "AuthRegister",
    components: {
      MainHeader,
      MainFooter,
    },
    data() {
      return {
        username: "",
        email: "",
        password: "",
        message: "",
        messageType: "",
      };
    },
    computed: {
      alertClass() {
        return this.messageType === "success" ? "screenAlert-success" : "screenAlert-error";
      },
    },
    methods: {
      async register() {
        try {
          const response = await axios.post("http://127.0.0.1:8000/api/v1/register", {
            name: this.username,
            email: this.email,
            password: this.password,
          });
          this.message = response.data.message;
          this.messageType = "success";
        } catch (error) {
          this.message = error.response?.data?.message || "Registration failed";
          this.messageType = "error";
        }
      },
    },
  };
  </script>
  
  <style scoped>
 
body {
  background: url("@/assets/images/meetings-bg.jpg") no-repeat center center fixed;
  background-size: cover;
}

.title {
  text-align: center;
  color: #f5a425;
}

.remember-me {
  display: flex;
  align-items: center;
  margin: 10px 0;
}

.remember-me label {
  margin-left: 10px;
}

.alert-container {
  margin-top: 15px;
  text-align: center;
}

.success-text {
  color: green;
}

.error-text {
  color: red;
}
  </style>