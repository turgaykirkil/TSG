'use client';

import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { Toaster } from '@/components/ui/toaster';
import { SessionProvider, useSession } from 'next-auth/react';
import { FullScreenLoader } from '@/components/ui/loading-spinner';

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

export function AppProviders({ children }: { children: React.ReactNode }) {
  return (
    <QueryClientProvider client={queryClient}>
      <SessionProvider>
        <AuthWrapper>
          {children}
          <Toaster />
        </AuthWrapper>
      </SessionProvider>
    </QueryClientProvider>
  );
}
