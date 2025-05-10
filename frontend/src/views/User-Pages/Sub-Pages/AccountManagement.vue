<template>
  <div class="page-background">
    <div class="account-management">
      <h2>Account Management</h2>
      <form @submit.prevent="updateAccount">
        <div class="form-group">
          <label for="username">New Username:</label>
          <div class="input-wrapper">
            <i class="fas fa-user"></i>
            <input type="text" id="username" v-model="username" placeholder="New Username" />
          </div>
        </div>

        <div class="form-group">
          <label for="email">New Email:</label>
          <div class="input-wrapper">
            <i class="fas fa-envelope"></i>
            <input type="email" id="email" v-model="email" placeholder="New Email" />
          </div>
        </div>

        <div class="form-group">
          <label for="new-password">New Password:</label>
          <div class="input-wrapper">
            <i class="fas fa-lock"></i>
            <input type="password" id="new-password" v-model="newPassword" placeholder="New Password" />
          </div>
        </div>

        <div class="form-group">
          <label for="confirm-password">Confirm Password:</label>
          <div class="input-wrapper">
            <i class="fas fa-lock"></i>
            <input type="password" id="confirm-password" v-model="confirmPassword" placeholder="Confirm Password" />
          </div>
        </div>

        <button class="ghost-round full-width" type="submit">Update</button>
        <p v-if="message" :class="alertClass">{{ message }}</p>
      </form>
    </div>
  </div>
</template>

<script>
import api from "@/api/axios";
import { useToast } from "vue-toastification";
import { useAuth } from "@/composables/useAuth";

const toast = useToast();

export default {
  name: "AccountManagement",
  data() {
    return {
      username: "",
      email: "",
      newPassword: "",
      confirmPassword: "",
      message: "",
      messageType: "",
    };
  },
  computed: {
    alertClass() {
      return this.messageType === "success"
        ? "success-message"
        : "error-message";
    },
  },
  setup() {
    const { setUser } = useAuth();
    return { setUser };
  },
  methods: {
    async updateAccount() {
      if (this.newPassword && this.newPassword !== this.confirmPassword) {
        toast.error("Passwords do not match!");
        return;
      }

      const payload = {};
      if (this.username) payload.username = this.username;
      if (this.email) payload.email = this.email;
      if (this.newPassword) payload.password = this.newPassword;

      if (Object.keys(payload).length === 0) {
        toast.error("Please fill at least one field to update.");
        return;
      }

      try {
        const response = await api.patch("/me", payload);
        toast.success(response.data.message || "Account updated successfully!");
        await this.fetchUser();
      } catch (error) {
        console.error("Update failed:", error);
      }
    },

    async fetchUser() {
      try {
        const response = await api.get("/me");
        if (response.data.user) {
          this.setUser(response.data.user);
        }
      } catch (error) {
        console.error("Failed to fetch user:", error);
      }
    },
  },
};
</script>

<style scoped>
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css');

.page-background {
  min-height: 100vh;
  width: 90%;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 40px 20px;
}

.account-management {
  width: 100%;
  max-width: 700px;
  padding: 40px;
  background: rgba(255, 255, 255, 0.3);
  -webkit-backdrop-filter: blur(10px);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(255, 255, 255, 0.3);
}

h2 {
  text-align: center;
  margin-bottom: 30px;
  font-size: 26px;
  color: #ffffff;
}

.form-group {
  margin-bottom: 22px;
}

label {
  display: block;
  font-weight: 600;
  margin-bottom: 6px;
  color: #ffffff;
}

.input-wrapper {
  position: relative;
}

.input-wrapper i {
  position: absolute;
  top: 50%;
  left: 12px;
  transform: translateY(-50%);
  color: #adb5bd;
}

input {
  width: 100%;
  padding: 12px 14px 12px 36px;
  border: 1px solid #d0d7de;
  border-radius: 8px;
  font-size: 15px;
  background-color: #ffffff;
  transition: border-color 0.3s;
}

input:focus {
  border-color: #ffa600cc;
  outline: none;
}

button {
  width: 50%;
  padding: 12px;
  background: #ffa500cc;
  color: #fff;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.3s ease;
  display: block;
  margin: 0 auto;
}

button:hover {
  background: #dd9000cc;
}

</style>
