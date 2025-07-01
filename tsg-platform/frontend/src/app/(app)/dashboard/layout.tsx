import React from 'react';

// This layout is intentionally left simple to avoid nested layouts.
// The main layout is handled by /app/(app)/layout.tsx.
export default function DashboardPassthroughLayout({ children }: { children: React.ReactNode }) {
  return <>{children}</>;
}
