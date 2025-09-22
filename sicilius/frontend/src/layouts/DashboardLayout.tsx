'use client';

import { type ReactNode, useState, useEffect } from 'react';
import { Sidebar } from '@/components/layout/Sidebar';
import { Header } from '@/components/layout/Header';
import { AppProviders } from '@/app/AppProviders';
import { cn } from '@/lib/utils';

interface DashboardLayoutProps {
  children: ReactNode;
}

export function DashboardLayout({ children }: DashboardLayoutProps) {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false); // Default to closed on mobile

  // Klavye: Escape ile mobil menüyü kapat
  useEffect(() => {
    const onKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') setIsSidebarOpen(false);
    };
    if (isSidebarOpen) {
      window.addEventListener('keydown', onKeyDown);
    }
    return () => window.removeEventListener('keydown', onKeyDown);
  }, [isSidebarOpen]);

  return (
    <AppProviders>
      <div className="relative flex h-screen min-h-screen w-full bg-background text-foreground">
        {/* Desktop Sidebar */}
        <div className="hidden lg:flex lg:w-64 lg:flex-col lg:border-r lg:bg-background">
          <Sidebar />
        </div>

        {/* Mobile Sidebar Overlay */}
        {isSidebarOpen && (
          <div
            className="fixed inset-0 z-30 bg-black/30 lg:hidden"
            onClick={() => setIsSidebarOpen(false)}
            role="presentation"
            aria-hidden="true"
          />
        )}
        {/* Mobile Sidebar Panel */}
        <div
          className={cn(
            'fixed top-0 left-0 z-40 h-full w-64 transform border-r bg-background transition-transform duration-300 ease-in-out lg:hidden',
            isSidebarOpen ? 'translate-x-0' : '-translate-x-full'
          )}
          id="mobile-sidebar"
          role="dialog"
          aria-modal="true"
          aria-label="Gezinme paneli"
        >
          <Sidebar isOpen onClose={() => setIsSidebarOpen(false)} />
        </div>

        <div className="flex flex-1 flex-col">
          <Header onMenuClick={() => setIsSidebarOpen(true)} isMenuOpen={isSidebarOpen} />
          <main className="flex-1 overflow-y-auto" role="main" aria-label="Ana içerik">
            <div className="container mx-auto px-4 py-6 sm:px-6 lg:px-8">
              {children}
            </div>
          </main>
        </div>
      </div>
    </AppProviders>
  );
}
