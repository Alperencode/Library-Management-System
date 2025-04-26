<template>
  <div>
    <section class="overdue-books">
      <div class="container">
        <h2>Overdue Books</h2>
        <p>Here you can see the books that are overdue.</p>

        <!-- Kullanıcının gecikmiş kitabı yoksa mesaj göster -->
        <div v-if="overdueBooks.length === 0" class="no-results">
          <p class="no-results-text">You have no overdue books.</p>
        </div>

        <!-- Gecikmiş kitapları listele -->
        <div v-else>
          <div class="row grid">
            <div
              v-for="(book, index) in paginatedBooks"
              :key="index"
              class="meeting-item"
            >
              <div class="meeting-box">
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
                  <p class="text-ellipsis" :title="book.authors.join(', ')">
                    <strong>Author:</strong>
                    {{ book.authors.join(", ") || "Unknown" }}
                  </p>
                  <p class="text-ellipsis" :title="book.publisher">
                    <strong>Publisher:</strong> {{ book.publisher }}
                  </p>
                  <p>
                    <strong>Return Date was:</strong> {{ book.return_date }}
                  </p>
                </div>
              </div>
            </div>
          </div>

          <!-- Sayfalama -->
          <div class="pagination" v-if="totalPages > 1">
            <button
              @click="goToPage(currentPage - 1)"
              :disabled="currentPage === 1"
              class="page-btn"
            >
              Prev
            </button>
            <button
              v-for="page in totalPages"
              :key="page"
              :class="{ active: currentPage === page }"
              @click="goToPage(page)"
              class="page-btn"
            >
              {{ page }}
            </button>
            <button
              @click="goToPage(currentPage + 1)"
              :disabled="currentPage === totalPages"
              class="page-btn"
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
import { ref, onMounted, computed } from "vue";
import api from "@/api/axios";
import defaultCover from "@/assets/images/default-cover.png";
import { formatDate } from "@/utils/date";

const overdueBooks = ref([]);
const currentPage = ref(1);
const itemsPerPage = 3;

const fetchOverdueBooks = async () => {
  try {
    const res = await api.get("/borrowed/overdue-books");
    overdueBooks.value = res.data.books.map((book) => ({
      id: book.id,
      title: book.title || "No Title",
      image: book.cover_image || defaultCover,
      link: `/books/${book.id}`,
      authors: book.authors || [],
      publisher: book.publisher || "Unknown",
      return_date: formatDate(book.return_date),
    }));
  } catch (error) {
    console.error("Error retrieving overdue books:", error);
  }
};

const paginatedBooks = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage;
  return overdueBooks.value.slice(start, start + itemsPerPage);
});

const totalPages = computed(() => {
  const pages = Math.ceil(overdueBooks.value.length / itemsPerPage);
  return pages > 0 ? pages : 1;
});

const goToPage = (page) => {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page;
  }
};

onMounted(fetchOverdueBooks);
</script>

<style scoped>
.overdue-books {
  padding-top: 40px;
  min-height: auto;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
}

.no-results {
  color: black !important;
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

.meeting-item {
  width: 100%;
}

@media (min-width: 768px) {
  .meeting-item {
    width: calc(33.333% - 20px);
  }
}

.meeting-box {
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
