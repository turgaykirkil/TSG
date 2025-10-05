import { useQuery } from '@tanstack/react-query';

import { Company } from '@/types/company.types';

/**
 * Supabase'den gelen ham şirket verisini temsil eder.
 * `select('*, koordinat_text:koordinat::text')` sorgusu ile `koordinat` alanı
 * metin formatında (`koordinat_text`) alınır ve daha sonra işlenir.
 * Orijinal `koordinat` alanı (`point` tipi) kullanılmaz.
 */
type SupabaseCompanyData = Omit<Company, 'koordinat'> & {
  koordinat: unknown; // Orijinal `point` tipi, işlenmeyecek.
  koordinat_text: string | null; // `koordinat::text` ile alınan metin gösterimi.
};

/**
 * Veritabanından arama terimine göre şirketleri getiren ve veriyi dönüştüren fonksiyon.
 * @param searchTerm Arama yapılacak metin.
 * @returns `Company` tipinde bir dizi.
 */
const fetchCompanies = async (searchTerm: string): Promise<Company[]> => {
  if (!searchTerm.trim()) {
    return [];
  }

  // Backend route structure: /api/v1/search (router prefix) + /search (endpoint) => /api/v1/search/search
  const url = `/api/v1/search/search?q=${encodeURIComponent(searchTerm.trim())}`;

  try {
    const response = await fetch(url);

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'API isteği başarısız oldu.');
    }

    const data = await response.json();

    if (!data) {
      return [];
    }

    // Gelen veriyi `Company` tipine dönüştürür.
    const transformedData = (data as SupabaseCompanyData[]).map((item): Company => {
      const { koordinat, ...rest } = item;
      let newKoordinat: { x: number; y: number } | null = null;

      if (
        koordinat &&
        typeof koordinat === 'object' &&
        'type' in koordinat &&
        (koordinat as any).type === 'Point' &&
        'coordinates' in koordinat &&
        Array.isArray((koordinat as any).coordinates) &&
        (koordinat as any).coordinates.length === 2
      ) {
        const [x, y] = (koordinat as any).coordinates;
        if (typeof x === 'number' && typeof y === 'number') {
          newKoordinat = { x, y };
        }
      } else if (koordinat) {
        console.warn(`Şirket ID ${item.id} için beklenmedik koordinat formatı:`, koordinat);
      }

      return { ...rest, koordinat: newKoordinat };
    });

    console.log('[useCompanySearch] Backend API üzerinden dönüştürülmüş şirket verisi:', transformedData);

    return transformedData;
  } catch (error) {
    console.error('Şirketler getirilirken hata:', error);
    throw new Error('Şirket verileri alınırken bir hata oluştu.');
  }
};

/**
 * Supabase'den şirketleri aramak için bir React Query hook'u.
 * @param searchTerm Arama yapılacak metin.
 */
export const useCompanySearch = (searchTerm: string) => {
  return useQuery<Company[], Error>({
    queryKey: ['companies', searchTerm],
    queryFn: () => fetchCompanies(searchTerm),
    enabled: !!searchTerm.trim(), // Sadece arama terimi varsa sorguyu çalıştır
    staleTime: 1000 * 60, // Veriyi 1 dakika taze tut (cache)
  });
};
