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
  const [roleChecked, setRoleChecked] = useState(false);
  const [isAdmin, setIsAdmin] = useState(false);

  useEffect(() => {
    if (!loading && !user) {
      router.push(`/login?callbackUrl=${pathname}`);
    }
  }, [user, loading, router, pathname]);

  // Role-based guard: only allow ADMIN
  useEffect(() => {
    const checkRole = async () => {
      if (loading || !user) return;
      try {
        const res = await fetch('/api/v1/users/me', { credentials: 'include', cache: 'no-store' });
        if (res.ok) {
          const data = await res.json();
          // Robust role extraction (handles plain string or enum-like object)
          let roleRaw: unknown = data?.role;
          let roleStr = '';
          if (typeof roleRaw === 'string') {
            roleStr = roleRaw;
          } else if (roleRaw && typeof roleRaw === 'object') {
            // Try common enum shapes
            const anyRole: any = roleRaw;
            roleStr = String(anyRole?.value || anyRole?.name || '');
          }
          const role = roleStr.toLowerCase();
          const email = String(data?.email || '').toLowerCase();
          const emailAdmin = email === 'turgaykirkil@me.com' || email === 'turgaykirkil@icloud.com';
          const ok = role === 'admin' || emailAdmin;
          setIsAdmin(ok);
          setRoleChecked(true);
          if (!ok) {
            router.replace('/dashboard');
          }
        } else {
          setRoleChecked(true);
          router.replace('/dashboard');
        }
      } catch {
        setRoleChecked(true);
        router.replace('/dashboard');
      }
    };
    checkRole();
  }, [loading, user, router]);

  if (loading || (user && !roleChecked)) {
    return (
      <div className="flex items-center justify-center h-screen bg-gray-50">
        <div className="text-2xl font-semibold text-gray-700">Yükleniyor...</div>
      </div>
    );
  }

  if (!user || !isAdmin) {
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
