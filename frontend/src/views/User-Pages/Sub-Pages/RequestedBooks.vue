<template>
  <div>
    <section class="requested-books">
      <div class="container">
        <h2>Requested Books</h2>
        <p>
          Here you can see the books you have requested to be added to the
          library.
        </p>

        <div v-if="user">
          <RouterLink to="/request-book" class="request-btn"
            >Request a Book</RouterLink
          >
        </div>

        <div v-if="requestedBooks.length === 0" class="no-results">
          <p class="no-results-text">You have not requested any books yet.</p>
        </div>

        <div v-else>
          <div class="row grid">
            <div
              v-for="(book, index) in requestedBooks"
              :key="index"
              class="book-item"
            >
              <div class="book-box">
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
                  <p class="text-ellipsis">
                    <strong>Publisher:</strong> {{ book.publisher }}
                  </p>
                  <p class="text-ellipsis">
                    <strong>Status:</strong>
                    <span
                      :class="
                        'status-badge ' +
                        book.status.toLowerCase().replace(/\s+/g, '-')
                      "
                    >
                      {{ book.status }}
                    </span>
                  </p>
                  <p class="text-ellipsis">
                    <strong>Requested At:</strong> {{ book.requested_at }}
                  </p>
                  <button class="remove-btn" @click="deleteRequest(book.id)">
                    Delete Request
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
import { useAuth } from "@/composables/useAuth"; // Import useAuth for user info
import api from "@/api/axios";
import defaultCover from "@/assets/images/default-cover.png";
import { formatDate } from "@/utils/date";

const requestedBooks = ref([]);
const { user } = useAuth(); // Get the user from useAuth

const fetchRequestedBooks = async () => {
  try {
    const res = await api.get("/request-book");
    requestedBooks.value = res.data.books.map((book) => ({
      id: book.id,
      title: book.title || "No Title",
      image: book.cover_image || defaultCover,
      authors: book.authors || [],
      publisher: book.publisher || "Unknown",
      status: book.status || "Request Sent",
      requested_at: formatDate(book.requested_at),
    }));
  } catch (error) {
    console.error("Error retrieving requested books:", error);
  }
};

const deleteRequest = async (id) => {
  try {
    await api.delete(`/requests/${id}`);
    requestedBooks.value = requestedBooks.value.filter((b) => b.id !== id);
  } catch (error) {
    console.error("Failed to delete book request:", error);
  }
};

onMounted(fetchRequestedBooks);
</script>

<style scoped>
.request-btn {
  display: inline-block;
  padding: 10px 16px;
  background-color: #3498db;
  color: white;
  font-weight: bold;
  text-decoration: none;
  border-radius: 6px;
  transition: background-color 0.3s ease;
}

.request-btn:hover {
  background-color: #2980b9;
}

.requested-books {
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

.status-badge {
  display: inline-block;
  padding: 4px 10px;
  font-size: 13px;
  font-weight: 600;
  border-radius: 6px;
  color: white;
  background-color: #7f8c8d;
  margin-left: 6px;
  text-transform: capitalize;
}

.status-badge.approved {
  background-color: #27ae60;
}

.status-badge.denied {
  background-color: #c0392b;
}

.status-badge.added {
  background-color: #2980b9;
}

.status-badge.on-hold {
  background-color: #f39c12;
}

.status-badge.request-sent {
  background-color: #7f8c8d;
}
</style>
