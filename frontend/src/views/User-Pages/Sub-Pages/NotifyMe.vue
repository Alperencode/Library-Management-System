<template>
  <div>
    <section class="notify-list">
      <div class="container">
        <h2>Notify Me List</h2>
        <p>Here you can see the books you've requested to be notified about.</p>

        <!-- Eğer bildirim listesi boşsa mesaj göster -->
        <div v-if="notifyMeBooks.length === 0" class="no-results">
          <p class="no-results-text">
            You have not added any books to the notify me list yet.
          </p>
        </div>

        <!-- Bildirim listesine eklenen kitapları göster -->
        <div v-else>
          <div class="row grid">
            <div
              v-for="(book, index) in notifyMeBooks"
              :key="index"
              class="book-item"
            >
              <div class="book-box">
                <div class="thumb">
                  <router-link :to="book.link">
                    <img
                      :src="book.image"
                      :alt="book.title"
                      class="book-thumbnail"
                    />
                  </router-link>
                </div>
                <div class="down-content">
                  <router-link :to="book.link">
                    <h4 class="book-title">{{ book.title }}</h4>
                  </router-link>
                  <p class="text-ellipsis">
                    <strong>Author:</strong>
                    {{ book.authors.join(", ") || "Unknown" }}
                  </p>
                  <p>
                    <strong>Requested On:</strong> {{ book.requested_date }}
                  </p>
                  <button
                    class="remove-btn"
                    @click="removeFromNotifyList(book.id)"
                  >
                    Remove
                  </button>
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

const notifyMeBooks = ref([]);

const fetchNotifyMeList = async () => {
  try {
    const res = await api.get("/notify-me-list");
    notifyMeBooks.value = res.data.books.map((book) => ({
      id: book.id,
      title: book.title || "No Title",
      image: book.cover_image || defaultCover,
      link: `/book/${book.id}`,
      authors: book.authors || [],
      requested_date: book.requested_date || "Unknown",
    }));
  } catch (error) {
    console.error("Error retrieving notify me list:", error);
  }
};

const removeFromNotifyList = async (bookId) => {
  try {
    await api.delete(`/notify-me-list/${bookId}`);
    notifyMeBooks.value = notifyMeBooks.value.filter(
      (book) => book.id !== bookId
    );
  } catch (error) {
    console.error("Error removing book from notify me list:", error);
  }
};

onMounted(fetchNotifyMeList);
</script>

<style scoped>
.notify-list {
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

.book-item {
  width: 100%;
}

@media (min-width: 768px) {
  .book-item {
    width: calc(33.333% - 20px);
  }
}

.book-box {
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

.remove-btn {
  background-color: #e74c3c;
  color: white;
  border: none;
  padding: 8px 12px;
  border-radius: 5px;
  font-size: 14px;
  cursor: pointer;
  margin-top: 10px;
  width: 100%;
  text-align: center;
}

.remove-btn:hover {
  background-color: #c0392b;
}
</style>
