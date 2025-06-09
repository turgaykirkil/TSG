import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { fileURLToPath } from 'url';
import path from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    react()
  ],
  server: {
    host: '0.0.0.0',
    port: 3000,
    strictPort: true,
    hmr: {
      clientPort: 3000,
      host: 'localhost',
      protocol: 'ws',
    },
    watch: {
      usePolling: true,
    },
    fs: {
      strict: false // node_modules içindeki dosyalara erişim için
    }
  },
  preview: {
    port: 3000,
    strictPort: true,
  },
  build: {
    outDir: 'dist',
    sourcemap: true,
    rollupOptions: {
      output: {
        manualChunks: {
          'pdf.worker': ['pdfjs-dist/build/pdf.worker.entry']
        }
      }
    }
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src')
    },
  },
  define: {
    'process.env': {},
    'process.browser': true,
    global: 'globalThis',
    'process.env.NODE_ENV': JSON.stringify(process.env.NODE_ENV || 'development'),
    'process.env.NODE_DEBUG': 'false',
  },
  worker: {
    format: 'es',
    plugins: () => [react()],
  },
  optimizeDeps: {
    include: ['react', 'react-dom', 'react-router-dom'],
    exclude: ['pdfjs-dist'],
    esbuildOptions: {
      define: {
        global: 'globalThis',
      },
      target: 'esnext'
    }
  }
})
