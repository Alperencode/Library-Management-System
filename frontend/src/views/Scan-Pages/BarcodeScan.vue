<template>
  <div class="how-to-page">
    <div class="blur-header">
      <h2 class="how-to-title">How to Use Barcode Scan</h2>
      <p class="how-to-description" >
        Follow the instructions below to scan the book's barcode:
      </p>
    </div>

    <div class="barcode-scan-container" ref="instructions">
      <img src="@/assets/images/Horizontal-Barcode-Scan-Instructions.png" alt="Barcode Scan Instructions"
        class="barcode-image" />
    </div>

    <div v-if="showVideo" class="video-container" ref="videoContainer">
      <div class="video-wrapper">
        <img :src="videoUrl" class="video-stream" alt="Barcode Camera Feed" />
      </div>
    </div>

    <button class="scan-btn" @click="startBarcodeScan" :disabled="loading" ref="scanButton">
      {{ loading ? "Scanning..." : "Start Barcode Scan" }}
    </button>

    <p class="support-message">
      If you experience any issues during the scanning process, please contact the librarian or a staff member.
    </p>
  </div>
</template>

<script setup>
import { ref, nextTick, onMounted } from "vue";
import { useRouter } from "vue-router";
import api from "@/api/axios";
import { useToast } from "vue-toastification";

const router = useRouter();
const toast = useToast();

const loading = ref(false);
const showVideo = ref(false);
const videoUrl = ref("");
const videoContainer = ref(null);
const instructions = ref(null);

const barcodeUrl = `${window.location.protocol}//${process.env.VUE_APP_API_HOST}:${process.env.VUE_APP_BARCODE_PORT}`;

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

const startBarcodeScan = async () => {
  loading.value = true;
  toast.clear();

  showVideo.value = true;
  videoUrl.value = `${barcodeUrl}/api/v1/barcode/video`;


  await nextTick();

  setTimeout(() => {
    if (videoContainer.value) {
      const elementTop = videoContainer.value.getBoundingClientRect().top + window.scrollY;
      const elementHeight = videoContainer.value.offsetHeight;
      const viewportHeight = window.innerHeight;

      const scrollTo = elementTop - (viewportHeight / 2) + (elementHeight / 2);
      window.scrollTo({ top: scrollTo, behavior: "smooth" });
    }
  }, 2000);

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
        router.push("/scan-book");
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
  align-items: center;
  padding: 150px 20px;
  font-family: 'Segoe UI', sans-serif;
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

.how-to-title {
  font-size: 30px;
  color: #fff;
  margin-bottom: 10px;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.4);
}

.how-to-description {
  font-size: 16px;
  color: #fffae3;
}

.barcode-scan-container {
  background-color: #fff;
  padding: 30px;
  border-radius: 16px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
  max-width: 1500px;
  width: 100%;
  margin-bottom: 20px;
  text-align: center;
}

.barcode-image {
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

.support-message {
  font-size: 14px;
  color: #ffffffcc;
  margin-top: 40px;
  text-align: center;
  font-style: italic;
}

.video-container {
  margin-top: 10px;
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


.how-to-description {
  font-size: 16px;
  color: #fffae3;
  margin-bottom: 0;
}
</style>
