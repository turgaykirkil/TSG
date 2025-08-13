'use client';

import { useEffect, useState } from 'react';
import { Icons } from '@/components/icons';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Building2, FileSearch, Activity, MapPin } from 'lucide-react';

import FileUploadSection from './components/file-upload-section';
import ScrapingDashboard from './components/scraping-dashboard';
import OCRProcessing from './components/ocr-processing';
import JobHistory from './components/job-history';
import CoordinatesDashboard from './components/coordinates-dashboard';
import { useAuth } from '@/contexts/AuthContext';
import { StatCard } from './components/StatCard';
import { useRealtimeStats } from '@/hooks/useRealtimeStats';

const AdminPage = () => {
  const { stats, error } = useRealtimeStats();
  const { session } = useAuth();
  const user = session?.user;

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
          <CoordinatesDashboard onStatsUpdate={() => {}} />
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

                  {error && <div className="text-red-500 text-center my-4 p-4 border border-red-500 rounded-md">{error}</div>}
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-5 mt-8">
        <StatCard
          title="Toplam Şirket"
          value={stats?.total_companies?.toLocaleString('tr-TR') || '0'}
          icon={Building2}
          change=""
          isLoading={!stats && !error}
        />
        <StatCard 
          title="Taranan Şirket"
          value={stats?.scraped_companies?.toLocaleString('tr-TR') || '0'}
          icon={FileSearch}
          change=""
          isLoading={!stats && !error}
        />
        <StatCard
          title="Toplam İlan"
          value={stats?.total_announcements?.toLocaleString('tr-TR') || '0'}
          icon={Activity}
          change=""
          isLoading={!stats && !error}
        />
        <StatCard
          title="Bugün Eklenen Şirket"
          value={stats?.new_companies_today?.toLocaleString('tr-TR') || '0'}
          icon={MapPin}
          change=""
          isLoading={!stats && !error}
        />
        <StatCard
          title="Bucket PDF"
          value={
            stats?.storage_pdf_count != null
              ? stats.storage_pdf_count.toLocaleString('tr-TR')
              : '0'
          }
          icon={FileSearch}
          change=""
          isLoading={!stats && !error}
        />
      </div>
    </div>
  );
};


export default AdminPage;
