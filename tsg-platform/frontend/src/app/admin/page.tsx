import { useState, useEffect } from 'react';
import { Icons } from '@/components/icons';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { supabase } from '@/lib/supabase';
import FileUploadSection from './components/file-upload-section';
import ScrapingDashboard from './components/scraping-dashboard';
import OCRProcessing from './components/ocr-processing';
import JobHistory from './components/job-history';

interface StatsState {
  totalCompanies: number;
  scrapedCompanies: number;
  isLoading: boolean;
}

const AdminPage = () => {
  const [stats, setStats] = useState<StatsState>({
    totalCompanies: 0,
    scrapedCompanies: 0,
    isLoading: true
  });

  useEffect(() => {
    const fetchStats = async () => {
      try {
        // Toplam yüklenen firma sayısını al
        const { count: totalCount } = await supabase
          .from('companies')
          .select('*', { count: 'exact', head: true });

        // Scraping yapılmış firma sayısını al
        const { count: scrapedCount } = await supabase
          .from('companies')
          .select('*', { count: 'exact', head: true })
          .not('last_scraped_at', 'is', null);

        setStats({
          totalCompanies: totalCount || 0,
          scrapedCompanies: scrapedCount || 0,
          isLoading: false
        });
      } catch (error) {
        console.error('İstatistikler yüklenirken hata oluştu:', error);
        setStats(prev => ({
          ...prev,
          totalCompanies: 0,
          scrapedCompanies: 0,
          isLoading: false
        }));
      }
    };

    // İlk yükleme
    fetchStats();

    // Realtime aboneliği başlat
    const subscription = supabase
      .channel('companies_changes')
      .on('postgres_changes', 
        { 
          event: '*', 
          schema: 'public', 
          table: 'companies' 
        }, 
        (payload) => {
          console.log('Değişiklik algılandı:', payload);
          // Herhangi bir değişiklik olduğunda istatistikleri yenile
          fetchStats();
        }
      )
      .subscribe();

    // Temizleme fonksiyonu
    return () => {
      supabase.removeChannel(subscription);
    };
  }, []);

  if (stats.isLoading) {
    return <div>Yükleniyor...</div>;
  }
  return (
    <div className="container mx-auto px-4 py-8">
      <div className="flex items-center justify-between mb-8">
        <h1 className="text-3xl font-bold">Admin Paneli</h1>
        <div className="flex items-center space-x-2">
          <Button variant="outline">
            <Icons.settings className="mr-2 h-4 w-4" /> Ayarlar
          </Button>
          <Button>
            <Icons.user className="mr-2 h-4 w-4" /> Profil
          </Button>
        </div>
      </div>

      <Tabs defaultValue="fileUpload" className="w-full">
        <TabsList className="grid grid-cols-4 w-full max-w-2xl mb-6">
          <TabsTrigger value="fileUpload">
            <Icons.upload className="mr-2 h-4 w-4" /> Dosya Yükleme
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
            <CardTitle className="text-sm font-medium">Yüklenen Firmalar</CardTitle>
            <Icons.building2 className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.totalCompanies}</div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Scraping Yapılan</CardTitle>
            <Icons.checkCircle className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.scrapedCompanies}</div>
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
