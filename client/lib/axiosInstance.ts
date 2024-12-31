import axios from "axios";

import { useAuthStore } from "../store/authStore";
import { redirect } from "next/navigation";


const axiosInstance = axios.create({baseURL: process.env.NEXT_PUBLIC_API_URL});

// Add request interceptor
axiosInstance.interceptors.request.use(
  (config) => {
    const accessToken = useAuthStore.getState().accessToken;
    
    // Do something before request is sent
    if (accessToken) {
      config.headers["Authorization"] = `Bearer ${accessToken}`;
    }
    return config;
  },
  (error) => {
    // Do something with request error
    return Promise.reject(error);
  }
);

// Add response interceptor
axiosInstance.interceptors.response.use(
  (response) => {
    // Any status code that lie within the range of 2xx cause this function to trigger
    // Do something with response data
    return response;
  },
  async (error) => {
    // Any status codes that falls outside the range of 2xx cause this function to trigger
    // Do something with response error
    const originalRequest = error.config;

    const setAccessToken = useAuthStore.getState().setAccessToken;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const token = await refreshAcessToken();

        // retry original request and rehydrate token state
        if (token) {
          setAccessToken(token);
          axiosInstance.defaults.headers.common["Authorization"] = `Bearer ${token}`;
          return axiosInstance(originalRequest);
        }
      } catch (error) {
        // refirect to login page
        redirect("/login");
        return Promise.reject(error);
      }
    }
    return Promise.reject(error);
  }
);

const refreshAcessToken = async () => {
  try {
    const response = await axiosInstance.post("/auth/refresh");
    return response.data.accessToken;
  } catch (error) {
    console.log("Error refreshing token", error);
    return null;
  }
}

export default axiosInstance;
