<template>
  <div>
    <section class="overdue-books">
      <div class="container">
        <h2>Overdue Books</h2>
        <p>Here you can see the books that are overdue.</p>

                <div class="search-bar-wrapper">
          <input v-model="searchQuery" @keyup.enter="onSearchEnter" class="search-input"
            placeholder="Search by title, author, publisher..." />
        </div>

        <div v-if="overdueBooks.length === 0" class="no-results">
          <p class="no-results-text">You have no overdue books.</p>
        </div>

        <div v-else>
          <div class="row grid">
            <div v-for="(book, index) in overdueBooks" :key="index" class="meeting-item">
              <div class="meeting-box">
                <div class="thumb">
                  <router-link :to="book.link">
                    <img :src="book.image" :alt="book.title" class="book-thumbnail" />
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
                  <p><strong>Return Date was:</strong> {{ book.return_date }}</p>
                  <p v-if="book.penalty > 0" style="color: #b91c1c; font-weight: 600;">
                    <strong>Penalty:</strong> {{ book.penalty }} ₺
                  </p>
                  <button class="return-btn" @click="returnBook(book.id)">
                    Return
                  </button>
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
import { formatDate } from "@/utils/date";
import { useRouter } from "vue-router";


const router = useRouter();
const overdueBooks = ref([]);
const currentPage = ref(1);
const itemsPerPage = 3;
const totalPages = ref(1);
const searchQuery = ref('');

const returnBook = () => {
  router.push("/scan-book");
};

const user = ref(null)
const savedUser = localStorage.getItem("user")
if (savedUser) {
  user.value = JSON.parse(savedUser)
}

const fetchOverdueBooks = async () => {
  try {
    const res = await api.get("/borrowed/overdue-books", {
      params: {
        page: currentPage.value,
        limit: itemsPerPage,
        q: searchQuery.value || undefined
      }
    });
    const penalties = user?.value.penalties || [];

    overdueBooks.value = res.data.books.map((book) => {
      const match = penalties.find((p) => p.book_id === book.id);
      return {
        id: book.id,
        title: book.title || "No Title",
        image: book.cover_image || defaultCover,
        link: `/books/${book.id}`,
        authors: book.authors || [],
        publisher: book.publisher || "Unknown",
        return_date: formatDate(book.return_date),
        penalty: match ? match.amount : 0,
      };
    });
  } catch (error) {
    console.error("Error retrieving overdue books:", error);
  }
};

const onSearchEnter = () => {
  currentPage.value = 1;
  fetchOverdueBooks();
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
  fetchOverdueBooks();
});

onMounted(fetchOverdueBooks);
</script>

<style scoped>

.return-btn {
  background-color: #27ae60;
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

.return-btn:hover {
  background-color: #1e8449;
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

.meeting-item {
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

  .meeting-item {
    flex: 0 0 100%;
    max-width: 100%;
  }
}

.meeting-box {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  height: 520px;
  width: 280px;
  padding: 10px;
  border-radius: 8px;
  background-color: white;
  border: 1px solid #ccc;
}

.thumb {
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
  overflow: hidden;
  text-overflow: ellipsis;
  word-break: break-word;
  text-align: center;
  margin-bottom: 8px;
  line-height: 1.3;
  max-height: calc(1.3em * 3);
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
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}

.pagination button {
  padding: 10px 16px;
  font-size: 14px;
  font-weight: 600;
  border: none;
  border-radius: 12px;
  min-width: 4px;
  background-color: #f2f2f2;
  color: #333;
  cursor: pointer;
  transition: all 0.2s ease;
  margin: 0 6px;
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
</style>
