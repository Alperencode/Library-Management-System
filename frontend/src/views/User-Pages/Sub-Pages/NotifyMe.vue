<template>
  <div>
    <section class="notify-list">
      <div class="container">
        <h2>Notify Me List</h2>
        <p>Here you can see the books you've requested to be notified about.</p>

        <div v-if="notifyMeBooks.length === 0" class="no-results">
          <p class="no-results-text">
            You have not added any books to the notify me list yet.
          </p>
        </div>

        <div v-else>
          <div class="row grid">
            <div
              v-for="(book, index) in paginatedNotifyMeBooks"
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
                  <p class="text-ellipsis" :title="book.publisher">
                    <strong>Publisher:</strong> {{ book.publisher }}
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

          <!-- Sayfalama numaralı -->
          <div class="pagination" v-if="totalPages > 1">
            <button
              @click="goToPage(currentPage - 1)"
              :disabled="currentPage === 1"
            >
              Prev
            </button>
            <button
              v-for="page in totalPages"
              :key="page"
              :class="{ active: currentPage === page }"
              @click="goToPage(page)"
            >
              {{ page }}
            </button>
            <button
              @click="goToPage(currentPage + 1)"
              :disabled="currentPage === totalPages"
            >
              Next
            </button>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import api from "@/api/axios";
import defaultCover from "@/assets/images/default-cover.png";
import { useToast } from "vue-toastification";

const notifyMeBooks = ref([]);
const currentPage = ref(1);
const booksPerPage = 3;
const toast = useToast();

const fetchNotifyMeList = async () => {
  try {
    const res = await api.get("/notify-me");
    notifyMeBooks.value = res.data.books.map((book) => ({
      id: book.id,
      title: book.title || "No Title",
      image: book.cover_image || defaultCover,
      link: `/books/${book.id}`,
      authors: book.authors || [],
      publisher: book.publisher || "Unknown",
    }));
  } catch (error) {
    console.error("Error retrieving notify me list:", error);
  }
};

const removeFromNotifyList = async (bookId) => {
  try {
    const res = await api.delete(`/notify-me/${bookId}`);
    toast.success(res.data.message);
    notifyMeBooks.value = notifyMeBooks.value.filter(
      (book) => book.id !== bookId
    );
  } catch (error) {
    console.error("Error removing book from notify me list:", error);
  }
};

const paginatedNotifyMeBooks = computed(() => {
  const start = (currentPage.value - 1) * booksPerPage;
  return notifyMeBooks.value.slice(start, start + booksPerPage);
});

const totalPages = computed(() => {
  return Math.ceil(notifyMeBooks.value.length / booksPerPage);
});

const goToPage = (page) => {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page;
  }
};

onMounted(fetchNotifyMeList);
</script>

<style scoped>
.notify-list {
  padding-top: 40px;
  padding-bottom: 40px;
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
  border-radius: 10px;
  background-color: white;
  height: 100%;
  display: flex;
  flex-direction: column;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.thumb {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 200px;
  background-color: #ffffff;
  overflow: hidden;
  border-radius: 8px;
}

.book-thumbnail {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}

.down-content {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
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
  margin-top: auto;
  width: 100%;
  text-align: center;
}
.remove-btn:hover {
  background-color: #c0392b;
}

.pagination {
  margin-top: 30px;
  text-align: center;
}

.pagination button {
  background-color: #f0f0f0;
  border: 1px solid #ccc;
  color: #333;
  padding: 8px 12px;
  margin: 0 4px;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
}

.pagination button.active {
  background-color: #3498db;
  color: white;
  border-color: #2980b9;
}

.pagination button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>
