// Polyfills for browser environment to provide Node.js-like features
// required by some libraries.

// Defines a minimal `process` object structure for the polyfill.
interface ProcessPolyfill {
  env: { NODE_ENV?: 'development' | 'production' | 'test' };
  versions: { node: string; [key: string]: unknown };
  browser: true;
  cwd: () => string;
}

// --- Type Augmentation for Global Scope ---

declare global {
  // Extends the global Window interface to include `global` and `process`.
  interface Window {
    global: Window & typeof globalThis;
    process: ProcessPolyfill;
  }

  // Extends the global BigInt interface to include a `toJSON` method for serialization.
  interface BigInt {
    toJSON(): string;
  }
}

// --- Polyfill Implementation ---

// 1. Polyfill for `window.global`
if (typeof window !== 'undefined' && typeof window.global === 'undefined') {
  window.global = window;
}

// 2. Polyfill for `BigInt.prototype.toJSON`
if (typeof BigInt.prototype.toJSON === 'undefined') {
  BigInt.prototype.toJSON = function () {
    return this.toString();
  };
}

// 3. Polyfill for `window.process`
if (typeof window !== 'undefined' && typeof window.process === 'undefined') {
  window.process = {
    env: { NODE_ENV: 'development' },
    versions: { node: '18.0.0' },
    browser: true,
    cwd: () => '/',
  } as any;
}

// This export statement makes the file a module, which is required for global augmentations.
export {};
