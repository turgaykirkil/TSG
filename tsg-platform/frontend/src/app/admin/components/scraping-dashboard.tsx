'use client';
import React, { useState, useEffect, FormEvent } from 'react';
import { Input } from '@/components/ui/input';
import { Select, SelectTrigger, SelectContent, SelectItem, SelectValue } from '@/components/ui/select';
import { Icons } from '@/components/icons';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';

export default function ScrapingDashboard() {
  const [isRunning, setIsRunning] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [processed, setProcessed] = useState<number>(0);
  const [total, setTotal] = useState<number>(0);
  const [pdfSize, setPdfSize] = useState<number>(0);
  const [count, setCount] = useState<number>(100);
  const [companyRows, setCompanyRows] = useState<Array<{
    id: string;
    trade_registry_number: string;
    title: string;
    status: 'success' | 'error';
    errorMessage?: string;
  }>>([]);

  // Adım 1: Giriş sayfasını yeni sekmede açar
  const openLoginPage = () => {
    const targetUrl = 'https://www.ticaretsicil.gov.tr/view/hizlierisim/ilangoruntuleme.php';
    window.open(targetUrl, '_blank');
  };

  // Adım 2: Backend'de scraping işlemini başlatır
  const handleStartBackendScraping = async () => {
    setIsRunning(true);
    setError(null);
    setProcessed(0);
    setTotal(0);
    setCompanyRows([]);

    try {
      const res = await fetch('/api/scraping/start', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ count }),
      });

      if (!res.ok) {
        const errorData = await res.json().catch(() => ({ message: 'Bilinmeyen bir sunucu hatası oluştu.' }));
        throw new Error(errorData.message || `Sunucu hatası: ${res.status}`);
      }
      // useEffect statusu kontrol etmeye başlayacak
    } catch (err: any) {
      setError(err.message);
      setIsRunning(false);
    }
  };

  const handleStopScraping = async () => {
    try {
      await fetch('/api/scraping/stop', { method: 'POST' });
    } catch {}
    setIsRunning(false);
    setProcessed(0);
    setTotal(0);
    setPdfSize(0);
  };

  useEffect(() => {
    let interval: NodeJS.Timeout;
    if (isRunning) {
      interval = setInterval(async () => {
        try {
          const res = await fetch('/api/scraping/status');
          if (!res.ok) throw new Error('Sunucu durumu alınamadı');
          const data = await res.json();
          setProcessed(data.processed || 0);
          setTotal(data.total || count);
          setPdfSize(data.pdfSize || 0);
          if (Array.isArray(data.companies)) {
            setCompanyRows(data.companies.map((c: any) => ({
              id: c.id,
              trade_registry_number: c.trade_registry_number,
              title: c.title,
              status: c.error ? 'error' : 'success',
              errorMessage: c.error || undefined,
            })));
          }
          if (!data.running) {
            setIsRunning(false);
          }
        } catch (e) {
          console.error(e);
          setError('Scraping durumu alınırken bir hata oluştu.');
          setIsRunning(false);
        }
      }, 2000);
    }
    return () => clearInterval(interval);
  }, [isRunning, count]);

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>Scraping Otomasyonu</CardTitle>
        </CardHeader>
        <CardContent>
          {error && <p className="text-red-500 text-sm font-medium mb-4">Hata: {error}</p>}
          {!isRunning ? (
            <div className="space-y-6">
              <div className="p-4 border rounded-lg bg-slate-50">
                <h3 className="font-semibold text-lg">Adım 1: Manuel Giriş</h3>
                <p className="text-sm text-muted-foreground mt-1">
                  Ticaret Sicil Gazetesi sitesine manuel olarak giriş yapın. Bu işlem, CAPTCHA gibi doğrulamaları geçmenizi sağlar.
                </p>
                <Button onClick={openLoginPage} className="mt-3">
                  <Icons.externalLink className="mr-2 h-4 w-4" />
                  Giriş Sayfasını Aç
                </Button>
              </div>

              <div className="p-4 border rounded-lg bg-slate-50">
                <h3 className="font-semibold text-lg">Adım 2: Scraping'i Başlat</h3>
                <p className="text-sm text-muted-foreground mt-1">
                  Giriş yaptıktan sonra, aşağıdaki butona basarak veri kazıma işlemini başlatın.
                </p>
                <div className="flex flex-col gap-4 mt-3">
                  <label className="flex flex-col gap-2">
                    <span className="font-medium">Kaç adet firma scrape edilsin?</span>
                    <Input
                      type="number"
                      min={1}
                      max={1000}
                      value={count}
                      onChange={e => setCount(Number(e.target.value))}
                      className="w-32"
                      required
                    />
                  </label>
                  <Button onClick={handleStartBackendScraping} className="w-full max-w-xs">
                    <Icons.arrowRightCircle className="mr-2 h-4 w-4" />
                    Giriş Yaptım, Scraping'i Başlat
                  </Button>
                </div>
              </div>
            </div>
          ) : (
            <div>
              <Progress value={total ? (processed / total) * 100 : 0} className="h-2 mb-2" />
              <p>İşlenen: {processed} / {total}</p>
              <p>PDF Toplam Boyutu: {(pdfSize / 1024).toFixed(2)} KB</p>
              <Button variant="destructive" onClick={handleStopScraping} className="mt-4 w-full">
                <Icons.xCircle className="mr-2 h-4 w-4" />
                Durdur
              </Button>
              <div className="mt-6 overflow-x-auto">
                <table className="min-w-full text-sm border">
                  <thead>
                    <tr className="bg-gray-100">
                      <th className="border px-2 py-1">#</th>
                      <th className="border px-2 py-1">Sicil No</th>
                      <th className="border px-2 py-1">Unvan</th>
                      <th className="border px-2 py-1">Durum</th>
                      <th className="border px-2 py-1">Hata Mesajı</th>
                    </tr>
                  </thead>
                  <tbody>
                    {companyRows.length === 0 ? (
                      <tr><td colSpan={5} className="text-center py-2">Henüz işlenen firma yok...</td></tr>
                    ) : (
                      companyRows.map((row, i) => (
                        <tr key={row.id} className={row.status === 'error' ? 'bg-red-50' : ''}>
                          <td className="border px-2 py-1">{i + 1}</td>
                          <td className="border px-2 py-1">{row.trade_registry_number}</td>
                          <td className="border px-2 py-1">{row.title}</td>
                          <td className="border px-2 py-1 font-semibold text-xs">
                            {row.status === 'success' ? <span className="text-green-600">Başarılı</span> : <span className="text-red-600">Hata</span>}
                          </td>
                          <td className="border px-2 py-1 text-xs text-red-600 max-w-xs truncate" title={row.errorMessage}>{row.errorMessage || '-'}</td>
                        </tr>
                      ))
                    )}
                  </tbody>
                </table>
              </div>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
