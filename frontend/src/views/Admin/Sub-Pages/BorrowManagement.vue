<template>
  <div class="admin-borrow-container">
    <h2>Borrowed Books</h2>

    <div v-if="borrowedBooks.length > 0" class="book-table-wrapper">
      <table class="book-table">
        <thead>
          <tr>
            <th>Cover</th>
            <th>Title</th>
            <th>Borrowed By</th>
            <th>Days Left</th>
            <th>Penalty Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="(book, index) in borrowedBooks"
            :key="book.id"
            class="fade-in-row"
            :style="{ animationDelay: `${index * 80}ms` }"
          >
            <td>
              <img :src="book.cover_image || defaultCover" alt="Cover" class="book-cover" />
            </td>
            <td>{{ book.title }}</td>
            <td>{{ book.currently_borrowed_by || 'Unknown' }}</td>
            <td>{{ getDaysLeft(book.return_date) }} days</td>
            <td>
              <span :class="getPenaltyClass(book)">
                {{ getPenaltyStatus(book) }}
              </span>
            </td>
            <td>
              <button class="edit-btn">Edit</button>
              <button class="delete-btn">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-else class="no-books">No borrowed books found.</div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import defaultCover from '@/assets/images/default-cover.png'

const borrowedBooks = ref([
  {
    id: "67e9de6730295c36e6ba0cef",
    title: "Sevgili Jude",
    authors: ["Thomas Hardy"],
    publisher: "Altinpost Yayinevi",
    cover_image: "http://books.google.com/books/content?id=-BzangEACAAJ&printsec=frontcover&img=1&zoom=1&imgtk=AFLRE73EKr2k1RVBMJdDUp9lueKJIOwq04AUCkFZOk7fgAwhSmLIs3Pf5EQcMhy3oxAf2k8lD7IC6ttsmWBuy1lYHFQr0JgLdPhIiCSZ_N3KN80Duh1TN-mkJuzjnmtD8eKU89_e8oeN&source=gbs_api",
    borrowed: true,
    isbn: "6054715968",
    borrowed_at: "2025-04-08T22:45:42.078000",
    return_date: "2025-04-20T23:59:00",
    currently_borrowed_by: "John Doe",
    penalty_status: "No Penalty"
  },
  {
    id: "68e9de6730295c36e6ba0cf0",
    title: "The Catcher in the Rye",
    authors: ["J.D. Salinger"],
    publisher: "Little, Brown and Company",
    cover_image: "https://covers.openlibrary.org/b/id/8225262-L.jpg",
    borrowed: true,
    isbn: "0316769487",
    borrowed_at: "2025-04-01T15:32:45.000000",
    return_date: "2025-04-15T23:59:00",
    currently_borrowed_by: "Jane Smith",
    penalty_status: "Overdue"
  }
])

const getDaysLeft = (returnDate) => {
  const returnDateObj = new Date(returnDate)
  const today = new Date()
  const diffTime = returnDateObj - today
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
  return diffDays
}

const getPenaltyStatus = (book) => {
  const daysLeft = getDaysLeft(book.return_date)
  if (daysLeft < 0) {
    return "Overdue"
  }
  return book.penalty_status || "No Penalty"
}

const getPenaltyClass = (book) => {
  const daysLeft = getDaysLeft(book.return_date)
  if (daysLeft < 0) {
    return "overdue-penalty"
  }
  return "no-penalty"
}

onMounted(() => {
  // API call to fetch borrowed books
})
</script>

<style scoped>

.admin-borrow-container {
  padding: 24px;
}

.book-table-wrapper {
  overflow-x: auto;
  margin-top: 20px;
}

.book-table {
  width: 100%;
  border-collapse: collapse;
}

.book-table th,
.book-table td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #eee;
}

.book-cover {
  width: 50px;
  height: 70px;
  object-fit: cover;
  border-radius: 4px;
}

.no-penalty {
  color: green;
  font-weight: bold;
}

.overdue-penalty {
  color: red;
  font-weight: bold;
}

.ellipsis {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.edit-btn,
.delete-btn {
  padding: 6px 12px;
  margin-right: 8px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}

.edit-btn {
  background-color: #3498db;
  color: white;
}

.delete-btn {
  background-color: #e74c3c;
  color: white;
}

.no-books {
  text-align: center;
  font-style: italic;
}

</style>
