import { Inter, Space_Grotesk } from 'next/font/google';
import 'leaflet/dist/leaflet.css';
import { cn } from '@/lib/utils';
import '@/globals.css';
import { AppProviders } from './AppProviders';
import { Suspense } from 'react';

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
                // Kayıtlı tema tercihini her sayfada uygula (public dahil).
                var saved = null;
                try { saved = localStorage.getItem(key); } catch(_) {}
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
          'bg-background text-foreground',
          inter.variable,
          spaceGrotesk.variable
        )}
      >
        <Suspense fallback={<div />}>
          <AppProviders>{children}</AppProviders>
        </Suspense>
      </body>
    </html>
  );
}
