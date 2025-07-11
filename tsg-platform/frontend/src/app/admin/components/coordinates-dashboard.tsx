'use client';

import { useState, useCallback, useEffect, useRef } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { toast } from 'sonner';
import { AnimatePresence, motion } from 'framer-motion';
import { dashboardService } from '@/lib/api/dashboard';
import { processingService } from '@/lib/api/processing';

interface Stats {
  coordinated: number;
  uncoordinated: number;
  conflicts: number;
}

interface CoordinatesDashboardProps {
  onStatsUpdate: (stats: Stats) => void;
}

const CoordinatesDashboard = ({ onStatsUpdate }: CoordinatesDashboardProps) => {
  const [stats, setStats] = useState<Stats>({ coordinated: 0, uncoordinated: 0, conflicts: 0 });
  const [isLoading, setIsLoading] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [limit, setLimit] = useState(100);
  const [logs, setLogs] = useState<string[]>([]);
  const [showLogs, setShowLogs] = useState(false);
  const logContainerRef = useRef<HTMLDivElement | null>(null);

  const fetchStats = useCallback(async () => {
    setIsLoading(true);
    try {
      const fetchedStats = await dashboardService.getCoordinateStats();
      setStats(fetchedStats);
      onStatsUpdate(fetchedStats);
    } catch (error) {
      console.error('Failed to fetch coordinate stats:', error);
      toast.error('İstatistikler yüklenemedi.');
    } finally {
      setIsLoading(false);
    }
  }, [onStatsUpdate]);

  useEffect(() => {
    fetchStats();
  }, [fetchStats]);

  useEffect(() => {
    if (logContainerRef.current) {
      logContainerRef.current.scrollTop = logContainerRef.current.scrollHeight;
    }
  }, [logs]);

  const handleFetchCoordinates = async (fetchLimit: number) => {
    if (!fetchLimit || fetchLimit <= 0) {
      toast.error("Lütfen 0'dan büyük geçerli bir sayı girin.");
      return;
    }
    setIsProcessing(true);
    setLogs(['İşlem başlatılıyor... Backend yanıtı bekleniyor.']);
    setShowLogs(true);

    try {
      const response = await processingService.startCoordinateProcessing(fetchLimit);
      if (response.logs) {
        setLogs(response.logs);
      } else {
        setLogs(prev => [...prev, 'İşlem tamamlandı ancak loglar alınamadı.']);
      }
      toast.success(response.message || 'Koordinat işleme tamamlandı.');
    } catch (error: any) {
      const errorMessage = error.response?.data?.detail || error.message || 'Bilinmeyen bir hata oluştu.';
      const errorLogs = error.response?.data?.logs || [];
      setLogs(prev => [...prev, '--- HATA ---', errorMessage, ...errorLogs]);
      toast.error(`Koordinat işleme hatası: ${errorMessage}`);
    } finally {
      setIsProcessing(false);
      fetchStats();
    }
  };

  const handleResolveConflicts = async () => {
    setIsLoading(true);
    try {
      const response = await processingService.resolveCoordinateConflicts();
      toast.success(response.message || 'Çakışma çözme tamamlandı.');
      console.log('Conflicts found:', response.conflicts);
    } catch (error: any) {
      const errorMessage = error.response?.data?.detail || error.message || 'Bilinmeyen bir hata oluştu.';
      toast.error(`Çakışmalar çözülemedi: ${errorMessage}`);
    } finally {
      setIsLoading(false);
      fetchStats();
    }
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
            <p className="text-2xl font-bold text-green-900">{stats.coordinated.toLocaleString('tr-TR')}</p>
          </div>
          <div className="p-4 bg-yellow-100 rounded-lg">
            <h3 className="text-lg font-semibold text-yellow-800">Koordinatsız</h3>
            <p className="text-2xl font-bold text-yellow-900">{stats.uncoordinated.toLocaleString('tr-TR')}</p>
          </div>
          <div className="p-4 bg-red-100 rounded-lg">
            <h3 className="text-lg font-semibold text-red-800">Çakışmalar</h3>
            <p className="text-2xl font-bold text-red-900">{stats.conflicts.toLocaleString('tr-TR')}</p>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Koordinat İşlemleri</CardTitle>
        </CardHeader>
        <CardContent className="space-y-6">
          <div className="flex items-start gap-4">
            <div className="flex flex-col gap-2">
              <p className="text-sm text-muted-foreground">Veritabanında koordinatı olmayan firmaların adreslerini alıp koordinatlarını günceller.</p>
              <div className="flex items-center gap-2">
                <Input
                  type="number"
                  value={limit}
                  onChange={(e) => setLimit(parseInt(e.target.value, 10))}
                  placeholder="İşlem Limiti"
                  className="max-w-[120px]"
                  disabled={isProcessing}
                />
                <Button onClick={() => handleFetchCoordinates(limit)} disabled={isProcessing}>
                  {isProcessing ? 'İşleniyor...' : 'Koordinatları Getir'}
                </Button>
              </div>
            </div>
          </div>

          <AnimatePresence>
            {showLogs && (
              <motion.div
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: 'auto' }}
                exit={{ opacity: 0, height: 0 }}
                transition={{ duration: 0.3 }}
                className="w-full"
              >
                <Card className="bg-gray-900 text-white font-mono">
                  <CardHeader className="flex flex-row items-center justify-between py-2 px-4">
                    <CardTitle className="text-sm font-medium">İşlem Logları</CardTitle>
                    <Button variant="ghost" size="sm" onClick={() => setShowLogs(false)} disabled={isProcessing}>Kapat</Button>
                  </CardHeader>
                  <CardContent className="p-2">
                    <div ref={logContainerRef} className="h-64 overflow-y-auto bg-black rounded-md p-4 text-xs whitespace-pre-wrap scrollbar-thin scrollbar-thumb-gray-600 scrollbar-track-gray-800">
                      {logs.map((log, index) => (
                        <p key={index}>{log}</p>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              </motion.div>
            )}
          </AnimatePresence>

          <hr />

          <div>
            <p className="text-sm text-muted-foreground mb-2">Aynı koordinata sahip farklı firmaları bularak çakışmaları listeler.</p>
            <Button onClick={handleResolveConflicts} disabled={isLoading || isProcessing} variant="secondary">
              {isLoading ? 'Aranıyor...' : 'Çakışmaları Çöz'}
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default CoordinatesDashboard;