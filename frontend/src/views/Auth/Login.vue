<template>
  <div class="auth-container">
    <MainHeader />
    <div class="login-box">
      <h2>Login</h2>
      <form @submit.prevent="login">
        <div class="form-group">
          <label>Email</label>
          <input type="email" v-model="email" placeholder="Email" required />
        </div>
        <div class="form-group">
          <label>Password</label>
          <input type="password" v-model="password" placeholder="Password" required />
        </div>
        <div class="form-group remember-me">
          <input type="checkbox" id="rememberMe" v-model="rememberMe" />
          <label for="rememberMe">Remember Me</label>
        </div>
        <button class="btn-primary" type="submit">Sign in</button>
      </form>
    </div>
    <MainFooter />
  </div>
</template>

<script>
import axios from "axios";
import MainHeader from "@/components/MainHeader.vue";
import MainFooter from "@/components/MainFooter.vue";
export default {
  name: "AuthLogin",
  components: {
    MainHeader,
    MainFooter,
  },
  data() {
    return {
      email: "",
      password: "",
      rememberMe: false,
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
    async login() {
      try {
        const response = await axios.post("http://127.0.0.1:8000/api/v1/login", {
          email: this.email,
          password: this.password,
          remember_me: this.rememberMe,
        });
        this.message = response.data.message;
        this.messageType = "success";
      } catch (error) {
        this.message = error.response?.data?.message || "Login failed";
        this.messageType = "error";
      }
    },
  },
};
</script>

<style scoped>
.auth-container {
  width: 100vw;
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: url('@/assets/images/meetings-bg.jpg') no-repeat center center fixed;
  position: fixed;
  top: 0;
  left: 0;
  z-index: 9999;
}

.auth-page {
  width: 100vw;
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f8f9fa;
}

body {
    font-family: 'Lato', sans-serif;
    background: url('@/assets/images/meetings-bg.jpg') no-repeat center center fixed;
    height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
}

.login-wrap {
    background: rgba(255, 255, 255, 0.9);
    padding: 30px;
    border-radius: 10px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

h2 {
  color: white; /* Login yazısını görünür hale getir */
  text-align: center;
  font-size: 24px;
}

label {
  color: white; /* Remember Me yazısını görünür hale getir */
  font-size: 16px;
}

.form-group input {
    width: 100%;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 5px;
    font-size: 16px;
}

.field-icon {
    float: right;
    margin-right: 10px;
    margin-top: -30px;
    position: relative;
    cursor: pointer;
}

.btn-primary {
    background-color: #007bff;
    border: none;
    padding: 10px;
    font-size: 18px;
    width: 100%;
    border-radius: 5px;
}

.btn-primary:hover {
    background-color: #0056b3;
}

input[type="checkbox"] {
  appearance: none;
  width: 20px;
  height: 20px;
  border: 2px solid #ccc;
  border-radius: 4px;
  position: relative;
  cursor: pointer;
  outline: none;
  background-color: white;
  transition: background 0.3s, border-color 0.3s;
}

input[type="checkbox"]:checked {
  background-color: #f5a425;
  border-color: #f5a425;
}

input[type="checkbox"]:checked::after {
  content: "✔";
  font-size: 14px;
  color: white;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.footer {
    text-align: center;
    color: white;
    position: absolute;
    bottom: 10px;
    width: 100%;
}

@import url(https://fonts.googleapis.com/css?family=Roboto:400,300,100,500);

body,
html {
  margin: 0;
  height: 100%;
}

input {
  border: none;
}

button:focus {
  outline: none;
}

::-webkit-input-placeholder {
  color: rgba(255, 255, 255, 0.65);
}

::-webkit-input-placeholder .input-line:focus +::input-placeholder {
  color: #fff;
}

.highlight {
  color: rgba(255, 255, 255, 0.8);
  font-weight: 400;
  cursor: pointer;
  transition: color .2s ease;
}

.highlight:hover {
  color: #fff;
  transition: color .2s ease;
}

.spacing {
  flex-grow: 1;
  height: 120px;
  font-weight: 300;
  text-align: center;
  margin-top: 10px;
  color: rgba(255, 255, 255, 0.65)
}

.input-line:focus {
  outline: none;
  border-color: #fff;
  transition: all .2s ease;
}

.ghost-round {
  cursor: pointer;
  background: none;
  border: 1px solid rgba(255, 255, 255, 0.65);
  border-radius: 25px;
  color: rgba(255, 255, 255, 0.65);
  align-self: flex-end;
  font-size: 1.2rem;
  font-family: roboto;
  font-weight: 300;
  line-height: 2.5em;
  margin-top: auto;
  margin-bottom: 25px;
  transition: all .2s ease;
}

.ghost-round:hover {
  background: rgba(255, 255, 255, 0.15);
  color: #fff;
  transition: all .2s ease;
}

.input-line {
  background: none;
  margin-bottom: 10px;
  line-height: 2.4em;
  color: #fff;
  font-family: roboto;
  font-weight: 300;
  font-size: 1.2rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.65);
  transition: all .2s ease;
}

.full-width {
  width: 100%;
}

.input-fields {
  margin-top: 25px;
}

.content {
  padding-left: 30px;
  padding-right: 30px;
  display: flex;
  flex-flow: column;
  z-index: 5;
}

.welcome {
  font-weight: 200;
  margin-top: 75px;
  text-align: center;
  font-size: 2.5rem;
}

.subtitle {
  text-align: center;
  line-height: 1em;
  font-weight: 100;
}

.menu {
  background: rgba(0, 0, 0, 0.2);
  width: 100%;
  height: 50px;
}

.window {
  z-index: 100;
  color: #fff;
  font-family: roboto;
  position: relative;
  display: flex;
  flex-flow: column;
  box-shadow: 0px 15px 50px 10px rgba(0, 0, 0, 0.2);
  box-sizing: border-box;
  height: 300px;
  width: 360px;
  margin: auto;
  background: url('https://pexels.imgix.net/photos/27718/pexels-photo-27718.jpg?fit=crop&w=1280&h=823') top left no-repeat;
}

.overlay {
  
  opacity: 0.85;
  height: 300px;
  position: absolute;
  width: 360px;
  z-index: 1;
}

.bold-line {
  background: #e7e7e7;
  position: absolute;
  top: 0px;
  bottom: 0px;
  margin: auto;
  width: 100%;
  height: 360px;
  z-index: 1;
  opacity: 0.1;
  background: url('https://pexels.imgix.net/photos/27718/pexels-photo-27718.jpg?fit=crop&w=1280&h=823') left no-repeat;
  background-size: cover;
}

@media (max-width: 500px) {
  .window {
    width: 100%;
    height: 100%;
  }
  .overlay {
    width: 100%;
    height: 100%;
  }
}

</style>
