import axios from 'axios'
import store from '@/store'

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/api/v1',
  withCredentials: true,
})

let isRefreshing = false
let failedQueue = []
let hasRedirected = false

const processQueue = (error) => {
  failedQueue.forEach(prom => {
    error ? prom.reject(error) : prom.resolve()
  })
  failedQueue = []
}

api.interceptors.response.use(
  res => res,
  async err => {
    const originalRequest = err.config

    if (err.response?.status === 401 && !originalRequest._retry) {
      if (isRefreshing) {
        return new Promise((resolve, reject) => {
          failedQueue.push({ resolve, reject })
        }).then(() => api(originalRequest))
      }

      originalRequest._retry = true
      isRefreshing = true

      try {
        const userId = store.state.user?.id || null

        await api.post(
          '/refresh-token',
          userId ? { id: userId } : null,
          { withCredentials: true }
        )

        processQueue(null)
        return api(originalRequest)
      } catch (refreshErr) {
        processQueue(refreshErr)
        if (!hasRedirected) {
          hasRedirected = true
          window.location.href = '/login'
        }
        return Promise.reject(refreshErr)
      } finally {
        isRefreshing = false
      }
    }

    return Promise.reject(err)
  }
)

export default api