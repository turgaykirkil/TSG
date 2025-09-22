import { useQuery } from '@tanstack/react-query';
import { API_ENDPOINTS } from '@/config/constants';
import api from '@/lib/axios';

export interface NearbyCompany {
  id: string;
  unvan?: string | null;
  title?: string | null;
  trade_name?: string | null;
  address?: string | null;
  city?: string | null;
  distance_km: number;
  koordinat?: { lat: number; lon: number } | null;
}

const fetchNearby = async (companyId: string, max_km: number, limit: number): Promise<NearbyCompany[]> => {
  const id = (companyId || '').trim();
  if (!id) return [];
  const url = API_ENDPOINTS.COMPANIES.NEARBY(id, max_km, limit);
  try {
    const res = await api.get<NearbyCompany[]>(url, { withCredentials: true });
    return Array.isArray(res.data) ? res.data : [];
  } catch (err: any) {
    const status = err?.response?.status;
    if (status === 400) return [];
    const message = err?.response?.data?.detail || 'Yakın şirketler alınamadı';
    throw new Error(message);
  }
};

export const useNearbyCompanies = (
  companyId: string | undefined,
  options?: { enabled?: boolean; max_km?: number; limit?: number }
) => {
  const max_km = options?.max_km ?? 5;
  const limit = options?.limit ?? 10;
  return useQuery<NearbyCompany[], Error>({
    queryKey: ['nearby-companies', companyId, max_km, limit],
    queryFn: () => fetchNearby(companyId as string, max_km, limit),
    enabled: !!companyId && (options?.enabled ?? true),
    staleTime: 60_000,
  });
};
