import { createStore } from "vuex";
import axios from "axios";

const store = createStore({
  state: {
    user: null,
  },
  mutations: {
    setUser(state, user) {
      state.user = user;
    },
    logout(state) {
      state.user = null;
      localStorage.removeItem("user");
    }
  },
  actions: {
    async fetchUser({ commit }) {
      try {
        const response = await axios.get("http://127.0.0.1:8000/api/v1/me", { withCredentials: true });
        commit("setUser", response.data.user);
      } catch (error) {
        console.error("Kullanıcı bilgisi alınamadı:", error);
      }
    }
  },
  modules: {},
});

export default store;
