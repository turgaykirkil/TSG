import type { ReactNode } from 'react';

export default function DashboardLayout({ children }: { children: ReactNode }) {
  return (
    <div className="relative min-h-[100svh] bg-background">
      {children}
    </div>
  );
}
