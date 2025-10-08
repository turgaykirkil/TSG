'use client';

import type { ReactNode } from 'react';
import { useEffect, useState } from 'react';
import { useRouter, usePathname } from 'next/navigation';
import { useAuth } from '@/contexts/AuthContext';
import { AppSidebar } from '@/app/(app)/admin/components/layout/AdminSidebar';
import { AppHeader } from '@/app/(app)/admin/components/layout/AdminHeader';

export default function AdminLayout({ children }: { children: ReactNode }) {
  const router = useRouter();
  const pathname = usePathname();
  const { session, loading } = useAuth();
  const user = session?.user;
  const [checkingRole, setCheckingRole] = useState(true);

  useEffect(() => {
    const run = async () => {
      if (loading) return;
      if (!user) {
        router.push(`/login?callbackUrl=${pathname}`);
        return;
      }
      try {
        const res = await fetch('/api/v1/auth/require-admin', { method: 'GET', credentials: 'include', cache: 'no-store' });
        if (res.status !== 204) {
          router.replace('/dashboard');
          return;
        }
      } catch {
        router.replace('/dashboard');
        return;
      } finally {
        setCheckingRole(false);
      }
    };
    run();
  }, [user, loading, router, pathname]);

  if (loading || checkingRole) {
    return (
      <div className="flex items-center justify-center h-screen bg-gray-50">
        <div className="text-2xl font-semibold text-gray-700">Yükleniyor...</div>
      </div>
    );
  }

  if (!user) {
    return null; // Yönlendirme useEffect içinde gerçekleşecek
  }

  return (
    <div className="flex h-screen bg-background text-foreground">
      <AppSidebar />
      <div className="flex flex-col flex-1 overflow-hidden">
        <AppHeader />
        <main className="flex-1 overflow-y-auto p-6">
          {children}
        </main>
      </div>
    </div>
  );
}
