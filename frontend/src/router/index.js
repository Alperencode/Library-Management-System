import { createRouter, createWebHistory } from "vue-router";
import store from '@/store';

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
import OverdueBooks from "@/views/User-Pages/Sub-Pages/OverdueBooks.vue";

// Book-Pages
import BooksPage from "@/views/Book-Pages/BooksPage.vue";
import BookDetails from "@/views/Book-Pages/BookDetails.vue";
import RequestBook from "@/views/Book-Pages/RequestBook.vue";

// Scan-Pages
import ScanBook from "@/views/Scan-Pages/ScanBook.vue";
import RfidScan from "@/views/Scan-Pages/RfidScan.vue";
import BarcodeScan from "@/views/Scan-Pages/BarcodeScan.vue";
import IsbnSearch from "@/views/Scan-Pages/IsbnSearch.vue";

// Admin-Page
import AdminPage from "@/views/Admin/AdminPage.vue";
import BookList from "@/views/Admin/Sub-Pages/BookList.vue";
import UserList from "@/views/Admin/Sub-Pages/UserList.vue";
import RequestList from "@/views/Admin/Sub-Pages/RequestList.vue";
import BorrowManagement from "@/views/Admin/Sub-Pages/BorrowManagement.vue"
import PenaltyManagement from "@/views/Admin/Sub-Pages/PenaltyManagement.vue";
import BannedUserManagement from "@/views/Admin/Sub-Pages/BannedUserManagement.vue";
import AdminAddBook from "@/views/Admin/Sub-Pages/AdminAddBook.vue"

//  Admin Dashboard Sub-Pages
import AdminDashboard from "@/views/Admin/Sub-Pages/AdminDashboard.vue"
import BorrowCount from "@/views/Admin/Sub-Pages/Dashboard/BorrowCount.vue";
import PenaltyBookCount from "@/views/Admin/Sub-Pages/Dashboard/PenaltyBookCount.vue";
import BookRequests from "@/views/Admin/Sub-Pages/Dashboard/BookRequests.vue";
import PenaltyUserCount from "@/views/Admin/Sub-Pages/Dashboard/PenaltyUserCount.vue";
import CurrentBookCount from "@/views/Admin/Sub-Pages/Dashboard/CurrentBookCount.vue";

import BookScanResult from "@/views/Scan-Pages/BookScanResult.vue";

const routes = [
  // Homeview
  { path: "/", component: HomeView },

  // Auth
  { path: "/login", component: Login },
  { path: "/register", component: Register },

  // User-Pages
  {
    path: "/user-page",
    component: UserPage,
    children: [
      { path: "account", component: AccountManagement },
      { path: "borrowed", component: BorrowedBooks },
      { path: "requested", component: RequestedBooks },
      { path: "notify", component: NotifyMeList },
      { path: "history", component: BorrowHistory },
      { path: "overdue", component: OverdueBooks },
    ],
  },

  // Book-Pages
  { path: "/books", component: BooksPage },
  { path: "/books/:id", component: BookDetails },
  { path: "/request-book", component: RequestBook },

  // Scan-Pages
  { path: "/scan-book", component: ScanBook },
  { path: "/rfid-scan", component: RfidScan },
  { path: "/barcode-scan", component: BarcodeScan },
  { path: "/isbn-search", component: IsbnSearch },
  { path: "/scan-book/:id", component: BookScanResult},

  // Admin-Page
  {
    path: "/admin",
    component: AdminPage,
    children: [
      { path: "", redirect: "/admin/dashboard" },
      { path: "books", component: BookList },
      { path: "users", component: UserList },
      { path: "dashboard", component: AdminDashboard },
      { path: "requests", component: RequestList },
      { path: "borrow", component: BorrowManagement },
      { path: "penalty", component: PenaltyManagement },
      { path: "banned-users", component: BannedUserManagement },
      { path: "add-book", component: AdminAddBook },
      
      // Dashboard Sub-Routes
      { path: "dashboard/borrow-count", component: BorrowCount },
      { path: "dashboard/penalty-book", component: PenaltyBookCount },
      { path: "dashboard/requests", component: BookRequests },
      { path: "dashboard/penalty-users", component: PenaltyUserCount },
      { path: "dashboard/current-books", component: CurrentBookCount },
    ]
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const isAuthenticated = store.state.user !== null;

  const protectedPaths = ['/user-page', '/request-book', '/scan-book'];
  const requiresAuth = protectedPaths.some(path => to.path.startsWith(path));

  if (requiresAuth && !isAuthenticated) {
    return next('/login');
  }

  return next();
});

export default router;
