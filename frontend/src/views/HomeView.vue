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
                <h6>Hello Students</h6>
                <h2>Welcome to Education</h2>
                <p>
                  This is an edu meeting HTML CSS template provided by
                  <a
                    rel="nofollow"
                    href="https://templatemo.com/page/1"
                    target="_blank"
                    >TemplateMo website</a
                  >. This is a Bootstrap v5.1.3 layout. The video background is
                  taken from Pexels website, a group of young people by
                  <a
                    rel="nofollow"
                    href="https://www.pexels.com/@pressmaster"
                    target="_blank"
                    >Pressmaster</a
                  >.
                </p>
                <div class="main-button-red">
                  <div class="scroll-to-section">
                    <a href="#contact">Join Us Now!</a>
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
        <div class="row">
          <div class="col-lg-12">
            <div class="section-heading">
              <h2 style="padding-top: 100px">Recently Added Books</h2>
            </div>
          </div>
          <div
            class="col-lg-3"
            v-for="book in recentlyAddedBooks.slice(0, 4)"
            :key="book.id"
          >
            <div class="meeting-item">
              <div class="thumb">
                <router-link :to="`/books/${book.id}`">
                  <img :src="book.cover_url" :alt="book.title" />
                </router-link>
              </div>
              <div class="down-content">
                <router-link :to="`/books/${book.id}`">
                  <h4>{{ book.title }}</h4>
                </router-link>
                <p>{{ book.authors.join(", ") || "Unknown Author" }}</p>
              </div>
            </div>
          </div>
          <div v-if="recentlyAddedBooks.length === 0" class="no-results">
            <p>No recently added books available.</p>
          </div>
        </div>
      </div>
    </section>

    <section class="apply-now" id="apply">
      <div class="container">
        <div class="row">
          <div class="col-lg-6 align-self-center">
            <div class="row">
              <div class="col-lg-12"></div>
              <div class="col-lg-12"></div>

              <div class="col-lg-12">
                <div class="item">
                  <h3>Request a Book from Google Books</h3>
                  <RequestBook />
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
              <router-link
                :to="`/books/${book.id}`"
                class="text-decoration-none"
              >
                <img
                  :src="book.cover_image || defaultCover"
                  :alt="book.title"
                  class="card-img-top"
                />
              </router-link>
              <div class="card-body d-flex flex-column justify-content-between">
                <div>
                  <h5 class="card-title">{{ book.title }}</h5>
                  <p class="card-text text-muted">
                    {{ book.authors?.join(", ") }}
                  </p>
                </div>
                <div class="mt-3">
                  <router-link
                    :to="`/books/${book.id}`"
                    class="view-details-btn"
                  >
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
                <h2>A Few Facts About Our University</h2>
              </div>
              <div class="col-lg-6">
                <div class="row">
                  <div class="col-12">
                    <div class="count-area-content percentage">
                      <div class="count-digit">94</div>
                      <div class="count-title">Succesed Students</div>
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
          <div class="col-lg-6 align-self-center">
            <div class="video">
              <a
                href="https://www.youtube.com/watch?v=HndV87XpkWg"
                target="_blank"
                ><img src="assets/images/play-icon.png" alt=""
              /></a>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="section contact-us" id="contact" data-section="contact">
      <div class="container">
        <div class="row">
          <div class="col-lg-9 align-self-center">
            <div class="row">
              <div class="col-lg-12">
                <form id="contact" action="" method="post">
                  <div class="row">
                    <div class="col-lg-12">
                      <h2>Let's get in touch</h2>
                    </div>
                    <div class="col-lg-4">
                      <fieldset>
                        <input
                          name="name"
                          type="text"
                          id="name"
                          placeholder="YOURNAME...*"
                          required=""
                        />
                      </fieldset>
                    </div>
                    <div class="col-lg-4">
                      <fieldset>
                        <input
                          name="email"
                          type="text"
                          id="email"
                          pattern="[^ @]*@[^ @]*"
                          placeholder="YOUR EMAIL..."
                          required=""
                        />
                      </fieldset>
                    </div>
                    <div class="col-lg-4">
                      <fieldset>
                        <input
                          name="subject"
                          type="text"
                          id="subject"
                          placeholder="SUBJECT...*"
                          required=""
                        />
                      </fieldset>
                    </div>
                    <div class="col-lg-12">
                      <fieldset>
                        <textarea
                          name="message"
                          type="text"
                          class="form-control"
                          id="message"
                          placeholder="YOUR MESSAGE..."
                          required=""
                        ></textarea>
                      </fieldset>
                    </div>
                    <div class="col-lg-12">
                      <fieldset>
                        <button type="submit" id="form-submit" class="button">
                          SEND MESSAGE NOW
                        </button>
                      </fieldset>
                    </div>
                  </div>
                </form>
              </div>
            </div>
          </div>
          <div class="col-lg-3">
            <div class="right-info">
              <ul>
                <li>
                  <h6>Phone Number</h6>
                  <span>010-020-0340</span>
                </li>
                <li>
                  <h6>Email Address</h6>
                  <span>info@meeting.edu</span>
                </li>
                <li>
                  <h6>Street Address</h6>
                  <span>Rio de Janeiro - RJ, 22795-008, Brazil</span>
                </li>
                <li>
                  <h6>Website URL</h6>
                  <span>www.meeting.edu</span>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import { onMounted, ref, nextTick } from "vue";
import api from "../api/axios";
import defaultCover from "@/assets/images/default-cover.png";
import RequestBook from "@/views/Book-Pages/RequestBook.vue";

export default {
  name: "HomeView",
  components: {
    RequestBook,
  },
  setup() {
    const books = ref([]);
    const recentlyAddedBooks = ref([]);

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

      scripts.forEach((src) => {
        const script = document.createElement("script");
        script.src = src;
        script.async = true;
        document.body.appendChild(script);
      });

      const res = await api.get("/books?most_borrowed=true&limit=10");
      books.value = res.data.books;
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
            {
              breakpoint: 1024,
              settings: {
                slidesToShow: 3,
              },
            },
            {
              breakpoint: 768,
              settings: {
                slidesToShow: 2,
              },
            },
            {
              breakpoint: 480,
              settings: {
                slidesToShow: 1,
              },
            },
          ],
        });
      } else {
        console.error("Slick failed to load!");
      }

      try {
        const { data } = await api.get("/books", {
          params: {
            page: 1,
            limit: 10,
            recently_added: true,
          },
        });

        if (data.code === "Success" && data.books) {
          recentlyAddedBooks.value = data.books.map((book) => ({
            id: book.id,
            title: book.title || "No Title",
            authors: book.authors || ["Unknown Author"],
            cover_url: book.cover_image || defaultCover,
            created_at: book.borrowed_at || new Date().toISOString(),
            borrow_count: book.borrowed ? 1 : 0,
          }));
        } else {
          console.error("No books found or error in response:", data.message);
        }
      } catch (error) {
        console.error("Error fetching recently added books:", error);
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

.popular-courses {
  background-color: #1f2a36;
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
  height: 200px;
  object-fit: cover;
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
  background-color: #f8f9fa;
}

.no-results p {
  text-align: center;
  font-size: 16px;
  color: #888;
}

.meeting-item {
  width: 200px;
  height: 380px;
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

.card-img-top {
  height: 220px;
  object-fit: cover;
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
</style>
