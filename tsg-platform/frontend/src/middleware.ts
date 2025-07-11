import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  const token = request.cookies.get('auth_token')?.value;
  const { pathname } = request.nextUrl;

  // If there's a token and the user is trying to access the login page,
  // redirect them to the dashboard.
  if (token && pathname.startsWith('/login')) {
    return NextResponse.redirect(new URL('/dashboard', request.url));
  }

  // Define public paths that don't require authentication
  const publicPaths = ['/', '/login', '/register', '/about', '/contact'];
  const isPublicPath = publicPaths.some(path => 
    pathname === path || pathname.startsWith(`${path}/`)
  );

  // If there's no token and the user is trying to access a protected route,
  // redirect them to the login page.
  if (!token && !isPublicPath) {
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
