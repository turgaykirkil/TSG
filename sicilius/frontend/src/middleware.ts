import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  const token = request.cookies.get('auth_token')?.value;
  const { pathname } = request.nextUrl;

  // Production hard block for /admin routes (admin only used locally)
  if (pathname.startsWith('/admin')) {
    const disableAdmin = process.env.NEXT_PUBLIC_DISABLE_ADMIN === 'true';
    if (disableAdmin) {
      return new NextResponse('Not Found', { status: 404 });
    }
  }

  // If there's a token and the user is trying to access the login page,
  // redirect them to the dashboard.
  if (token && pathname.startsWith('/login')) {
    return NextResponse.redirect(new URL('/dashboard', request.url));
  }

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
