"use client";
import type { ReactNode } from 'react';
import { usePathname } from 'next/navigation';
import { PublicHeader } from '@/components/layout/PublicHeader';
import { PublicFooter } from '@/components/layout/PublicFooter';

export default function PublicLayout({ children }: { children: ReactNode }) {
  const pathname = usePathname();
  const hideChrome = pathname?.startsWith('/login');
  return (
    <div className="min-h-screen flex flex-col">
      {!hideChrome && <PublicHeader />}
      <main className={"flex-1 " + (!hideChrome ? "pt-20 md:pt-24" : "") }>
        {children}
      </main>
      {!hideChrome && <PublicFooter />}
    </div>
  );
}
