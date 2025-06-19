import { useQuery } from '@tanstack/react-query';
import { supabase } from '@/lib/supabaseClient';
import { CompanyData } from '@/lib/types/company.types';

const fetchCompanies = async (searchTerm: string): Promise<CompanyData[]> => {
  // Arama terimi boşsa sorguyu çalıştırma
  if (!searchTerm.trim()) {
    return [];
  }

  // Arama terimini ILIKE operatörü için uygun formata getiriyoruz.
  const query = `%${searchTerm.trim().replace(/ /g, '%')}%`;

  const { data, error } = await supabase
    .from('companies')
    .select('*') // Tip uyumluluğu için tüm kolonları seç
    .or(`firma_unvani.ilike.${query},sicil_no.ilike.${query},adres.ilike.${query}`)
    .limit(50); // Sonuçları sınırlayarak performansı artır

  if (error) {
    console.error('Error fetching companies:', error);
    throw new Error('Şirket verileri alınırken bir hata oluştu.');
  }

  return data || [];
};

/**
 * Supabase'den şirketleri aramak için bir React Query hook'u.
 * @param searchTerm Arama yapılacak metin.
 */
export const useCompanySearch = (searchTerm: string) => {
  return useQuery<CompanyData[], Error>({
    queryKey: ['companies', searchTerm],
    queryFn: () => fetchCompanies(searchTerm),
    enabled: !!searchTerm.trim(), // Sadece arama terimi varsa sorguyu çalıştır
    staleTime: 1000 * 60, // Veriyi 1 dakika taze tut
  });
};
