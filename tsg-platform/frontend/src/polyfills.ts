// Sadece gerekli polyfill'leri ekliyoruz
if (typeof global === 'undefined' && typeof window !== 'undefined') {
  (window as any).global = window;
}

// Basit process polyfill
if (typeof process === 'undefined' && typeof window !== 'undefined') {
  (window as any).process = {
    env: { NODE_ENV: 'development' },
    versions: { node: '16.0.0' },
    browser: true,
    cwd: () => '/'
  };
}
