'use client';

import React, { useEffect, useState, useMemo } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Building2, 
  FileText, 
  MapPin, 
  Zap, 
  RefreshCcw, 
  Download, 
  Printer, 
  TrendingUp, 
  Layers, 
  PieChart as PieChartIcon, 
  Activity, 
  CheckCircle2, 
  Clock, 
  AlertTriangle,
  ArrowUpRight,
  Filter,
  BarChart3,
  Calendar,
  Sparkles,
  ExternalLink
} from 'lucide-react';
import { 
  ResponsiveContainer, 
  AreaChart, 
  Area, 
  BarChart, 
  Bar, 
  PieChart, 
  Pie, 
  Cell, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  Legend 
} from 'recharts';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { Skeleton } from '@/components/ui/skeleton';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { useToast } from '@/components/ui/use-toast';
import axios from '@/lib/axios';

interface AnalyticsData {
  kpis: {
    total_companies: number;
    total_announcements: number;
    total_ocr_chunks: number;
    total_cities: number;
    enrichment_rate: number;
    completed_ocrs: number;
    pending_ocrs: number;
    failed_ocrs: number;
  };
  timeline: Array<{
    date: string;
    label: string;
    companies: number;
    announcements: number;
  }>;
  cities: Array<{
    name: string;
    value: number;
  }>;
  subjects: Array<{
    name: string;
    value: number;
  }>;
  top_companies: Array<{
    id: string;
    unvan: string;
    city: string;
    sicil_no: string;
    announcement_count: number;
  }>;
}

const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#8b5cf6', '#ec4899', '#06b6d4', '#f97316', '#64748b'];

export default function ReportsPage() {
  const { toast } = useToast();
  const [data, setData] = useState<AnalyticsData | null>(null);
  const [loading, setLoading] = useState(true);
  const [selectedDays, setSelectedDays] = useState<number>(30);
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [activeTab, setActiveTab] = useState('market');

  const fetchAnalytics = async (days = selectedDays) => {
    try {
      setIsRefreshing(true);
      const res = await axios.get(`/api/v1/stats/analytics?days=${days}`);
      setData(res.data);
    } catch (err) {
      console.error('Failed to fetch analytics report:', err);
      toast({
        title: 'Veri Yüklenemedi',
        description: 'İş zekası raporları alınırken bir hata oluştu.',
        variant: 'destructive',
      });
    } finally {
      setLoading(false);
      setIsRefreshing(false);
    }
  };

  useEffect(() => {
    fetchAnalytics(selectedDays);
  }, [selectedDays]);

  // Export Data to CSV
  const handleExportCSV = () => {
    if (!data) return;
    try {
      const csvRows = [
        ['Rapor Türü', 'Sicilius B2B İstihbarat Raporu'],
        ['Oluşturulma Tarihi', new Date().toLocaleDateString('tr-TR')],
        ['Seçilen Dönem', `${selectedDays === 0 ? 'Tüm Zamanlar' : `Son ${selectedDays} Gün`}`],
        [],
        ['--- GENEL KPI ÖZETİ ---'],
        ['Toplam Şirket', data.kpis.total_companies],
        ['Toplam İlan', data.kpis.total_announcements],
        ['OCR Parçası', data.kpis.total_ocr_chunks],
        ['Kapsanan İl Sayısı', data.kpis.total_cities],
        ['AI Zenginleştirme Oranı (%)', data.kpis.enrichment_rate],
        [],
        ['--- İL DAĞILIMI (TOP 10) ---'],
        ['Şehir', 'Şirket Sayısı'],
        ...data.cities.map(c => [c.name, c.value]),
        [],
        ['--- İLAN KONULARI VE DAĞILIM ---'],
        ['Konu / Husus', 'Adet'],
        ...data.subjects.map(s => [s.name, s.value]),
        [],
        ['--- EN HAREKETLİ ŞİRKETLER ---'],
        ['Şirket Unvanı', 'Şehir', 'Sicil No', 'İlan Sayısı'],
        ...data.top_companies.map(tc => [tc.unvan, tc.city, tc.sicil_no, tc.announcement_count])
      ];

      const csvContent = "data:text/csv;charset=utf-8,\uFEFF" 
        + csvRows.map(e => e.join(';')).join('\n');
      
      const encodedUri = encodeURI(csvContent);
      const link = document.createElement("a");
      link.setAttribute("href", encodedUri);
      link.setAttribute("download", `Sicilius_Istihbarat_Raporu_${new Date().toISOString().slice(0,10)}.csv`);
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);

      toast({
        title: "CSV İndirildi",
        description: "Rapor verileri başarıyla CSV dosyası olarak dışa aktarıldı.",
      });
    } catch (e) {
      toast({
        title: "Dışa Aktarma Hatası",
        description: "CSV oluşturulurken bir sorun oluştu.",
        variant: "destructive"
      });
    }
  };

  const handlePrint = () => {
    window.print();
  };

  if (loading) {
    return (
      <div className="space-y-6 max-w-7xl mx-auto p-4 md:p-6">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div className="space-y-2">
            <Skeleton className="h-8 w-64" />
            <Skeleton className="h-4 w-96" />
          </div>
          <div className="flex items-center gap-2">
            <Skeleton className="h-9 w-32" />
            <Skeleton className="h-9 w-24" />
          </div>
        </div>
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
          {[...Array(4)].map((_, i) => (
            <Skeleton key={i} className="h-28 rounded-2xl" />
          ))}
        </div>
        <Skeleton className="h-[400px] rounded-2xl w-full" />
      </div>
    );
  }

  const kpis = data?.kpis || {
    total_companies: 0,
    total_announcements: 0,
    total_ocr_chunks: 0,
    total_cities: 0,
    enrichment_rate: 0,
    completed_ocrs: 0,
    pending_ocrs: 0,
    failed_ocrs: 0
  };

  return (
    <div className="space-y-6 max-w-7xl mx-auto p-4 md:p-6 print:p-0">
      
      {/* Top Header Bar */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-2 border-b border-border/40">
        <div>
          <div className="flex items-center gap-2.5">
            <div className="p-2 rounded-xl bg-blue-500/10 text-blue-500">
              <BarChart3 className="h-5 w-5" />
            </div>
            <div>
              <h1 className="text-2xl font-bold tracking-tight text-foreground">
                İş Zekası ve İstihbarat Raporları
              </h1>
              <p className="text-xs text-muted-foreground mt-0.5">
                Türkiye geneli şirket hareketleri, sektörel dinamikler ve veri hattı analitiği
              </p>
            </div>
          </div>
        </div>

        {/* Date Selector & Action Buttons */}
        <div className="flex flex-wrap items-center gap-2 print:hidden">
          {/* Range Pills */}
          <div className="flex bg-muted/60 p-1 rounded-xl border border-border/60 text-xs">
            {[
              { label: '7 Gün', val: 7 },
              { label: '30 Gün', val: 30 },
              { label: '90 Gün', val: 90 },
              { label: 'Tümü', val: 0 },
            ].map((item) => (
              <button
                key={item.val}
                onClick={() => setSelectedDays(item.val)}
                className={`px-3 py-1.5 rounded-lg font-medium transition-all text-xs ${
                  selectedDays === item.val
                    ? 'bg-background text-foreground font-bold shadow-xs'
                    : 'text-muted-foreground hover:text-foreground'
                }`}
              >
                {item.label}
              </button>
            ))}
          </div>

          <Button
            variant="outline"
            size="sm"
            onClick={() => fetchAnalytics(selectedDays)}
            disabled={isRefreshing}
            className="h-9 px-3 rounded-xl border-border hover:bg-muted/50 text-xs gap-1.5"
          >
            <RefreshCcw className={`h-3.5 w-3.5 ${isRefreshing ? 'animate-spin' : ''}`} />
            <span className="hidden sm:inline">Yenile</span>
          </Button>

          <Button
            variant="outline"
            size="sm"
            onClick={handleExportCSV}
            className="h-9 px-3 rounded-xl border-border hover:bg-muted/50 text-xs gap-1.5"
          >
            <Download className="h-3.5 w-3.5 text-emerald-500" />
            <span>Excel / CSV</span>
          </Button>

          <Button
            variant="outline"
            size="sm"
            onClick={handlePrint}
            className="h-9 px-3 rounded-xl border-border hover:bg-muted/50 text-xs gap-1.5"
          >
            <Printer className="h-3.5 w-3.5 text-blue-500" />
            <span>Yazdır</span>
          </Button>
        </div>
      </div>

      {/* 4 Executive KPI Cards */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-3.5">
        
        {/* Card 1: Total Companies */}
        <Card className="border border-border/60 bg-card/60 backdrop-blur-md shadow-xs rounded-2xl p-4 transition-all hover:border-blue-500/30">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-muted-foreground uppercase tracking-wider">Şirket Portföyü</span>
            <div className="p-2 rounded-xl bg-blue-500/10 text-blue-500">
              <Building2 className="h-4 w-4" />
            </div>
          </div>
          <div className="mt-2 flex items-baseline justify-between">
            <h3 className="text-2xl font-black tabular-nums tracking-tight text-foreground">
              {kpis.total_companies.toLocaleString('tr-TR')}
            </h3>
            <Badge variant="outline" className="text-[10px] font-bold bg-blue-500/5 text-blue-600 dark:text-blue-400 border-blue-500/20">
              Tekil Firma
            </Badge>
          </div>
          <p className="text-[11px] text-muted-foreground mt-1.5 flex items-center gap-1">
            <TrendingUp className="h-3 w-3 text-emerald-500" />
            <span>Kayıtlı veri havuzu</span>
          </p>
        </Card>

        {/* Card 2: Total Announcements */}
        <Card className="border border-border/60 bg-card/60 backdrop-blur-md shadow-xs rounded-2xl p-4 transition-all hover:border-purple-500/30">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-muted-foreground uppercase tracking-wider">İşlenen İlan</span>
            <div className="p-2 rounded-xl bg-purple-500/10 text-purple-500">
              <FileText className="h-4 w-4" />
            </div>
          </div>
          <div className="mt-2 flex items-baseline justify-between">
            <h3 className="text-2xl font-black tabular-nums tracking-tight text-foreground">
              {kpis.total_announcements.toLocaleString('tr-TR')}
            </h3>
            <Badge variant="outline" className="text-[10px] font-bold bg-purple-500/5 text-purple-600 dark:text-purple-400 border-purple-500/20">
              Gazete İlanı
            </Badge>
          </div>
          <p className="text-[11px] text-muted-foreground mt-1.5 flex items-center gap-1">
            <span>{kpis.total_ocr_chunks.toLocaleString('tr-TR')} OCR bloğu çıkarıldı</span>
          </p>
        </Card>

        {/* Card 3: Cities Covered */}
        <Card className="border border-border/60 bg-card/60 backdrop-blur-md shadow-xs rounded-2xl p-4 transition-all hover:border-emerald-500/30">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-muted-foreground uppercase tracking-wider">Şehir Kapsamı</span>
            <div className="p-2 rounded-xl bg-emerald-500/10 text-emerald-500">
              <MapPin className="h-4 w-4" />
            </div>
          </div>
          <div className="mt-2 flex items-baseline justify-between">
            <h3 className="text-2xl font-black tabular-nums tracking-tight text-foreground">
              {kpis.total_cities} <span className="text-sm font-semibold text-muted-foreground">İl</span>
            </h3>
            <Badge variant="outline" className="text-[10px] font-bold bg-emerald-500/5 text-emerald-600 dark:text-emerald-400 border-emerald-500/20">
              81 İl Ağı
            </Badge>
          </div>
          <p className="text-[11px] text-muted-foreground mt-1.5 flex items-center gap-1">
            <span>Sicil müdürlükleri entegre</span>
          </p>
        </Card>

        {/* Card 4: AI Enrichment Rate */}
        <Card className="border border-border/60 bg-card/60 backdrop-blur-md shadow-xs rounded-2xl p-4 transition-all hover:border-amber-500/30">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-muted-foreground uppercase tracking-wider">AI Zenginleştirme</span>
            <div className="p-2 rounded-xl bg-amber-500/10 text-amber-500">
              <Zap className="h-4 w-4" />
            </div>
          </div>
          <div className="mt-2 flex items-baseline justify-between">
            <h3 className="text-2xl font-black tabular-nums tracking-tight text-foreground">
              %{kpis.enrichment_rate}
            </h3>
            <Badge variant="outline" className="text-[10px] font-bold bg-amber-500/5 text-amber-600 dark:text-amber-400 border-amber-500/20">
              Llama 3.2 NLP
            </Badge>
          </div>
          <div className="mt-2">
            <Progress value={kpis.enrichment_rate} className="h-1.5 bg-amber-500/20" />
          </div>
        </Card>

      </div>

      {/* Main Tabs Navigation */}
      <Tabs defaultValue="market" value={activeTab} onValueChange={setActiveTab} className="space-y-4">
        
        <TabsList className="bg-muted/60 p-1 rounded-2xl border border-border/60 w-full sm:w-auto grid grid-cols-2 sm:flex gap-1 h-auto print:hidden">
          <TabsTrigger value="market" className="rounded-xl py-2 px-3.5 text-xs font-bold data-[state=active]:bg-background data-[state=active]:shadow-xs flex items-center gap-2">
            <TrendingUp className="h-3.5 w-3.5 text-blue-500" />
            <span>Piyasa & Aktivite Trendleri</span>
          </TabsTrigger>
          
          <TabsTrigger value="geo" className="rounded-xl py-2 px-3.5 text-xs font-bold data-[state=active]:bg-background data-[state=active]:shadow-xs flex items-center gap-2">
            <MapPin className="h-3.5 w-3.5 text-emerald-500" />
            <span>Coğrafi & İl Analitiği</span>
          </TabsTrigger>

          <TabsTrigger value="subjects" className="rounded-xl py-2 px-3.5 text-xs font-bold data-[state=active]:bg-background data-[state=active]:shadow-xs flex items-center gap-2">
            <PieChartIcon className="h-3.5 w-3.5 text-purple-500" />
            <span>İlan Konuları & Dinamikler</span>
          </TabsTrigger>

          <TabsTrigger value="pipeline" className="rounded-xl py-2 px-3.5 text-xs font-bold data-[state=active]:bg-background data-[state=active]:shadow-xs flex items-center gap-2">
            <Activity className="h-3.5 w-3.5 text-amber-500" />
            <span>Pipeline & Veri Sağlığı</span>
          </TabsTrigger>
        </TabsList>

        {/* ================= TAB 1: MARKET & ACTIVITY TRENDS ================= */}
        <TabsContent value="market" className="space-y-4">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
            
            {/* Left 2 Cols: Main Interactive Timeline Chart */}
            <Card className="lg:col-span-2 border border-border/60 bg-card/60 shadow-xs rounded-2xl p-5">
              <CardHeader className="p-0 pb-4 flex flex-row items-center justify-between">
                <div>
                  <CardTitle className="text-base font-bold text-foreground">
                    Zaman Serisi: Yeni Şirketler ve İlan Akışı
                  </CardTitle>
                  <CardDescription className="text-xs text-muted-foreground mt-0.5">
                    {selectedDays === 0 ? 'Tüm zamanlar' : `Son ${selectedDays} günlük`} günlük şirket kayıtları ve ilan hacmi
                  </CardDescription>
                </div>
                <div className="flex items-center gap-3 text-xs font-medium">
                  <div className="flex items-center gap-1.5">
                    <span className="h-2.5 w-2.5 rounded-full bg-blue-500"></span>
                    <span className="text-muted-foreground">Yeni Şirket</span>
                  </div>
                  <div className="flex items-center gap-1.5">
                    <span className="h-2.5 w-2.5 rounded-full bg-emerald-500"></span>
                    <span className="text-muted-foreground">İlan Hacmi</span>
                  </div>
                </div>
              </CardHeader>

              <CardContent className="p-0 pt-2">
                <div className="h-[320px] w-full">
                  <ResponsiveContainer width="100%" height="100%">
                    <AreaChart data={data?.timeline || []} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                      <defs>
                        <linearGradient id="compGrad" x1="0" y1="0" x2="0" y2="1">
                          <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.4}/>
                          <stop offset="95%" stopColor="#3b82f6" stopOpacity={0.0}/>
                        </linearGradient>
                        <linearGradient id="annGrad" x1="0" y1="0" x2="0" y2="1">
                          <stop offset="5%" stopColor="#10b981" stopOpacity={0.4}/>
                          <stop offset="95%" stopColor="#10b981" stopOpacity={0.0}/>
                        </linearGradient>
                      </defs>
                      <CartesianGrid strokeDasharray="3 3" stroke="currentColor" className="text-border/30" />
                      <XAxis 
                        dataKey="label" 
                        stroke="currentColor" 
                        className="text-muted-foreground text-[11px]" 
                        tickLine={false} 
                      />
                      <YAxis 
                        stroke="currentColor" 
                        className="text-muted-foreground text-[11px]" 
                        tickLine={false} 
                      />
                      <Tooltip 
                        contentStyle={{ 
                          backgroundColor: 'rgba(15, 23, 42, 0.95)', 
                          borderColor: 'rgba(255, 255, 255, 0.1)', 
                          borderRadius: '12px',
                          fontSize: '12px',
                          color: '#fff',
                          boxShadow: '0 10px 25px -5px rgba(0, 0, 0, 0.3)'
                        }} 
                      />
                      <Area 
                        type="monotone" 
                        dataKey="companies" 
                        name="Yeni Şirket" 
                        stroke="#3b82f6" 
                        strokeWidth={2.5}
                        fillOpacity={1} 
                        fill="url(#compGrad)" 
                      />
                      <Area 
                        type="monotone" 
                        dataKey="announcements" 
                        name="Yeni İlan" 
                        stroke="#10b981" 
                        strokeWidth={2.5}
                        fillOpacity={1} 
                        fill="url(#annGrad)" 
                      />
                    </AreaChart>
                  </ResponsiveContainer>
                </div>
              </CardContent>
            </Card>

            {/* Right Column: Key Takeaways & Activity Highlights */}
            <Card className="border border-border/60 bg-card/60 shadow-xs rounded-2xl p-5 flex flex-col justify-between">
              <div>
                <CardTitle className="text-base font-bold text-foreground flex items-center gap-2">
                  <Sparkles className="h-4 w-4 text-amber-500" /> B2B Fırsat İçgörüleri
                </CardTitle>
                <CardDescription className="text-xs text-muted-foreground mt-1">
                  Mevcut dönem verilerine dayalı ticari sinyaller
                </CardDescription>

                <div className="mt-4 space-y-3">
                  <div className="p-3 rounded-xl bg-blue-500/5 border border-blue-500/10">
                    <div className="flex items-center justify-between text-xs font-bold text-blue-600 dark:text-blue-400">
                      <span>Günlük Ortalama İlan</span>
                      <span>~{Math.round((kpis.total_announcements / Math.max(1, data?.timeline.length || 1)))} Adet</span>
                    </div>
                    <p className="text-[11px] text-muted-foreground mt-1">
                      Platform üzerinden her gün düzenli olarak yüzlerce yeni ticari sicil ilanı sisteme akmaktadır.
                    </p>
                  </div>

                  <div className="p-3 rounded-xl bg-emerald-500/5 border border-emerald-500/10">
                    <div className="flex items-center justify-between text-xs font-bold text-emerald-600 dark:text-emerald-400">
                      <span>Yeni Lead Üretimi</span>
                      <span>%{kpis.enrichment_rate} Zenginleştirilmiş</span>
                    </div>
                    <p className="text-[11px] text-muted-foreground mt-1">
                      OCR ile taranan şirket ilanları Llama 3.2 AI ile anında yapılandırılmış B2B lead'e dönüştürülüyor.
                    </p>
                  </div>

                  <div className="p-3 rounded-xl bg-purple-500/5 border border-purple-500/10">
                    <div className="flex items-center justify-between text-xs font-bold text-purple-600 dark:text-purple-400">
                      <span>En Yüksek Yoğunluk</span>
                      <span>{data?.cities[0]?.name || 'İSTANBUL'}</span>
                    </div>
                    <p className="text-[11px] text-muted-foreground mt-1">
                      Şirket hareketlerinin ve sermaye artırımlarının en yoğun olduğu merkez bölge.
                    </p>
                  </div>
                </div>
              </div>

              <div className="pt-4 border-t border-border/40 mt-4 flex items-center justify-between text-xs text-muted-foreground">
                <span>Veri Kaynağı: TSG Resmi Gazete</span>
                <span className="font-semibold text-foreground">Canlı Senkron</span>
              </div>
            </Card>

          </div>
        </TabsContent>

        {/* ================= TAB 2: GEOGRAPHICAL ANALYTICS ================= */}
        <TabsContent value="geo" className="space-y-4">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
            
            {/* Left: Top Cities Bar Chart */}
            <Card className="border border-border/60 bg-card/60 shadow-xs rounded-2xl p-5">
              <CardHeader className="p-0 pb-4">
                <CardTitle className="text-base font-bold text-foreground">
                  En Yüksek Şirket Yoğunluğuna Sahip İller (Top 10)
                </CardTitle>
                <CardDescription className="text-xs text-muted-foreground">
                  Sicil müdürlükleri ve şirket merkez adreslerine göre sıralama
                </CardDescription>
              </CardHeader>
              <CardContent className="p-0 pt-2">
                <div className="h-[340px] w-full">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={data?.cities || []} layout="vertical" margin={{ top: 5, right: 20, left: 40, bottom: 5 }}>
                      <CartesianGrid strokeDasharray="3 3" stroke="currentColor" className="text-border/30" />
                      <XAxis type="number" stroke="currentColor" className="text-muted-foreground text-[11px]" tickLine={false} />
                      <YAxis dataKey="name" type="category" stroke="currentColor" className="text-muted-foreground text-[11px] font-bold" tickLine={false} />
                      <Tooltip 
                        formatter={(val: any) => [`${val} Şirket`, 'Hacim']}
                        contentStyle={{ 
                          backgroundColor: 'rgba(15, 23, 42, 0.95)', 
                          borderColor: 'rgba(255, 255, 255, 0.1)', 
                          borderRadius: '12px',
                          fontSize: '12px',
                          color: '#fff'
                        }} 
                      />
                      <Bar dataKey="value" fill="#3b82f6" radius={[0, 8, 8, 0]}>
                        {(data?.cities || []).map((_, index) => (
                          <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                        ))}
                      </Bar>
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </CardContent>
            </Card>

            {/* Right: City Breakdown List with Share */}
            <Card className="border border-border/60 bg-card/60 shadow-xs rounded-2xl p-5">
              <CardHeader className="p-0 pb-3 flex flex-row items-center justify-between">
                <div>
                  <CardTitle className="text-base font-bold text-foreground">
                    Bölgesel Dağılım Tablosu
                  </CardTitle>
                  <CardDescription className="text-xs text-muted-foreground">
                    Toplam şirket havuzundaki pay ve hacim yüzdeleri
                  </CardDescription>
                </div>
                <Badge variant="outline" className="text-xs font-bold bg-muted">
                  {kpis.total_cities} İl Kayıtlı
                </Badge>
              </CardHeader>

              <CardContent className="p-0 pt-2 space-y-3">
                <div className="divide-y divide-border/40 max-h-[330px] overflow-y-auto pr-1">
                  {(data?.cities || []).map((city, idx) => {
                    const percentage = Math.round((city.value / Math.max(1, kpis.total_companies)) * 100);
                    return (
                      <div key={city.name} className="py-2.5 flex items-center justify-between gap-3">
                        <div className="flex items-center gap-2.5 min-w-[120px]">
                          <span className="text-xs font-bold text-muted-foreground w-4">{idx + 1}.</span>
                          <span className="text-xs font-bold text-foreground">{city.name}</span>
                        </div>
                        
                        <div className="flex-1 max-w-[160px] hidden sm:block">
                          <Progress value={percentage} className="h-1.5" />
                        </div>

                        <div className="text-right flex items-center gap-2">
                          <span className="text-xs font-bold tabular-nums text-foreground">
                            {city.value.toLocaleString('tr-TR')}
                          </span>
                          <Badge variant="secondary" className="text-[10px] font-bold py-0.5 px-1.5">
                            %{percentage}
                          </Badge>
                        </div>
                      </div>
                    );
                  })}
                </div>
              </CardContent>
            </Card>

          </div>
        </TabsContent>

        {/* ================= TAB 3: SUBJECTS & ACTIVE COMPANIES ================= */}
        <TabsContent value="subjects" className="space-y-4">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
            
            {/* Left: Announcement Topics Pie Chart */}
            <Card className="border border-border/60 bg-card/60 shadow-xs rounded-2xl p-5">
              <CardHeader className="p-0 pb-2">
                <CardTitle className="text-base font-bold text-foreground">
                  Ticari İlan Konuları & Hususlar
                </CardTitle>
                <CardDescription className="text-xs text-muted-foreground">
                  Kuruluş, Sermaye Artırımı, Temsil & İlzam, Adres Değişikliği vb.
                </CardDescription>
              </CardHeader>
              <CardContent className="p-0 pt-2">
                <div className="h-[320px] w-full">
                  <ResponsiveContainer width="100%" height="100%">
                    <PieChart>
                      <Pie
                        data={data?.subjects || []}
                        cx="50%"
                        cy="50%"
                        innerRadius={65}
                        outerRadius={100}
                        paddingAngle={3}
                        dataKey="value"
                      >
                        {(data?.subjects || []).map((_, index) => (
                          <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                        ))}
                      </Pie>
                      <Tooltip 
                        formatter={(val: any) => [`${val} İlan`, 'Adet']}
                        contentStyle={{ 
                          backgroundColor: 'rgba(15, 23, 42, 0.95)', 
                          borderColor: 'rgba(255, 255, 255, 0.1)', 
                          borderRadius: '12px',
                          fontSize: '12px',
                          color: '#fff'
                        }} 
                      />
                      <Legend 
                        layout="horizontal" 
                        verticalAlign="bottom" 
                        align="center"
                        wrapperStyle={{ fontSize: '11px', paddingTop: '10px' }} 
                      />
                    </PieChart>
                  </ResponsiveContainer>
                </div>
              </CardContent>
            </Card>

            {/* Right: Top Active Companies Table */}
            <Card className="border border-border/60 bg-card/60 shadow-xs rounded-2xl p-5">
              <CardHeader className="p-0 pb-3 flex flex-row items-center justify-between">
                <div>
                  <CardTitle className="text-base font-bold text-foreground">
                    En Çok Hareket Gören Şirketler
                  </CardTitle>
                  <CardDescription className="text-xs text-muted-foreground">
                    Son dönemde en fazla resmi sicil ilanı yayımlanan şirketler
                  </CardDescription>
                </div>
                <Badge variant="outline" className="text-xs font-bold bg-muted text-purple-600 dark:text-purple-400">
                  Sıcak Lead
                </Badge>
              </CardHeader>

              <CardContent className="p-0 pt-2">
                <div className="divide-y divide-border/40">
                  {(data?.top_companies || []).map((comp, i) => (
                    <div key={comp.id} className="py-3 flex items-center justify-between gap-3 hover:bg-muted/30 px-2 rounded-xl transition-all">
                      <div className="space-y-0.5 max-w-[280px]">
                        <div className="text-xs font-bold text-foreground truncate" title={comp.unvan}>
                          {comp.unvan}
                        </div>
                        <div className="text-[11px] text-muted-foreground flex items-center gap-2">
                          <span>{comp.city}</span>
                          <span>•</span>
                          <span>Sicil No: {comp.sicil_no}</span>
                        </div>
                      </div>

                      <div className="text-right">
                        <Badge className="bg-purple-500/10 text-purple-600 dark:text-purple-400 border border-purple-500/20 text-xs font-bold">
                          {comp.announcement_count} İlan
                        </Badge>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

          </div>
        </TabsContent>

        {/* ================= TAB 4: PIPELINE & DATA HEALTH ================= */}
        <TabsContent value="pipeline" className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            
            {/* Metric 1: Completed OCRs */}
            <Card className="border border-emerald-500/20 bg-emerald-500/5 shadow-xs rounded-2xl p-4">
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold text-emerald-600 dark:text-emerald-400 uppercase tracking-wider">Tamamlanan OCR</span>
                <CheckCircle2 className="h-4 w-4 text-emerald-500" />
              </div>
              <h3 className="text-2xl font-black tabular-nums mt-2 text-foreground">
                {kpis.completed_ocrs.toLocaleString('tr-TR')}
              </h3>
              <p className="text-[11px] text-muted-foreground mt-1">
                Yapay zeka ile tam yapılandırılmış veri
              </p>
            </Card>

            {/* Metric 2: Pending LLM */}
            <Card className="border border-amber-500/20 bg-amber-500/5 shadow-xs rounded-2xl p-4">
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold text-amber-600 dark:text-amber-400 uppercase tracking-wider">AI Bekleyen Kuyruk</span>
                <Clock className="h-4 w-4 text-amber-500" />
              </div>
              <h3 className="text-2xl font-black tabular-nums mt-2 text-foreground">
                {kpis.pending_ocrs.toLocaleString('tr-TR')}
              </h3>
              <p className="text-[11px] text-muted-foreground mt-1">
                Llama 3.2 zenginleştirme kuyruğunda
              </p>
            </Card>

            {/* Metric 3: Failed Items */}
            <Card className="border border-rose-500/20 bg-rose-500/5 shadow-xs rounded-2xl p-4">
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold text-rose-600 dark:text-rose-400 uppercase tracking-wider">Hatalı / Denenecek</span>
                <AlertTriangle className="h-4 w-4 text-rose-500" />
              </div>
              <h3 className="text-2xl font-black tabular-nums mt-2 text-foreground">
                {kpis.failed_ocrs.toLocaleString('tr-TR')}
              </h3>
              <p className="text-[11px] text-muted-foreground mt-1">
                Format uyuşmazlığı veya OCR hata kaydı
              </p>
            </Card>

          </div>

          {/* Full Pipeline Flow Diagram Card */}
          <Card className="border border-border/60 bg-card/60 shadow-xs rounded-2xl p-5">
            <CardHeader className="p-0 pb-4">
              <CardTitle className="text-base font-bold text-foreground">
                Veri İşleme Hattı (Pipeline Architecture)
              </CardTitle>
              <CardDescription className="text-xs text-muted-foreground">
                Ticaret Sicil Gazetesi scraping aşamasından B2B CRM zenginleştirmesine kadar uçtan uca akış
              </CardDescription>
            </CardHeader>

            <CardContent className="p-0 pt-2">
              <div className="grid grid-cols-1 md:grid-cols-4 gap-3 text-center">
                
                <div className="p-3.5 rounded-xl bg-background border border-border/60 space-y-1">
                  <div className="text-[10px] font-bold uppercase text-muted-foreground">1. Portal Scraping</div>
                  <div className="text-sm font-bold text-foreground">Playwright + TSG</div>
                  <div className="text-[11px] text-muted-foreground">Gazete PDF İndirme</div>
                </div>

                <div className="p-3.5 rounded-xl bg-background border border-border/60 space-y-1">
                  <div className="text-[10px] font-bold uppercase text-muted-foreground">2. Vision & Chunking</div>
                  <div className="text-sm font-bold text-blue-500">Guardian OCR</div>
                  <div className="text-[11px] text-muted-foreground">Sayfa Başı ~3-5 İlan</div>
                </div>

                <div className="p-3.5 rounded-xl bg-background border border-border/60 space-y-1">
                  <div className="text-[10px] font-bold uppercase text-muted-foreground">3. NLP Enrichment</div>
                  <div className="text-sm font-bold text-amber-500">Llama 3.2 (3B)</div>
                  <div className="text-[11px] text-muted-foreground">JSON Structured Output</div>
                </div>

                <div className="p-3.5 rounded-xl bg-background border border-border/60 space-y-1">
                  <div className="text-[10px] font-bold uppercase text-muted-foreground">4. Coğrafi & Graph DB</div>
                  <div className="text-sm font-bold text-emerald-500">PostGIS + CRM</div>
                  <div className="text-[11px] text-muted-foreground">Saha Satışı & Lead</div>
                </div>

              </div>
            </CardContent>
          </Card>
        </TabsContent>

      </Tabs>

    </div>
  );
}
