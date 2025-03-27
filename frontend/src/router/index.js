import { createRouter, createWebHistory } from "vue-router";
import Login from "@/views/Auth/Login.vue";
import HomeView from "@/views/HomeView.vue";
import MeetingDetails from "@/views/MeetingDetails.vue";
import Register from "@/views/Auth/Register.vue";

const routes = [
  { path: '/', component: HomeView }, 
  { path: "/login", component: Login },
  { path: "/register", component: Register },
  { path: "/meetings", component: MeetingDetails },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;