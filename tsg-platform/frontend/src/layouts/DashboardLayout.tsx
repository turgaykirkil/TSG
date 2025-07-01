'use client';

import { type ReactNode, useState } from 'react';
import { AppSidebar } from '@/components/layout/AppSidebar';
import { Header } from '@/components/layout/Header';
import { AppProviders } from '@/app/AppProviders';
import { cn } from '@/lib/utils';

interface DashboardLayoutProps {
  children: ReactNode;
}

export function DashboardLayout({ children }: DashboardLayoutProps) {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false); // Default to closed on mobile

  return (
    <AppProviders>
      <div className="relative flex h-screen min-h-screen w-full bg-slate-50 dark:bg-slate-900">
        {/* Desktop Sidebar */}
        <div className="hidden lg:flex lg:w-64 lg:flex-col lg:border-r lg:bg-background">
          <AppSidebar />
        </div>

        {/* Mobile Sidebar Overlay */}
        {isSidebarOpen && (
          <div
            className="fixed inset-0 z-30 bg-black/30 lg:hidden"
            onClick={() => setIsSidebarOpen(false)}
            aria-hidden="true"
          />
        )}
        {/* Mobile Sidebar Panel */}
        <div
          className={cn(
            'fixed top-0 left-0 z-40 h-full w-64 transform border-r bg-background transition-transform duration-300 ease-in-out lg:hidden',
            isSidebarOpen ? 'translate-x-0' : '-translate-x-full'
          )}
        >
          {/* The onLinkClick prop will be implemented in the next step */}
          <AppSidebar onLinkClick={() => setIsSidebarOpen(false)} />
        </div>

        <div className="flex flex-1 flex-col">
          <Header onMenuClick={() => setIsSidebarOpen(true)} />
          <main className="flex-1 overflow-y-auto">
            <div className="container mx-auto px-4 py-6 sm:px-6 lg:px-8">
              {children}
            </div>
          </main>
        </div>
      </div>
    </AppProviders>
  );
}
