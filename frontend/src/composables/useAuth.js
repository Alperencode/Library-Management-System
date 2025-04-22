import api from "@/api/axios";

let userPromise = null

export const useAuth = () => {

  const fetchUser = async () => {
    if (localStorage.getItem("user") || userPromise) return userPromise;
  
    userPromise = api.get("/me")
      .then((res) => {
        if (res.data.user) {
          localStorage.setItem("user", JSON.stringify(res.data.user));
        }
      })
      .catch(() => {
        localStorage.removeItem("user");
      });
  
    return userPromise;
  };  

  return { fetchUser };
};