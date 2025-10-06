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

  // Backend-enforced admin gate for /admin
  if (pathname.startsWith('/admin')) {
    try {
      const adminUrl = new URL('/api/v1/auth/require-admin', request.url);
      const res = await fetch(adminUrl, {
        // Pass through cookies for backend auth check
        headers: { cookie: request.headers.get('cookie') ?? '' },
        cache: 'no-store',
        credentials: 'include',
      });
      if (res.status !== 204) {
        // Fallback: fetch current user and inspect role
        try {
          const meUrl = new URL('/api/v1/users/me', request.url);
          const meRes = await fetch(meUrl, {
            headers: { cookie: request.headers.get('cookie') ?? '' },
            cache: 'no-store',
          });
          if (meRes.ok) {
            const data = await meRes.json().catch(() => null);
            const role = (data?.role ?? '').toString().toLowerCase();
            if (role === 'admin') {
              return NextResponse.next();
            }
          }
        } catch {}
        // Not admin -> apply env-based policy, default redirect to dashboard
        const disableAdmin = process.env.NEXT_PUBLIC_DISABLE_ADMIN === 'true';
        if (disableAdmin) {
          return new NextResponse('Not Found', { status: 404 });
        }
        return NextResponse.redirect(new URL('/dashboard', request.url));
      }
    } catch {
      // On any error contacting backend, fail closed to dashboard
      return NextResponse.redirect(new URL('/dashboard', request.url));
    }
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
