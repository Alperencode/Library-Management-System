import { createRouter, createWebHistory } from 'vue-router';
import Login from '../views/Auth/Login.vue';
import Register from '../views/Auth/Register.vue';

const routes = [
  { path: '/login', component: Login },
  { path: '/register', component: Register }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;