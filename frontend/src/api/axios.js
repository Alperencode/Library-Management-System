import axios from 'axios'
import store from '@/store'
import { createToastInterface } from 'vue-toastification'

const protocol = window.location.protocol;
const hostname = process.env.VUE_APP_API_HOST || window.location.hostname;
const port = process.env.VUE_APP_API_PORT || 8000;
const baseUrl = `${protocol}//${hostname}:${port}/api/v1`;
const toast = createToastInterface()

const api = axios.create({
  baseURL: baseUrl,
  withCredentials: true,
})

const plainAxios = axios.create({
  baseURL: baseUrl,
  withCredentials: true,
})

let isRefreshing = false
let failedQueue = []
let hasRedirected = false;

api.interceptors.response.use(
  (res) => {
    // Handle API responses that return { success: false }
    if (res?.data?.success === false) {
      const msg = res.data.message || res.data.detail;
      if (msg) toast.error(msg);
    }
    return res;
  },
  async (err) => {
    const extractPath = (url) => {
      try {
        const parsed = new URL(url, baseUrl);
        return parsed.pathname.replace('/api/v1', '');
      } catch {
        return url.startsWith('/api/v1') ? url.replace('/api/v1', '') : url;
      }
    };
    
    const originalPath = extractPath(originalPath.url);
    
    const ignoredPaths = [
      '/', '/login', '/register', '/books', '/books/', '/scan-book'
    ];
    
    const ignoreCall = ignoredPaths.some(path => {
      if (path === '/') return originalPath === '/';
      if (path.endsWith('/')) return originalPath.startsWith(path);
      return originalPath === path || originalPath.startsWith(path + '/');
    });

    if (err.response?.status === 401 && !originalPath._retry && !ignoreCall) {
      if (isRefreshing) {
        return new Promise((resolve, reject) => {
          failedQueue.push({ resolve, reject });
        }).then(() => api(originalPath));
      }

      originalPath._retry = true;
      isRefreshing = true;

      try {
        const userId = store.state.user?.id || null;

        await plainAxios.post(
          '/refresh-token',
          userId ? { id: userId } : {},
          { withCredentials: true }
        );

        hasRedirected = false;
        return api(originalPath);
      } catch (error) {
        const router = require('@/router').default;
        if (!hasRedirected && router.currentRoute.value.path !== '/login') {
          hasRedirected = true;
          router.push('/login');
        }

        return Promise.reject(error);
      } finally {
        isRefreshing = false;
      }
    }

    if (!ignoreCall) {
      const generalMessage =
        err.response?.data?.message ||
        err.response?.data?.detail?.message ||
        "An unexpected error occurred";

      toast.dismiss();
      if (generalMessage) toast.error(generalMessage);
    }

    return Promise.reject(err);
  }
);

export default api
