<template>
  <div>
    <section class="notify-list">
      <div class="container">
        <h2>Notify Me List</h2>
        <p>Here you can see the books you've requested to be notified about.</p>

        <div class="search-bar-wrapper">
          <input v-model="searchQuery" @keyup.enter="onSearchEnter" class="search-input"
            placeholder="Search by title, author, publisher..." />
        </div>

        <div v-if="notifyMeBooks.length === 0" class="no-results">
          <p class="no-results-text">
            You have not added any books to the notify me list yet.
          </p>
        </div>

        <div v-else>
          <div class="row grid">
            <div v-for="(book, index) in notifyMeBooks" :key="index" class="meeting-item">
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
                  <p class="text-ellipsis">
                    <strong>Author:</strong>
                    {{ book.authors.join(", ") || "Unknown" }}
                  </p>
                  <p class="text-ellipsis" :title="book.publisher">
                    <strong>Publisher:</strong> {{ book.publisher }}
                  </p>
                  <p class="text-ellipsis">
                    <strong>Categories: </strong>
                    <span v-if="book.categories.length">
                      {{book.categories.map(c => c.subcategory ? `${c.category} / ${c.subcategory}` :
                        c.category).join(', ') }}
                    </span>
                    <span v-else>
                      Not specified
                    </span>
                  </p>
                  <p v-if="book.returnDate" class="text-ellipsis">
                    <strong>Return Date:</strong> {{ new Date(book.returnDate).toLocaleDateString() }}
                  </p>
                  <button class="remove-btn" @click="removeFromNotifyList(book.id)">
                    Remove
                  </button>
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
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from "vue";
import api from "@/api/axios";
import defaultCover from "@/assets/images/default-cover.png";
import { useToast } from 'vue-toastification';

const toast = useToast();

const notifyMeBooks = ref([]);
const currentPage = ref(1);
const itemsPerPage = 3;
const totalPages = ref(1);
const searchQuery = ref('');

const fetchNotifyMeList = async () => {
  try {
    const res = await api.get("/notify-me", {
      params: {
        page: currentPage.value,
        limit: itemsPerPage,
        q: searchQuery.value || undefined
      }
    });

    totalPages.value = res.data.last_page || 1;

    notifyMeBooks.value = res.data.books.map((book) => ({
      id: book.id,
      title: book.title || "No Title",
      image: book.cover_image || defaultCover,
      link: `/books/${book.id}`,
      authors: book.authors || [],
      publisher: book.publisher || "Unknown",
      categories: book.categories || [],
      returnDate: book.return_date || null,
    }));
  } catch (error) {
    console.error("Error retrieving borrowed books:", error);
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

const onSearchEnter = () => {
  currentPage.value = 1;
  fetchNotifyMeList();
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
  fetchNotifyMeList();
});

onMounted(fetchNotifyMeList);
</script>

<style scoped>
.remove-btn {
  margin-top: auto;
  background-color: #e74c3c;
  color: white;
  border: none;
  padding: 8px 12px;
  border-radius: 5px;
  font-size: 14px;
  cursor: pointer;
  width: 100%;
  text-align: center;
}

.remove-btn:hover {
  background-color: #c0392b;
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
  height: 480px;
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
  height: 160px;
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
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  flex-grow: 1;
  text-align: left;
  padding: 10px;
  gap: 6px;
}

.down-content .book-title {
  font-weight: bold;
  margin-bottom: 4px;
}

.down-content .text-ellipsis {
  font-size: 14px;
  max-width: 100%;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
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