const path = require('path');

/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  poweredByHeader: false,
  productionBrowserSourceMaps: process.env.NODE_ENV === 'development',

  // Security headers
  async headers() {
    return [
      {
        source: '/(.*)',
        headers: [
          {
            key: 'X-Content-Type-Options',
            value: 'nosniff',
          },
          {
            key: 'X-Frame-Options',
            value: 'DENY',
          },
          {
            key: 'X-XSS-Protection',
            value: '1; mode=block',
          },
        ],
      },
    ];
  },

  // Environment variables
  env: {
    NEXT_PUBLIC_SUPABASE_URL: process.env.NEXT_PUBLIC_SUPABASE_URL,
    NEXT_PUBLIC_SUPABASE_ANON_KEY: process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY,
    NEXTAUTH_URL: process.env.NEXTAUTH_URL || 'http://localhost:3000',
    NEXTAUTH_SECRET: process.env.NEXTAUTH_SECRET,
  },

  // Webpack configuration
  webpack: (config, { isServer }) => {
    const resolvedSrcPath = path.resolve(__dirname, 'src');
    // Log only once during the build process
    if (isServer) {
      console.log('--- [DEBUG] Webpack Alias Resolution ---');
      console.log('__dirname:', __dirname);
      console.log('Resolved @ path:', resolvedSrcPath);
      console.log('------------------------------------');
    }

    // Add path aliases
    config.resolve.alias = {
      ...config.resolve.alias,
      '@': resolvedSrcPath,
    };

    return config;
  },

  // Image domains
  images: {
    domains: ['localhost'],
  },
};

module.exports = nextConfig;
