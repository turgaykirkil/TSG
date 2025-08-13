import { useState, useEffect } from 'react';
import axios from 'axios';

// Backend'den gelen istatistik verisinin tip tanımı
export interface StatsData {
  total_companies: number;
  scraped_companies: number;
  total_announcements: number;
  new_companies_today: number;
  storage_pdf_count?: number | null;
}

const API_URL = '/api/v1/stats';

export const useRealtimeStats = () => {
  const [stats, setStats] = useState<StatsData | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const token = localStorage.getItem('access_token');
        const response = await axios.get<StatsData>(API_URL, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
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
