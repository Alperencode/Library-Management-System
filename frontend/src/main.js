import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import Toast from 'vue-toastification'
import 'vue-toastification/dist/index.css'

import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.min.js';
import 'bootstrap';

const app = createApp(App);
app.use(router);
app.use(Toast)
app.mount("#app");