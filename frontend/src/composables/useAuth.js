import { useStore } from "vuex";
import api from "@/api/axios";

let userPromise = null

export const useAuth = () => {
  const store = useStore();

  const fetchUser = async () => {
    if (store.state.user || userPromise) return userPromise;

    userPromise = api.get("/me")
      .then((res) => {
        if (res.data.user) {
          store.commit("setUser", res.data.user);
        }
      })
      .catch(() => {
        store.commit("setUser", null);
      });

    return userPromise;
  };

  return { fetchUser };
};