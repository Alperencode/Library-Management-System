<template>
  <div class="register-page">
    <div class="register-wrapper">
      <div class="register-form-container">
        <h2 class="title">Register</h2>
        <div class="input-fields">
          <input type="text" v-model="username" placeholder="Name" class="input-line full-width" />
          <input type="email" v-model="email" placeholder="Email" class="input-line full-width" />
          <input type="password" v-model="password" placeholder="Password" class="input-line full-width" />
        </div>
        <div class="spacer"></div>
        <button class="ghost-round full-width" @click="register">Register</button>
      </div>
    </div>
  </div>
</template>

<script>
import api from "@/api/axios";
import { useRouter } from "vue-router";
import { useToast } from "vue-toastification";
import { useAuth } from "@/composables/useAuth";

const toast = useToast();

export default {
  name: "AuthRegister",

  data() {
    return {
      username: "",
      email: "",
      password: "",
    };
  },

  setup() {
    const router = useRouter();
    const { setUser } = useAuth();
    return { router, setUser };
  },

  methods: {
    async register() {
      try {
        const response = await api.post("/register", {
          username: this.username,
          email: this.email,
          password: this.password,
        });

        toast.success(response.data.message);

        if (response.data.user) {
          this.setUser(response.data.user);
          this.router.push("/");
        } else {
          toast.error("Registration failed. Unexpected response.");
        }
      } catch (error) {
        const msg = error?.response?.data?.message || "Registration failed. Please try again.";
        toast.error(msg);
      }
    }
  },
};
</script>


<style scoped>
.register-page {
  display: flex;
  flex-direction: column;
  min-height: 92.3vh;
  background: url('@/assets/images/meetings-bg.jpg') no-repeat center center fixed;
  background-size: cover;
}

.register-wrapper {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
}

.register-form-container {
  width: 100%;
  max-width: 600px;
  padding: 30px;
  color: white;
}

.title {
  text-align: center;
  font-size: 24px;
  margin-bottom: 20px;
}

.input-fields {
  margin-top: 20px;
}

.full-width {
  width: 100%;
}

.input-line {
  background: none;
  margin-bottom: 10px;
  line-height: 2.4em;
  color: #fff;
  font-family: Roboto, sans-serif;
  font-weight: 300;
  font-size: 1.2rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.65);
  transition: all 0.2s ease;
}

.ghost-round {
  cursor: pointer;
  background: none;
  border: 1px solid rgba(255, 255, 255, 0.65);
  border-radius: 25px;
  color: rgba(255, 255, 255, 0.65);
  font-size: 1.2rem;
  line-height: 2.5em;
  margin-top: auto;
  transition: all 0.2s ease;
}

.ghost-round:hover {
  background: #d4881a;
  border-color: #d4881a;
  color: white;
  box-shadow: 0 0 10px rgba(245, 164, 37, 0.7);
}

.spacer {
  height: 20px;
}

.success-text {
  color: #4caf50;
  font-weight: bold;
  font-size: 16px;
  text-align: center;
  margin-top: 10px;
}

.error-text {
  color: #ff4d4d;
  font-weight: bold;
  font-size: 16px;
  text-align: center;
  margin-top: 10px;
  padding: 10px;
  border-radius: 5px;
}

.spacer {
  height: 20px;
}

.auth-container {
  width: 100vw;
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: url('@/assets/images/meetings-bg.jpg');
  position: fixed;
  top: 0;
  left: 0;
  z-index: 9999;
}

body {
  font-family: 'Lato', sans-serif;
  background: url('@/assets/images/meetings-bg.jpg') no-repeat center center fixed;
  background-size: cover;
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
  color: white;
  text-align: center;
  font-size: 24px;
}

label {
  color: white;
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

::-webkit-input-placeholder .input-line:focus+::input-placeholder {
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
  background: #d48d29;
  border-color: #d48d29;
  color: white;
  box-shadow: 0 0 10px rgba(245, 164, 37, 0.7);
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
  width: 600px;
  min-height: 300px;
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