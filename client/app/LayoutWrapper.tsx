"use client";

import { useEffect } from "react";
import { useAuthStore } from "@/store/authStore";
import Navbar from "./components/Navbar";


const LayoutWrapper = ({ children }: { children: React.ReactNode }) => {
  const checkAuth = useAuthStore((state) => state.checkAuth);

  useEffect(() => {
    checkAuth();
  }, [checkAuth]);

  return (
    <>
      <Navbar />
      {children}
    </>
  )
}

export default LayoutWrapper
