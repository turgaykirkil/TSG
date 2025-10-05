"use client";

import { useCallback, useEffect, useState } from "react";

type DailyUsage = {
  date: string;
  count: number;
  limit: number;
  remaining: number;
};

export function useDailyUsage() {
  const [data, setData] = useState<DailyUsage | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const refetch = useCallback(async () => {
    let isMounted = true;
    try {
      setLoading(true);
      setError(null);
      const res = await fetch(`/api/v1/usage/me`, { credentials: "include" });
      if (!res.ok) {
        throw new Error(`Kullanım bilgisi alınamadı (${res.status})`);
      }
      const json = await res.json();
      if (isMounted) setData(json);
    } catch (e: any) {
      if (isMounted) setError(e?.message || "Bilinmeyen hata");
    } finally {
      if (isMounted) setLoading(false);
    }
    return () => { isMounted = false; };
  }, []);

  useEffect(() => {
    let cleanup: any;
    // initial
    refetch();
    // polling
    const id = setInterval(refetch, 60_000);
    // custom event listener
    const onRefresh = () => { refetch(); };
    if (typeof window !== 'undefined') {
      window.addEventListener('daily-usage:refresh', onRefresh);
    }
    cleanup = () => {
      clearInterval(id);
      if (typeof window !== 'undefined') {
        window.removeEventListener('daily-usage:refresh', onRefresh);
      }
    };
    return cleanup;
  }, [refetch]);

  return { data, loading, error, refetch };
}
