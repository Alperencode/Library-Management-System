<template>
    <div class="request-list-container">
      <h2 class="mb-4">Requested Books</h2>
  
      <div v-if="requests.length > 0" class="request-table-wrapper">
        <table class="request-table">
          <thead>
            <tr>
              <th>Cover</th>
              <th>Title</th>
              <th>Author</th>
              <th>Publisher</th>
              <th>Status</th>
              <th>Change Status</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="(book, index) in requests"
              :key="book.id"
              class="fade-in-row"
              :style="{ animationDelay: `${index * 80}ms` }"
            >
              <td>
                <img
                  :src="book.cover_image || defaultCover"
                  alt="Cover"
                  class="book-cover"
                />
              </td>
              <td>{{ book.title }}</td>
              <td class="ellipsis">{{ book.authors?.join(', ') || 'Unknown' }}</td>
              <td class="ellipsis">{{ book.publisher || 'Unknown' }}</td>
              <td>
                <span class="status-label">{{ book.status }}</span>
              </td>
              <td>
                <select v-model="book.status" @change="changeStatus(book)">
                  <option value="Request Sent">Request Sent</option>
                  <option value="Approved">Approved</option>
                  <option value="Denied">Denied</option>
                  <option value="Added">Added</option>
                </select>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
  
      <div v-else class="no-requests">No requested books found.</div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import defaultCover from '@/assets/images/default-cover.png'
  
  const requests = ref([])
  
  const mockData = [
    {
      id: '1',
      title: 'The Martian',
      authors: ['Andy Weir'],
      isbn: '9780804139021',
      publisher: 'Crown',
      cover_image: '',
      status: 'Request Sent',
    },
    {
      id: '2',
      title: 'Dune',
      authors: ['Frank Herbert'],
      isbn: '9780441172719',
      publisher: 'Ace Books',
      cover_image: '',
      status: 'Approved',
    }
  ]
  
  onMounted(() => {
    requests.value = mockData
  })

  
  const changeStatus = (book) => {
    console.log(`Status of "${book.title}" changed to "${book.status}"`)
      // API call to fetch requested books
  }
  </script>
  
  <style scoped>

  .request-list-container {
    padding: 24px;
  }
  
  .request-table-wrapper {
    overflow-x: auto;
    margin-top: 16px;
  }
  
  .request-table {
    width: 100%;
    border-collapse: collapse;
  }
  
  .request-table th,
  .request-table td {
    padding: 10px;
    border-bottom: 1px solid #eee;
    text-align: left;
    vertical-align: middle;
  }
  
  .book-cover {
    width: 50px;
    height: 70px;
    object-fit: cover;
    border-radius: 4px;
  }
  
  .ellipsis {
    max-width: 160px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
  
  .status-label {
    background-color: #f0f0f0;
    padding: 4px 10px;
    border-radius: 6px;
    font-size: 13px;
  }
  
  .no-requests {
    text-align: center;
    margin-top: 40px;
    font-style: italic;
  }
  
  .fade-in-row {
    animation: fadeUp 0.4s ease-out both;
  }
  
  @keyframes fadeUp {
    0% {
      opacity: 0;
      transform: translateY(15px);
    }
    100% {
      opacity: 1;
      transform: translateY(0);
    }
  }
  
  select {
    padding: 6px;
    border-radius: 4px;
    background-color: #f7f7f7;
    border: 1px solid #ccc;
  }
  
  </style>
  