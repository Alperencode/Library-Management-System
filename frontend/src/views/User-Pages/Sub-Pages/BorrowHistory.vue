<template>
  <div>
    <section class="borrow-history">
      <div class="container">
        <h2>Borrow History</h2>
        <p>Here you can see the books you have previously borrowed.</p>

        <!-- Eğer ödünç alınan kitap yoksa mesaj göster -->
        <div v-if="borrowHistory.length === 0" class="no-results">
          <p class="no-results-text">You have not borrowed any books yet.</p>
        </div>

        <!-- Ödünç alınan kitapları listele -->
        <div v-else>
          <div class="row grid">
            <div
              v-for="(book, index) in borrowHistory"
              :key="index"
              class="history-item"
            >
              <div class="history-box">
                <div class="thumb">
                  <img
                    :src="book.image"
                    :alt="book.title"
                    class="book-thumbnail"
                  />
                </div>
                <div class="down-content">
                  <h4 class="book-title">{{ book.title }}</h4>
                  <p class="text-ellipsis">
                    <strong>Author:</strong>
                    {{ book.authors.join(", ") || "Unknown" }}
                  </p>
                  <p class="text-ellipsis" :title="book.publisher">
                    <strong>Publisher:</strong> {{ book.publisher }}
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import api from "@/api/axios";
import defaultCover from "@/assets/images/default-cover.png";

const borrowHistory = ref([]);

const fetchBorrowHistory = async () => {
  try {
    const res = await api.get("/borrowed/history");
    borrowHistory.value = res.data.books.map((book) => ({
      id: book.id,
      title: book.title || "No Title",
      image: book.cover_image || defaultCover,
      authors: book.authors || [],
      publisher: book.publisher || "Unknown",
    }));
  } catch (error) {
    console.error("Error retrieving borrow history:", error);
  }
};

onMounted(fetchBorrowHistory);
</script>

<style scoped>
.borrow-history {
  padding-top: 40px;
  min-height: auto;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
}

.no-results {
  color: #ffffff !important;
  padding: 20px;
  font-size: 18px;
  text-align: center;
  border-radius: 8px;
  font-weight: 600;
  position: relative;
}

.no-results-text {
  color: black !important;
  font-size: 15px;
  font-weight: bold;
}
.grid {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  margin-top: 20px;
}

.history-item {
  width: 100%;
}

@media (min-width: 768px) {
  .history-item {
    width: calc(33.333% - 20px);
  }
}

.history-box {
  border: 1px solid #ccc;
  padding: 10px;
  border-radius: 8px;
  background-color: white;
  height: 100%;
  min-height: 100px;
}

.thumb {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 180px;
  background-color: #ffffff;
  padding: 8px;
  overflow: hidden;
  border-radius: 8px;
}

.book-thumbnail {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}

.down-content {
  text-align: left;
  padding: 10px;
}

.down-content h4 {
  margin-bottom: 8px;
  text-align: center;
}

.down-content p {
  margin: 4px 0;
  font-size: 14px;
}

.book-title {
  text-align: center;
  margin-bottom: 8px;
}

.text-ellipsis {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  display: block;
  width: 100%;
  max-width: 100%;
}
</style>
