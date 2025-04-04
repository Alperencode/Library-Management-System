<template>
  <div class="scan-page">
    <h2 class="scan-title">Scan a Book</h2>

    <div class="scan-options">
      <button class="scan-btn" @click="goToRfidScan">RFID Scan</button>
      <button class="scan-btn" @click="goToBarcodeScan">Barcode Scan</button>
      <button class="scan-btn" @click="goToIsbnSearch">ISBN Search</button>
    </div>

    <div v-if="popularBooks.length > 0" class="popular-books">
      <h3 class="popular-title">You might also like</h3>
      <div class="book-list">
        <div class="book-item">
          <img
            src="https://via.placeholder.com/100x150"
            alt="Book Image"
            class="book-image"
          />
          <p class="book-title">Book 1</p>
          <p class="book-author">Author 1</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();

const popularBooks = ref([]);

const fetchPopularBooks = async () => {
  try {
    const response = await fetch("/api/v1/books/search/popular");
    const data = await response.json();
    console.log(data);
    if (data.code === "Success") {
      popularBooks.value = data.books;
    }
  } catch (error) {
    console.error("Failed to fetch popular books", error);
  }
};

onMounted(() => {
  fetchPopularBooks();
});

const goToRfidScan = () => {
  router.push("/rfid-scan");
};

const goToBarcodeScan = () => {
  router.push("/barcode-scan");
};

const goToIsbnSearch = () => {
  router.push("/isbn-search");
};
</script>

<style scoped>
.scan-page {
  text-align: center;
  min-height: 100vh;
  background: url("@/assets/images/meetings-bg.jpg") no-repeat center center
    fixed;
  background-size: cover;
  display: flex;
  flex-direction: column;
  justify-content: top;
}

.scan-title {
  font-size: 28px;
  font-weight: bold;
  margin-bottom: 20px;
}

.scan-options {
  display: flex;
  justify-content: center;
  gap: 30px;
  margin-top: 160px;
  margin-bottom: 30px;
}

.scan-btn {
  padding: 14px 24px;
  font-size: 20px;
  border: none;
  border-radius: 10px;
  background-color: #007bff;
  color: white;
  cursor: pointer;
  transition: 0.3s;
  max-width: 300px; /* Butonun maksimum genişliği */
  width: 100%; /* Küçük ekranlarda tam genişlik kullanır */
}

.scan-btn:hover {
  background-color: #0056b3;
}

.popular-books {
  margin-top: 50px;
  padding: 20px;
  background-color: rgba(255, 255, 255, 0.8);
  border-radius: 10px;
  max-width: 900px;
  margin: 0 auto;
}

.popular-title {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 20px;
  color: #333;
}

.book-list {
  display: flex;
  justify-content: space-between;
  gap: 20px;
  flex-wrap: wrap;
}

.book-item {
  text-align: center;
  max-width: 150px;
  background-color: #f8f8f8;
  padding: 10px;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.book-image {
  width: 100px;
  height: 150px;
  object-fit: cover;
  border-radius: 8px;
}

.book-title {
  font-weight: bold;
  margin-top: 10px;
  font-size: 16px;
}

.book-author {
  font-style: italic;
  color: #777;
  font-size: 14px;
}
</style>
