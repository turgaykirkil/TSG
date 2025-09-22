import { Inter, Space_Grotesk } from 'next/font/google';
import 'leaflet/dist/leaflet.css';
import { cn } from '@/lib/utils';
import '@/globals.css';
import { AppProviders } from './AppProviders';

// Font ayarları
const inter = Inter({
  subsets: ['latin'],
  variable: '--font-inter',
  display: 'swap',
});

const spaceGrotesk = Space_Grotesk({
  subsets: ['latin'],
  variable: '--font-space-grotesk',
  display: 'swap',
});

export const metadata = {
  title: 'Sicilius',
  description: 'Sicilius Platform',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="tr" suppressHydrationWarning>
      <head>
        {/* Early theme script to avoid FOUC */}
        <script
          dangerouslySetInnerHTML={{
            __html: `
            (function(){
              try {
                var key = 'sicilius.theme';
                var path = window.location.pathname || '/';
                var isPublic = (
                  path === '/' ||
                  path.startsWith('/about') ||
                  path.startsWith('/contact') ||
                  path.startsWith('/sss') ||
                  path.startsWith('/davet') ||
                  path.startsWith('/home') ||
                  path.startsWith('/gizlilik-politikasi') ||
                  path.startsWith('/kullanici-sozlesmesi') ||
                  path.startsWith('/cerez-politikasi') ||
                  path.startsWith('/kvkk-aydinlatma') ||
                  path.startsWith('/login')
                );
                var saved = isPublic ? null : localStorage.getItem(key);
                var prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
                var useDark = saved ? (saved === 'dark') : prefersDark;
                var root = document.documentElement;
                if (useDark) root.classList.add('dark'); else root.classList.remove('dark');
              } catch(_) {}
            })();
          `}}
        />
        {/* Leaflet CSS now imported locally; external link removed to satisfy CSP */}
      </head>
      <body
        className={cn(
          'min-h-[100svh] font-sans antialiased',
          // Light: gradient background, Dark: solid slate background
          'bg-gradient-to-b from-[#FAFCFF] via-[#F7FAFF] to-[#EFF4FF] text-slate-900 dark:bg-slate-950 dark:text-slate-100',
          inter.variable,
          spaceGrotesk.variable
        )}
      >
        <AppProviders>{children}</AppProviders>
      </body>
    </html>
  );
}
