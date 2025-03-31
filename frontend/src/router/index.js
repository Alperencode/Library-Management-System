import { createRouter, createWebHistory } from "vue-router";
import Login from "@/views/Auth/Login.vue";
import Register from "@/views/Auth/Register.vue";
import HomeView from "@/views/HomeView.vue";
import MeetingDetails from "@/views/MeetingDetails.vue";
import BooksPage from "@/views/BooksPage.vue";    

const routes = [
  { path: '/', component: HomeView },
  { path: '/login', component: Login, meta: { hideLayout: true } },
  { path: '/register', component: Register,meta: { hideLayout: true } },
  { path: '/books', component: BooksPage },
  { path: '/meeting/:id', component: MeetingDetails, meta: { hideLayout: true } },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;