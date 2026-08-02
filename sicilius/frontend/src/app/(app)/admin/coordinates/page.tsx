'use client';

import { useState, useEffect, useCallback } from 'react';
import dynamic from 'next/dynamic';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Progress } from '@/components/ui/progress';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Badge } from '@/components/ui/badge';
import { MapPin, RefreshCw, Layers, CheckCircle2, AlertTriangle, Play, HelpCircle } from 'lucide-react';
import { toast } from 'sonner';
import apiClient from '@/lib/api/client';
import { CoordinatesTable, CompanyRow } from './components/CoordinatesTable';
import { CompanyMapPin } from './components/AdminCoordinatesMap';

// Dynamically import Leaflet Map with SSR disabled
const AdminCoordinatesMap = dynamic(
  () => import('./components/AdminCoordinatesMap').then((mod) => mod.AdminCoordinatesMap),
  {
    ssr: false,
    loading: () => (
      <div className="h-[600px] w-full flex items-center justify-center bg-muted/20 rounded-xl border border-dashed">
        <div className="flex flex-col items-center gap-2 text-muted-foreground">
          <RefreshCw className="h-8 w-8 animate-spin text-primary" />
          <p className="text-sm font-medium">İnteraktif Harita Yükleniyor...</p>
        </div>
      </div>
    ),
  }
);

interface CoordinateStats {
  coordinated: number;
  uncoordinated: number;
  conflicts: number;
}

export default function AdminCoordinatesPage() {
  const [stats, setStats] = useState<CoordinateStats>({ coordinated: 0, uncoordinated: 0, conflicts: 0 });
  const [mapPins, setMapPins] = useState<CompanyMapPin[]>([]);
  const [companiesList, setCompaniesList] = useState<CompanyRow[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [processLimit, setProcessLimit] = useState(50);
  const [progress, setProgress] = useState(0);
  const [activeTab, setActiveTab] = useState('map');

  const fetchStats = useCallback(async () => {
    try {
      const res = await apiClient.get<CoordinateStats>('/api/v1/stats/coordinates/');
      setStats(res.data);
    } catch (err) {
      console.error('Failed to fetch stats:', err);
    }
  }, []);

  const fetchMapPins = useCallback(async () => {
    try {
      const res = await apiClient.get<CompanyMapPin[]>('/api/v1/companies/coordinates/map-pins/', {
        params: { limit: 500 },
      });
      setMapPins(res.data);
    } catch (err) {
      console.error('Failed to fetch map pins:', err);
    }
  }, []);

  const fetchCompanies = useCallback(async () => {
    setIsLoading(true);
    try {
      const res = await apiClient.get('/api/v1/companies/admin-list/', {
        params: { skip: 0, limit: 200 },
      });
      setCompaniesList(res.data);
    } catch (err) {
      console.error('Failed to fetch companies:', err);
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchStats();
    fetchMapPins();
    fetchCompanies();
  }, [fetchStats, fetchMapPins, fetchCompanies]);

  const handleStartBatchGeocoding = async () => {
    if (processLimit <= 0) {
      toast.error('Lütfen geçerli bir limit girin.');
      return;
    }

    setIsProcessing(true);
    setProgress(5);
    toast.info(`${processLimit} adet şirket için kademeli OpenStreetMap geocoding başlatıldı.`);

    // Smoothly increment progress bar while POST is in-flight (approx 0.8s per company)
    let currentPercentage = 5;
    const interval = setInterval(() => {
      currentPercentage = Math.min(92, currentPercentage + Math.max(1, Math.floor(90 / (processLimit * 0.8))));
      setProgress(currentPercentage);
    }, 800);

    try {
      const res = await apiClient.post('/api/v1/processing/process-coordinates/', {
        limit: processLimit,
      });
      clearInterval(interval);
      setProgress(100);
      toast.success(res.data.message || 'Geocoding işlemi tamamlandı.');
      fetchStats();
      fetchMapPins();
      fetchCompanies();
    } catch (err: any) {
      clearInterval(interval);
      toast.error('Geocoding işlemi sırasında hata oluştu.');
    } finally {
      clearInterval(interval);
      setTimeout(() => {
        setIsProcessing(false);
        setProgress(0);
      }, 2000);
    }
  };

  const handleResolveConflicts = async () => {
    setIsLoading(true);
    try {
      const res = await apiClient.post('/api/v1/processing/resolve-conflicts/');
      toast.success(res.data.message || 'Çakışmalar çözüldü.');
      fetchStats();
      fetchMapPins();
    } catch (err) {
      toast.error('Çakışmalar çözülemedi.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header Title */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b pb-4">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-foreground flex items-center gap-2">
            <MapPin className="h-7 w-7 text-primary" />
            Koordinat & Canlı Harita Yönetimi
          </h1>
          <p className="text-sm text-muted-foreground mt-1">
            Şirket adreslerini OpenStreetMap geocoding motoru ile haritaya işleyin, canlı izleyin ve manuel pin düzenlemeleri yapın.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <Button variant="outline" size="sm" onClick={() => { fetchStats(); fetchMapPins(); fetchCompanies(); }} className="gap-1.5">
            <RefreshCw className="h-4 w-4" /> Yenile
          </Button>
        </div>
      </div>

      {/* Stats Summary Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <Card className="bg-emerald-500/5 border-emerald-500/20">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-semibold text-emerald-600 dark:text-emerald-400">
              Koordinatlı Şirketler
            </CardTitle>
            <CheckCircle2 className="h-5 w-5 text-emerald-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-extrabold text-foreground">
              {stats.coordinated.toLocaleString('tr-TR')}
            </div>
            <p className="text-xs text-muted-foreground mt-1">Harita üzerinde konumlandı</p>
          </CardContent>
        </Card>

        <Card className="bg-amber-500/5 border-amber-500/20">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-semibold text-amber-600 dark:text-amber-400">
              Bekleyen (Koordinatsız)
            </CardTitle>
            <HelpCircle className="h-5 w-5 text-amber-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-extrabold text-foreground">
              {stats.uncoordinated.toLocaleString('tr-TR')}
            </div>
            <p className="text-xs text-muted-foreground mt-1">Geocoding bekliyor</p>
          </CardContent>
        </Card>

        <Card className="bg-rose-500/5 border-rose-500/20">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-semibold text-rose-600 dark:text-rose-400">
              Çakışan Adresler
            </CardTitle>
            <AlertTriangle className="h-5 w-5 text-rose-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-extrabold text-foreground">
              {stats.conflicts.toLocaleString('tr-TR')}
            </div>
            <p className="text-xs text-muted-foreground mt-1">Çözüm bekleyen çakışma</p>
          </CardContent>
        </Card>
      </div>

      {/* Main Content Tabs */}
      <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-4">
        <TabsList className="bg-muted p-1 rounded-lg">
          <TabsTrigger value="map" className="gap-2 text-xs font-semibold">
            <MapPin className="h-4 w-4" /> Canlı İnteraktif Harita
          </TabsTrigger>
          <TabsTrigger value="batch" className="gap-2 text-xs font-semibold">
            <Play className="h-4 w-4" /> Toplu Geocoding Paneli
          </TabsTrigger>
          <TabsTrigger value="table" className="gap-2 text-xs font-semibold">
            <Layers className="h-4 w-4" /> Şirket Listesi & Arama
          </TabsTrigger>
        </TabsList>

        {/* TAB 1: Canlı Harita */}
        <TabsContent value="map" className="space-y-4">
          <Card>
            <CardHeader className="pb-3">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                <div>
                  <CardTitle className="text-base font-bold">Haritada Konumlanan Şirketler</CardTitle>
                  <CardDescription className="text-xs">
                    Pinleri fare ile tutup sürükleyerek şirketlerin adres konumunu doğrudan harita üzerinde güncelleyebilirsiniz.
                  </CardDescription>
                </div>
                <div className="flex items-center gap-2">
                  <Badge variant="outline" className="bg-emerald-500/10 text-emerald-600 border-emerald-500/20">
                    🟢 Bina Kesin
                  </Badge>
                  <Badge variant="outline" className="bg-blue-500/10 text-blue-600 border-blue-500/20">
                    🔵 Cadde
                  </Badge>
                  <Badge variant="outline" className="bg-amber-500/10 text-amber-600 border-amber-500/20">
                    🟡 Mahalle
                  </Badge>
                </div>
              </div>
            </CardHeader>
            <CardContent>
              <AdminCoordinatesMap pins={mapPins} onCoordinateUpdated={fetchMapPins} height="620px" />
            </CardContent>
          </Card>
        </TabsContent>

        {/* TAB 2: Toplu Geocoding Paneli */}
        <TabsContent value="batch" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="text-base font-bold">OpenStreetMap Kademeli Geocoding Motoru</CardTitle>
              <CardDescription className="text-xs">
                Veritabanında koordinatı olmayan şirketlerin adreslerini otomatik temizler, 4 kademeli arama yaparak enlem ve boylamlarını atar.
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="flex flex-col sm:flex-row items-start sm:items-center gap-4 bg-muted/40 p-4 rounded-xl border">
                <div className="space-y-1 flex-1">
                  <label className="text-xs font-semibold text-foreground">İşlenecek Adet Limiti</label>
                  <Input
                    type="number"
                    value={processLimit}
                    onChange={(e) => setProcessLimit(parseInt(e.target.value, 10) || 10)}
                    className="max-w-[160px]"
                    disabled={isProcessing}
                  />
                </div>

                <Button
                  onClick={handleStartBatchGeocoding}
                  disabled={isProcessing}
                  className="gap-2 bg-primary text-primary-foreground hover:bg-primary/90 mt-2 sm:mt-0"
                >
                  <Play className="h-4 w-4" />
                  {isProcessing ? 'Geocoding İşleniyor...' : 'Geocoding Çalıştır'}
                </Button>
              </div>

              {isProcessing && (
                <div className="space-y-2 p-4 rounded-xl bg-primary/5 border border-primary/20">
                  <div className="flex items-center justify-between text-xs font-semibold text-primary">
                    <span className="flex items-center gap-2">
                      <RefreshCw className="h-3.5 w-3.5 animate-spin" />
                      Arka plan adres ayrıştırma ve OpenStreetMap sorgulaması... ({Math.min(processLimit, Math.round((progress / 100) * processLimit))}/{processLimit} Şirket)
                    </span>
                    <span className="font-bold">%{progress}</span>
                  </div>
                  <Progress value={progress} className="h-2.5" />
                </div>
              )}

              <hr />

              <div className="flex items-center justify-between p-4 bg-muted/20 rounded-xl border">
                <div className="space-y-1">
                  <h4 className="text-sm font-bold text-foreground">Çakışan Adresleri Çöz</h4>
                  <p className="text-xs text-muted-foreground">
                    Aynı adrese sahip olup farklı koordinatlanan veya aynı koordinattaki çakışmalı şirketleri yeniden doğrular.
                  </p>
                </div>
                <Button variant="outline" size="sm" onClick={handleResolveConflicts} disabled={isLoading}>
                  Çakışmaları Bul ve Çöz
                </Button>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* TAB 3: Şirket Listesi & Arama */}
        <TabsContent value="table" className="space-y-4">
          <CoordinatesTable
            companies={companiesList}
            stats={stats}
            onRefresh={() => { fetchStats(); fetchMapPins(); fetchCompanies(); }}
            onSelectOnMap={(company) => {
              setActiveTab('map');
            }}
          />
        </TabsContent>
      </Tabs>
    </div>
  );
}
