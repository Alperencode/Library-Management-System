import { createRouter, createWebHistory } from "vue-router";
import Login from "@/views/Auth/Login.vue";
import Register from "@/views/Auth/Register.vue";
import HomeView from "@/views/HomeView.vue";
import MeetingDetails from "@/views/MeetingDetails.vue";
import UserPage from "@/views/UserPage.vue";
import BooksPage from "@/views/BooksPage.vue";

// Sub-pages of User-Page
import AccountManagement from "@/views/AccountManagement.vue";
import BorrowedBooks from "@/views/BorrowedBooks.vue";
import RequestedBooks from "@/views/RequestedBooks.vue";
import NotifyMeList from "@/views/NotifyMe.vue";
import BorrowHistory from "@/views/BorrowHistory.vue";

const routes = [
  { path: "/", component: HomeView },
  { path: "/login", component: Login },
  { path: "/register", component: Register },
  { path: "/meetings", component: MeetingDetails },
  { path: '/books', component: BooksPage },

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
