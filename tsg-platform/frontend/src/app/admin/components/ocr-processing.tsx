import { useState } from 'react';
import { Icons } from '@/components/icons';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';

export default function OCRProcessing() {
  const [ocrStatus, setOcrStatus] = useState<'idle' | 'running' | 'completed'>('idle');
  const [progress, setProgress] = useState(0);
  
  const [ocrQueue] = useState([
    { id: 1, fileName: 'firma-listesi.xlsx', status: 'Bekliyor', date: '2025-06-05' },
    { id: 2, fileName: 'resmi-gazete.pdf', status: 'Tamamlandı', date: '2025-06-04' },
    { id: 3, fileName: 'ilanlar.pdf', status: 'Başarısız', date: '2025-06-03', error: 'Dosya formatı desteklenmiyor' },
  ]);

  const startOCR = () => {
    if (ocrStatus === 'running') return;
    
    setOcrStatus('running');
    setProgress(0);
    
    // Simulate OCR progress
    const interval = setInterval(() => {
      setProgress(prev => {
        const newProgress = prev + 5;
        if (newProgress >= 100) {
          clearInterval(interval);
          setOcrStatus('completed');
          return 100;
        }
        return newProgress;
      });
    }, 500);
  };

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>OCR İşlemi</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="font-medium">İşlem Durumu</h3>
                <p className="text-sm text-muted-foreground">
                  {ocrStatus === 'idle' && 'OCR başlatılmadı'}
                  {ocrStatus === 'running' && 'OCR işlemi devam ediyor'}
                  {ocrStatus === 'completed' && 'OCR işlemi tamamlandı'}
                </p>
              </div>
              <Button 
                onClick={startOCR}
                disabled={ocrStatus === 'running'}
              >
                {ocrStatus === 'running' ? (
                  <>
                    <Icons.spinner className="mr-2 h-4 w-4 animate-spin" />
                    Devam Ediyor
                  </>
                ) : 'OCR Başlat'}
              </Button>
            </div>
            
            {ocrStatus !== 'idle' && (
              <div className="space-y-2">
                <Progress value={progress} />
                <div className="flex justify-between text-sm">
                  <span>İlerleme</span>
                  <span>{progress}%</span>
                </div>
              </div>
            )}
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>OCR Kuyruğu</CardTitle>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Dosya Adı</TableHead>
                <TableHead>Tarih</TableHead>
                <TableHead>Durum</TableHead>
                <TableHead>İşlemler</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {ocrQueue.map((item) => (
                <TableRow key={item.id}>
                  <TableCell className="font-medium">{item.fileName}</TableCell>
                  <TableCell>{item.date}</TableCell>
                  <TableCell>
                    <span className={`px-2 py-1 rounded-full text-xs ${item.status === 'Tamamlandı' ? 'bg-green-100 text-green-800' : item.status === 'Başarısız' ? 'bg-red-100 text-red-800' : 'bg-yellow-100 text-yellow-800'}`}>
                      {item.status}
                    </span>
                  </TableCell>
                  <TableCell>
                    {item.status === 'Tamamlandı' && (
                      <Button variant="outline" size="sm">
                        <Icons.fileText className="mr-1 h-4 w-4" /> Görüntüle
                      </Button>
                    )}
                    {item.status === 'Başarısız' && (
                      <Button variant="outline" size="sm">
                        <Icons.refreshCw className="mr-1 h-4 w-4" /> Yeniden Dene
                      </Button>
                    )}
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
