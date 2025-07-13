'use client';

import type { ReactNode } from 'react';
import { useEffect } from 'react';
import { useRouter, usePathname } from 'next/navigation';
import { useAuth } from '@/contexts/AuthContext';


export default function AdminLayout({ children }: { children: ReactNode }) {
  const router = useRouter();
  const pathname = usePathname();
  const { session, loading } = useAuth();
  const user = session?.user;

  useEffect(() => {
    if (!loading && !user) {
      router.push(`/login?callbackUrl=${pathname}`);
    }
  }, [user, loading, router, pathname]);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen bg-gray-50">
        <div className="text-2xl font-semibold text-gray-700">Yükleniyor...</div>
      </div>
    );
  }

  if (!user) {
    return null; // Yönlendirme useEffect içinde gerçekleşecek
  }

  return <>{children}</>;
}
