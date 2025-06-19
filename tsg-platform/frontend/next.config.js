const path = require('path');
const withPWA = require('next-pwa')({
  dest: 'public',
  register: true,
  skipWaiting: true,
  disable: process.env.NODE_ENV === 'development',
});

/** @type {import('next').NextConfig} */
const nextConfig = {
  webpack: (config, { isServer }) => {
    // Add path alias
    config.resolve.alias['@'] = path.join(__dirname, 'src');

    return config;
  },
};

module.exports = withPWA(nextConfig);
