'use client';

import { AuthProvider as SupabaseAuthProvider } from '@/contexts/AuthContext';
import type { ReactNode } from 'react';

export function AuthProvider({ children }: { children: ReactNode }) {
  return <SupabaseAuthProvider>{children}</SupabaseAuthProvider>;
}
