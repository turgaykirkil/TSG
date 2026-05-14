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
  Layers
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
    } finally {
      // isScraping will be updated by polling
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
    } finally {
      setIsEnriching(false);
    }
  };

  return (
    <div className="flex-1 space-y-6 container mx-auto pb-12">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-extrabold tracking-tight text-foreground flex items-center gap-3">
             <Activity className="h-8 w-8 text-primary" /> Operasyon Merkezi
          </h1>
          <p className="text-muted-foreground mt-1 text-lg">
            Sistem kazıma ve OCR süreçlerini gerçek zamanlı yönetin.
          </p>
        </div>
        <div className="flex items-center gap-6">
           <div className="flex items-center space-x-2 bg-card/40 px-3 py-2 rounded-full border border-border shadow-sm">
             <Switch 
               id="live-mode" 
               checked={isLive} 
               onCheckedChange={setIsLive}
               className="data-[state=checked]:bg-emerald-500"
             />
             <Label htmlFor="live-mode" className="text-xs font-bold cursor-pointer uppercase tracking-tighter">
                {isLive ? 'Canlı İzleme Açık' : 'İzleme Durduruldu'}
             </Label>
           </div>
           <div className="hidden md:flex gap-2">
             <Badge variant="outline" className="px-3 py-1 bg-primary/5 text-primary border-primary/20">
               Llama 3 Active
             </Badge>
             <Badge variant="outline" className="px-3 py-1 bg-emerald-500/5 text-emerald-500 border-emerald-500/20">
               Vision OCR Online
             </Badge>
           </div>
        </div>
      </div>

      {/* Stats Overview */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {[
          { 
            label: 'Toplam Veri', 
            val: stats?.total_announcements || 0, 
            icon: Database, 
            color: 'text-blue-500', 
            bg: 'bg-blue-500/10' 
          },
          { 
            label: 'Taranan PDF', 
            val: stats?.scraped_pdfs || 0, 
            icon: Globe, 
            color: 'text-purple-500', 
            bg: 'bg-purple-500/10' 
          },
          { 
            label: 'AI Bekleyen', 
            val: stats?.pending_llm || 0, 
            icon: Zap, 
            color: 'text-amber-500', 
            bg: 'bg-amber-500/10' 
          },
          { 
            label: 'Başarı Oranı', 
            val: `${stats?.success_rate || 0}%`, 
            icon: CheckCircle2, 
            color: 'text-emerald-500', 
            bg: 'bg-emerald-500/10' 
          },
        ].map((item, i) => (
          <motion.div
            key={item.label}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.1 }}
          >
            <Card className="border-none shadow-sm bg-card/50 backdrop-blur-sm overflow-hidden relative">
              <div className={`absolute top-0 right-0 p-3 opacity-20 ${item.color}`}>
                <item.icon className="h-12 w-12" />
              </div>
              <CardContent className="pt-6">
                <p className="text-sm font-medium text-muted-foreground uppercase tracking-wider">{item.label}</p>
                <h3 className="text-3xl font-bold mt-1 tabular-nums">{item.val}</h3>
                <div className="mt-2 text-xs flex items-center gap-1 text-muted-foreground">
                  <span className={`${item.color} font-bold`}>•</span> Sistem Durumu: Normal
                </div>
              </CardContent>
            </Card>
          </motion.div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 items-start">
        {/* Controls Panel */}
        <Card className="lg:col-span-1 border-none bg-card/50 shadow-sm overflow-hidden">
          <CardHeader className="bg-primary/5 border-b border-primary/10">
            <CardTitle className="text-xl flex items-center gap-2">
              <RefreshCcw className="h-5 w-5" /> Kontrol Paneli
            </CardTitle>
            <CardDescription>
              İşlemleri manuel tetikleyin.
            </CardDescription>
          </CardHeader>
          <CardContent className="pt-6 space-y-8">
            {/* Scraping Section */}
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <h4 className="font-semibold text-primary flex items-center gap-2 italic">
                  <Globe className="h-4 w-4" /> Web Scraper
                </h4>
                {isScraping && <Loader2 className="h-4 w-4 animate-spin text-primary" />}
              </div>
              <div className="grid gap-2">
                <label className="text-xs uppercase text-muted-foreground font-bold">Şehir</label>
                <Input 
                  value={city} 
                  onChange={(e) => setCity(e.target.value)}
                  className="bg-background/20"
                />
              </div>
              <div className="grid gap-2">
                <label className="text-xs uppercase text-muted-foreground font-bold">Hedef İlan Sayısı</label>
                <Input 
                  type="number" 
                  value={scrapeCount} 
                  onChange={(e) => setScrapeCount(Number(e.target.value))}
                  className="bg-background/20"
                />
              </div>

              <div className="pt-2 space-y-4">
                <div className="grid gap-2">
                  <label className="text-xs uppercase text-muted-foreground font-bold">Strateji</label>
                  <Select value={strategy} onValueChange={(v: any) => setStrategy(v)}>
                    <SelectTrigger className="bg-background/20">
                      <SelectValue placeholder="Strateji seçin" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="gap_fill">
                        <div className="flex items-center gap-2">
                          <Layers className="h-4 w-4 text-blue-500" />
                          <span>Boşlukları Doldur (Hızlı)</span>
                        </div>
                      </SelectItem>
                      <SelectItem value="sequential">
                        <div className="flex items-center gap-2">
                          <ListOrdered className="h-4 w-4 text-emerald-500" />
                          <span>Sıralı İlerle (Kapsamlı)</span>
                        </div>
                      </SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                <div className="grid gap-2">
                  <div className="flex items-center justify-between">
                    <label className="text-xs uppercase text-muted-foreground font-bold">Başlangıç No</label>
                    <div className="flex items-center space-x-2">
                       <Switch 
                         id="fresh-start" 
                         checked={isFreshStart} 
                         onCheckedChange={setIsFreshStart}
                       />
                       <Label htmlFor="fresh-start" className="text-[10px] font-bold uppercase text-muted-foreground">Sıfırdan Başla</Label>
                    </div>
                  </div>
                  <Input 
                    type="number" 
                    placeholder="Otomatik (Boş Bırakın)"
                    value={startFrom} 
                    onChange={(e) => setStartFrom(e.target.value)}
                    className="bg-background/20"
                  />
                  {isFreshStart && !startFrom && (
                    <p className="text-[10px] text-amber-500 italic">
                      * {city} için {city === 'İSTANBUL' ? '100.000' : '1'}'den başlanacak.
                    </p>
                  )}
                </div>
              </div>

              <Button 
                onClick={handleStartScrape} 
                disabled={isScraping}
                className="w-full bg-primary hover:bg-primary/90 text-primary-foreground shadow-lg shadow-primary/20"
              >
                {isScraping ? "Kazıma Yapılıyor..." : "Kazımayı Başlat"}
              </Button>
            </div>

            <div className="border-t border-border pt-6 space-y-4">
              <div className="flex items-center justify-between">
                <h4 className="font-semibold text-amber-500 flex items-center gap-2 italic">
                  <Zap className="h-4 w-4" /> AI Enrichment
                </h4>
                {isEnriching && <Loader2 className="h-4 w-4 animate-spin text-amber-500" />}
              </div>
              <p className="text-sm text-muted-foreground">
                Bekleyen ilanları Llama 3 ile yapılandırılmış veriye dönüştürün.
              </p>
              <div className="grid gap-2">
                <label className="text-xs uppercase text-muted-foreground font-bold">Batch Boyutu</label>
                <Input 
                  type="number" 
                  value={batchLimit} 
                  onChange={(e) => setBatchLimit(Number(e.target.value))}
                  className="bg-background/20"
                />
              </div>
              <Button 
                variant="outline"
                onClick={handleTriggerEnrichment}
                disabled={isEnriching || (stats?.pending_llm === 0)}
                className="w-full border-amber-500/20 hover:bg-amber-500/10 text-amber-500"
              >
                {isEnriching ? "İşleniyor..." : "Yapay Zeka Analizini Başlat"}
              </Button>
            </div>
          </CardContent>
        </Card>

        {/* Console / Log Panel */}
        <Card className="lg:col-span-2 border-none bg-zinc-950 text-zinc-300 shadow-xl overflow-hidden font-mono text-sm ring-1 ring-white/10 flex flex-col h-[650px] sticky top-6">
          <CardHeader className="bg-zinc-900 border-b border-zinc-800 flex flex-row items-center justify-between py-3 shrink-0">
             <div className="flex items-center gap-2 font-bold text-zinc-100 uppercase tracking-widest text-xs">
                <Terminal className="h-4 w-4 text-emerald-500" /> System Activity Stream
             </div>
             <div className="flex gap-2">
                <div className="w-3 h-3 rounded-full bg-red-500/20 ring-1 ring-red-500/50"></div>
                <div className="w-3 h-3 rounded-full bg-amber-500/20 ring-1 ring-amber-500/50"></div>
                <div className="w-3 h-3 rounded-full bg-emerald-500/20 ring-1 ring-emerald-500/50"></div>
             </div>
          </CardHeader>
          <CardContent className="p-0 flex-1 overflow-hidden flex flex-col min-h-0">
            <div 
              ref={scrollRef}
              className="flex-1 w-full p-4 overflow-y-auto scrollbar-thin scrollbar-thumb-zinc-800 scrollbar-track-transparent"
            >
              <div className="space-y-1">
                {logs.length > 0 ? logs.map((log, i) => (
                  <div key={i} className="flex gap-3 animate-in fade-in slide-in-from-left-2 duration-300">
                    <span className="text-zinc-600 shrink-0 tabular-nums">[{new Date().toLocaleTimeString()}]</span>
                    <span className={
                      log.includes('ERROR') ? 'text-red-400 font-medium' :
                      log.includes('OCR_SUCCESS') ? 'text-emerald-400' :
                      log.includes('OCR_START') ? 'text-blue-400' :
                      log.includes('DUPLICATE_SKIP') ? 'text-amber-400/80 italic' :
                      'text-zinc-400'
                    }>
                      {log}
                    </span>
                  </div>
                )) : (
                  <div className="text-zinc-600 italic">Listening for system events...</div>
                )}
              </div>
            </div>
          </CardContent>
          <div className="p-3 bg-zinc-900 border-t border-zinc-800 text-[10px] uppercase text-zinc-500 tracking-widest flex justify-between shrink-0">
             <span>Sicilius Pulse v2.0</span>
             <span className="flex items-center gap-1">
                <div className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></div>
                Live Connection Established
             </span>
          </div>
        </Card>
      </div>
    </div>
  );
}
