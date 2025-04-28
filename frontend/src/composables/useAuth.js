import { ref } from 'vue'

const user = ref(JSON.parse(localStorage.getItem('user')))
const admin = ref(JSON.parse(localStorage.getItem('admin')))

export function useAuth() {
  const setUser = (val) => {
    user.value = val
    admin.value = null
    if (val) {
      localStorage.setItem('user', JSON.stringify(val))
      localStorage.removeItem('admin')
    } else {
      localStorage.removeItem('user')
    }
  }

  const setAdmin = (val) => {
    admin.value = val
    user.value = null
    if (val) {
      localStorage.setItem('admin', JSON.stringify(val))
      localStorage.removeItem('user')
    } else {
      localStorage.removeItem('admin')
    }
  }

  return {
    user,
    admin,
    setUser,
    setAdmin,
  }
}