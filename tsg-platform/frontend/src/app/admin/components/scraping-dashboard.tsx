import { useState } from 'react';
import { Icons } from '@/components/icons';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';

export default function ScrapingDashboard() {
  const [scrapingStatus, setScrapingStatus] = useState({
    istanbul: { status: 'idle', progress: 0 },
    ankara: { status: 'idle', progress: 0 },
    izmir: { status: 'idle', progress: 0 }
  });

  const [recentScraping] = useState([
    { id: 1, city: 'İstanbul', date: '2025-06-05', status: 'Tamamlandı', companies: 142 },
    { id: 2, city: 'Ankara', date: '2025-06-04', status: 'Tamamlandı', companies: 98 },
    { id: 3, city: 'İzmir', date: '2025-06-03', status: 'Başarısız', companies: 0, error: 'Bağlantı hatası' },
  ]);

  const startScraping = (city: 'istanbul' | 'ankara' | 'izmir') => {
    setScrapingStatus(prev => ({
      ...prev,
      [city]: { status: 'running', progress: 0 }
    }));

    // Simulate scraping progress
    const interval = setInterval(() => {
      setScrapingStatus(prev => {
        const newProgress = prev[city].progress + 5;
        if (newProgress >= 100) {
          clearInterval(interval);
          return {
            ...prev,
            [city]: { status: 'completed', progress: 100 }
          };
        }
        return {
          ...prev,
          [city]: { ...prev[city], progress: newProgress }
        };
      });
    }, 500);
  };

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <Icons.building2 className="h-5 w-5 mr-2" /> İstanbul Müdürlüğü
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <Progress value={scrapingStatus.istanbul.progress} />
              <div className="flex justify-between text-sm">
                <span>
                  {scrapingStatus.istanbul.status === 'idle' && 'Başlatılmadı'}
                  {scrapingStatus.istanbul.status === 'running' && 'Devam ediyor'}
                  {scrapingStatus.istanbul.status === 'completed' && 'Tamamlandı'}
                </span>
                <span>{scrapingStatus.istanbul.progress}%</span>
              </div>
              <Button 
                onClick={() => startScraping('istanbul')}
                disabled={scrapingStatus.istanbul.status === 'running'}
                className="w-full"
              >
                {scrapingStatus.istanbul.status === 'running' ? (
                  <>
                    <Icons.spinner className="mr-2 h-4 w-4 animate-spin" />
                    Devam Ediyor
                  </>
                ) : 'Scraping Başlat'}
              </Button>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <Icons.building2 className="h-5 w-5 mr-2" /> Ankara Müdürlüğü
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <Progress value={scrapingStatus.ankara.progress} />
              <div className="flex justify-between text-sm">
                <span>
                  {scrapingStatus.ankara.status === 'idle' && 'Başlatılmadı'}
                  {scrapingStatus.ankara.status === 'running' && 'Devam ediyor'}
                  {scrapingStatus.ankara.status === 'completed' && 'Tamamlandı'}
                </span>
                <span>{scrapingStatus.ankara.progress}%</span>
              </div>
              <Button 
                onClick={() => startScraping('ankara')}
                disabled={scrapingStatus.ankara.status === 'running'}
                className="w-full"
              >
                {scrapingStatus.ankara.status === 'running' ? (
                  <>
                    <Icons.spinner className="mr-2 h-4 w-4 animate-spin" />
                    Devam Ediyor
                  </>
                ) : 'Scraping Başlat'}
              </Button>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <Icons.building2 className="h-5 w-5 mr-2" /> İzmir Müdürlüğü
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <Progress value={scrapingStatus.izmir.progress} />
              <div className="flex justify-between text-sm">
                <span>
                  {scrapingStatus.izmir.status === 'idle' && 'Başlatılmadı'}
                  {scrapingStatus.izmir.status === 'running' && 'Devam ediyor'}
                  {scrapingStatus.izmir.status === 'completed' && 'Tamamlandı'}
                </span>
                <span>{scrapingStatus.izmir.progress}%</span>
              </div>
              <Button 
                onClick={() => startScraping('izmir')}
                disabled={scrapingStatus.izmir.status === 'running'}
                className="w-full"
              >
                {scrapingStatus.izmir.status === 'running' ? (
                  <>
                    <Icons.spinner className="mr-2 h-4 w-4 animate-spin" />
                    Devam Ediyor
                  </>
                ) : 'Scraping Başlat'}
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Son Scraping İşlemleri</CardTitle>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Tarih</TableHead>
                <TableHead>Müdürlük</TableHead>
                <TableHead>Durum</TableHead>
                <TableHead>Şirket Sayısı</TableHead>
                <TableHead>Detay</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {recentScraping.map((item) => (
                <TableRow key={item.id}>
                  <TableCell>{item.date}</TableCell>
                  <TableCell>{item.city}</TableCell>
                  <TableCell>
                    <span className={`px-2 py-1 rounded-full text-xs ${item.status === 'Tamamlandı' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
                      {item.status}
                    </span>
                  </TableCell>
                  <TableCell>{item.companies}</TableCell>
                  <TableCell>
                    <Button variant="outline" size="sm">
                      Detay
                    </Button>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  );
}
