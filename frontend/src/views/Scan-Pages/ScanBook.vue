<template>
  <div class="scan-page">
    <h2 class="scan-title">Scan a Book</h2>
    <p>Scan books to:</p>
    <li>- Return a book you own</li>
    <li>- Borrow a book you like</li>
    <li>- Extend the return date</li>
    <p></p>
    <p>Feel free to use the options below to identify your book!</p>

    <div class="scan-options">
      <button class="scan-btn" @click="goToRfidScan">RFID Scan</button>
      <button class="scan-btn" @click="goToBarcodeScan">Barcode Scan</button>
      <button class="scan-btn" @click="goToIsbnSearch">ISBN Search</button>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from "vue-router";

const router = useRouter();

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
  background: url("@/assets/images/meetings-bg.jpg") no-repeat center center fixed;
  background-size: cover;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  padding-top: 100px;
  color: white;
}

.scan-title {
  font-size: 28px;
  font-weight: bold;
  margin-bottom: 10px;
  color: white;
}

.scan-page p {
  color: white;
  font-size: 16px;
  margin-bottom: 30px;
}

.scan-options {
  display: flex;
  justify-content: center;
  gap: 30px;
  margin-bottom: 30px;
}

.scan-btn {
  padding: 14px 24px;
  font-size: 20px;
  border: none;
  border-radius: 10px;
  background-color: #3b63ff;
  color: white;
  cursor: pointer;
  transition: 0.3s;
  max-width: 300px;
  width: 100%;
}

.scan-btn:hover {
  background-color: #254edb;
}

.popular-books {
  margin-top: 50px;
  padding: 20px;
  background-color: rgba(255, 255, 255, 0.85);
  border-radius: 10px;
  max-width: 900px;
  margin-left: auto;
  margin-right: auto;
  color: #222;
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
  color: #333;
}

.book-author {
  font-style: italic;
  color: #777;
  font-size: 14px;
}
</style>