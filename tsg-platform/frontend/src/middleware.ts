import { withAuth } from 'next-auth/middleware';

// Public rotalar (auth gerektirmez)
const PUBLIC_PATHS = [
  '/',
  '/about',
  '/contact',
  '/login',
  '/register',
  '/forgot-password',
  '/reset-password',
];

export default withAuth({
  callbacks: {
    authorized: ({ token, req }) => {
      const { pathname } = req.nextUrl;

      // Public path ise izin ver
      if (PUBLIC_PATHS.includes(pathname)) return true;

      // Oturum yoksa engelle
      if (!token) return false;

      // Admin route ise rol kontrolü yap
      if (pathname.startsWith('/admin') && (token as any).role !== 'admin') {
        return false;
      }

      return true;
    },
  },
});

// Configure which routes should be processed by this middleware
export const config = {
  matcher: [
    /*
     * Match all request paths except for the ones starting with:
     * - api (API routes)
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     * - public folder
     */
    '/((?!api|_next/static|_next/image|favicon.ico|.*\.(?:svg|png|jpg|jpeg|gif|webp)$).*)',
  ],
};
