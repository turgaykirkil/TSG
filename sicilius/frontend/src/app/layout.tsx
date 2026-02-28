import { Inter, Space_Grotesk } from 'next/font/google';
import 'leaflet/dist/leaflet.css';
import { cn } from '@/lib/utils';
import '@/globals.css';
import { AppProviders } from './AppProviders';
import { Suspense } from 'react';
import StructuredData from '@/components/seo/StructuredData';


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
  title: {
    default: 'Sicilius | Kurumsal Veri Analizi ve Sorgulama',
    template: '%s | Sicilius'
  },
  description: 'Sicilius, Türkiye\'deki halka açık kayıtları modernize ederek hızlı arama, ilişki analizi ve görselleştirme sunan profesyonel veri platformudur.',
  keywords: ['kurumsal veri', 'firma analizi', 'şirket sorgulama', 'ilişki analizi', 'sicil verisi', 'veri görselleştirme'],
  authors: [{ name: 'Sicilius Team' }],
  creator: 'Sicilius',
  publisher: 'Sicilius',
  formatDetection: {
    email: false,
    address: false,
    telephone: false,
  },
  openGraph: {
    title: 'Sicilius | Kurumsal Veri Analizi ve Sorgulama',
    description: 'Halka açık kayıtları modernize ederek hızlı arama ve ilişki analizi sunan profesyonel veri platformu.',
    url: 'https://sicilius.com.tr',
    siteName: 'Sicilius',
    locale: 'tr_TR',
    type: 'website',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'Sicilius | Kurumsal Veri Analizi',
    description: 'Halka açık kayıtları modernize ederek hızlı arama ve analiz sunan veri platformu.',
  },
  metadataBase: new URL('https://sicilius.com.tr'),
  alternates: {
    canonical: '/',
  },
  category: 'Business & Finance',
  other: {
    'apple-mobile-web-app-capable': 'yes',
    'apple-mobile-web-app-status-bar-style': 'black-translucent',
    'theme-color': '#0f172a',
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      'max-video-preview': -1,
      'max-image-preview': 'large',
      'max-snippet': -1,
    },
  },
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
          <StructuredData />
          <AppProviders>{children}</AppProviders>
        </Suspense>
      </body>
    </html>
  );
}
