<template>
  <div class="how-to-page">
    <div class="blur-header">
      <h2 class="how-to-title">How to Use RFID Scan</h2>
      <p class="how-to-description">Follow the instructions below to scan using RFID:</p>
    </div>
    <div class="rfid-scan-container" ref="instructions">
      <img src="@/assets/images/Horizontal-RFID-Scan-Instructions.png" alt="RFID Scan Instructions"
        class="rfid-image" />
    </div>
    <button class="scan-btn" @click="startRfidScan" :disabled="loading">
      {{ loading ? "Scanning..." : scanButtonText }}
    </button>
    <p class="support-message">
      If you experience any issues during the scanning process, please contact the librarian or a staff member.
    </p>
  </div>
</template>

<script setup>
import { ref, nextTick, onMounted, onBeforeUnmount } from "vue";
import { useRouter } from "vue-router";
import api from "@/api/axios";
import { useToast } from 'vue-toastification';

const router = useRouter();

const rfidFailed = ref(false);
const loading = ref(false);
const toast = useToast();
const scanButtonText = ref("Start RFID Scan");
const instructions = ref(null);
const abortController = ref(null);

const rfidUrl = `${window.location.protocol}//${process.env.VUE_APP_API_HOST}:${process.env.VUE_APP_RFID_PORT}`;

onMounted(() => {
  nextTick(() => {
    setTimeout(() => {
      if (instructions.value) {
        const elementTop = instructions.value.getBoundingClientRect().top + window.scrollY;
        const elementHeight = instructions.value.offsetHeight;
        const viewportHeight = window.innerHeight;

        const scrollTo = elementTop - (viewportHeight / 2) + (elementHeight / 2);
        window.scrollTo({ top: scrollTo, behavior: "smooth" });
      }
    }, 1000);
  });
});

onBeforeUnmount(() => {
  if (abortController.value) {
    abortController.value.abort();
  }
});

const startRfidScan = async () => {
  loading.value = true;
  rfidFailed.value = false;
  scanButtonText.value = "Start RFID Scan";

  abortController.value = new AbortController();
  const signal = abortController.value.signal;

  try {
    const response = await fetch(`${rfidUrl}/api/v1/read`, {
      method: 'GET',
      credentials: 'include',
      signal
    });

    const result = await response.json();

    if (response.ok) {
      if (result.code === "Success") {
        if (result.message) toast.success(result.message);
        setTimeout(async () => {
          await handleIsbn(result.data);
        }, 1000);
      } else {
        toast.error(result.message || "RFID scan failed");
      }
    } else {
      toast.error(result.message || "RFID scan failed due to server error");
    }

  } catch (err) {
    if (err.name === 'AbortError') {
      toast.warning("RFID scan request was aborted due to route change.");
    } else {
      console.error("RFID Scan error:", err);
      toast.error("RFID scanner is not responding or unreachable.");
    }
  } finally {
    loading.value = false;
  }
};

const handleIsbn = async (isbn, rfidMessage = null) => {
  try {
    const searchResponse = await api.get("/books/search/", {
      params: { q: isbn }
    });

    const books = searchResponse.data.books;

    if (Array.isArray(books) && books.length > 0 && books[0]?.id) {
      const message = rfidMessage || searchResponse.data.message || "Book scanned successfully.";
      toast.success(message);
      router.push(`/scan-book/${books[0].id}`);
    } else {
      throw new Error("Book not found.");
    }
  } catch (error) {
    console.error("Book fetch error:", error);
    rfidFailed.value = true;
    scanButtonText.value = "Retry RFID Scan";

    const errorMessage =
      error.response?.data?.message ||
      error.response?.data?.detail ||
      error.message ||
      "Book not found.";

    toast.error(errorMessage);

    setTimeout(() => {
      router.push("/scan-book");
    }, 2000);
  }
};

</script>

<style scoped>
.how-to-page {
  min-height: 100vh;
  background: url("@/assets/images/meetings-bg.jpg") no-repeat center center fixed;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 150px 20px;
  font-family: 'Segoe UI', sans-serif;
}

.how-to-title {
  font-size: 32px;
  margin-bottom: 10px;
  color: #d4881a;
  text-shadow: 1px 1px 4px rgba(0, 0, 0, 0.2);
}

.how-to-description {
  font-size: 18px;
  margin-bottom: 30px;
  text-align: center;
  max-width: 600px;
  color: #fffbe9;
}

.rfid-scan-container {
  background-color: #fff;
  padding: 20px;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  max-width: 1500px;
  width: 100%;
  margin-bottom: 60px;
  text-align: center;
}

.rfid-image {
  width: 100%;
  height: auto;
  border-radius: 16px;
  border: 3px solid #f0a623;
  box-shadow: 0 0 15px #f0a62366;
}

.scan-btn {
  background: linear-gradient(135deg, #d4881a, #f0a623);
  border: none;
  padding: 15px 25px;
  border-radius: 10px;
  font-weight: bold;
  font-size: 20px;
  color: white;
  cursor: pointer;
  transition: all 0.3s ease;
}

.scan-btn:hover {
  transform: translateY(-2px);
}

.blur-header {
  background: rgba(255, 255, 255, 0.08);
  border-radius: 16px;
  padding: 30px 40px;
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  text-align: center;
  max-width: 800px;
  margin-bottom: 30px;
}

.support-message {
  font-size: 14px;
  color: #ffffffcc;
  margin-top: 40px;
  text-align: center;
  font-style: italic;
}

.how-to-description {
  font-size: 16px;
  color: #fffae3;
  margin-bottom: 0;
}
</style>
