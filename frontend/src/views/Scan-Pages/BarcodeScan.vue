<template>
    <div class="how-to-page">
      <h2 class="how-to-title">How to Use Barcode Scan</h2>
      <p class="how-to-description">
        Follow the instructions below to scan using Barcode:
        `This place will be replaced by instructions image`
      </p>
  
      <button class="scan-btn" @click="startBarcodeScan">Start Barcode Scan</button>
  
    </div>
  </template>
  
  <script setup>
  
  const startBarcodeScan = () => {
    alert("Barcode scan started (Not implemented)"); 
  };
  </script>
  
  <style scoped>

  .how-to-page {
    text-align: center;
    min-height: 100vh;
    background: url("@/assets/images/meetings-bg.jpg") no-repeat center center
      fixed;
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
    margin: 0 auto;
  }
  
  .scan-btn:hover {
    background-color: #0056b3;
  }
  </style>
  