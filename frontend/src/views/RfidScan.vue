<template>
    <div class="how-to-page">
      <MainHeader />
  
      <h2 class="how-to-title">How to Use RFID Scan</h2>
      <p class="how-to-description">
        Follow the instructions below to scan using RFID:
        <ul>
          <li>Ensure your RFID scanner is connected and working properly.</li>
          <li>Scan the RFID tag on the book to get information.</li>
          <li>The book information will appear on the screen after a successful scan.</li>
        </ul>
      </p>
  
      <button class="scan-btn" @click="startRfidScan">Start RFID Scan</button>
  
      <div v-if="rfidFailed" class="manual-isbn-section">
        <p class="error-message">
          RFID scan failed! Please click the button below to try with ISBN.
        </p>
        <button class="scan-btn" @click="enableIsbnInput">Use ISBN to Try</button>
  
        <div v-if="isbnInputVisible">
          <input
            type="text"
            v-model="manualIsbn"
            placeholder="Enter ISBN"
            class="isbn-input"
          />
          <button class="scan-btn" @click="submitIsbn">Submit ISBN</button>
        </div>
      </div>
  
      <MainFooter />
    </div>
  </template>
  
  <script setup>
  import { ref } from "vue";
  import MainHeader from "@/components/MainHeader.vue";
  import MainFooter from "@/components/MainFooter.vue";
  
  const rfidFailed = ref(false); 
  const manualIsbn = ref(""); 
  const isbnInputVisible = ref(false); 
  
  const startRfidScan = () => {
    setTimeout(() => {
      const success = Math.random() > 0.5; 
      if (!success) {
        rfidFailed.value = true;
      } else {
        alert("RFID scan successful! Book found.");
      }
    }, 2000);
  };
  
  const enableIsbnInput = () => {
    isbnInputVisible.value = true;
  };

  const submitIsbn = () => {
    if (manualIsbn.value.trim()) {
      alert(`Manual ISBN submitted: ${manualIsbn.value}`);
    } else {
      alert("Please enter a valid ISBN.");
    }
  };
  </script>
  
  <style scoped>
  .error-message {
    color: red;
    font-weight: bold;
    margin-bottom: 10px;
  }
  
  .manual-isbn-section {
    margin-top: 40px;
  }
  
  .isbn-input {
    padding: 20px;
    font-size: 18px;
    width: 200px;
    margin-bottom: 20px;
    margin-top: 20px; 
    padding-right: 10px;
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
    margin: 0 auto;
    margin: 10px auto;
  }
  
  .scan-btn:hover {
    background-color: #0056b3;
  }
  </style>
  
  <style scoped>
  .how-to-page {
    text-align: center;
    min-height: 100vh;
    background: url("@/assets/images/meetings-bg.jpg") no-repeat center center
      fixed;
    background-size: cover;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
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

  .scan-btn:hover {
    background-color: #0056b3;
  }
  </style>
  