'use client';

import { AuthProvider } from '@/contexts/AuthContext';
import type { ReactNode } from 'react';

interface SessionProviderProps {
  children: ReactNode;
}

export function SessionProvider({ children }: SessionProviderProps) {
  return (
    <AuthProvider>
      {children}
    </AuthProvider>
  );
}
