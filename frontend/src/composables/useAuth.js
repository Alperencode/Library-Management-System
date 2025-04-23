import { ref } from 'vue'

const user = ref(JSON.parse(localStorage.getItem('user')))

export function useAuth() {
  const setUser = (val) => {
    user.value = val
    if (val) {
      localStorage.setItem('user', JSON.stringify(val))
    } else {
      localStorage.removeItem('user')
    }
  }

  return {
    user,
    setUser,
  }
}