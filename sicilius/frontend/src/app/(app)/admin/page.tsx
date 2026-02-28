'use client';

import { useEffect, useState } from 'react';
import { Icons } from '@/components/icons';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Building2, FileSearch, Activity, MapPin, Sun, Moon } from 'lucide-react';

import FileUploadSection from './components/file-upload-section';
import ScrapingDashboard from './components/scraping-dashboard';
import OCRProcessing from './components/ocr-processing';
import JobHistory from './components/job-history';
import CoordinatesDashboard from './components/coordinates-dashboard';
import { useAuth } from '@/contexts/AuthContext';
// import { StatCard } from './components/StatCard';
// import { useRealtimeStats } from '@/hooks/useRealtimeStats';
import { Button } from '@/components/ui/button';
import { useTheme } from '@/contexts/ThemeContext';

import { AdminStats } from '@/app/(app)/admin/components/dashboard/AdminStats';

const AdminPage = () => {
  // const { stats, error } = useRealtimeStats(); // Removed by User Request
  const { session } = useAuth();
  const user = session?.user;
  const { theme, setTheme } = useTheme();
  const toggleTheme = () => setTheme(theme === 'dark' ? 'light' : 'dark');

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="flex items-center justify-between mb-8">
        <h1 className="text-3xl font-bold">Sicilius Admin Paneli</h1>
        <Button variant="outline" onClick={toggleTheme} aria-label="Tema değiştir">
          {theme === 'dark' ? (
            <>
              <Sun className="mr-2 h-4 w-4" /> Açık Tema
            </>
          ) : (
            <>
              <Moon className="mr-2 h-4 w-4" /> Koyu Tema
            </>
          )}
        </Button>
      </div>

      <AdminStats />

      <Tabs defaultValue="fileUpload" className="w-full">
        <TabsList className="grid grid-cols-2 md:grid-cols-5 w-full max-w-3xl mb-6 h-auto">
          <TabsTrigger value="fileUpload">
            <Icons.upload className="mr-2 h-4 w-4" /> Dosya Yükleme
          </TabsTrigger>
          <TabsTrigger value="coordinates">
            <Icons.mapPin className="mr-2 h-4 w-4" /> Koordinat
          </TabsTrigger>
          <TabsTrigger value="scraping">
            <Icons.layoutDashboard className="mr-2 h-4 w-4" /> Web Scraping
          </TabsTrigger>

          <TabsTrigger value="history">
            <Icons.history className="mr-2 h-4 w-4" /> Geçmiş
          </TabsTrigger>
        </TabsList>

        <TabsContent value="fileUpload">
          <FileUploadSection />
        </TabsContent>
        <TabsContent value="coordinates">
          <CoordinatesDashboard onStatsUpdate={() => { }} />
        </TabsContent>
        <TabsContent value="scraping">
          <ScrapingDashboard />
        </TabsContent>

        <TabsContent value="history">
          <JobHistory />
        </TabsContent>
      </Tabs>

      {/* Stats Section Removed by User Request */}
      {/* <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-5 mt-8">
        ... (Stats Removed) ...
      </div> */}
    </div>
  );
};


export default AdminPage;
