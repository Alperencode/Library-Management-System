import axios from 'axios'
import store from '@/store'

const api = axios.create({
  baseURL: 'http://localhost:8000/api/v1',
  withCredentials: true,
})

const plainAxios = axios.create({
  baseURL: 'http://localhost:8000/api/v1',
  withCredentials: true,
})

let isRefreshing = false
let failedQueue = []
let hasRedirected = false

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

    const ignoredPaths = ['/refresh-token', '/login', '/books', '/scan-book', '/'];
    const ignoreCall = ignoredPaths.includes(originalRequest.url);    if (err.response?.status === 401 && !originalRequest._retry && !ignoreCall) {
      if (isRefreshing) {
        return new Promise((resolve, reject) => {
          failedQueue.push({ resolve, reject })
        }).then(() => {
          if (!hasRedirected) {
            return api(originalRequest)
          }
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
        processQueue(null)
        if (!hasRedirected) {
          return api(originalRequest)
        }
      } catch (error) {
        processQueue(error)
        if (!hasRedirected) {
          hasRedirected = true
          const router = require('@/router').default;
          if (router.currentRoute.value.path !== '/login') {
            router.push('/login');
          }
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