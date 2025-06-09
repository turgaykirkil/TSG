import { Icons } from '@/components/icons';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import FileUploadSection from './components/file-upload-section';
import ScrapingDashboard from './components/scraping-dashboard';
import OCRProcessing from './components/ocr-processing';
import JobHistory from './components/job-history';

const AdminPage = () => {
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
            <CardTitle className="text-sm font-medium">Aktif İşler</CardTitle>
            <Icons.refreshCw className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">12</div>
            <p className="text-xs text-muted-foreground">Son 24 saat</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Tamamlanan İşler</CardTitle>
            <Icons.checkCircle className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">342</div>
            <p className="text-xs text-muted-foreground">Bu ay</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Başarısız İşler</CardTitle>
            <Icons.alertTriangle className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">8</div>
            <p className="text-xs text-muted-foreground">Bu ay</p>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default AdminPage;
