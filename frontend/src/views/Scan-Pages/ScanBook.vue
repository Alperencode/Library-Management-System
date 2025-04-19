<template>
  <div class="scan-page">
    <div class="glass-card">
      <h2 class="scan-title">Scan a Book</h2>
      <ul class="scan-list">
        <li>Return a book you own</li>
        <li>Borrow a book you like</li>
        <li>Extend the return date</li>
      </ul>
      <p class="scan-subtext">Choose a method below to identify your book:</p>

      <div class="scan-options">
        <div class="scan-option">
          <button class="scan-btn" @click="goToRfidScan">RFID Scan</button>
          <p class="option-note">Use your RFID card</p>
        </div>
        <div class="scan-option">
          <button class="scan-btn" @click="goToBarcodeScan">Barcode Scan</button>
          <p class="option-note">Scan the book's barcode</p>
        </div>
      </div>
    </div>
    <section class="popular-courses" v-if="books.length">
      <div class="container">
        <h2 class="section-heading text-white text-center mb-5"> Most Borrowed Books </h2>
        <div class="slick-carousel">
          <div class="course-card" v-for="book in books" :key="book.id">
            <div class="card text-center text-dark">
              <router-link :to="`/books/${book.id}`" class="text-decoration-none">
                <img :src="book.cover_image || defaultCover" :alt="book.title" class="card-img-top" />
              </router-link>
              <div class="card-body d-flex flex-column justify-content-between">
                <div>
                  <h5 class="card-title" :title="book.title">{{ book.title }}</h5>
                  <p class="card-text text-muted" :title="book.authors?.join(', ')">
                    {{ book.authors?.join(', ') }}
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
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from "vue"
import { useRouter } from "vue-router"
import api from "@/api/axios"
import defaultCover from "@/assets/images/default-cover.png"
import $ from "jquery"
import "slick-carousel/slick/slick.css"
import "slick-carousel/slick/slick-theme.css"
import "slick-carousel"

window.$ = $
window.jQuery = $

const router = useRouter()

const books = ref([])

const goToRfidScan = () => router.push("/rfid-scan")
const goToBarcodeScan = () => router.push("/barcode-scan")

const fetchBooks = async () => {
  try {
    const res = await api.get("/books?most_borrowed=true&limit=10")
    books.value = res.data.books
    await nextTick()
    initSlider()
  } catch (err) {
    console.error("Book fetch failed", err)
  }
}

const initSlider = () => {
  if (window.$ && window.$(".slick-carousel").slick) {
    window.$(".slick-carousel").slick({
      slidesToShow: 4,
      slidesToScroll: 1,
      autoplay: true,
      autoplaySpeed: 3000,
      speed: 600,
      arrows: true,
      dots: true,
      infinite: true,
      pauseOnHover: true,
      responsive: [
        { breakpoint: 1024, settings: { slidesToShow: 3 } },
        { breakpoint: 768, settings: { slidesToShow: 2 } },
        { breakpoint: 480, settings: { slidesToShow: 1 } },
      ],
    })
  } else {
    console.error("Slick not loaded")
  }
}

onMounted(fetchBooks)
</script>

<style scoped>

.scan-page {
  min-height: 100vh;
  background: url("@/assets/images/meetings-bg.jpg") no-repeat center center fixed;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-top: 100px;
}

.glass-card {
  background: rgba(255, 255, 255, 0.08);
  border-radius: 20px;
  padding: 40px 30px;
  backdrop-filter: blur(10px);
  width: 100%;
  max-width: 700px;
  text-align: center;
  color: white;
}

.scan-title {
  font-size: 32px;
  font-weight: bold;
  background: linear-gradient(to right, #d4881a, #ffb347);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.scan-list {
  list-style-type: disc;
  margin: 0 auto 20px;
  padding-left: 20px;
  text-align: center;
  color: #ddd;
}

.scan-options {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 16px;
}

.scan-btn {
  background: linear-gradient(135deg, #d4881a, #f0a623);
  border: none;
  padding: 10px 20px;
  border-radius: 10px;
  font-weight: bold;
  color: white;
  cursor: pointer;
  transition: all 0.3s ease;
}

.scan-btn:hover {
  transform: translateY(-2px);
}

.popular-courses {
  background: url("@/assets/images/meetings-bg.jpg") no-repeat center center fixed;
  padding: 60px 0;
  width: 100%;
}

.section-heading {
  font-size: 28px;
  font-weight: 600;
  color: white;
}

.slick-carousel {
  width: 100%;
}

.course-card {
  padding: 10px;
}

.card {
  border: none;
  border-radius: 12px;
  overflow: hidden;
  background: white;
  height: 100%;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  transition: all 0.3s ease;
  transform: translateY(0);
}

.card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.2);
}

.card-img-top {
  height: 250px;
  object-fit: contain;
  padding-top: 10px;
  width: 100%;
}

.card-body {
  padding: 16px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  min-height: 160px;
}

.card-title {
  font-size: 16px;
  font-weight: bold;
  color: #333;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.card-text {
  font-size: 14px;
  color: #777;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}


.view-details-btn {
  font-size: 14px;
  color: #d4881a;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.2s;
}

.view-details-btn:hover {
  transform: translateX(4px);
}

.ellipsis {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.slick-prev:before,
.slick-next:before {
  color: #d4881a;
  font-size: 22px;
  opacity: 0.7;
}

.slick-dots li button:before {
  font-size: 10px;
  color: white;
  opacity: 0.5;
}

.slick-dots li.slick-active button:before {
  opacity: 1;
  color: #d4881a;
}

.scan-subtext, .option-note {
  color: white;
}

</style>
