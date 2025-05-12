<template>
  <div>
    <section class="borrow-history">
      <div class="container">
        <h2>Borrow History</h2>
        <p>Here you can see the books you have previously borrowed.</p>

        <div class="search-bar-wrapper">
          <input v-model="searchQuery" @keyup.enter="onSearchEnter" class="search-input"
            placeholder="Search by title, author, publisher..." />
        </div>

        <div v-if="borrowHistory.length === 0" class="no-results">
          <p class="no-results-text">You have not borrowed any books yet.</p>
        </div>

        <div v-else>
          <div class="row grid">
            <div v-for="(book, index) in borrowHistory" :key="index" class="history-item">
              <div class="history-box">
                <div class="thumb">
                  <img :src="book.image" :alt="book.title" class="book-thumbnail" />
                </div>
                <div class="down-content">
                  <router-link :to="book.link" class="book-title">
                    <h4>{{ book.title }}</h4>
                  </router-link>
                  <p class="text-ellipsis">
                    <strong>Author:</strong>
                    {{ book.authors.join(", ") || "Unknown" }}
                  </p>
                  <p class="text-ellipsis" :title="book.publisher">
                    <strong>Publisher:</strong> {{ book.publisher }}
                  </p>
                  <div class="borrowed-date-badge" :title="book.borrowed_at">
                    <strong>Borrowed At:</strong> {{ book.borrowed_at }}
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div v-if="totalPages > 1" class="pagination">
            <button @click="prevPage" :disabled="currentPage === 1">‹</button>
            <button v-for="page in visiblePages" :key="page" :class="{ active: page === currentPage }"
              @click="goToPage(page)">
              {{ page }}
            </button>
            <button @click="nextPage" :disabled="currentPage === totalPages">›</button>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from "vue";
import api from "@/api/axios";
import defaultCover from "@/assets/images/default-cover.png";
import { formatDateWithoutTime } from "@/utils/date";

const borrowHistory = ref([]);
const currentPage = ref(1);
const itemsPerPage = 3;
const totalPages = ref(1);
const searchQuery = ref('');

const fetchBorrowHistory = async () => {
  try {
    const res = await api.get("/borrowed/history", {
      params: {
        page: currentPage.value,
        limit: itemsPerPage,
        q: searchQuery.value || undefined
      }
    });

    const { books, last_page } = res.data;
    totalPages.value = last_page || 1;

    borrowHistory.value = books.map((book) => ({
      id: book.id,
      title: book.title || "No Title",
      link: `/books/${book.id}`,
      image: book.cover_image || defaultCover,
      authors: book.authors || [],
      publisher: book.publisher || "Unknown",
      borrowed_at: formatDateWithoutTime(book.borrowed_at),
      return_date: formatDateWithoutTime(book.return_date)
    }));
  } catch (error) {
    console.error("Error retrieving borrow history:", error);
  }
};

const onSearchEnter = () => {
  currentPage.value = 1;
  fetchBorrowHistory();
};

const goToPage = (page) => {
  currentPage.value = page;
};

const prevPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--;
  }
};

const nextPage = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value++;
  }
};

const visiblePages = computed(() => {
  const pages = [];
  const maxButtons = 5;
  let startPage = Math.max(1, currentPage.value - 2);
  let endPage = Math.min(totalPages.value, startPage + maxButtons - 1);

  if (endPage - startPage < maxButtons - 1) {
    startPage = Math.max(1, endPage - maxButtons + 1);
  }

  for (let i = startPage; i <= endPage; i++) {
    pages.push(i);
  }

  return pages;
});

watch(currentPage, () => {
  fetchBorrowHistory();
});

onMounted(fetchBorrowHistory);
</script>

<style scoped>
.borrow-history {
  padding-top: 40px;
  min-height: auto;
}

.container {
  width: 110%;
  max-width: none;
  min-width: 1000px;
  height: 800px;
  min-height: 800px;
  position: relative;
  left: 50%;
  transform: translateX(-50%);
  padding: 40px;
  background: rgba(255, 255, 255, 0.3);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(255, 255, 255, 0.3);
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
}

.container h2,
.container>p {
  color: white;
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
  justify-content: center;
  gap: 20px;
  width: 100%;
  min-height: 300px;
  margin: 0 auto;
}

.history-item {
  flex: 0 0 calc(33.333% - 20px);
  max-width: calc(33.333% - 20px);
  min-width: 280px;
  box-sizing: border-box;
}

@media (max-width: 768px) {
  .container {
    min-width: auto;
    max-width: 90%;
  }

  .history-item {
    flex: 0 0 100%;
    max-width: 100%;
  }
}

.history-box {
  display: flex;
  flex-direction: column;
  align-items: stretch;
  height: 520px;
  width: 280px;
  padding: 10px;
  border-radius: 8px;
  background-color: white;
  border: 1px solid #ccc;
}

.thumb {
  margin-bottom: 12px;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 200px;
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
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 3;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: normal;
  text-align: center;
  margin-bottom: 8px;
  text-decoration: none;
  color: #2980b9;
  font-weight: 600;
  font-size: 16px;
  line-height: 1.3;
  transition: color 0.2s ease;
}

.book-title:hover {
  color: #ffb03b; /* Optional: highlight color on hover */
}

.book-title h4 {
  font-weight: 600;
  font-size: 16px;
  margin: 0;
  line-height: 1.3;
}

.text-ellipsis {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  display: block;
  width: 100%;
  max-width: 100%;
}

.search-bar-wrapper {
  margin: 12px 0;
}

.search-input {
  width: 100%;
  padding: 10px;
  border-radius: 6px;
  border: 1px solid #ccc;
  font-size: 14px;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
  margin-top: 20px;
}

.pagination button {
  padding: 10px 16px;
  font-size: 14px;
  font-weight: 600;
  border: none;
  border-radius: 12px;
  background-color: #f2f2f2;
  color: #333;
  cursor: pointer;
  transition: all 0.2s ease;
}

.pagination button:hover:not(:disabled) {
  background-color: #ffb03b;
}

.pagination button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.pagination button.active {
  background-color: #ffb03b;
  color: #fff;
}

.borrowed-date-badge {
  background-color: #e67e22;
  color: white;
  font-weight: 600;
  text-align: center;
  padding: 6px 12px;
  border-radius: 20px;
  margin: 10px auto 4px auto;
  width: fit-content;
  font-size: 13px;
}
</style>
