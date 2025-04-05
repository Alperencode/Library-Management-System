<template>
  <div>
    <section class="borrowed-books">
      <div class="container">
        <h2>Borrowed Books</h2>
        <p>Here you can see the books you have borrowed.</p>

        <div v-if="borrowedBooks.length === 0" class="no-results">
          <p class="no-results-text">You have not borrowed any books yet.</p>
        </div>

        <div v-else>
          <div class="row grid">
            <div v-for="(book, index) in borrowedBooks" :key="index" class="meeting-item">
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
                    <strong>Author:</strong> {{ book.authors.join(", ") || "Unknown" }}
                  </p>
                  <p class="text-ellipsis" :title="book.publisher">
                    <strong>Publisher:</strong> {{ book.publisher }}
                  </p>
                  <p class="text-ellipsis" :title="book.borrowed_at">
                    <strong>Borrowed At:</strong> {{ book.borrowed_at }}
                  </p>
                  <p class="text-ellipsis" :title="book.return_date">
                    <strong>Return Date:</strong> {{ book.return_date }}
                  </p>
                  <button class="return-btn" @click="returnBook(book.id)">
                    Return
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
import { formatDate } from "@/utils/date";
import { useRouter } from "vue-router";

const router = useRouter();

const returnBook = () => {
  router.push("/scan-book");
};

const borrowedBooks = ref([]);

const fetchBorrowedBooks = async () => {
  try {
    const res = await api.get("/borrowed");
    borrowedBooks.value = res.data.books.map((book) => ({
      id: book.id,
      title: book.title || "No Title",
      image: book.cover_image || defaultCover,
      link: `/books/${book.id}`,
      authors: book.authors || [],
      publisher: book.publisher || "Unknown",
      borrowed_at: formatDate(book.borrowed_at),
      return_date: formatDate(book.return_date),
    }));
  } catch (error) {
    console.error("Error retrieving borrowed books:", error);
  }
};

onMounted(fetchBorrowedBooks);
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

.borrowed-books {
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

.status-badge {
  display: inline-block;
  padding: 4px 10px;
  font-size: 14px;
  font-weight: 600;
  border-radius: 6px;
  margin-left: 6px;
  color: white;
  min-width: 80px;
  text-align: center;
}

.status-badge.taken {
  background-color: #e74c3c;
}

.status-badge.available {
  background-color: #27ae60;
}
</style>