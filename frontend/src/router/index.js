import { createRouter, createWebHistory } from "vue-router";
import { createToastInterface } from "vue-toastification";
import api from '@/api/axios'


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

// Admin-Page
import AdminPage from "@/views/Admin/AdminPage.vue";
import BookList from "@/views/Admin/Sub-Pages/BookList.vue";
import UserList from "@/views/Admin/Sub-Pages/UserList.vue";
import RequestList from "@/views/Admin/Sub-Pages/RequestList.vue";
import BorrowManagement from "@/views/Admin/Sub-Pages/BorrowManagement.vue";
import PenaltyManagement from "@/views/Admin/Sub-Pages/PenaltyManagement.vue";
import BannedUserManagement from "@/views/Admin/Sub-Pages/BannedUserManagement.vue";
import AdminAddBook from "@/views/Admin/Sub-Pages/AdminAddBook.vue";

//  Admin Dashboard Sub-Pages
import AdminDashboard from "@/views/Admin/Sub-Pages/AdminDashboard.vue";

import BookScanResult from "@/views/Scan-Pages/BookScanResult.vue";

// Not-Found
import NotFound from "@/views/NotFound.vue";

import UserDetail from "@/views/Admin/Sub-Pages/UserDetail.vue";

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
  { path: "/scan-book/:id", component: BookScanResult },

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
      { path: "users/:id", component: UserDetail },
    ],
  },
  { path: "/:pathMatch(.*)*", name: "NotFound", component: NotFound },
];

const toast = createToastInterface();
const router = createRouter({
  history: createWebHistory(),
  routes,
});

import { useAuth } from "@/composables/useAuth";

router.beforeEach((to, from, next) => {
  const { user, admin } = useAuth();

  const isAuthenticated = !!user.value || !!admin.value;
  const isAdmin = !!admin.value;
  const isUser = !!user.value;

  const adminPaths = ["/admin"];
  const userPaths = ["/user-page", "/request-book", "/scan-book"];

  const isAdminPage = adminPaths.some((path) => to.path.startsWith(path));
  const isUserPage = userPaths.some((path) => to.path.startsWith(path));

  if (!isAuthenticated && (isAdminPage || isUserPage)) {
    toast.error("You must be logged in to continue.");
    return next("/login");
  }

  if (isUserPage && !isUser) {
    toast.error("You need user privilages to continue.");
    return next("/");
  }

  if (isAdminPage && !isAdmin) {
    toast.error("You need admins privilages to continue.");
    return next("/");
  }

  return next();
});

router.afterEach((to, from) => {
  const leftScanBookRoute =
    from.path.startsWith("/scan-book/") && !to.path.startsWith("/scan-book/");

  if (leftScanBookRoute) {
    api.post("/remove-scanned").catch((err) => {
      console.warn(
        "Failed to remove scanned_book cookie:",
        err?.response?.data?.message || err.message
      );
    });
  }
});

export default router;
