// Sadece gerekli polyfill'leri ekliyoruz
if (typeof global === 'undefined' && typeof window !== 'undefined') {
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  (window as any).global = window;
}

// Basit process polyfill
if (typeof process === 'undefined' && typeof window !== 'undefined') {
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  (BigInt.prototype as any).toJSON = function () { return this.toString(); };
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  (window as any).process = {
    env: { NODE_ENV: 'development' },
    versions: { node: '16.0.0' },
    browser: true,
    cwd: () => '/'
  };
}
