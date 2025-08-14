import type { ReactNode } from 'react';

export default function DashboardLayout({ children }: { children: ReactNode }) {
  return (
    <div className="relative min-h-[100svh] bg-background overflow-hidden">
      {/* Animasyonlu gradient overlay - orijinal arka plan rengini korur */}
      <div className="pointer-events-none absolute inset-0 animated-gradient-bg" aria-hidden="true" />
      {/* İçerik */}
      <div className="relative z-10">
        {children}
      </div>
    </div>
  );
}
