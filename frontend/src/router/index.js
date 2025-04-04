import { createRouter, createWebHistory } from "vue-router";

// Homeview
import HomeView from "@/views/HomeView.vue";

// Auth
import Login from "@/views/Auth/Login.vue";
import Register from "@/views/Auth/Register.vue";

// User-Pages
import UserPage from "@/views/User-Pages/UserPage.vue";
import AccountManagement from "@/views/User-Pages/Sub-Pages/AccountManagement.vue";
import BorrowedBooks from "@/views/User-Pages/Sub-Pages/BorrowedBooks.vue";
import RequestedBooks from "@/views/User-Pages/Sub-Pages/RequestedBooks.vue";
import NotifyMeList from "@/views/User-Pages/Sub-Pages/NotifyMe.vue";
import BorrowHistory from "@/views/User-Pages/Sub-Pages/BorrowHistory.vue";

// Book-Pages
import BooksPage from "@/views/Book-Pages/BooksPage.vue";
import BookDetails from "@/views/Book-Pages/BookDetails.vue";
import RequestBook from "@/views/Book-Pages/RequestBook.vue";

// Scan-Pages
import ScanBook from "@/views/Scan-Pages/ScanBook.vue";
import RfidScan from "@/views/Scan-Pages/RfidScan.vue";
import BarcodeScan from "@/views/Scan-Pages/BarcodeScan.vue";
import IsbnSearch from "@/views/Scan-Pages/IsbnSearch.vue";


const routes = [
  // Homeview
  { path: "/", component: HomeView },

  // Auth
  { path: "/login", component: Login },
  { path: "/register", component: Register },

  // User-Pages
  {
    path: "/User-Pages",
    component: UserPage,
    children: [
      { path: "account", component: AccountManagement },
      { path: "borrowed", component: BorrowedBooks },
      { path: "requested", component: RequestedBooks },
      { path: "notify", component: NotifyMeList },
      { path: "history", component: BorrowHistory },
    ],
  },

  // Book-Pages
  { path: "/books", component: BooksPage },
  { path: '/books/:id', component: BookDetails },
  { path: "/request-book", component: RequestBook },

  // Scan-Pages
  { path: "/scan-book", component: ScanBook },
  { path: "/rfid-scan", component: RfidScan },
  { path: "/barcode-scan", component: BarcodeScan },
  { path: "/isbn-search", component: IsbnSearch },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
