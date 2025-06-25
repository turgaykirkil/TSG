'use client';

import { Suspense, useEffect, useState } from 'react';
import LoadingSpinner from '@/components/ui/loading-spinner';

export default function Template({ children }: { children: React.ReactNode }) {
  const [isMounted, setIsMounted] = useState(false);

  useEffect(() => {
    setIsMounted(true);
  }, []);

  if (!isMounted) {
    return <LoadingSpinner />;
  }

  return <Suspense fallback={<LoadingSpinner />}>{children}</Suspense>;
}
