import { useState, useEffect } from 'react';
import axios from 'axios';

// Backend'den gelen istatistik verisinin tip tanımı
export interface StatsData {
  total_companies: number;
  scraped_companies: number;
  total_announcements: number;
  new_companies_today: number;
  storage_total_files?: number;
  storage_total_bytes?: number;
  storage_buckets?: {
    gazette_pdfs?: {
      bucket: string;
      pdf_count: number;
      total_bytes: number;
      status?: string;
    };
    company_gazettes?: {
      bucket: string;
      pdf_count: number;
      total_bytes: number;
      status?: string;
    };
  };
}

const API_URL = `/api/v1/stats`;

export const useRealtimeStats = () => {
  const [stats, setStats] = useState<StatsData | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const response = await axios.get<StatsData>(API_URL, { withCredentials: true });
        setStats(response.data);
      } catch (err) {
        setError('İstatistikler yüklenirken bir hata oluştu.');
        console.error('Error fetching stats:', err);
      }
    };

    fetchStats(); // Veriyi yalnızca bir kez, sayfa yüklendiğinde çek
  }, []);

  return { stats, error };
};
