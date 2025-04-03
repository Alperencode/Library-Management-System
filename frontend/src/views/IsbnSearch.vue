<template>
    <div class="how-to-page">
      <MainHeader />
  
      <h2 class="how-to-title">How to Use ISBN Search</h2>
      <p class="how-to-description">
        To search for a book by ISBN:
        <ul>
          <li>Enter the book's ISBN into the search field.</li>
          <li>Click "Submit" to get the book information based on the ISBN.</li>
        </ul>
      </p>
  
      <div v-if="isbnInputVisible" class="isbn-search-container">
        <input
          v-model="isbn"
          type="text"
          placeholder="Enter ISBN"
          class="isbn-input"
        />
        <button class="scan-btn" @click="searchIsbn">Submit</button>
      </div>
  
      <button v-else class="scan-btn" @click="startIsbnSearch">Start ISBN Search</button>
  
      <MainFooter />
    </div>
  </template>
  
  <script setup>
  import { ref } from "vue";
  import MainHeader from "@/components/MainHeader.vue";
  import MainFooter from "@/components/MainFooter.vue";
  
  const isbnInputVisible = ref(false);
  const isbn = ref(""); 
  
  const startIsbnSearch = () => {
    isbnInputVisible.value = true;
  };
  
  const searchIsbn = () => {
    if (isbn.value.trim()) {
      alert(`Searching for ISBN: ${isbn.value}`); 
    } else {
      alert("Please enter a valid ISBN.");
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
  
  .isbn-search-container {
    margin-top: 20px;
  }
  
  .isbn-input {
    padding: 10px;
    font-size: 18px;
    width: 250px;
    margin-right: 10px;
  }
  
  </style>
  