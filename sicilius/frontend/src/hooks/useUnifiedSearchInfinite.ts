import { useInfiniteQuery } from '@tanstack/react-query';
import { useEffect } from 'react';
import { SEARCH_MAX_COMPANIES } from '@/config/constants';
import type { Company } from '@/types/company.types';

export interface PersonLite {
  id: string;
  full_name?: string | null;
  email?: string | null;
  nationality_id?: string | null;
  updated_at?: string | null;
}

export interface HistoryEntryLite {
  id: string;
  entry_type?: string | null;
  entry_date?: string | null;
  company_id?: string | null;
  processed_text?: string | null;
}

export interface UnifiedSearchPage {
  companies: Company[];
  persons: PersonLite[];
  history: HistoryEntryLite[];
  total_matches?: number;
  limit?: number;
  next_offset?: number | null;
  next_cursor?: number | null;
}

const fetchUnifiedPage = async (searchTerm: string, cursor: number): Promise<UnifiedSearchPage> => {
  const trimmed = searchTerm.trim();
  if (!trimmed) {
    return { companies: [], persons: [], history: [], total_matches: 0, limit: SEARCH_MAX_COMPANIES, next_offset: null, next_cursor: null };
    }
  const url = `/api/v1/search/all?q=${encodeURIComponent(trimmed)}&cursor=${cursor}&limit=${SEARCH_MAX_COMPANIES}`;
  const res = await fetch(url, { credentials: 'include' });
  if (!res.ok) {
    let message = 'API isteği başarısız oldu.';
    try {
      const data = await res.json();
      message = data?.detail || message;
    } catch {}
    throw new Error(message);
  }
  const data = await res.json();
  return {
    companies: Array.isArray(data?.companies) ? data.companies : [],
    persons: Array.isArray(data?.persons) ? data.persons : [],
    history: Array.isArray(data?.history) ? data.history : [],
    total_matches: typeof data?.total_matches === 'number' ? data.total_matches : undefined,
    limit: typeof data?.limit === 'number' ? data.limit : SEARCH_MAX_COMPANIES,
    next_offset: (typeof data?.next_offset === 'number') ? data.next_offset : null,
    next_cursor: (typeof data?.next_cursor === 'number') ? data.next_cursor : null,
  };
};

export const useUnifiedSearchInfinite = (searchTerm: string) => {
  const q = useInfiniteQuery<UnifiedSearchPage, Error>({
    queryKey: ['unified-search-infinite', searchTerm],
    queryFn: ({ pageParam }) => fetchUnifiedPage(searchTerm, typeof pageParam === 'number' ? pageParam : 0),
    initialPageParam: 0,
    getNextPageParam: (lastPage) => {
      // Güvenlik: son sayfada şirket yoksa devam etme
      if (!lastPage || !Array.isArray(lastPage.companies) || lastPage.companies.length === 0) return undefined;
      return (typeof lastPage.next_cursor === 'number' ? lastPage.next_cursor : (typeof lastPage.next_offset === 'number' ? lastPage.next_offset : undefined));
    },
    enabled: !!searchTerm.trim(),
    staleTime: 60_000,
    retry: 0,
    refetchOnWindowFocus: false,
  });
  useEffect(() => {
    if (q.status === 'success') {
      if (typeof window !== 'undefined') {
        try { window.dispatchEvent(new Event('daily-usage:refresh')); } catch {}
      }
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [q.dataUpdatedAt, q.status]);
  return q;
};
