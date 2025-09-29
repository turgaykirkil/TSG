const path = require('path');

/** @type {import('next').NextConfig} */
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

  // Proxy API requests to the backend
  async rewrites() {
    return [
      {
        // Only proxy backend API (FastAPI) which is mounted under /api/v1
        source: '/api/v1/:path*',
        destination: 'http://localhost:5001/api/v1/:path*',
      },
    ];
  },

  // Security headers
  async headers() {
    const csp = [
      "default-src 'self';",
      // Next.js dev ihtiyaçları için 'unsafe-eval' ve style inline izinleri
      "script-src 'self' 'unsafe-inline' 'unsafe-eval' blob:;",
      "style-src 'self' 'unsafe-inline';",
      "img-src 'self' data: blob:;",
      "font-src 'self' data:;",
      // Backend ve dev sunucularına bağlantı izni
      "connect-src 'self' http://localhost:5001 http://localhost:3000 http://localhost:3001 ws://localhost:3000 ws://localhost:3001;",
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
          // HSTS: prod ortamında etkilidir
          { key: 'Strict-Transport-Security', value: 'max-age=63072000; includeSubDomains; preload' },
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
