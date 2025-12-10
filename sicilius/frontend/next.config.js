const path = require('path');

/** @type {import('next').NextConfig} */
const BACKEND_ORIGIN =
  process.env.API_URL ||
  (process.env.NODE_ENV === 'development'
    ? 'http://localhost:5001'
    : 'http://sicilius-backend:5001');
const nextConfig = {

  webpack: (config, { isServer }) => {
    config.resolve.alias['@'] = path.join(__dirname, 'src');
    return config;
  },
  reactStrictMode: true,
  trailingSlash: true,
  poweredByHeader: false,
  productionBrowserSourceMaps: process.env.NODE_ENV === 'development',

  // Disable lint/type errors from failing production builds (Docker CI)
  eslint: {
    ignoreDuringBuilds: true,
  },
  typescript: {
    ignoreBuildErrors: true,
  },

  // Proxy API requests to the backend (server-side). Browser hep same-origin'e çağırır.
  async rewrites() {
    return [
      {
        source: '/nexus',
        destination: '/nexus/index.html',
      },
      {
        source: '/nexus/',
        destination: '/nexus/index.html',
      },
      {
        source: '/api/v1/:path*',
        destination: `${BACKEND_ORIGIN}/api/v1/:path*`,
      },
    ];
  },

  // Security headers
  async headers() {
    const connectSrc = [
      "'self'",
      'https://api.sicilius.com.tr',
      'https://sicilius.com.tr',
    ];
    if (process.env.NODE_ENV !== 'production') {
      connectSrc.push('http://localhost:5001');
    }

    const csp = [
      "default-src 'self';",
      // Next.js dev ihtiyaçları için 'unsafe-eval' ve style inline izinleri
      "script-src 'self' 'unsafe-inline' 'unsafe-eval' blob: https://cdn.tailwindcss.com https://cdn.jsdelivr.net https://cdn.plot.ly https://cdnjs.cloudflare.com;",
      "style-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com https://fonts.googleapis.com;",
      "img-src 'self' data: blob:;",
      "font-src 'self' data: https://fonts.gstatic.com https://cdnjs.cloudflare.com;",
      // Backend ve dev/prod sunucularına bağlantı izni
      `connect-src ${connectSrc.join(' ')};`,
      "frame-ancestors 'none';",
      "base-uri 'self';",
      "form-action 'self';",
    ].join(' ');

    return [
      {
        source: '/(.*)',
        headers: [
          { key: 'X-Content-Type-Options', value: 'nosniff' },
          { key: 'X-Frame-Options', value: 'DENY' },
          { key: 'Referrer-Policy', value: 'strict-origin-when-cross-origin' },
          { key: 'Referrer-Policy', value: 'strict-origin-when-cross-origin' },
          { key: 'Cross-Origin-Opener-Policy', value: 'same-origin' },
          { key: 'Cross-Origin-Resource-Policy', value: 'same-origin' },
          // CSP en sonda
          { key: 'Content-Security-Policy', value: csp },
        ],
      },
    ];
  },



  // Image domains
  images: {
    domains: ['localhost'],
  },
};

module.exports = nextConfig;
