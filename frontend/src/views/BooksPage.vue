<template>
  <div>
    <MainHeader />
    <section class="meetings-page" id="meetings">
      <div class="container two-column-layout">
        <div class="sidebar">
          <FiltersPanel />
        </div>
        <div class="main-content">
          <SearchBar v-model="searchQuery" @order="orderBy" />
          <div v-if="paginatedBooks.length === 0" class="no-results">
            <p class="no-results-text">No books found for "{{ searchQuery }}"</p>
          </div>
          <div class="row grid">
            <div
              v-for="(meeting, index) in paginatedBooks"
              :key="index"
              class="meeting-item"
              :ref="el => setBooksRef(meeting.title, el)"
            >
              <div class="meeting-box">
                <div class="thumb">
                  <router-link :to="meeting.link">
                    <img :src="meeting.image" :alt="meeting.title" />
                  </router-link>
                </div>
                <div class="down-content">
                  <router-link :to="meeting.link">
                    <h4>{{ meeting.title }}</h4>
                  </router-link>
                  <p v-html="meeting.description"></p>
                </div>
              </div>
            </div>
          </div>
          <PaginationControl
            :totalPages="totalPages"
            :currentPage="currentPage"
            @update:currentPage="currentPage = $event"
          />
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, computed, watch, nextTick } from 'vue';
import MainHeader from '@/components/MainHeader.vue';
import FiltersPanel from './FiltersPanel.vue';
import SearchBar from './SearchBar.vue';
import PaginationControl from './PaginationControl.vue';

const searchQuery = ref('');
const currentPage = ref(1);
const itemsPerPage = 9;

const books = ref([
  {
    title: 'New Lecturers Meeting',
    dateMonth: 'Nov',
    dateDay: '12',
    image: '/assets/images/meeting-01.jpg',
    link: '/meeting/1',
    description: 'Morbi in libero blandit lectus<br>cursus ullamcorper.',
  },
  {
    title: 'Online Teaching Techniques',
    dateMonth: 'Nov',
    dateDay: '14',
    image: '/assets/images/meeting-02.jpg',
    link: '/meeting/2',
    description: 'Morbi in libero blandit lectus<br>cursus ullamcorper.',
  },
  {
    title: 'deneme',
    dateMonth: 'Nov',
    dateDay: '12',
    image: '/assets/images/meeting-01.jpg',
    link: '/meeting/1',
    description: 'Morbi in libero blandit lectus<br>cursus ullamcorper.',
  },
  {
    title: 'test',
    dateMonth: 'Nov',
    dateDay: '12',
    image: '/assets/images/meeting-01.jpg',
    link: '/meeting/1',
    description: 'Morbi in libero blandit lectus<br>cursus ullamcorper.',
  },
  {
    title: 'simal',
    dateMonth: 'Nov',
    dateDay: '12',
    image: '/assets/images/meeting-01.jpg',
    link: '/meeting/1',
    description: 'Morbi in libero blandit lectus<strong>cursus ullamcorper.</strong>',
  },
  {
    title: 'alperen',
    dateMonth: 'Nov',
    dateDay: '12',
    image: '/assets/images/meeting-01.jpg',
    link: '/meeting/1',
    description: 'Morbi in libero blandit lectus<br>cursus ullamcorper.',
  },
  {
    title: 'emirhan',
    dateMonth: 'Nov',
    dateDay: '12',
    image: '/assets/images/meeting-01.jpg',
    link: '/meeting/1',
    description: 'Morbi in libero blandit lectus<br>cursus ullamcorper.',
  },
]);

const BooksRefs = ref({});
const setBooksRef = (title, el) => {
  BooksRefs.value[title] = el;
};

const filteredBooks = computed(() =>
  books.value.filter((m) =>
    m.title.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
);

const totalPages = computed(() =>
  Math.ceil(filteredBooks.value.length / itemsPerPage)
);

const paginatedBooks = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage;
  return filteredBooks.value.slice(start, start + itemsPerPage);
});

const orderBy = (type) => {
  if (type === 'az') {
    books.value.sort((a, b) => a.title.localeCompare(b.title));
  } else if (type === 'za') {
    books.value.sort((a, b) => b.title.localeCompare(a.title));
  }
};

watch(searchQuery, async () => {
  currentPage.value = 1;
  await nextTick();
  const firstBook = filteredBooks.value[0];
  if (!firstBook) return;
  const firstRef = BooksRefs.value[firstBook.title];
  if (firstRef && typeof firstRef.scrollIntoView === 'function') {
    firstRef.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }
});
</script>

<style scoped>
.meetings-page {
  display: flex;
  min-height: 100vh;
}

.two-column-layout {
  display: flex;
  flex: 1;
}

.sidebar {
  width: 250px;
  background-color: rgba(255, 255, 255, 0.02);
  backdrop-filter: blur(5px);
  -webkit-backdrop-filter: blur(5px);
  box-shadow: 2px 0 8px rgba(0, 0, 0, 0.05);
  border-right: 1px solid rgba(0, 0, 0, 0.05);
  border-top: 1px solid rgba(0, 0, 0, 0.02);
  padding: 16px;
  position: sticky;
  top: 0;
  align-self: flex-start;
  height: 100vh;
  overflow-y: auto;
  padding-top: 50px;
  margin-top: 15px;
}

.main-content {
  flex: 1;
  padding: 24px;
  background-color: transparent;
}

.no-results {
  color: #ffffff !important;
  padding: 20px;
  font-size: 18px;
  text-align: center;
  border-radius: 8px;
  font-weight: 600;
  z-index: 1000;
  position: relative;
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
}

.thumb img {
  width: 100%;
  border-radius: 6px;
}
</style>
