import { NextRequest, NextResponse } from "next/server";


// protected routes
const protectedRoutes = ["/", "/profile"];

// public routes
const publicRoutes = ["/login", "/register"];


export default async function middleware(req: NextRequest) {
  const { pathname } = req.nextUrl;

  const token = req.headers.get("Authorization")?.split(" ")[1];

  const isProtectedRoute = pathname && protectedRoutes.includes(pathname);
  const isPublicRoute = pathname && publicRoutes.includes(pathname);

  if (token && isPublicRoute) {
    return NextResponse.redirect(new URL("/", req.nextUrl));
  }

  if (!token && isProtectedRoute) {
    return NextResponse.redirect(new URL("/login", req.nextUrl));
  }

  return NextResponse.next();

}
