'use client';

import { useState, useEffect, useCallback } from 'react';
import { Icons } from '@/components/icons';

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';

import FileUploadSection from './components/file-upload-section';
import ScrapingDashboard from './components/scraping-dashboard';
import OCRProcessing from './components/ocr-processing';
import JobHistory from './components/job-history';
import LoadingSpinner from '@/components/ui/loading-spinner';
import CoordinatesDashboard from '@/app/admin/components/coordinates-dashboard'; // Renders the new coordinates management panel

interface StatsState {
  totalCompanies: number;
  scrapedCompanies: number;
  withCoordinates: number;
}

const AdminPage = () => {
  const [stats, setStats] = useState<StatsState>({
    totalCompanies: 0,
    scrapedCompanies: 0,
    withCoordinates: 0,
  });

    const fetchStats = useCallback(async () => {
    try {
      // Backend API'den istatistikleri çekiyoruz. URL'nin ortam değişkeninden gelmesi daha doğrudur.
      const apiUrl = process.env.NEXT_PUBLIC_API_URL;
      if (!apiUrl) {
        throw new Error('API URL is not configured in environment variables.');
      }
      const response = await fetch(`${apiUrl}/stats`);
      if (!response.ok) {
        throw new Error(`API isteği başarısız oldu: ${response.status}`);
      }
      const data = await response.json();
      setStats({
        totalCompanies: data.totalCompanies || 0,
        scrapedCompanies: data.scrapedCompanies || 0,
        withCoordinates: data.withCoordinates || 0,
      });
    } catch (error) {
      console.error('İstatistikler yüklenirken hata oluştu:', error);
      setStats({
        totalCompanies: 0,
        scrapedCompanies: 0,
        withCoordinates: 0,
      });
    }
  }, []);

  useEffect(() => {
    fetchStats();
    // Not: Supabase abonelikleri ile sağlanan gerçek zamanlı güncelleme kaldırıldı.
    // Bu özellik gerekirse, backend üzerinden WebSocket gibi bir teknoloji ile yeniden uygulanmalıdır.
  }, [fetchStats]);
  return (
    <div className="container mx-auto px-4 py-8">
      <div className="flex items-center justify-between mb-8">
        <h1 className="text-3xl font-bold">Sicilius Admin Paneli</h1>
      </div>

      <Tabs defaultValue="fileUpload" className="w-full">
        <TabsList className="grid grid-cols-5 w-full max-w-3xl mb-6">
          <TabsTrigger value="fileUpload">
            <Icons.upload className="mr-2 h-4 w-4" /> Dosya Yükleme
          </TabsTrigger>
          <TabsTrigger value="coordinates">
            <Icons.mapPin className="mr-2 h-4 w-4" /> Koordinat
          </TabsTrigger>
          <TabsTrigger value="scraping">
            <Icons.layoutDashboard className="mr-2 h-4 w-4" /> Web Scraping
          </TabsTrigger>
          <TabsTrigger value="ocr">
            <Icons.fileText className="mr-2 h-4 w-4" /> OCR İşlemleri
          </TabsTrigger>
          <TabsTrigger value="history">
            <Icons.history className="mr-2 h-4 w-4" /> İş Geçmişi
          </TabsTrigger>
        </TabsList>

        <TabsContent value="fileUpload">
          <FileUploadSection />
        </TabsContent>
        <TabsContent value="coordinates">
          <CoordinatesDashboard stats={stats} refreshStats={fetchStats} />
        </TabsContent>
        <TabsContent value="scraping">
          <ScrapingDashboard />
        </TabsContent>
        <TabsContent value="ocr">
          <OCRProcessing />
        </TabsContent>
        <TabsContent value="history">
          <JobHistory />
        </TabsContent>
      </Tabs>

      <div className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Yüklenen Sicil Numaraları</CardTitle>
            <Icons.hash className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.totalCompanies.toLocaleString('tr-TR')}</div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Scraping Yapılan</CardTitle>
            <Icons.checkCircle className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.scrapedCompanies.toLocaleString('tr-TR')}</div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">OCR Yapılan</CardTitle>
            <Icons.fileText className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">0</div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default AdminPage;
