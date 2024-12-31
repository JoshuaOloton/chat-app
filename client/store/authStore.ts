import { create } from "zustand";
import axiosInstance from "@/lib/axiosInstance";


interface AuthStore {
  authUser: any;
  accessToken: string | null;
  isSigningIn: boolean;
  isSigningUp: boolean;
  isCheckAuth: boolean;

  setAccessToken: (token: string) => void;
  checkAuth: () => Promise<void>;
  clearAuth: () => void;
}

export const useAuthStore = create<AuthStore>((set) => ({
  authUser: null,
  accessToken: null,
  isSigningIn: false,
  isSigningUp: false,

  isCheckAuth: true,

  setAccessToken: (token: string) => {
    set({ accessToken: token });
  },

  checkAuth: async () => {
    try {
      const response = await axiosInstance.post("/auth/refresh");
      if (response.data.user) {
        set({ 
          authUser: response.data.user, 
          accessToken: response.data.accessToken
        });
      }
    } catch (error) {
      set({ 
        authUser: null,
        accessToken: null
      });
    } finally {
      set({ 
        isCheckAuth: false 
      });
    }
  },

  clearAuth: () => {
    set({ 
      authUser: null,
      accessToken: null
    });
  }
}));
