import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export async function middleware(request: NextRequest) {
  const token = request.cookies.get('auth_token')?.value;
  const { pathname } = request.nextUrl;


  // Allow accessing /login even if a stale token cookie exists.
  // Do NOT auto-redirect to /dashboard; validity will be checked client-side.

  // Define protected paths that require authentication
  const protectedPaths = ['/dashboard', '/admin', '/profile']; // Örnek korumalı yollar
  const isProtectedPath = protectedPaths.some(path => pathname.startsWith(path));

  // If there's no token and the user is trying to access a protected route,
  // redirect them to the login page.
  if (!token && isProtectedPath) {
    const loginUrl = new URL('/login', request.url);
    loginUrl.searchParams.set('callbackUrl', pathname);
    return NextResponse.redirect(loginUrl);
  }

  // Admin rol kontrolü sayfa içinde ve backend endpoint'lerinde yapılır.

  return NextResponse.next();
}

export const config = {
  matcher: [
    /*
     * Match all request paths except for the ones starting with:
     * - api (API routes)
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     * - and other static assets
     */
    '/((?!api|_next/static|_next/image|favicon.ico|logo.svg|placeholder.svg).*)',
  ],
};
