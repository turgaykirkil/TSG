'use client';

import { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Activity, 
  Cpu, 
  Database, 
  Play, 
  Square, 
  RefreshCcw, 
  CheckCircle2, 
  AlertCircle, 
  Terminal,
  Zap,
  Globe,
  Loader2,
  ListOrdered,
  Layers,
  Trash2,
  ArrowDown,
  Sparkles,
  Filter,
  Sun,
  Moon
} from 'lucide-react';
import axios from '@/lib/axios';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Progress } from '@/components/ui/progress';
import { 
  Select, 
  SelectContent, 
  SelectItem, 
  SelectTrigger, 
  SelectValue 
} from '@/components/ui/select';
import { useToast } from '@/components/ui/use-toast';

import { Switch } from '@/components/ui/switch';
import { Label } from '@/components/ui/label';

interface Stats {
  total_announcements: number;
  scraped_pdfs: number;
  pending_llm: number;
  completed_ocr: number;
  failed_llm: number;
  success_rate: number;
}

export default function OperationsPage() {
  const { toast } = useToast();
  const [stats, setStats] = useState<Stats | null>(null);
  const [logs, setLogs] = useState<string[]>([]);
  const [isEnriching, setIsEnriching] = useState(false);
  const [isScraping, setIsScraping] = useState(false);
  const [isLive, setIsLive] = useState(true);
  const [batchLimit, setBatchLimit] = useState(20);
  const [scrapeCount, setScrapeCount] = useState(10);
  const [city, setCity] = useState('İSTANBUL');
  const [strategy, setStrategy] = useState<'gap_fill' | 'sequential'>('gap_fill');
  const [startFrom, setStartFrom] = useState<string>('');
  const [isFreshStart, setIsFreshStart] = useState(false);
  const [logTab, setLogTab] = useState<'all' | 'scraping' | 'ai'>('all');
  
  const scrollRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom when logs change
  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [logs]);

  const fetchStatus = async () => {
    try {
      const response = await axios.get('/api/v1/operations/status');
      setStats(response.data.stats);
      setLogs(response.data.logs);
      setIsScraping(response.data.is_scraping_active);
      setIsEnriching(response.data.is_enrichment_active);
    } catch (error) {
      console.error('Failed to fetch status:', error);
    }
  };

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [logs]);

  useEffect(() => {
    fetchStatus();
    if (!isLive) return;

    // Smart Interval: Use 3s if something is running, 10s if idle
    const intervalTime = (isScraping || isEnriching) ? 3000 : 10000;
    
    const interval = setInterval(fetchStatus, intervalTime);
    return () => clearInterval(interval);
  }, [isLive, isScraping, isEnriching]);

  const handleStartScrape = async () => {
    try {
      setIsScraping(true);
      
      let effectiveStart = startFrom ? parseInt(startFrom) : undefined;
      // If "Sıfırdan Başla" is active and no startFrom is given, we set default min
      if (isFreshStart && !effectiveStart) {
        effectiveStart = city === 'İSTANBUL' ? 100000 : 1;
      }

      await axios.post('/api/v1/scraping/start', {
        count: scrapeCount,
        mode: 'city_fill',
        city: city,
        strategy: strategy,
        start_from: effectiveStart
      });
      toast({
        title: "Kazıma Başlatıldı",
        description: `${city} için ${scrapeCount} ilan ${strategy === 'gap_fill' ? 'boşlukları doldurarak' : 'sırayla'} kazınmaya başlandı.`,
      });
      fetchStatus();
    } catch (error) {
      toast({
        title: "Hata",
        description: "Kazıma işlemi başlatılamadı.",
        variant: "destructive"
      });
    }
  };

  const handleStopScrape = async () => {
    try {
      await axios.post('/api/v1/scraping/stop');
      toast({
        title: "Kazıma Durduruldu",
        description: "Kazıma işlemine durdurma sinyali gönderildi.",
      });
      fetchStatus();
    } catch (error) {
      toast({
        title: "Hata",
        description: "Kazıma işlemi durdurulamadı.",
        variant: "destructive"
      });
    }
  };

  const handleTriggerEnrichment = async () => {
    try {
      setIsEnriching(true);
      await axios.post('/api/v1/operations/enrich', null, { params: { limit: batchLimit } });
      toast({
        title: "AI Zenginleştirme Başlatıldı",
        description: `${batchLimit} adet ilan Llama 3 tarafından işleniyor.`,
      });
      fetchStatus();
    } catch (error) {
      toast({
        title: "Hata",
        description: "AI işlemi başlatılamadı.",
        variant: "destructive"
      });
    }
  };

  const handleStopEnrichment = async () => {
    try {
      await axios.post('/api/v1/operations/enrich/stop');
      toast({
        title: "AI Zenginleştirme Durduruldu",
        description: "Yapay zeka analizine durdurma sinyali gönderildi.",
      });
      fetchStatus();
    } catch (error) {
      toast({
        title: "Hata",
        description: "AI analizi durdurulamadı.",
        variant: "destructive"
      });
    }
  };

  const [isDark, setIsDark] = useState(true);

  const toggleThemeMode = () => {
    const nextDark = !isDark;
    setIsDark(nextDark);
    const root = document.documentElement;
    if (nextDark) {
      root.classList.add('dark');
      root.classList.remove('light');
    } else {
      root.classList.remove('dark');
      root.classList.add('light');
    }
  };

  return (
    <div className="flex-1 space-y-4 container mx-auto pb-8 pt-2 max-w-7xl">
      {/* Compact Header Bar */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 bg-card border border-border p-4 rounded-2xl shadow-sm">
        <div>
          <div className="flex items-center gap-2.5">
            <h1 className="text-xl font-extrabold tracking-tight text-foreground flex items-center gap-2">
              <Activity className="h-5 w-5 text-emerald-500" /> Operasyon Merkezi
            </h1>
            <Badge variant="outline" className="text-[10px] px-2 py-0.5 bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border-emerald-500/30">
              Sicilius v2.0
            </Badge>
            <Badge variant="outline" className="text-[10px] px-2 py-0.5 bg-amber-500/10 text-amber-600 dark:text-amber-400 border-amber-500/30">
              Llama 3.2:3b
            </Badge>
          </div>
          <p className="text-xs text-muted-foreground mt-0.5">
            Gazete kazıma, Vision OCR ve Ollama yerel yapay zeka zenginleştirme akışı.
          </p>
        </div>

        <div className="flex items-center gap-2.5">
           {/* Gündüz / Gece Modu Butonu */}
           <Button
             variant="outline"
             size="sm"
             onClick={toggleThemeMode}
             className="h-8 px-2.5 text-xs rounded-xl border-border hover:bg-muted"
             title={isDark ? 'Gündüz Moduna Geç' : 'Gece Moduna Geç'}
           >
             {isDark ? (
               <Sun className="h-4 w-4 text-amber-400 mr-1.5" />
             ) : (
               <Moon className="h-4 w-4 text-slate-700 mr-1.5" />
             )}
             <span className="font-medium text-xs">{isDark ? 'Gündüz' : 'Gece'}</span>
           </Button>

           {/* Canlı Akış Toggle */}
           <div className="flex items-center space-x-2 bg-muted/50 px-3 py-1 rounded-xl border border-border">
             <Switch 
               id="live-mode" 
               checked={isLive} 
               onCheckedChange={setIsLive}
               className="data-[state=checked]:bg-emerald-500 scale-90"
             />
             <Label htmlFor="live-mode" className="text-[11px] font-bold cursor-pointer uppercase text-muted-foreground select-none">
                {isLive ? 'Canlı' : 'Durduruldu'}
             </Label>
           </div>

           <Button
             variant="ghost"
             size="sm"
             onClick={fetchStatus}
             className="h-8 px-2 text-xs text-muted-foreground hover:text-foreground rounded-xl"
           >
             <RefreshCcw className="h-3.5 w-3.5" />
           </Button>
        </div>
      </div>

      {/* KPI Stats Overview Cards (Compact Height) */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-3">
        {[
          { 
            label: 'Toplam İlan', 
            val: stats?.total_announcements || 0, 
            icon: Database, 
            color: 'text-blue-500 bg-blue-500/10'
          },
          { 
            label: 'Taranan PDF', 
            val: stats?.scraped_pdfs || 0, 
            icon: Globe, 
            color: 'text-purple-500 bg-purple-500/10'
          },
          { 
            label: 'AI Bekleyen', 
            val: stats?.pending_llm || 0, 
            icon: Zap, 
            color: 'text-amber-500 bg-amber-500/10'
          },
          { 
            label: 'Başarı Oranı', 
            val: `${stats?.success_rate || 0}%`, 
            icon: CheckCircle2, 
            color: 'text-emerald-500 bg-emerald-500/10'
          },
        ].map((item, i) => (
          <Card key={item.label} className="border border-border bg-card shadow-sm rounded-xl p-3">
            <div className="flex items-center justify-between">
              <span className="text-[11px] font-bold text-muted-foreground uppercase tracking-wider">{item.label}</span>
              <div className={`p-1.5 rounded-lg ${item.color}`}>
                <item.icon className="h-3.5 w-3.5" />
              </div>
            </div>
            <h3 className="text-xl font-bold mt-1 tabular-nums text-foreground">{item.val}</h3>
          </Card>
        ))}
      </div>

      {/* Workstation Grid Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 items-start">
        
        {/* Left Column: Control Center Panels */}
        <div className="lg:col-span-1 space-y-4">
          
          {/* Card 1: Web Scraper Engine */}
          <Card className="border border-border bg-card shadow-sm rounded-2xl overflow-hidden">
            <CardHeader className="py-3 px-4 border-b border-border bg-muted/30">
              <CardTitle className="text-sm font-bold flex items-center justify-between">
                <span className="flex items-center gap-2">
                  <Globe className="h-4 w-4 text-emerald-500" /> Web Scraper Engine
                </span>
                {isScraping && <Loader2 className="h-3.5 w-3.5 animate-spin text-emerald-500" />}
              </CardTitle>
            </CardHeader>
            <CardContent className="p-4 space-y-3">
              <div className="grid grid-cols-2 gap-2">
                <div className="grid gap-1">
                  <label className="text-[11px] font-bold uppercase text-muted-foreground">Şehir</label>
                  <Input 
                    value={city} 
                    onChange={(e) => setCity(e.target.value)}
                    className="h-8 text-xs bg-background border-border"
                  />
                </div>
                <div className="grid gap-1">
                  <label className="text-[11px] font-bold uppercase text-muted-foreground">Hedef Sayı</label>
                  <Input 
                    type="number" 
                    value={scrapeCount} 
                    onChange={(e) => setScrapeCount(Number(e.target.value))}
                    className="h-8 text-xs bg-background border-border"
                  />
                </div>
              </div>

              <div className="grid gap-1">
                <label className="text-[11px] font-bold uppercase text-muted-foreground">Strateji</label>
                <Select value={strategy} onValueChange={(v: any) => setStrategy(v)}>
                  <SelectTrigger className="h-8 text-xs bg-background border-border">
                    <SelectValue placeholder="Strateji" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="gap_fill">
                      <div className="flex items-center gap-1.5 text-xs">
                        <Layers className="h-3.5 w-3.5 text-blue-500" />
                        <span>Boşlukları Doldur (Hızlı)</span>
                      </div>
                    </SelectItem>
                    <SelectItem value="sequential">
                      <div className="flex items-center gap-1.5 text-xs">
                        <ListOrdered className="h-3.5 w-3.5 text-emerald-500" />
                        <span>Sıralı İlerle (Kapsamlı)</span>
                      </div>
                    </SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="grid gap-1">
                <div className="flex items-center justify-between">
                  <label className="text-[11px] font-bold uppercase text-muted-foreground">Başlangıç No</label>
                  <div className="flex items-center space-x-1.5">
                     <Switch 
                       id="fresh-start" 
                       checked={isFreshStart} 
                       onCheckedChange={setIsFreshStart}
                       className="scale-75"
                     />
                     <Label htmlFor="fresh-start" className="text-[10px] font-bold uppercase text-muted-foreground cursor-pointer">Sıfırdan</Label>
                  </div>
                </div>
                <Input 
                  type="number" 
                  placeholder="Otomatik"
                  value={startFrom} 
                  onChange={(e) => setStartFrom(e.target.value)}
                  className="h-8 text-xs bg-background border-border placeholder:text-muted-foreground/50"
                />
              </div>

              {isScraping ? (
                <Button 
                  onClick={handleStopScrape}
                  size="sm"
                  className="w-full bg-rose-600 hover:bg-rose-700 text-white font-bold text-xs h-9 rounded-xl shadow-sm flex items-center justify-center gap-2"
                >
                  <Square className="h-3.5 w-3.5 fill-current" />
                  <span>Kazımayı Durdur</span>
                </Button>
              ) : (
                <Button 
                  onClick={handleStartScrape} 
                  size="sm"
                  className="w-full bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs h-9 rounded-xl shadow-sm flex items-center justify-center gap-2"
                >
                  <Play className="h-3.5 w-3.5 fill-current" />
                  <span>Kazımayı Başlat</span>
                </Button>
              )}
            </CardContent>
          </Card>

          {/* Card 2: AI Enrichment Engine */}
          <Card className="border border-amber-500/30 bg-card shadow-sm rounded-2xl overflow-hidden">
            <CardHeader className="py-3 px-4 border-b border-amber-500/20 bg-amber-500/5">
              <CardTitle className="text-sm font-bold text-amber-600 dark:text-amber-400 flex items-center justify-between">
                <span className="flex items-center gap-2">
                  <Sparkles className="h-4 w-4" /> Llama 3 AI Enrichment
                </span>
                {isEnriching && <Loader2 className="h-3.5 w-3.5 animate-spin text-amber-500" />}
              </CardTitle>
            </CardHeader>
            <CardContent className="p-4 space-y-3">
              <div className="grid gap-1">
                <label className="text-[11px] font-bold uppercase text-muted-foreground">Batch Boyutu (Kayıt Sayısı)</label>
                <Input 
                  type="number" 
                  value={batchLimit} 
                  onChange={(e) => setBatchLimit(Number(e.target.value))}
                  className="h-8 text-xs bg-background border-border font-bold text-foreground"
                />
              </div>

              {isEnriching ? (
                <Button 
                  onClick={handleStopEnrichment}
                  size="sm"
                  className="w-full bg-rose-600 hover:bg-rose-700 text-white font-bold text-xs h-9 rounded-xl shadow-sm flex items-center justify-center gap-2"
                >
                  <Square className="h-3.5 w-3.5 fill-current" />
                  <span>Yapay Zeka Analizini Durdur</span>
                </Button>
              ) : (
                <Button 
                  onClick={handleTriggerEnrichment}
                  size="sm"
                  className="w-full bg-amber-500 hover:bg-amber-600 text-zinc-950 font-extrabold text-xs h-9 rounded-xl shadow-sm flex items-center justify-center gap-2"
                >
                  <Play className="h-3.5 w-3.5 fill-current" />
                  <span>Yapay Zeka Analizini Başlat</span>
                </Button>
              )}
            </CardContent>
          </Card>

        </div>

        {/* Right Column: Ergonomic Activity Console (Height 520px) */}
        <Card className="lg:col-span-2 border border-border bg-card text-card-foreground shadow-sm overflow-hidden flex flex-col h-[520px] rounded-2xl">
          
          {/* Header Bar */}
          <div className="bg-muted/40 border-b border-border flex flex-wrap items-center justify-between py-2.5 px-4 shrink-0 gap-2">
             <div className="flex items-center gap-2">
                <Terminal className="h-4 w-4 text-emerald-500" />
                <span className="font-bold uppercase tracking-wider text-xs font-sans">Activity Stream</span>
                
                {/* Tab Switcher */}
                <div className="flex bg-background p-0.5 rounded-lg border border-border text-xs ml-1">
                  <button
                    onClick={() => setLogTab('all')}
                    className={`px-2.5 py-1 rounded-md transition-all font-sans text-[11px] ${
                      logTab === 'all' 
                        ? 'bg-muted text-foreground font-bold shadow-sm' 
                        : 'text-muted-foreground hover:text-foreground'
                    }`}
                  >
                    Tüm Akış
                  </button>
                  <button
                    onClick={() => setLogTab('scraping')}
                    className={`px-2.5 py-1 rounded-md transition-all font-sans text-[11px] flex items-center gap-1 ${
                      logTab === 'scraping' 
                        ? 'bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 font-bold border border-emerald-500/20' 
                        : 'text-muted-foreground hover:text-foreground'
                    }`}
                  >
                    <Globe className="h-3 w-3" />
                    <span>Kazıma</span>
                  </button>
                  <button
                    onClick={() => setLogTab('ai')}
                    className={`px-2.5 py-1 rounded-md transition-all font-sans text-[11px] flex items-center gap-1 ${
                      logTab === 'ai' 
                        ? 'bg-amber-500/10 text-amber-600 dark:text-amber-400 font-bold border border-amber-500/20' 
                        : 'text-muted-foreground hover:text-foreground'
                    }`}
                  >
                    <Sparkles className="h-3 w-3" />
                    <span>Llama 3 AI</span>
                  </button>
                </div>
             </div>

             <Button 
               variant="ghost" 
               size="sm" 
               onClick={() => setLogs([])}
               className="h-7 px-2 text-[11px] text-muted-foreground hover:text-rose-500"
               title="Temizle"
             >
               <Trash2 className="h-3 w-3 mr-1" /> Temizle
             </Button>
          </div>

          {/* Console Viewport */}
          <CardContent className="p-0 flex-1 overflow-hidden flex flex-col min-h-0 bg-slate-950 dark:bg-zinc-950 text-slate-200 font-mono text-xs">
            <div 
              ref={scrollRef}
              className="flex-1 w-full p-4 overflow-y-auto scrollbar-thin scrollbar-thumb-zinc-800 scrollbar-track-transparent space-y-2"
            >
              {(() => {
                const filteredLogs = logs.filter(log => {
                  if (logTab === 'scraping') {
                    return !log.includes('[AI Enrichment]') && !log.includes('Llama') && !log.includes('NEYDİ') && !log.includes('NE OLDU');
                  }
                  if (logTab === 'ai') {
                    return log.includes('[AI Enrichment]') || log.includes('Llama') || log.includes('zenginleştirildi') || log.includes('NEYDİ') || log.includes('NE OLDU') || log.includes('🔴') || log.includes('🟢');
                  }
                  return true;
                });

                if (filteredLogs.length === 0) {
                  return (
                    <div className="h-full flex flex-col items-center justify-center text-zinc-500 space-y-2 py-16">
                      <Terminal className="h-7 w-7 opacity-40" />
                      <p className="text-xs font-sans italic text-zinc-500">
                        {logTab === 'ai' ? 'Llama 3 AI bekleniyor...' : logTab === 'scraping' ? 'Kazıma akışı bekleniyor...' : 'Sistem olayları dinleniyor...'}
                      </p>
                    </div>
                  );
                }

                return filteredLogs.map((log, i) => {
                  const timestamp = new Date().toLocaleTimeString();

                  // 🔴 NEYDİ Card
                  if (log.includes('🔴') || log.includes('NEYDİ')) {
                    return (
                      <div 
                        key={i}
                        className="p-2.5 rounded-lg bg-rose-950/40 border border-rose-900/50 text-[11px] leading-relaxed"
                      >
                        <div className="flex items-center justify-between mb-1">
                          <span className="px-1.5 py-0.5 rounded bg-rose-500/20 text-rose-300 font-bold text-[10px]">
                            🔴 ÖNCEKİ DURUM (HAM REGEX)
                          </span>
                          <span className="text-zinc-500 tabular-nums">[{timestamp}]</span>
                        </div>
                        <p className="text-rose-200/90 font-mono">
                          {log.replace(/^.*\[AI Enrichment NEYDİ \d+\/\d+\]\s*/, '')}
                        </p>
                      </div>
                    );
                  }

                  // 🟢 NE OLDU Card
                  if (log.includes('🟢') || log.includes('NE OLDU')) {
                    return (
                      <div 
                        key={i}
                        className="p-3 rounded-lg bg-emerald-950/50 border border-emerald-500/40 text-[11px] leading-relaxed shadow-sm"
                      >
                        <div className="flex items-center justify-between mb-1">
                          <span className="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-bold text-[10px] flex items-center gap-1">
                            <Sparkles className="h-3 w-3 text-emerald-400" />
                            🟢 AI SONRASI (LLAMA 3.2 ZENGİNLEŞTİRİLDİ)
                          </span>
                          <span className="text-zinc-500 tabular-nums">[{timestamp}]</span>
                        </div>
                        <div className="text-emerald-200 font-mono font-medium">
                          {log.replace(/^.*\[AI Enrichment NE OLDU \d+\/\d+\]\s*/, '')}
                        </div>
                      </div>
                    );
                  }

                  // Standard Line
                  return (
                    <div key={i} className="flex items-start gap-2.5 text-[11px] py-0.5 px-1 rounded hover:bg-zinc-900/50 transition-colors">
                      <span className="text-zinc-500 shrink-0 tabular-nums select-none">[{timestamp}]</span>
                      <span className={
                        log.includes('ERROR') || log.includes('❌') ? 'text-rose-400 font-medium' :
                        log.includes('[AI Enrichment]') || log.includes('✨') ? 'text-amber-300 font-medium' :
                        log.includes('OCR_SUCCESS') || log.includes('✅') ? 'text-emerald-400 font-medium' :
                        log.includes('OCR_START') ? 'text-sky-400' :
                        log.includes('DUPLICATE_SKIP') ? 'text-amber-400/70 italic' :
                        'text-zinc-300'
                      }>
                        {log}
                      </span>
                    </div>
                  );
                });
              })()}
            </div>
          </CardContent>

          {/* Footer Bar */}
          <div className="px-4 py-2 bg-muted/40 border-t border-border text-[10px] uppercase text-muted-foreground flex items-center justify-between shrink-0 font-sans">
             <div className="flex items-center gap-2">
                <span>Ollama Llama 3.2:3b</span>
                <span>•</span>
                <span>Apple Vision OCR</span>
             </div>
             <span className="flex items-center gap-1 text-emerald-500 font-bold">
                <div className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></div>
                Live Bağlandı
             </span>
          </div>
        </Card>
      </div>
    </div>
  );
}
