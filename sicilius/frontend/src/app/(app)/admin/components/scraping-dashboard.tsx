'use client';

import React, { useState, useCallback, useEffect } from 'react';
import { toast } from 'sonner';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Icons } from '@/components/icons';
import LoadingSpinner from '@/components/ui/loading-spinner';

export default function ScrapingDashboard() {
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [scrapeCount, setScrapeCount] = useState<number>(10);
  const [status, setStatus] = useState<any | null>(null);
  const [selectedCity, setSelectedCity] = useState<'İSTANBUL' | 'ANKARA' | 'İZMİR' | null>(null);
  const [workerSource, setWorkerSource] = useState<'local' | 'remote'>('remote'); // Default to Old Mac

  const getApiUrl = useCallback(() => `/api/v1`, []);

  const handleStartScraping = async () => {
    if (isLoading) return;
    if (scrapeCount <= 0) {
      toast.error('Lütfen geçerli bir adet girin.');
      return;
    }
    setError(null);
    setIsLoading(true);
    try {
      const response = await fetch(`/api/scraping/start`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ count: scrapeCount, worker_source: workerSource }),
        credentials: 'include',
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ detail: 'Scraping başlatılamadı.' }));
        throw new Error(errorData.detail || `Server error: ${response.status}`);
      }
      const result = await response.json();
      toast.success(result.message || 'Scraping başlatıldı.');
    } catch (err: any) {
      setError(err.message);
      toast.error(err.message || 'Bir hata oluştu.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleStartCityFill = async (city: 'İSTANBUL' | 'ANKARA' | 'İZMİR') => {
    if (isLoading) return;
    if (scrapeCount <= 0) {
      toast.error('Lütfen geçerli bir adet girin.');
      return;
    }
    setError(null);
    setIsLoading(true);
    setSelectedCity(city);
    try {
      const response = await fetch(`/api/scraping/start`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ count: scrapeCount, mode: 'city_fill', city, worker_source: workerSource }),
        credentials: 'include',
      });
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ detail: 'Scraping başlatılamadı.' }));
        throw new Error(errorData.detail || `Server error: ${response.status}`);
      }
      const result = await response.json();
      toast.success(result.message || `${city} için city_fill scraping başlatıldı.`);
    } catch (err: any) {
      setError(err.message);
      toast.error(err.message || 'Bir hata oluştu.');
    } finally {
      setIsLoading(false);
    }
  };

  const fetchStatus = useCallback(async () => {
    try {
      const apiUrl = getApiUrl();
      const res = await fetch(`${apiUrl}/scraping/browser/status`, { credentials: 'include' });
      if (!res.ok) return;
      const data = await res.json();
      setStatus(data);
    } catch (e) {
      // sessiz geç
    }
  }, [getApiUrl]);

  useEffect(() => {
    fetchStatus();
  }, [fetchStatus]);

  useEffect(() => {
    if (status?.scraping?.running) {
      const id = setInterval(fetchStatus, 3000);
      return () => clearInterval(id);
    }
    return;
  }, [status?.scraping?.running, fetchStatus]);

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>Web Scraping</CardTitle>
          <CardDescription>
            Ticaret Sicil Gazetesi'nden şirket ilânları ve PDF'leri otomatik olarak çekin.
          </CardDescription>
        </CardHeader>
        <CardContent>
          {error && (
            <div className="mb-4 rounded-md border border-destructive bg-destructive/10 p-3">
              <p className="text-sm font-medium text-destructive">Hata: {error}</p>
            </div>
          )}

          <div className="p-4 border rounded-lg bg-slate-50 dark:bg-slate-800/50">
            <p className="text-sm text-muted-foreground mt-1">
              Taramak istediğiniz şirket adedini girin ve scraping işlemini başlatın. Sistem companies tablosundan sicil no ve sicil müdürlüğü olan şirketleri alacak, otomatik form doldurup ilân verileri ile PDF'leri Supabase'e yükleyecektir. Tarayıcı ve giriş işlemi otomatik olarak yönetilir (OCR CAPTCHA dahil).
            </p>
            <div className="flex flex-wrap items-center gap-3 mt-3">
              <Input
                type="number"
                value={scrapeCount}
                onChange={(e) => setScrapeCount(Math.max(0, Number(e.target.value)))}
                placeholder="Adet"
                className="w-28"
                disabled={isLoading}
              />
              <Button onClick={handleStartScraping} disabled={isLoading || scrapeCount <= 0}>
                {isLoading ? <LoadingSpinner className="mr-2" /> : <Icons.arrowRightCircle className="mr-2 h-4 w-4" />}
                Scraping'i Başlat
              </Button>
              <div className="h-6 w-px bg-border" />
              <Button variant={selectedCity === 'İSTANBUL' ? 'default' : 'outline'} disabled={isLoading || scrapeCount <= 0} onClick={() => handleStartCityFill('İSTANBUL')}>
                İstanbul
              </Button>
              <Button variant={selectedCity === 'ANKARA' ? 'default' : 'outline'} disabled={isLoading || scrapeCount <= 0} onClick={() => handleStartCityFill('ANKARA')}>
                Ankara
              </Button>
              <Button variant={selectedCity === 'İZMİR' ? 'default' : 'outline'} disabled={isLoading || scrapeCount <= 0} onClick={() => handleStartCityFill('İZMİR')}>
                İzmir
              </Button>
            </div>

            <div className="mt-4 flex items-center gap-4 p-3 border rounded-md bg-white dark:bg-black/40">
              <span className="text-sm font-medium">Kaynak:</span>
              <div className="flex items-center gap-2">
                <Button
                  variant={workerSource === 'local' ? 'secondary' : 'ghost'}
                  size="sm"
                  onClick={() => setWorkerSource('local')}
                  className={workerSource === 'local' ? 'bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-300' : ''}
                >
                  <Icons.laptop className="mr-2 h-4 w-4" />
                  Bu Bilgisayar (5001)
                </Button>
                <Button
                  variant={workerSource === 'remote' ? 'secondary' : 'ghost'}
                  size="sm"
                  onClick={() => setWorkerSource('remote')}
                  className={workerSource === 'remote' ? 'bg-amber-100 text-amber-700 dark:bg-amber-900/30 dark:text-amber-300' : ''}
                >
                  <Icons.server className="mr-2 h-4 w-4" />
                  Eski Mac (5002)
                </Button>
              </div>
            </div>
            <div className="mt-4 rounded-md border bg-white/50 dark:bg-black/20 p-3 text-sm">
              <div className="flex items-center justify-between">
                <div>
                  <span className="font-medium">Durum: </span>
                  {status?.scraping?.running ? 'Çalışıyor' : 'Beklemede'}
                </div>
                <Button variant="secondary" size="sm" onClick={fetchStatus}>
                  Durumu Yenile
                </Button>
              </div>
              <div className="mt-2 grid grid-cols-3 gap-3">
                <div className="rounded bg-slate-100 dark:bg-slate-900/40 p-2">
                  <div className="text-xs text-muted-foreground">İşlenen</div>
                  <div className="font-semibold">{status?.scraping?.processed ?? 0}</div>
                </div>
                <div className="rounded bg-slate-100 dark:bg-slate-900/40 p-2">
                  <div className="text-xs text-muted-foreground">Toplam</div>
                  <div className="font-semibold">{status?.scraping?.total ?? 0}</div>
                </div>
                <div className="rounded bg-slate-100 dark:bg-slate-900/40 p-2">
                  <div className="text-xs text-muted-foreground">Hata</div>
                  <div className="font-semibold truncate" title={status?.scraping?.error || '-'}>
                    {status?.scraping?.error ? 'Var' : 'Yok'}
                  </div>
                </div>
              </div>
              {Array.isArray(status?.scraping?.logs) && status.scraping.logs.length > 0 && (
                <div className="mt-3 max-h-48 overflow-auto border-t pt-2 text-xs">
                  {status.scraping.logs.slice(-20).map((l: string, idx: number) => (
                    <div key={idx} className="text-muted-foreground">• {l}</div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
