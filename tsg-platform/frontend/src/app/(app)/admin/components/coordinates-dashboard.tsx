'use client';

import { useState, useCallback, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Progress } from '@/components/ui/progress';
import { toast } from 'sonner';
import { AnimatePresence, motion } from 'framer-motion';
import { dashboardService } from '@/lib/api/dashboard';
import { processingService } from '@/lib/api/processing';

interface Stats {
  coordinated: number;
  uncoordinated: number;
  conflicts: number;
}

interface ProcessingResult {
  processed: number;
  failed: number;
}

interface CoordinatesDashboardProps {
  onStatsUpdate: (stats: Stats) => void;
}

const CoordinatesDashboard = ({ onStatsUpdate }: CoordinatesDashboardProps) => {
  const [stats, setStats] = useState<Stats>({ coordinated: 0, uncoordinated: 0, conflicts: 0 });
  const [isLoading, setIsLoading] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [limit, setLimit] = useState(100);
  const [progress, setProgress] = useState(0);
  const [processingResult, setProcessingResult] = useState<ProcessingResult | null>(null);

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

  const handleFetchCoordinates = async (fetchLimit: number) => {
    if (!fetchLimit || fetchLimit <= 0) {
      toast.error("Lütfen 0'dan büyük geçerli bir sayı girin.");
      return;
    }
    setIsProcessing(true);
    setProgress(0);
    setProcessingResult(null);

    let processedCount = 0;
    const progressInterval = setInterval(() => {
      processedCount++;
      const newProgress = Math.min(100, (processedCount / fetchLimit) * 100);
      setProgress(newProgress);

      if (processedCount >= fetchLimit) {
        clearInterval(progressInterval);
      }
    }, 1000);

    try {
      const response = await processingService.startCoordinateProcessing(fetchLimit);
      setProcessingResult({ processed: response.processed_count, failed: response.failed_count });
      toast.success(response.message || 'Koordinat işleme tamamlandı.');
    } catch (error: any) {
      const errorMessage = error.response?.data?.detail || error.message || 'Bilinmeyen bir hata oluştu.';
      toast.error(`Koordinat işleme hatası: ${errorMessage}`);
      setProcessingResult({ processed: 0, failed: fetchLimit });
    } finally {
      clearInterval(progressInterval);
      setProgress(100);
      setTimeout(() => {
        setIsProcessing(false);
        fetchStats();
        setProgress(0); 
      }, 2000);
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
            <div className="flex flex-col gap-2 w-full">
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
              
              <AnimatePresence>
                {isProcessing && (
                  <motion.div
                    initial={{ opacity: 0, height: 0 }}
                    animate={{ opacity: 1, height: 'auto' }}
                    exit={{ opacity: 0, height: 0 }}
                    className="w-full pt-4"
                  >
                    <Progress value={progress} className="w-full" />
                    <p className="text-sm text-center text-muted-foreground mt-2">{progress}% tamamlandı...</p>
                  </motion.div>
                )}
              </AnimatePresence>

              <AnimatePresence>
                {processingResult && !isProcessing && (
                   <motion.div
                    initial={{ opacity: 0, y: -10 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="mt-4 p-4 border rounded-lg bg-gray-50 dark:bg-gray-800"
                  >
                    <h4 className="font-semibold">İşlem Sonucu:</h4>
                    <p className="text-green-600">Başarılı: {processingResult.processed}</p>
                    <p className="text-red-600">Başarısız: {processingResult.failed}</p>
                  </motion.div>
                )}
              </AnimatePresence>

            </div>
          </div>

          <hr />

          <div>
            <h4 className="font-semibold mb-2">Çakışmaları Çöz</h4>
            <p className="text-sm text-muted-foreground mb-4">Aynı adrese veya koordinata sahip birden fazla şirketi bulur ve çözmek için işaretler.</p>
            <Button onClick={handleResolveConflicts} disabled={isLoading || isProcessing}>
              {isLoading ? 'Yükleniyor...' : 'Çakışmaları Bul ve Çöz'}
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default CoordinatesDashboard;