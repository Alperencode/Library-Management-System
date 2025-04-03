import { createRouter, createWebHistory } from "vue-router";
import Login from "@/views/Auth/Login.vue";
import Register from "@/views/Auth/Register.vue";
import HomeView from "@/views/HomeView.vue";
import MeetingDetails from "@/views/MeetingDetails.vue";
import UserPage from "@/views/UserPage.vue";
import BooksPage from "@/views/BooksPage.vue";
import RequestBook from "@/views/RequestBook.vue";

// Sub-pages of User-Page
import AccountManagement from "@/views/AccountManagement.vue";
import BorrowedBooks from "@/views/BorrowedBooks.vue";
import RequestedBooks from "@/views/RequestedBooks.vue";
import NotifyMeList from "@/views/NotifyMe.vue";
import BorrowHistory from "@/views/BorrowHistory.vue";
import ScanBook from "@/views/ScanBook.vue";

import RfidScan from "@/views/RfidScan.vue";
import BarcodeScan from "@/views/BarcodeScan.vue";
import IsbnSearch from "@/views/IsbnSearch.vue";

const routes = [
  { path: "/", component: HomeView },
  { path: "/login", component: Login },
  { path: "/register", component: Register },
  { path: "/meetings", component: MeetingDetails },
  { path: "/books", component: BooksPage },
  { path: "/request-book", component: RequestBook },
  { path: "/scan-book", component: ScanBook },
  { path: "/rfid-scan", component: RfidScan },
  { path: "/barcode-scan", component: BarcodeScan },
  { path: "/isbn-search", component: IsbnSearch },

  {
    path: "/user-page",
    component: UserPage,
    children: [
      { path: "account", component: AccountManagement },
      { path: "borrowed", component: BorrowedBooks },
      { path: "requested", component: RequestedBooks },
      { path: "notify", component: NotifyMeList },
      { path: "history", component: BorrowHistory },
    ],
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
