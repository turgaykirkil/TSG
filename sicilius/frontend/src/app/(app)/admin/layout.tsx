'use client';

import type { ReactNode } from 'react';
import { useEffect, useState } from 'react';
import { useRouter, usePathname } from 'next/navigation';
import { useAuth } from '@/contexts/AuthContext';
import { AppSidebar } from './components/layout/AdminSidebar';
import { AppHeader } from './components/layout/AdminHeader';
import { FullScreenLoader } from '@/components/ui/loading-spinner';

export default function AdminLayout({ children }: { children: ReactNode }) {
  const router = useRouter();
  const pathname = usePathname();
  const { session, loading } = useAuth();
  const user = session?.user;
  const [checkingRole, setCheckingRole] = useState(true);

  useEffect(() => {
    const checkAdmin = async () => {
      if (loading) return;
      
      if (!user) {
        router.push('/login');
        return;
      }

      // Check if user has admin role (optional, adding for safety)
      const role = (user as any)?.role;
      const roleValue = typeof role === 'string' ? role : (role?.value || role?.name);
      
      if (roleValue !== 'admin') {
        router.replace('/dashboard');
        return;
      }
      
      setCheckingRole(false);
    };

    checkAdmin();
  }, [user, loading, router]);

  if (loading || checkingRole) {
    return <FullScreenLoader />;
  }

  return (
    <div className="flex h-screen bg-background text-foreground overflow-hidden">
      <div className="hidden md:flex w-64 flex-col border-r bg-background">
        <AppSidebar />
      </div>
      <div className="flex flex-col flex-1 overflow-hidden">
        <AppHeader />
        <main className="flex-1 overflow-y-auto p-6">
          {children}
        </main>
      </div>
    </div>
  );
}
