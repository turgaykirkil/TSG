'use client';

import { useState, useCallback, useEffect } from 'react';
import { Progress } from '@/components/ui/progress';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import api from '@/lib/axios';
import { API_ENDPOINTS } from '@/config/constants';

// Type definitions
export type Stats = {
  coordinated: number;
  uncoordinated: number;
  conflicts: number;
};

interface CoordinatesDashboardProps {
  onStatsUpdate?: (stats: Stats) => void;
}

const CoordinatesDashboard = ({ onStatsUpdate }: CoordinatesDashboardProps) => {
  const [stats, setStats] = useState<Stats>({ coordinated: 0, uncoordinated: 0, conflicts: 0 });
  const [isLoading, setIsLoading] = useState(false);
  const [message, setMessage] = useState<{ type: 'success' | 'error' | 'info'; text: string } | null>(null);
  const [limit, setLimit] = useState(100);

  const fetchStats = useCallback(async () => {
    try {
      const response = await api.get(API_ENDPOINTS.STATS.COORDINATES);
      if (response.status >= 400) {
        throw new Error(response.data.detail || 'Failed to fetch stats');
      }
      const statsData = response.data;
      setStats(statsData);
      // Eğer bir onStatsUpdate fonksiyonu verildiyse, verileri yukarı iletiyoruz
      if (onStatsUpdate) {
        onStatsUpdate(statsData);
      }
    } catch (error: any) {
      console.error('Error fetching coordinate stats:', error);
      setMessage({ type: 'error', text: `İstatistikler yüklenemedi: ${error.message}` });
    }
  }, [onStatsUpdate]);

  useEffect(() => {
    fetchStats();
  }, [fetchStats]);

  const handleFetchCoordinates = useCallback(async (fetchLimit: number) => {
    if (!fetchLimit || fetchLimit <= 0) {
      setMessage({ type: 'error', text: "Lütfen 0'dan büyük geçerli bir sayı girin." });
      return;
    }
    setIsLoading(true);
    setMessage(null);

    try {
      // The original logic for fetching and geocoding coordinates on the client-side
      // was inefficient and has been moved to a backend process.
      // For now, we just show a message that this feature is under development.
      setMessage({ type: 'info', text: 'Bu özellik şu anda geliştirme aşamasındadır. Koordinatlar yakında backend servisi tarafından otomatik olarak işlenecektir.' });
      // In the future, you might trigger a backend job here:
      // await api.post('/api/v1/jobs/process-coordinates', { limit: fetchLimit });
    } catch (error: any) {
      console.error('Error triggering coordinate processing job:', error);
      setMessage({ type: 'error', text: `Koordinat işleme başlatılamadı: ${error.message}` });
    } finally {
      setIsLoading(false);
    }
  }, []);

  const handleResolveConflicts = async () => {
    // This should also be a backend job.
    setMessage({ type: 'info', text: 'Bu özellik de backend tarafında geliştirme aşamasındadır.' });
  };

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>Koordinat İstatistikleri</CardTitle>
        </CardHeader>
        <CardContent className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="p-4 bg-green-100 rounded-lg">
            <h3 className="text-lg font-semibold text-green-800">Koordinatlı</h3>
            <p className="text-2xl font-bold text-green-900">{stats.coordinated}</p>
          </div>
          <div className="p-4 bg-yellow-100 rounded-lg">
            <h3 className="text-lg font-semibold text-yellow-800">Koordinatsız</h3>
            <p className="text-2xl font-bold text-yellow-900">{stats.uncoordinated}</p>
          </div>
          <div className="p-4 bg-red-100 rounded-lg">
            <h3 className="text-lg font-semibold text-red-800">Çakışmalar</h3>
            <p className="text-2xl font-bold text-red-900">{stats.conflicts}</p>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Koordinat İşlemleri</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div>
            <p className="mb-2">Koordinatı olmayan firmaların adreslerini alıp koordinatlarını bulur.</p>
            <div className="flex items-center space-x-2">
              <Input 
                type="number" 
                value={limit} 
                onChange={(e) => setLimit(parseInt(e.target.value, 10))} 
                placeholder="İşlenecek firma sayısı"
                className="max-w-xs"
                disabled={true} // Disabled for now
              />
              <Button onClick={() => handleFetchCoordinates(limit)} disabled={isLoading || true}>
                {isLoading ? 'İşleniyor...' : 'Koordinatları Getir'}
              </Button>
            </div>
          </div>
          
          <hr />

          <div>
            <p className="mb-2">Aynı koordinata sahip farklı firmaları bularak çakışmaları çözer.</p>
            <Button onClick={handleResolveConflicts} disabled={true} variant="destructive">
              {'Çakışmaları Çöz'}
            </Button>
          </div>

          {message && (
            <div className={`p-4 rounded-md ${
              message.type === 'success' ? 'bg-green-100 text-green-800' :
              message.type === 'error' ? 'bg-red-100 text-red-800' :
              'bg-blue-100 text-blue-800'
            }`}>
              {message.text}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
};

export default CoordinatesDashboard;