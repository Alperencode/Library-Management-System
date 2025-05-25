import { createRouter, createWebHistory } from "vue-router";
import { createToastInterface } from "vue-toastification";
import api from '@/api/axios'


// Homeview
import HomeView from "@/views/HomeView.vue";

// Auth
import Login from "@/views/Auth/Login.vue";
import Register from "@/views/Auth/Register.vue";
import ForgotPassword from "@/views/Auth/ForgotPassword.vue";
import ResetPassword from "@/views/Auth/ResetPassword.vue";

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
import BookScanResult from "@/views/Scan-Pages/BookScanResult.vue";

// Admin-Pages
import AdminSidebar from "@/views/Admin/AdminSidebar.vue";
import AdminBookList from "@/views/Admin/Sub-Pages/AdminBookList.vue";
import AdminUserList from "@/views/Admin/Sub-Pages/AdminUserList.vue";
import AdminRequestList from "@/views/Admin/Sub-Pages/AdminRequestList.vue";
import AdminBorrowManagement from "@/views/Admin/Sub-Pages/AdminBorrowManagement.vue";
import AdminPenaltyManagement from "@/views/Admin/Sub-Pages/AdminPenaltyManagement.vue";
import AdminBannedUserManagement from "@/views/Admin/Sub-Pages/AdminBannedUserManagement.vue";
import AdminAddBook from "@/views/Admin/Sub-Pages/AdminAddBook.vue";
import AdminDashboard from "@/views/Admin/Sub-Pages/AdminDashboard.vue";
import AdminRequestDetails from '@/views/Admin/Sub-Pages/AdminRequestDetails.vue';

import AdminUserDetail from "@/views/Admin/Sub-Pages/AdminUserDetail.vue";
import AdminBookDetails from "@/views/Admin/Sub-Pages/AdminBookDetails.vue";
import NotFound from "@/views/NotFound.vue";
import AdminEditBook from "@/views/Admin/Sub-Pages/AdminEditBook.vue";
import AdminRequestAdded from "@/views/Admin/Sub-Pages/AdminRequestAdded.vue";
import AdminRequestDenied from '@/views/Admin/Sub-Pages/AdminRequestDenied.vue'

const routes = [
  // Homeview
  { path: "/", component: HomeView },

  // Auth
  { path: "/login", component: Login },
  { path: "/register", component: Register },
  { path: "/forgot-password", component: ForgotPassword },
  {
    path: "/reset-password",
    component: ResetPassword,
    beforeEnter: (to, from, next) => {
      if (!to.query.token) {
        toast.error("Reset token is missing.");
        return next("/login");
      }
      next();
    }
  },

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
    component: AdminSidebar,
    children: [
      { path: "", redirect: "/admin/dashboard" },
      { path: "books", component: AdminBookList },
      { path: "users", component: AdminUserList },
      { path: "dashboard", component: AdminDashboard },
      { path: "requests", component: AdminRequestList },
      { path: "borrow", component: AdminBorrowManagement },
      { path: "penalty", component: AdminPenaltyManagement },
      { path: "banned-users", component: AdminBannedUserManagement },
      { path: "add-book", component: AdminAddBook },
      { path: "users/:id", component: AdminUserDetail },
      { path: "books/:id", component: AdminBookDetails },
      { path: 'requests/:id', component: AdminRequestDetails },
      { path: "/admin/edit-book/:id", component: AdminEditBook },
      { path: "requests/added", component: AdminRequestAdded },
      { path: 'requests/denied', component: AdminRequestDenied },
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
    toast.error("You need user privileges to continue.");
    return next("/admin");
  }

  if (isAdminPage && !isAdmin) {
    toast.error("You need admins privileges to continue.");
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
