import { AppSidebar } from '@/components/layout/AppSidebar';
import { AppHeader } from '@/components/layout/AppHeader';
import type { ReactNode } from 'react';
import { Suspense } from 'react';
import Loader from '@/components/ui/loader';

export default function AppLayout({ children }: { children: ReactNode }) {
  return (
    <div className="flex h-screen bg-gray-50">
      <AppSidebar />
      <div className="flex flex-col flex-1 overflow-hidden">
        <AppHeader />
        <main className="flex-1 overflow-y-auto p-6 bg-gray-50">
          <Suspense fallback={<Loader />}>{children}</Suspense>
        </main>
      </div>
    </div>
  );
}
