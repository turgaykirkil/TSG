'use client';

import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { Toaster } from '@/components/ui/toaster';

import { SessionProvider } from '@/providers/SessionProvider';
import { useSession } from 'next-auth/react';
import { FullScreenLoader } from '@/components/ui/loading-spinner';
import { Inter, Space_Grotesk } from 'next/font/google';
import { cn } from '@/lib/utils';
import '@/globals.css';

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

// QueryClient yapılandırması
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
      staleTime: 5 * 60 * 1000, // 5 dakika
    },
  },
});

function AuthWrapper({ children }: { children: React.ReactNode }) {
  const { status } = useSession();

  if (status === 'loading') {
    return <FullScreenLoader />;
  }

  return <>{children}</>;
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html 
      lang="tr" 
      className={cn(
        'h-full antialiased',
        inter.variable,
        spaceGrotesk.variable
      )}
      suppressHydrationWarning
    >
      <head>
        <meta name="theme-color" content="#3b82f6" />
        <meta name="msapplication-TileColor" content="#3b82f6" />
      </head>
      <body className="min-h-screen bg-gradient-to-br from-background via-background/95 to-background/90 font-sans text-foreground">
        <QueryClientProvider client={queryClient}>
          <SessionProvider>
            <AuthWrapper>
              <div className="relative min-h-screen flex flex-col">
                {/* Gradient overlay */}
                <div className="absolute inset-0 -z-10 overflow-hidden">
                  <div className="absolute -top-24 -right-24 w-96 h-96 bg-primary/20 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob" />
                  <div className="absolute -bottom-24 -left-24 w-96 h-96 bg-secondary/20 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob animation-delay-2000" />
                  <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-accent/20 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob animation-delay-4000" />
                </div>
                
                {children}
                
                {/* Toaster için özel stil */}
                <Toaster />
              </div>
            </AuthWrapper>
          </SessionProvider>
        </QueryClientProvider>
      </body>
    </html>
  );
}
