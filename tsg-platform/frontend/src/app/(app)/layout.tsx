import type { ReactNode } from 'react';

// Bu layout artık sadece bir sarmalayıcı görevi görüyor.
// Gerçek layout'lar (admin, dashboard vb.) kendi klasörlerinde tanımlanacak.
export default function AppLayout({ children }: { children: ReactNode }) {
  return <>{children}</>;
}
