"use client";
import type { ReactNode } from 'react';
import { usePathname } from 'next/navigation';
import { PublicHeader } from '@/components/layout/PublicHeader';
import { PublicFooter } from '@/components/layout/PublicFooter';

export default function PublicLayout({ children }: { children: ReactNode }) {
  const pathname = usePathname();
  const hideChrome = pathname?.startsWith('/login') || pathname?.startsWith('/register');
  return (
    <div className="min-h-screen flex flex-col bg-background text-foreground">
      {!hideChrome && <PublicHeader />}
      <main className={
        "flex-1 " +
        (!hideChrome
          ? "h-[calc(100svh-4rem)] md:h-[calc(100svh-5rem)] overflow-y-auto snap-y snap-mandatory scroll-pt-24 md:scroll-pt-28"
          : "")
      }>
        {children}
      </main>
      {!hideChrome && <PublicFooter />}
    </div>
  );
}
