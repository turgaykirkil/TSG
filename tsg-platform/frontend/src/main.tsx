// Polyfill'leri en üste ekleyin
import './polyfills';

import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import { ThemeProvider } from '@/contexts/ThemeContext';
import { AuthProvider } from '@/contexts/AuthContext';
import './globals.css';
import App from './App.tsx';

// Set the default theme based on system preference or saved preference
const rootElement = document.documentElement;
const savedTheme = localStorage.getItem('theme');
const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;

if (savedTheme === 'dark' || (!savedTheme && systemPrefersDark)) {
  rootElement.classList.add('dark');
  document
    .querySelector('meta[name="theme-color"]')
    ?.setAttribute('content', '#0f172a'); // slate-900
} else {
  rootElement.classList.remove('dark');
  document
    .querySelector('meta[name="theme-color"]')
    ?.setAttribute('content', '#ffffff');
}

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <BrowserRouter>
      <ThemeProvider>
        <AuthProvider>
          <App />
        </AuthProvider>
      </ThemeProvider>
    </BrowserRouter>
  </StrictMode>,
);
