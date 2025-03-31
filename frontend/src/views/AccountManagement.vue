<template>
  <div class="account-management">
    <h2>Account Management</h2>
    <form @submit.prevent="updateAccount">
      <div class="form-group">
        <label for="username">New Username:</label>
        <input
          type="text"
          id="username"
          v-model="username"
          placeholder="New Username"
        />
      </div>

      <div class="form-group">
        <label for="email">New Email:</label>
        <input
          type="email"
          id="email"
          v-model="email"
          placeholder="New Email"
        />
      </div>

      <div class="form-group">
        <label for="new-password">New Password:</label>
        <input
          type="password"
          id="new-password"
          v-model="newPassword"
          placeholder="New Password"
        />
      </div>

      <div class="form-group">
        <label for="confirm-password">Confirm Password:</label>
        <input
          type="password"
          id="confirm-password"
          v-model="confirmPassword"
          placeholder="Confirm Password"
        />
      </div>

      <button class="ghost-round full-width" type="submit">Update</button>
      <p v-if="message" :class="alertClass">{{ message }}</p>
    </form>
  </div>
</template>

<script>
import api from "@/api/axios";
import { useStore } from "vuex";

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
    const store = useStore();
    return { store };
  },
  methods: {
    async updateAccount() {
      if (this.newPassword && this.newPassword !== this.confirmPassword) {
        this.message = "Passwords do not match!";
        this.messageType = "error";
        return;
      }

      const payload = {};
      if (this.username) payload.username = this.username;
      if (this.email) payload.email = this.email;
      if (this.newPassword) payload.password = this.newPassword;

      if (Object.keys(payload).length === 0) {
        this.message = "Please fill at least one field to update.";
        this.messageType = "error";
        return;
      }

      try {
        const response = await api.patch("/me", payload);

        this.message = response.data.message || "Account updated successfully!";
        this.messageType = "success";

        await this.fetchUser();
      } catch (error) {
        this.message = error.response?.data?.message || "Update failed";
        this.messageType = "error";
      }
    },

    async fetchUser() {
      try {
        const response = await api.get("/me");
        if (response.data.user) {
          this.store.commit("setUser", response.data.user);
        }
      } catch (error) {
        console.error("Failed to fetch user:", error);
      }
    },
  },
};
</script>

<style scoped>
.account-management {
  max-width: 400px;
  margin: auto;
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
}

h2 {
  text-align: center;
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 15px;
}

label {
  display: block;
  font-weight: bold;
}

input {
  width: 100%;
  padding: 10px;
  margin-top: 5px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

button {
  width: 100%;
  padding: 10px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}

.success-message {
  color: #4caf50;
  font-weight: bold;
  font-size: 16px;
  text-align: center;
  margin-top: 10px;
}

.error-message {
  color: #ff4d4d;
  font-weight: bold;
  font-size: 16px;
  text-align: center;
  margin-top: 10px;
  padding: 10px;
  border-radius: 5px;
}
</style>
