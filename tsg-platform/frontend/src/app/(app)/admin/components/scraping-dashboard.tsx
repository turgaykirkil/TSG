'use client';
import React, { useState, useCallback } from 'react';
import { toast } from 'sonner';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Icons } from '@/components/icons';
import LoadingSpinner from '@/components/ui/loading-spinner';

export default function ScrapingDashboard() {
  const [error, setError] = useState<string | null>(null);
  const [isBrowserReady, setIsBrowserReady] = useState<boolean>(false);
  const [isNavigating, setIsNavigating] = useState<boolean>(false); // Re-using for loading state
  const [scrapeCount, setScrapeCount] = useState<number>(10);

  const getApiUrl = useCallback(() => {
    const apiUrl = process.env.NEXT_PUBLIC_API_URL;
    if (!apiUrl) {
      const errorMessage = 'API URL is not configured. Please set NEXT_PUBLIC_API_URL in your environment variables.';
      setError(errorMessage);
      toast.error(errorMessage);
      throw new Error(errorMessage);
    }
    return `${apiUrl}/api/v1`;
  }, []);

  const handleOpenBrowser = async () => {
    setError(null);
    setIsNavigating(true);
    try {
      const apiUrl = getApiUrl();
      const res = await fetch(`${apiUrl}/scraping/browser/open`, {
        method: 'POST',
      });

      if (!res.ok) {
        const errorData = await res.json().catch(() => ({ detail: 'Failed to open browser.' }));
        throw new Error(errorData.detail || `Server error: ${res.status}`);
      }
      toast.success('Tarayıcı başarıyla açıldı. Lütfen giriş yapın.');
      setIsBrowserReady(true);
    } catch (err: any) {
      setError(err.message);
      toast.error(err.message);
    } finally {
      setIsNavigating(false);
    }
  };

  const handleStartScraping = async () => {
    if (isNavigating) return;

    if (scrapeCount <= 0) {
      toast.error('Lütfen geçerli bir adet girin.');
      return;
    }

    setError(null);
    setIsNavigating(true);
    try {
      const apiUrl = getApiUrl();

      // First, check browser status
      const statusResponse = await fetch(`${apiUrl}/scraping/browser/status`);
      const statusData = await statusResponse.json();

      if (!statusData.is_open) {
        throw new Error("Tarayıcı açık değil. Lütfen önce 'Giriş Sayfasını Aç' butonu ile tarayıcıyı açın.");
      }

      // If open, proceed to start enhanced scraping with count parameter
      const response = await fetch(`${apiUrl}/scraping/start`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ count: scrapeCount }),
        credentials: 'include', // Send cookies for authentication
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ detail: 'Enhanced scraping başlatılamadı.' }));
        throw new Error(errorData.detail || `Server error: ${response.status}`);
      }

      const result = await response.json();
      toast.success(result.message);
    } catch (err: any) {
      setError(err.message);
      toast.error(err.message || 'Bir hata oluştu.');
    } finally {
      setIsNavigating(false);
    }
  };

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>İnteraktif Web Scraping</CardTitle>
          <CardDescription>
            Ticaret Sicil Gazetesi'nden şirket verilerini adım adım kontrol ederek çekin.
          </CardDescription>
        </CardHeader>
        <CardContent>
          {error && (
            <div className="mb-4 rounded-md border border-destructive bg-destructive/10 p-3">
              <p className="text-sm font-medium text-destructive">Hata: {error}</p>
            </div>
          )}

          <div className="space-y-6">
            <div className="p-4 border rounded-lg bg-slate-50 dark:bg-slate-800/50">
              <h3 className="font-semibold text-lg">Adım 1: Tarayıcıyı Başlat</h3>
              <p className="text-sm text-muted-foreground mt-1">
                Veri çekme işlemine başlamadan önce, Sicil Gazetesi sitesine manuel giriş yapabilmeniz için Playwright tarayıcısını başlatın. Tarayıcı yeni bir pencerede açılacaktır.
              </p>
              <Button onClick={handleOpenBrowser} disabled={isNavigating || isBrowserReady} className="mt-3">
                {isNavigating && !isBrowserReady ? <LoadingSpinner className="mr-2" /> : <Icons.externalLink className="mr-2 h-4 w-4" />}
                {isBrowserReady ? 'Tarayıcı Açık' : 'Giriş Sayfasını Aç'}
              </Button>
            </div>

            {isBrowserReady && (
              <div className="p-4 border rounded-lg bg-slate-50 dark:bg-slate-800/50">
                <h3 className="font-semibold text-lg">Adım 2: Enhanced Scraping'i Başlat</h3>
                <p className="text-sm text-muted-foreground mt-1">
                  Taramak istediğiniz şirket adedini girin ve enhanced scraping işlemini başlatın. Sistem companies tablosundan sicil no ve sicil müdürlüğü olan şirketleri alacak, otomatik form doldurup ilan verilerini çekecektir.
                </p>
                <div className="flex items-center gap-4 mt-3">
                  <Input
                    type="number"
                    value={scrapeCount}
                    onChange={(e) => setScrapeCount(Math.max(0, Number(e.target.value)))}
                    placeholder="Adet"
                    className="w-28"
                    disabled={isNavigating}
                  />
                  <Button onClick={handleStartScraping} disabled={isNavigating || scrapeCount <= 0}>
                    {isNavigating ? <LoadingSpinner className="mr-2" /> : <Icons.arrowRightCircle className="mr-2 h-4 w-4" />}
                    Scraping'i Başlat
                  </Button>
                </div>
              </div>
            )}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
