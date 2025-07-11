'use client';

import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { Toaster } from '@/components/ui/toaster';
import { FullScreenLoader } from '@/components/ui/loading-spinner';
import { AuthProvider, useAuth } from '@/contexts/AuthContext';

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
  const { loading } = useAuth();

  if (loading) {
    return <FullScreenLoader />;
  }

  return <>{children}</>;
}

export function AppProviders({ children }: { children: React.ReactNode }) {
  return (
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <AuthWrapper>
          {children}
          <Toaster />
        </AuthWrapper>
      </AuthProvider>
    </QueryClientProvider>
  );
}
