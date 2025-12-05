import { useQuery } from '@tanstack/react-query';
import type { Company } from '@/types/company.types';

export interface PersonWithRelation {
  id: string;
  full_name?: string | null;
  first_name?: string | null;
  last_name?: string | null;
  email?: string | null;
  nationality_id?: string | null;
  birth_date?: string | null;
  is_active?: boolean | null;
  updated_at?: string | null;
  relation_type?: string | null;
  position?: string | null;
  is_current?: boolean | null;
  start_date?: string | null;
  end_date?: string | null;
}

export interface AnnouncementLite {
  id: string;
  title?: string;
  publication_date?: string | null;
  issue_number?: string | number | null;
  page_number?: string | number | null;
  announcement_type?: string | null;
  newspaper_name?: string | null;
  original_text?: string | null;
  hususlar?: string | string[] | null; // New field
  pdf_url?: string | null;
  ocr_status?: string | null;
  created_at?: string | null;
  _ocr_id?: number | null; // OCR result ID for virtual announcements
}

export interface HistoryEntryLite {
  id: string;
  entry_type?: string | null;
  entry_date?: string | null;
  company_id?: string | null;
  processed_text?: string | null;
}

export interface SharedPersonLite {
  id: string;
  full_name?: string | null;
  first_name?: string | null;
  last_name?: string | null;
  relation_type?: string | null;
  position?: string | null;
  is_current?: boolean | null;
  start_date?: string | null;
  end_date?: string | null;
}

export interface RelatedCompany {
  id: string;
  unvan?: string | null;
  firma_unvani?: string | null;
  sicil_no?: string | null;
  sicil_mudurluk?: string | null;
  address?: string | null;
  adres?: string | null;
  shared_persons: SharedPersonLite[];
}

export interface SameAddressCompany {
  id: string;
  unvan?: string | null;
  firma_unvani?: string | null;
  sicil_no?: string | null;
  sicil_mudurluk?: string | null;
  address?: string | null;
  adres?: string | null;
}

export interface CompanyDetailPayload {
  company: Company | null;
  persons: PersonWithRelation[];
  announcements: AnnouncementLite[];
  history: HistoryEntryLite[];
  related_companies: RelatedCompany[];
  same_address_companies: SameAddressCompany[];
  shared_person_companies?: SameAddressCompany[];  // New: companies sharing same persons
  old_addresses: { address: string; matched_company_id?: string | null; matched_company?: any }[];
  old_trade_names?: string[];
}

const fetchCompanyDetail = async (companyId: string): Promise<CompanyDetailPayload> => {
  const id = (companyId || '').trim();
  if (!id) throw new Error('Geçersiz şirket kimliği');
  const url = `/api/v1/search/company-detail?company_id=${encodeURIComponent(id)}`;
  const res = await fetch(url, { credentials: 'include' });
  if (!res.ok) {
    const status = res.status;
    let message = 'Şirket detayları getirilemedi';
    try {
      const data = await res.json();
      message = data?.detail || message;
    } catch { }
    const err: any = new Error(message);
    err.status = status;
    throw err;
  }
  const data = await res.json();
  return {
    company: data.company || null,
    persons: Array.isArray(data?.persons) ? data.persons : [],
    announcements: Array.isArray(data?.announcements) ? data.announcements : [],
    history: Array.isArray(data?.history) ? data.history : [],
    related_companies: Array.isArray(data?.related_companies) ? data.related_companies : [],
    same_address_companies: Array.isArray(data?.same_address_companies) ? data.same_address_companies : [],
    shared_person_companies: Array.isArray(data?.shared_person_companies) ? data.shared_person_companies : [],
    old_addresses: Array.isArray(data?.old_addresses) ? data.old_addresses : [],
    old_trade_names: Array.isArray(data?.old_trade_names) ? data.old_trade_names : [],
  };
};

export const useCompanyDetail = (companyId: string | undefined, enabled: boolean) => {
  return useQuery<CompanyDetailPayload, Error>({
    queryKey: ['company-detail', companyId],
    queryFn: () => fetchCompanyDetail(companyId as string),
    enabled: !!companyId && enabled,
    staleTime: 0, // her açılışta güncel veriyi tercih et
    refetchOnMount: 'always',
    refetchOnReconnect: true,
    refetchOnWindowFocus: false,
  });
};
