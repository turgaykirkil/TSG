'use client';

import { useCallback, useEffect, useMemo, useState } from 'react';

export type SearchEntry = {
  id: string;
  query: string;
  createdAt: number; // epoch ms
  pinned?: boolean;
};

const STORAGE_KEY_V1 = 'sicilius.searchHistory.v1';
const STORAGE_KEY = 'sicilius.searchHistory.v2';
const MAX_ITEMS = 50;

function readStorage(): SearchEntry[] {
  if (typeof window === 'undefined') return [];
  try {
    const rawV2 = window.localStorage.getItem(STORAGE_KEY);
    if (rawV2) {
      const parsed = JSON.parse(rawV2) as SearchEntry[];
      if (!Array.isArray(parsed)) return [];
      return parsed.filter((x) => typeof x?.query === 'string' && typeof x?.createdAt === 'number' && typeof x?.id === 'string');
    }
    // migrate from v1 if exists
    const rawV1 = window.localStorage.getItem(STORAGE_KEY_V1);
    if (rawV1) {
      const parsedV1 = JSON.parse(rawV1) as Omit<SearchEntry, 'pinned'>[];
      const migrated: SearchEntry[] = (Array.isArray(parsedV1) ? parsedV1 : []).map((x) => ({ ...x, pinned: false }));
      window.localStorage.setItem(STORAGE_KEY, JSON.stringify(migrated));
      return migrated;
    }
    return [];
  } catch {
    return [];
  }
}

function writeStorage(items: SearchEntry[]) {
  if (typeof window === 'undefined') return;
  try {
    window.localStorage.setItem(STORAGE_KEY, JSON.stringify(items));
  } catch {
    // ignore quota errors
  }
}

export function useSearchHistory() {
  const [items, setItems] = useState<SearchEntry[]>([]);

  // Initial load
  useEffect(() => {
    setItems(readStorage());
  }, []);

  // Listen storage changes from other tabs
  useEffect(() => {
    const onStorage = (e: StorageEvent) => {
      if (e.key === STORAGE_KEY) setItems(readStorage());
    };
    window.addEventListener('storage', onStorage);
    return () => window.removeEventListener('storage', onStorage);
  }, []);

  // Persist on changes
  useEffect(() => {
    writeStorage(items);
  }, [items]);

  const add = useCallback((query: string) => {
    const q = query.trim();
    if (!q) return;
    setItems((prev) => {
      // dedup by query (case-insensitive)
      const without = prev.filter((x) => x.query.toLowerCase() !== q.toLowerCase());
      const next: SearchEntry[] = [
        { id: crypto.randomUUID(), query: q, createdAt: Date.now(), pinned: false },
        ...without,
      ];
      // order: pinned first by createdAt desc within groups
      const ordered = next
        .sort((a, b) => (b.createdAt || 0) - (a.createdAt || 0))
        .sort((a, b) => (b.pinned ? 1 : 0) - (a.pinned ? 1 : 0));
      return ordered.slice(0, MAX_ITEMS);
    });
  }, []);

  const remove = useCallback((id: string) => {
    setItems((prev) => prev.filter((x) => x.id !== id));
  }, []);

  const clear = useCallback(() => {
    setItems([]);
  }, []);

  const togglePin = useCallback((id: string) => {
    setItems((prev) => {
      const mapped = prev.map((x) => (x.id === id ? { ...x, pinned: !x.pinned } : x));
      // reorder after pin change
      return mapped
        .sort((a, b) => (b.createdAt || 0) - (a.createdAt || 0))
        .sort((a, b) => (b.pinned ? 1 : 0) - (a.pinned ? 1 : 0));
    });
  }, []);

  const api = useMemo(() => ({ items, add, remove, clear, togglePin }), [items, add, remove, clear, togglePin]);
  return api;
}
