import { useQuery } from '@tanstack/react-query';
import { API_BASE_URL } from '@/config/constants';
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

export interface UnifiedSearchResult {
  companies: Company[];
  persons: PersonLite[];
  history: HistoryEntryLite[];
  total_matches?: number;
}

const fetchUnified = async (searchTerm: string): Promise<UnifiedSearchResult> => {
  const trimmed = searchTerm.trim();
  if (!trimmed) {
    return { companies: [], persons: [], history: [] };
  }
  const url = `${API_BASE_URL}/api/v1/search/all?q=${encodeURIComponent(trimmed)}`;
  const res = await fetch(url);
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
  };
};

export const useUnifiedSearch = (searchTerm: string) => {
  return useQuery<UnifiedSearchResult, Error>({
    queryKey: ['unified-search', searchTerm],
    queryFn: () => fetchUnified(searchTerm),
    enabled: !!searchTerm.trim(),
    staleTime: 60_000,
  });
};
