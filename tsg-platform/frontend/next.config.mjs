/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  poweredByHeader: false,
  productionBrowserSourceMaps: true,
  // Tarayıcı uzantılarından kaynaklanan hataları önlemek için
  experimental: {
    esmExternals: false,
  },
  // Environment değişkenlerini istemci tarafında kullanılabilir yap
  env: {
    NEXT_PUBLIC_SUPABASE_URL: process.env.NEXT_PUBLIC_SUPABASE_URL,
    NEXT_PUBLIC_SUPABASE_ANON_KEY: process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY,
  },
  // PWA desteği için
  pwa: {
    dest: 'public',
    disable: process.env.NODE_ENV === 'development',
  },
  // Görseller için domain ayarları
  images: {
    domains: ['localhost'],
  },
  // Webpack yapılandırması
  webpack: (config, { isServer }) => {
    // Eğer gerekirse, buraya özel webpack kuralları ekleyebilirsiniz
    return config;
  },
};

export default nextConfig;
