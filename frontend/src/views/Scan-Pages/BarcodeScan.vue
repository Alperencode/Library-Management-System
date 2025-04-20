<template>
  <div class="how-to-page">
    <h2 class="how-to-title">How to Use Barcode Scan</h2>
    <p class="how-to-description">
      Follow the instructions below to scan using Barcode: <br />
      `This place will be replaced by instructions image`
    </p>
    <div v-if="showVideo" class="video-container">
      <div class="video-wrapper">
        <img :src="videoUrl" class="video-stream" alt="Barcode Camera Feed" />
      </div>
    </div>

    <button class="scan-btn" @click="startBarcodeScan" :disabled="loading">
      {{ loading ? "Scanning..." : "Start Barcode Scan" }}
    </button>

  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import api from "@/api/axios";
import { useToast } from "vue-toastification";

const router = useRouter();
const toast = useToast();

const loading = ref(false);
const showVideo = ref(false);
const videoUrl = ref("");

const barcodeUrl = `${window.location.protocol}//${process.env.VUE_APP_API_HOST}:${process.env.VUE_APP_BARCODE_PORT}`;

const startBarcodeScan = async () => {
  loading.value = true;
  toast.clear();

  showVideo.value = true;
  videoUrl.value = `${barcodeUrl}/api/v1/barcode/video`;

  try {
    const response = await fetch(`${barcodeUrl}/api/v1/barcode/scan`, {
      method: "GET",
      credentials: "include",
    });

    await fetch(`${barcodeUrl}/api/v1/barcode/video`, {
      method: "GET",
      credentials: "include",
    });


    const result = await response.json();

    if (response.ok && result.code === "Success") {
      toast.success(result.message || "Barcode scanned!");

      setTimeout(async () => {
        await handleIsbn(result.data);
      }, 2500);
    } else {
      toast.error(result.message || "Barcode scan failed.");
      setTimeout(async () => {
        router.push("/scan-book")
      }, 2500);
    }
  } catch (err) {
    toast.error("Barcode scanner is not responding or unreachable.");
    console.error(err);
  } finally {
    loading.value = false;
  }
};

const handleIsbn = async (isbn) => {
  try {
    const res = await api.get("/books/search/", {
      params: { q: isbn },
    });

    const books = res.data.books;
    if (Array.isArray(books) && books.length > 0 && books[0]?.id) {
      router.push(`/scan-book/${books[0].id}`);
    } else {
      throw new Error("Book not found.");
    }
  } catch (err) {
    toast.error(err.response?.data?.message || "Book fetch failed.");

    router.push("/scan-book")
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
  padding: 40px 20px;
}

.how-to-title {
  padding-top: 120px;
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

.video-container {
  margin-top: 40px;
  display: flex;
  justify-content: center;
  padding: 20px;
}

.video-wrapper {
  border: 4px solid white;
  border-radius: 16px;
  padding: 10px;
  background-color: #000;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.5);
  max-width: 90%;
  width: 720px;
}

.video-stream {
  width: 100%;
  height: auto;
  border-radius: 10px;
  display: block;
}
</style>
