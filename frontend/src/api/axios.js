import axios from 'axios'
import store from '@/store'

const protocol = window.location.protocol;
const hostname = process.env.VUE_APP_API_HOST || window.location.hostname;
const port = process.env.VUE_APP_API_PORT || 8000;
const baseUrl = `${protocol}//${hostname}:${port}/api/v1`;

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

const processQueue = (error) => {
  failedQueue.forEach(({ resolve, reject }) => {
    error ? reject(error) : resolve()
  })
  failedQueue = []
}

api.interceptors.response.use(
  (res) => res,
  async (err) => {
    const originalRequest = err.config

    const ignoredPaths = ['/me','/refresh-token', '/login', '/register', '/books', '/books/', '/scan-book', '/'];
    const ignoreCall = ignoredPaths.some(path => {
      if (path === '/') return originalRequest.url === '/';
      if (path.endsWith('/')) return originalRequest.url.startsWith(path);
      return originalRequest.url === path || originalRequest.url.startsWith(path + '/');
    });
    if (err.response?.status === 401 && !originalRequest._retry && !ignoreCall) {
      if (isRefreshing) {
        return new Promise((resolve, reject) => {
          failedQueue.push({ resolve, reject })
        }).then(() => {
          return api(originalRequest)
        })
      }

      originalRequest._retry = true
      isRefreshing = true

      try {
        const userId = store.state.user?.id || null
        await plainAxios.post(
          '/refresh-token',
          userId ? { id: userId } : {},
          { withCredentials: true }
        )
        hasRedirected = false;
        return api(originalRequest)
      } catch (error) {
        processQueue(error)
        const router = require('@/router').default;
        if (!hasRedirected && router.currentRoute.value.path !== '/login') {
          hasRedirected = true;
          router.push('/login');
        }
        return Promise.reject(error)
      } finally {
        isRefreshing = false
      }
    }

    return Promise.reject(err)
  }
)

export default api