import axios from 'axios'
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

const extractApiPath = (url) => {
  try {
    const parsed = new URL(url, baseUrl);
    return parsed.pathname.replace('/api/v1', '');
  } catch {
    return url.startsWith('/api/v1') ? url.replace('/api/v1', '') : url;
  }
};

const ignoredApiToastPaths = [
  '/refresh-token'
];

api.interceptors.response.use(
  (res) => {
    if (res?.data?.success === false) {
      const msg = res.data.message || res.data.detail;
      if (msg) toast.error(msg);
    }
    return res;
  },
  async (err) => {
    const originalRequest = err?.config || {};
    const originalPath = extractApiPath(originalRequest.url);

    const isIgnoredForToast = ignoredApiToastPaths.includes(originalPath);

    if (
      err.response?.status === 401 &&
      !originalRequest._retry &&
      !isIgnoredForToast &&
      originalRequest?.url
    ) {
      if (isRefreshing) {
        return new Promise((resolve, reject) => {
          failedQueue.push({ resolve, reject });
        }).then(() => api(originalRequest));
      }

      originalRequest._retry = true;
      isRefreshing = true;

      try {
        const user = JSON.parse(localStorage.getItem("user"));
        const admin = JSON.parse(localStorage.getItem("admin"));
        const id = user?.id || admin?.id || null;

        await plainAxios.post(
          "/refresh-token",
          id ? { id: id } : {},
          { withCredentials: true }
        );

        hasRedirected = false;
        return api(originalRequest);
      } catch (error) {
        const router = require('@/router').default;
        if (!hasRedirected && router.currentRoute.value.path !== '/login') {
          hasRedirected = true;

          localStorage.removeItem("user");
          localStorage.removeItem("admin");

          router.push('/login');
        }

        return Promise.reject(error);
      } finally {
        isRefreshing = false;
      }
    }

    if (!isIgnoredForToast) {
      toast.dismiss();
      const generalMessage =
        err.response?.data?.message ||
        err.response?.data?.detail?.message ||
        err.response?.data?.detail ||
        "An unexpected error occurred";
      if (generalMessage) toast.error(generalMessage);
    }

    return Promise.reject(err);
  }
);

export default api