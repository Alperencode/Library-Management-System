<template>
  <div>
    <section class="overdue-books">
      <div class="container">
        <h2>Overdue Books</h2>
        <p>Here you can see the books that are overdue.</p>

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
import { useStore } from "vuex";


const store = useStore();
const router = useRouter();
const overdueBooks = ref([]);

const returnBook = () => {
  router.push("/scan-book");
};
const user = store.state.user;
if (!store.state.user) {
  const savedUser = localStorage.getItem("user");
  if (savedUser) {
    store.commit("setUser", JSON.parse(savedUser));
  }
}

const fetchOverdueBooks = async () => {
  try {
    const res = await api.get("/borrowed/overdue-books");
    const penalties = user?.penalties || [];

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
</style>
