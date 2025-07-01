import type { BaseModel } from '@/types/base';

export type CompanyScrapeStatus = 'pending' | 'in_progress' | 'completed' | 'failed';

export interface CompanyScrape extends BaseModel {
  sicil_no: string;
  firma_unvani: string | null;
  adres?: string | null;  // Yeni eklenen adres alanı
  is_scraped: boolean;
  last_scraped_at: string | null;
  status: CompanyScrapeStatus;
  error_message?: string | null;
  created_at: string;
  updated_at: string;
}

export interface CompanyScrapeCreate {
  sicil_no: string;
  firma_unvani?: string | null;
  adres?: string | null;  // Yeni eklenen adres alanı
  is_scraped?: boolean;
  last_scraped_at?: string | null;
}

export type CompanyScrapeUpdate = Partial<CompanyScrapeCreate>;

export interface CompanyScrapeResponse {
  data: CompanyScrape | CompanyScrape[];
  message?: string;
}

export interface CompanyScrapeError {
  message: string;
  errors?: Record<string, string[]>;
}
