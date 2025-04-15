<template>
  <div class="how-to-page">
    <h2 class="how-to-title">How to Use RFID Scan</h2>
    <p class="how-to-description">
      Follow the instructions below to scan using RFID:
      `This place will be replaced by instructions image`
    </p>

    <button class="scan-btn" @click="startRfidScan" :disabled="loading">
      {{ loading ? "Scanning..." : "Start RFID Scan" }}
    </button>

    <div v-if="rfidFailed" class="error-message">
      RFID scan failed. Please try again.
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import api from "@/api/axios";
import { useToast } from 'vue-toastification'

const router = useRouter();

const rfidFailed = ref(false);
const loading = ref(false);
const toast = useToast()

const rfidUrl = `${window.location.protocol}//${process.env.VUE_APP_API_HOST}:${process.env.VUE_APP_RFID_PORT}`;

const startRfidScan = async () => {
  loading.value = true;
  rfidFailed.value = false;

  try {
    const response = await fetch(`${rfidUrl}/api/v1/read`, {
      method: 'GET',
      credentials: 'include'
    });

    if (!response.ok) {
      console.warn("RFID failed, using fallback ISBN");
      throw new Error("Simulated fallback trigger");
    }

    const result = await response.json();

    if (result.code === "Success") {
      if (result.message) {
        toast.success(result.message)
      }
      await handleIsbn(result.data);
    } else {
      throw new Error("RFID scan unsuccessful");
    }
  } catch (err) {
    console.error("RFID Scan error:", err);
  } finally {
    loading.value = false;
  }
};

const handleIsbn = async (isbn) => {
  try {
    const searchResponse = await api.get("/books/search/", {
      params: { q: isbn }
    });

    console.log("Search API Response:", searchResponse.data);

    const books = searchResponse.data.books;

    if (Array.isArray(books) && books.length > 0 && books[0]?.id) {
      router.push(`/scan-book/${books[0].id}`);
    } else {
      throw new Error("Book not found.");
    }
  } catch (error) {
    console.error("Book fetch error:", error);
    rfidFailed.value = true;
  }
};


</script>

<style scoped>
.how-to-page {
  text-align: center;
  min-height: 100vh;
  background: url("@/assets/images/meetings-bg.jpg") no-repeat center center fixed;
  background-size: cover;
  display: flex;
  flex-direction: column;
  justify-content: top;
}

.how-to-title {
  padding-top: 200px;
  color: aliceblue;
  font-size: 28px;
  font-weight: bold;
  margin-bottom: 20px;
}

.how-to-description {
  color: aliceblue;
  font-size: 18px;
  margin: 20px;
}

.scan-btn {
  padding: 18px 28px;
  font-size: 22px;
  border: none;
  border-radius: 10px;
  background-color: #007bff;
  color: white;
  cursor: pointer;
  transition: 0.3s;
  max-width: 300px;
  width: 100%;
  margin: 10px auto;
}

.scan-btn:hover {
  background-color: #0056b3;
}

.error-message {
  color: red;
  font-weight: bold;
  margin-top: 20px;
}
</style>
