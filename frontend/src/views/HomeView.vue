<template>
  <div id="home">
    <!-- ***** Main Banner Area Start ***** -->
    <section class="section main-banner" id="top" data-section="section1">
      <video autoplay muted loop id="bg-video">
        <source src="assets/images/course-video.mp4" type="video/mp4" />
      </video>

      <div class="video-overlay header-text">
        <div class="container">
          <div class="row">
            <div class="col-lg-12">
              <div class="caption">
                <h6 v-if="user">Welcome back, {{ user.username }}</h6>
                <h6 v-else>Welcome to your digital library</h6>
                <h2>Welcome to Library Management System</h2>
                <p>
                  Easily manage your library activities, scan books with RFID or ISBN,
                  discover new titles via Google Books, and request additions directly through the system.
                </p>
                <div class="main-button-red">
                  <div class="scroll-to-section">
                    <a href="/books">Check Out the Book Catalog</a>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
    <!-- ***** Main Banner Area End ***** -->

    <section class="services">
      <div class="container">
        <div class="row">
          <div class="col-lg-12">
            <div class="owl-service-item owl-carousel">
              <div class="item">
                <div class="icon">
                  <img src="assets/images/service-icon-01.png" alt="" />
                </div>
                <div class="down-content">
                  <h4>Best Education</h4>
                  <p>
                    Suspendisse tempor mauris a sem elementum bibendum. Praesent
                    facilisis massa non vestibulum.
                  </p>
                </div>
              </div>

              <div class="item">
                <div class="icon">
                  <img src="assets/images/service-icon-02.png" alt="" />
                </div>
                <div class="down-content">
                  <h4>Best Teachers</h4>
                  <p>
                    Suspendisse tempor mauris a sem elementum bibendum. Praesent
                    facilisis massa non vestibulum.
                  </p>
                </div>
              </div>

              <div class="item">
                <div class="icon">
                  <img src="assets/images/service-icon-03.png" alt="" />
                </div>
                <div class="down-content">
                  <h4>Best Students</h4>
                  <p>
                    Suspendisse tempor mauris a sem elementum bibendum. Praesent
                    facilisis massa non vestibulum.
                  </p>
                </div>
              </div>

              <div class="item">
                <div class="icon">
                  <img src="assets/images/service-icon-02.png" alt="" />
                </div>
                <div class="down-content">
                  <h4>Online Meeting</h4>
                  <p>
                    Suspendisse tempor mauris a sem elementum bibendum. Praesent
                    facilisis massa non vestibulum.
                  </p>
                </div>
              </div>

              <div class="item">
                <div class="icon">
                  <img src="assets/images/service-icon-03.png" alt="" />
                </div>
                <div class="down-content">
                  <h4>Best Networking</h4>
                  <p>
                    Suspendisse tempor mauris a sem elementum bibendum. Praesent
                    facilisis massa non vestibulum.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="upcoming-meetings" id="meetings">
      <div class="container">
        <h2 class="section-heading text-white text-center mb-5">
          Recently Added Books
        </h2>
        <div class="slick-carousel">
          <div class="course-card" v-for="book in recentlyAddedBooks" :key="book.id">
            <div class="card text-center text-dark">
              <router-link :to="`/books/${book.id}`" class="text-decoration-none">
                <img :src="book.cover_url || defaultCover" :alt="book.title" class="card-img-top" />
              </router-link>
              <div class="card-body d-flex flex-column justify-content-between">
                <div>
                  <h5 class="card-title">{{ book.title }}</h5>
                  <p class="card-text text-muted">
                    {{ book.authors?.join(", ") }}
                  </p>
                </div>
                <div class="mt-3">
                  <router-link :to="`/books/${book.id}`" class="view-details-btn">
                    View Details →
                  </router-link>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Eğer hiç kitap yoksa -->
        <div v-if="recentlyAddedBooks.length === 0" class="no-results mt-4">
          <p>No recently added books available.</p>
        </div>
      </div>
    </section>

    <section class="apply-now" id="apply">
      <div class="container">
        <div class="item">
          <h3 class="text-center mb-3">Request a Book from Google Books</h3>
          <div class="meetings-page">
            <div class="main-content">
              <div class="search-bar mb-4">
                <input class="input-line full-width" type="text" :value="searchQuery" @input="updateSearchQuery"
                  @keyup.enter="performSearch" placeholder="Search by Author, Title, Publisher, ISBN..." />
              </div>

              <div v-if="requestBooks.length === 0 && searchPerformed" class="no-results">
                <p class="no-results-text">
                  No books found for "{{ searchQuery }}"
                </p>
              </div>

              <div v-else>
                <div class="row grid">
                  <div v-for="(book, index) in requestBooks.slice(0, 8)" :key="index" class="meeting-item">
                    <div class="meeting-box">
                      <div class="thumb">
                        <img :src="book.cover_image" :alt="book.title" class="book-thumbnail" />
                      </div>
                      <div class="down-content">
                        <h4 class="book-title">{{ book.title }}</h4>
                        <p class="text-ellipsis" :title="book.authors.join(', ')">
                          <strong>Author:</strong> {{ book.authors.join(", ") }}
                        </p>
                        <p class="text-ellipsis" :title="book.publisher">
                          <strong>Publisher:</strong> {{ book.publisher }}
                        </p>
                        <p v-if="book.categories" class="text-ellipsis" :title="book.categories">
                          <strong>Categories:</strong> {{ book.categories }}
                        </p>
                        <button v-if="user" class="request-button" @click="requestBook(book)"
                          :disabled="requestedBookIds.has(book.id)">
                          {{ requestedBookIds.has(book.id) ? "Requested" : "Request" }}
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="popular-courses">
      <div class="container">
        <h2 class="section-heading text-white text-center mb-5">
          Most Borrowed Books
        </h2>
        <div class="slick-carousel">
          <div class="course-card" v-for="book in books" :key="book.id">
            <div class="card text-center text-dark">
              <router-link :to="`/books/${book.id}`" class="text-decoration-none">
                <img :src="book.cover_image || defaultCover" :alt="book.title" class="card-img-top" />
              </router-link>
              <div class="card-body d-flex flex-column justify-content-between">
                <div>
                  <h5 class="card-title">{{ book.title }}</h5>
                  <p class="card-text text-muted">
                    {{ book.authors?.join(", ") }}
                  </p>
                </div>
                <div class="mt-3">
                  <router-link :to="`/books/${book.id}`" class="view-details-btn">
                    View Details →
                  </router-link>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="our-facts">
      <div class="container">
        <div class="row">
          <div class="col-lg-6">
            <div class="row">
              <div class="col-lg-12">
                <h2>A Few Facts About Our Library Management System</h2>
              </div>
              <div class="col-lg-6">
                <div class="row">
                  <div class="col-12">
                    <div class="count-area-content">
                      <div class="count-digit">{{ totalBooks }}</div>
                      <div class="count-title">Total Books</div>
                    </div>
                  </div>
                  <div class="col-12">
                    <div class="count-area-content">
                      <div class="count-digit">126</div>
                      <div class="count-title">Current Teachers</div>
                    </div>
                  </div>
                </div>
              </div>
              <div class="col-lg-6">
                <div class="row">
                  <div class="col-12">
                    <div class="count-area-content new-students">
                      <div class="count-digit">2345</div>
                      <div class="count-title">New Students</div>
                    </div>
                  </div>
                  <div class="col-12">
                    <div class="count-area-content">
                      <div class="count-digit">32</div>
                      <div class="count-title">Awards</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="col-lg-6 align-self-center"></div>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import { onMounted, ref, nextTick, computed } from "vue";
import { useStore } from "vuex";
import api from "../api/axios";
import defaultCover from "@/assets/images/default-cover.png";
import { useToast } from 'vue-toastification'

const toast = useToast()

export default {
  name: "HomeView",
  setup() {
    const store = useStore();
    const user = computed(() => store.state.user);

    const books = ref([]);
    const recentlyAddedBooks = ref([]);
    const totalBooks = ref(0);
    const requestedBookIds = ref(new Set());

    const fetchRequestedBooks = async () => {
      try {
        const res = await api.get("/request-book");
        const ids = res.data.books.map((book) => book.id);
        ids.forEach((id) => requestedBookIds.value.add(id));
      } catch (err) {
        console.warn("İstek yapılan kitaplar alınamadı:", err);
      }
    };

    const searchQuery = ref("");
    const searchPerformed = ref(false);
    const currentPage = ref(1);
    const limit = ref(4);
    const requestBooks = ref([]);

    const fetchBooks = async () => {
      if (!searchQuery.value.trim()) {
        requestBooks.value = [];
        searchPerformed.value = false;
        return;
      }
      try {
        const res = await api.get("/google-books/search", {
          params: {
            q: searchQuery.value,
            page: currentPage.value,
            limit: limit.value,
          },
        });

        requestBooks.value = res.data.books.map((book) => {
          const authors =
            Array.isArray(book.authors) && book.authors.length
              ? book.authors
              : ["Unknown"];
          const publisher = book.publisher || "Unknown";
          const categoriesString =
            Array.isArray(book.categories) && book.categories.length
              ? book.categories
                .map((cat) => {
                  let main = cat.category || "Unknown Category";
                  if (cat.subcategory) {
                    main += ` - ${cat.subcategory}`;
                  }
                  return main;
                })
                .join(", ")
              : "Unknown";

          return {
            id: book.id,
            title: book.title || "No Title",
            cover_image: book.cover_image || defaultCover,
            isbn: book.isbn || null,
            authors,
            publisher,
            categories: categoriesString,
          };
        });

        searchPerformed.value = true;
      } catch (err) {
        requestBooks.value = [];
        searchPerformed.value = true;
      }
    };

    const performSearch = () => {
      currentPage.value = 1;
      fetchBooks();
    };

    const updateSearchQuery = (event) => {
      searchQuery.value = event.target.value;
    };

    const requestBook = async (book) => {
      try {
        const payload = {
          id: book.id,
          title: book.title,
          authors: book.authors,
          isbn: book.isbn,
          publisher: book.publisher,
          cover_image: book.cover_image,
        };

        const res = await api.post("/request-book", payload);
        toast.success(res.data.message)
        requestedBookIds.value.add(book.id);
      } catch (err) {
        console.error("Failed to request the book:", err)
      }
    };

    onMounted(async () => {
      const scripts = [
        "vendor/jquery/jquery.min.js",
        "assets/js/isotope.min.js",
        "assets/js/isotope.js",
        "assets/js/lightbox.js",
        "assets/js/tabs.js",
        "assets/js/video.js",
        "assets/js/slick-slider.js",
        "assets/js/custom.js",
      ];

      for (const src of scripts) {
        const script = document.createElement("script");
        script.src = src;
        script.async = false;
        document.head.appendChild(script);
      }

      await new Promise((resolve) => setTimeout(resolve, 300));

      if (user.value) {
        await fetchRequestedBooks();
      }

      try {
        const mostBorrowedRes = await api.get("/books", {
          params: {
            page: 1,
            limit: 10,
            most_borrowed: true,
          },
        });

        if (mostBorrowedRes.data.code === "Success" && mostBorrowedRes.data.books) {
          books.value = mostBorrowedRes.data.books;
        }

        const recentlyAddedRes = await api.get("/books", {
          params: {
            page: 1,
            limit: 10,
            recently_added: true,
          },
        });

        if (recentlyAddedRes.data.code === "Success" && recentlyAddedRes.data.books) {
          recentlyAddedBooks.value = recentlyAddedRes.data.books.map((book) => ({
            id: book.id,
            title: book.title || "No Title",
            authors: book.authors || ["Unknown Author"],
            cover_url: book.cover_image || defaultCover,
            created_at: book.borrowed_at || new Date().toISOString(),
            borrow_count: book.borrowed ? 1 : 0,
          }));

          totalBooks.value = recentlyAddedRes.data.total;
        }

      } catch (error) {
        console.error("Error fetching books:", error);
      }

      await nextTick();

      if (window.$ && window.$(".slick-carousel").slick) {
        window.$(".slick-carousel").slick({
          slidesToShow: 4,
          slidesToScroll: 1,
          autoplay: true,
          autoplaySpeed: 3000,
          arrows: true,
          dots: true,
          responsive: [
            { breakpoint: 1024, settings: { slidesToShow: 3 } },
            { breakpoint: 768, settings: { slidesToShow: 2 } },
            { breakpoint: 480, settings: { slidesToShow: 1 } },
          ],
        });
      }

      setTimeout(() => {
        const items = document.querySelectorAll(".meeting-item");
        let maxHeight = 0;
        items.forEach((item) => {
          maxHeight = Math.max(maxHeight, item.offsetHeight);
        });
        items.forEach((item) => {
          item.style.height = `${maxHeight}px`;
        });
      }, 500);
    });

    return {
      books,
      defaultCover,
      recentlyAddedBooks,
      totalBooks,
      searchQuery,
      searchPerformed,
      requestBooks,
      requestedBookIds,
      performSearch,
      updateSearchQuery,
      requestBook,
      user,
    };
  },
};
</script>

<style scoped>
@import "@/vendor/bootstrap/css/bootstrap.min.css";
@import "@/assets/css/fontawesome.css";
@import "@/assets/css/templatemo-edu-meeting.css";
@import "@/assets/css/owl.css";
@import "@/assets/css/lightbox.css";

.meetings-page {
  display: flex;
  min-height: 100vh;
}

.main-content {
  flex: 1;
  padding: 24px;
  background-color: transparent;
}

.search-bar {
  margin: 50px 10px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.input-line {
  background: none;
  margin-bottom: 0;
  padding: 6px 10px;
  line-height: 2.4em;
  color: #fff;
  font-family: roboto;
  font-weight: 300;
  font-size: 1.2rem;
  border: none;
  border-bottom: 1px solid rgba(255, 255, 255, 0.65);
  transition: all 0.2s ease;
  width: 100%;
}

.input-line:focus {
  outline: none;
}

::placeholder {
  color: rgba(255, 255, 255, 0.65);
}

.no-results {
  color: #ffffff !important;
  padding: 20px;
  font-size: 18px;
  text-align: center;
  border-radius: 8px;
  font-weight: 600;
}

.no-results-text {
  color: rgb(226, 226, 226) !important;
  font-size: 15px;
  font-weight: bold;
  text-shadow: 1px 1px 3px black;
}

.grid {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
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
  padding: 8px;
  overflow: hidden;
}

.book-thumbnail {
  height: 100%;
  object-fit: contain;
  padding-top: 10px;
}

.down-content {
  text-align: left !important;
}

.book-title {
  text-align: center;
  overflow: hidden;
  margin-bottom: 8px;
}

.text-ellipsis {
  margin: 0 !important;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  display: block;
  width: 100%;
  max-width: 100%;
  color: black;
}

.status-badge.taken {
  background-color: #e74c3c;
}

.status-badge.available {
  background-color: #27ae60;
}

.request-button {
  width: 100%;
  padding: 8px;
  font-size: 14px;
  font-weight: bold;
  background-color: #3498db;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  margin-top: 10px;
  transition: 0.3s;
}

.request-button:hover {
  background-color: #2980b9;
}

.request-button:disabled {
  background-color: #bdc3c7;
  cursor: not-allowed;
}

.popular-courses {
  background-color: #1f2a36;
  background-image: url("@/assets/images/meetings-bg.jpg");
  background-repeat: no-repeat;
  background-size: cover;
  background-position: center;
  padding: 50px 0;
}

.card {
  border: none;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  transition: transform 0.3s ease;
  height: 100%;
}

.card:hover {
  transform: translateY(-5px);
}

.card-img-top {
  height: 250px;
  object-fit: contain;
  padding-top: 10px;
}

.course-card {
  padding: 15px;
}

.section-heading {
  font-size: 28px;
  font-weight: 600;
}

.view-details-btn {
  display: inline-block;
  font-size: 0.9rem;
  color: #d4881a;
  font-weight: 500;
  transition: all 0.2s ease-in-out;
}

.view-details-btn:hover {
  text-decoration: none;
  color: #d4881a;
  transform: translateX(4px);
}

.upcoming-meetings {
  padding: 60px 0;
}

.no-results p {
  text-align: center;
  font-size: 16px;
  color: #888;
}

.meeting-item {
  width: 200px;
  height: auto;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  background-color: #fff;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  overflow: hidden;
}

.meeting-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15);
}

.thumb {
  position: relative;
}

.thumb img {
  width: 100%;
  height: 250px;
  object-fit: cover;
  border-bottom: 2px solid #ddd;
}

.down-content {
  padding: 10px;
  text-align: center;
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
}

.down-content h4,
.down-content p {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
  margin: 4px 0;
  color: #333;
  font-size: 14px;
}

.card-title,
.card-text {
  display: -webkit-box;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
  line-height: 1.2em;
  max-height: 2.4em;
}

.card {
  border: none;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  transition: transform 0.3s ease;
  height: 100%;
  min-height: 420px;
}

.card:hover {
  transform: translateY(-5px);
}

.course-card {
  padding: 15px;
}

.card-body {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 15px;
}

.card-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: #333;
  margin-bottom: 8px;
}

.card-text {
  font-size: 0.95rem;
  color: #666;
  margin-bottom: 12px;
}

.view-details-btn {
  display: inline-block;
  font-size: 0.9rem;
  color: #d4881a;
  font-weight: 500;
  transition: all 0.2s ease-in-out;
}

.view-details-btn:hover {
  text-decoration: none;
  color: #d4881a;
  transform: translateX(4px);
}

.apply-now .container {
  max-width: 1100px;
  padding: 0 24px;
  margin: 0 auto;
}

.apply-now .item {
  padding: 20px;
  border-radius: 12px;
  background: transparent;
}

.apply-now .main-content {
  height: auto;
  width: 100%;
  padding: 24px;
  background-color: transparent;
}

@media (max-width: 768px) {
  .section-heading h2 {
    font-size: 28px;
  }

  .meeting-item {
    width: 100%;
    max-width: 300px;
    margin: auto;
  }
}

.apply-now {
  padding: 40px 0;
}

.apply-now .item {
  padding: 24px 0;
}

.apply-now .main-content {
  padding: 24px;
}

.search-bar {
  margin: 30px 0 20px;
}

.meetings-page {
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  min-height: 500px;
}
</style>
