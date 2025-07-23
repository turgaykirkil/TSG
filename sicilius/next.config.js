/** @type {import('next').NextConfig} */
const nextConfig = {
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'http://backend:5001/api/:path*', // Docker backend servisi
      },
    ];
  },
};

module.exports = nextConfig;
