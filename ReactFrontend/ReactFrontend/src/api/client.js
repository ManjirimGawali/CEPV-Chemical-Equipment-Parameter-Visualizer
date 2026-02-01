import axios from "axios";

const baseURL = import.meta.env.VITE_API_BASE_URL;
const api = axios.create({
  baseURL: baseURL + "/api/",
});

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("token");
    if (token) {
      config.headers.Authorization = `Token ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error),
);

export default api;
