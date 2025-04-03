import { createRouter, createWebHistory } from "vue-router";
import Login from "@/views/Auth/Login.vue";
import Register from "@/views/Auth/Register.vue";
import HomeView from "@/views/HomeView.vue";
import UserPage from "@/views/UserPage/UserPage.vue";
import BooksPage from "@/views/Books/BooksPage.vue";
import BookDetails from "@/views/Books/BookDetails.vue";

// Sub-pages of User-Page
import AccountManagement from "@/views/UserPage/SubPages/AccountManagement.vue";
import BorrowedBooks from "@/views/UserPage/SubPages/BorrowedBooks.vue";
import RequestedBooks from "@/views/UserPage/SubPages/RequestedBooks.vue";
import NotifyMeList from "@/views/UserPage/SubPages/NotifyMe.vue";
import BorrowHistory from "@/views/UserPage/SubPages/BorrowHistory.vue";

const routes = [
  { path: "/", component: HomeView },
  { path: "/login", component: Login },
  { path: "/register", component: Register },
  { path: '/books/:id', component: BookDetails },
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
