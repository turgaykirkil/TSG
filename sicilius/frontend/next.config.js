const path = require('path');

/** @type {import('next').NextConfig} */
const BACKEND_ORIGIN =
  process.env.BACKEND_ORIGIN ||
  (process.env.NODE_ENV === 'development'
    ? 'http://localhost:5001'
    : 'https://api.sicilius.com.tr');
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
      "script-src 'self' 'unsafe-inline' 'unsafe-eval' blob:;",
      "style-src 'self' 'unsafe-inline';",
      "img-src 'self' data: blob:;",
      "font-src 'self' data:;",
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
          {
            key: 'Permissions-Policy',
            // Tüm potansiyel riskli API'leri kapat
            value: 'camera=(), microphone=(), geolocation=(), payment=(), usb=(), fullscreen=*, accelerometer=(), ambient-light-sensor=(), autoplay=(), battery=(), clipboard-read=(), clipboard-write=(), display-capture=(), encrypted-media=(), gyroscope=(), magnetometer=(), midi=(), picture-in-picture=*',
          },
          { key: 'Cross-Origin-Opener-Policy', value: 'same-origin' },
          { key: 'Cross-Origin-Resource-Policy', value: 'same-origin' },
          { key: 'Cross-Origin-Embedder-Policy', value: 'require-corp' },
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
