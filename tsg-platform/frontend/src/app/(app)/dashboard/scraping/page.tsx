'use client';

import { useEffect, useState } from 'react';
import { createClient } from '@/lib/supabase/client';
import { Button } from '@/components/ui/button';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Badge } from '@/components/ui/badge';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import { 
  Loader2, 
  AlertCircle, 
  CheckCircle2, 
  Play, 
  RefreshCw,
  AlertTriangle,
  Search,
  Filter, // Added missing import
  ChevronLeft,
  ChevronRight,
  ChevronsLeft,
  ChevronsRight
} from 'lucide-react';
import { toast } from 'sonner';
import { PageHeader, PageHeaderHeading, PageHeaderDescription } from '@/components/ui/page-header';
import { Input } from '@/components/ui/input';
import { 
  Select, 
  SelectContent, 
  SelectItem, 
  SelectTrigger, 
  SelectValue 
} from '@/components/ui/select'; // Added missing imports

type Company = {
  id: string;
  firma_unvani: string | null;
  sicil_no: string;
  sicil_mudurluk: string | null;
  created_at: string;
};

type ScrapingStatus = 'idle' | 'scraping' | 'success' | 'error';

export default function ScrapingPage() {
  const [companies, setCompanies] = useState<Company[]>([]);
  const [loading, setLoading] = useState(true);
  const [scrapingStatus, setScrapingStatus] = useState<Record<string, ScrapingStatus>>({});
  const [searchTerm, setSearchTerm] = useState('');
  const [filterStatus, setFilterStatus] = useState<string>('all');
  const [currentPage, setCurrentPage] = useState(1);
  const [itemsPerPage] = useState(10);
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [progress, setProgress] = useState(0);
  const supabase = createClient();

  useEffect(() => {
    fetchUnscrapedCompanies();
  }, []);

  // Filtrelenmiş ve sayfalanmış şirketleri hesapla
  const filteredCompanies = companies.filter(company => {
    const matchesSearch = searchTerm === '' || 
      (company.firma_unvani?.toLowerCase().includes(searchTerm.toLowerCase()) ||
       company.sicil_no.includes(searchTerm) ||
       company.sicil_mudurluk?.toLowerCase().includes(searchTerm.toLowerCase()));
    
    const status = scrapingStatus[company.id] || 'idle';
    const matchesStatus = filterStatus === 'all' || 
      (filterStatus === 'in-progress' && status === 'scraping') ||
      (filterStatus === 'completed' && status === 'success') ||
      (filterStatus === 'error' && status === 'error') ||
      (filterStatus === 'pending' && status === 'idle');
    
    return matchesSearch && matchesStatus;
  });

  // Sayfa başına göre şirketleri filtrele
  const indexOfLastItem = currentPage * itemsPerPage;
  const indexOfFirstItem = indexOfLastItem - itemsPerPage;
  const currentItems = filteredCompanies.slice(indexOfFirstItem, indexOfLastItem);
  const totalPages = Math.ceil(filteredCompanies.length / itemsPerPage);

  // Sayfa değiştirme fonksiyonları
  const nextPage = () => setCurrentPage(prev => Math.min(prev + 1, totalPages));
  const prevPage = () => setCurrentPage(prev => Math.max(prev - 1, 1));
  const firstPage = () => setCurrentPage(1);
  const lastPage = () => setCurrentPage(totalPages);

  async function fetchUnscrapedCompanies() {
    setLoading(true);
    setIsRefreshing(true);
    try {
      const { data, error } = await supabase
        .from('companies')
        .select('*')
        .is('scraped_at', null)
        .order('created_at', { ascending: true });

      if (error) throw error;
      setCompanies(data || []);
    } catch (error) {
      console.error('Error fetching companies:', error);
      toast.error('Firmalar yüklenirken bir hata oluştu', {
        description: 'Lütfen bağlantınızı kontrol edip tekrar deneyin.',
        action: {
          label: 'Yenile',
          onClick: () => fetchUnscrapedCompanies(),
        },
      });
    } finally {
      setLoading(false);
      setIsRefreshing(false);
    }
  }

  const handleScrape = async (companyId: string) => {
    setScrapingStatus(prev => ({ ...prev, [companyId]: 'scraping' }));
    setProgress(30);

    try {
      const response = await fetch(`/api/v1/scraping/company/${companyId}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || 'Bir hata oluştu');
      }
      
      setProgress(80);
      setScrapingStatus(prev => ({ ...prev, [companyId]: 'success' }));
      
      await new Promise(resolve => setTimeout(resolve, 500));
      
      setCompanies(prev => prev.filter(c => c.id !== companyId));
      setProgress(100);
      
      toast.success('Kazıma Başarılı', {
        description: 'Firma verileri başarıyla kazındı ve işlendi.',
      });

    } catch (error: any) {
      setScrapingStatus(prev => ({ ...prev, [companyId]: 'error' }));
      setProgress(0);
      
      toast.error('Kazıma Hatası', {
        description: error.message || 'Firma kazınırken bir hata oluştu. Lütfen tekrar deneyin.',
        action: {
          label: 'Yeniden Dene',
          onClick: () => handleScrape(companyId),
        },
      });
      
      console.error('Scraping error:', error);
    }
  };

  const handleRefresh = async () => {
    setIsRefreshing(true);
    await fetchUnscrapedCompanies();
    setIsRefreshing(false);
  };

  const getStatusBadge = (status: ScrapingStatus) => {
    switch (status) {
      case 'scraping':
        return (
          <Badge variant="outline" className="bg-blue-50 text-blue-700 border-blue-200 flex items-center gap-1.5">
            <Loader2 className="h-3.5 w-3.5 animate-spin" />
            <span>İşleniyor</span>
          </Badge>
        );
      case 'success':
        return (
          <Badge variant="outline" className="bg-green-50 text-green-700 border-green-200">
            <CheckCircle2 className="h-3.5 w-3.5 mr-1.5" />
            Başarılı
          </Badge>
        );
      case 'error':
        return (
          <Badge variant="outline" className="bg-red-50 text-red-700 border-red-200">
            <AlertTriangle className="h-3.5 w-3.5 mr-1.5" />
            Hata
          </Badge>
        );
      default:
        return (
          <Badge variant="outline" className="bg-gray-50 text-gray-700 border-gray-200">
            Bekliyor
          </Badge>
        );
    }
  };

  return (
    <div className="container mx-auto py-8 space-y-6">
      <PageHeader className="px-0">
        <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
          <div>
            <PageHeaderHeading className="text-2xl md:text-3xl">Veri Kazıma İşlemleri</PageHeaderHeading>
            <PageHeaderDescription className="mt-1.5">
              Henüz kazınmamış firmaları görüntüleyebilir ve kazıma işlemini başlatabilirsiniz.
            </PageHeaderDescription>
          </div>
          <div className="flex items-center gap-2">
            <Button 
              variant="outline" 
              size="sm" 
              onClick={handleRefresh}
              disabled={isRefreshing}
            >
              {isRefreshing ? (
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
              ) : (
                <RefreshCw className="mr-2 h-4 w-4" />
              )}
              Yenile
            </Button>
          </div>
        </div>
      </PageHeader>

      <Card>
        <CardHeader className="pb-3">
          <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
            <div>
              <CardTitle className="text-lg">Firma Listesi</CardTitle>
              <CardDescription>
                Toplam {filteredCompanies.length} firma bulundu
              </CardDescription>
            </div>
            <div className="flex flex-col sm:flex-row gap-3">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                <Input
                  placeholder="Firma ara..."
                  className="pl-9 w-full sm:w-[250px]"
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                />
              </div>
              <div className="w-full sm:w-[180px]">
                <Select value={filterStatus} onValueChange={setFilterStatus}>
                  <SelectTrigger className="w-full">
                    <Filter className="mr-2 h-4 w-4 text-muted-foreground" />
                    <SelectValue placeholder="Durum Filtrele" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">Tümü</SelectItem>
                    <SelectItem value="pending">Bekliyor</SelectItem>
                    <SelectItem value="in-progress">İşlemde</SelectItem>
                    <SelectItem value="completed">Tamamlandı</SelectItem>
                    <SelectItem value="error">Hatalı</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>
          </div>
        </CardHeader>
        
        <CardContent>
          <div className="rounded-md border">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead className="w-[40%]">Firma Ünvanı</TableHead>
                  <TableHead className="w-[15%]">Sicil No</TableHead>
                  <TableHead className="w-[25%]">Sicil Müdürlüğü</TableHead>
                  <TableHead className="w-[10%]">Durum</TableHead>
                  <TableHead className="w-[10%] text-right">İşlemler</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {loading ? (
                  <TableRow>
                    <TableCell colSpan={5} className="h-64 text-center">
                      <div className="flex flex-col items-center justify-center space-y-3">
                        <Loader2 className="h-8 w-8 animate-spin text-muted-foreground" />
                        <span className="text-sm text-muted-foreground">Firmalar yükleniyor...</span>
                      </div>
                    </TableCell>
                  </TableRow>
                ) : currentItems.length === 0 ? (
                  <TableRow>
                    <TableCell colSpan={5} className="h-64 text-center">
                      <div className="flex flex-col items-center justify-center space-y-2">
                        <Search className="h-10 w-10 text-muted-foreground" />
                        <div className="text-sm text-muted-foreground">
                          {searchTerm || filterStatus !== 'all' 
                            ? 'Aramanızla eşleşen sonuç bulunamadı.'
                            : 'Henüz kazınacak firma bulunmamaktadır.'}
                        </div>
                        <Button 
                          variant="ghost" 
                          size="sm" 
                          className="mt-2"
                          onClick={() => {
                            setSearchTerm('');
                            setFilterStatus('all');
                          }}
                        >
                          Filtreleri Temizle
                        </Button>
                      </div>
                    </TableCell>
                  </TableRow>
                ) : (
                  currentItems.map((company) => (
                    <TableRow key={company.id} className="group hover:bg-muted/50">
                      <TableCell className="font-medium">
                        <div className="flex items-center">
                          <span className="line-clamp-1">
                            {company.firma_unvani || 'Bilinmeyen Firma'}
                          </span>
                        </div>
                        {scrapingStatus[company.id] === 'scraping' && (
                          <div className="mt-1.5 w-full">
                            <Progress value={progress} className="h-1.5" />
                            <div className="text-xs text-muted-foreground mt-1">
                              Veriler alınıyor...
                            </div>
                          </div>
                        )}
                      </TableCell>
                      <TableCell>
                        <code className="relative rounded bg-muted px-[0.3rem] py-[0.2rem] font-mono text-sm font-semibold">
                          {company.sicil_no}
                        </code>
                      </TableCell>
                      <TableCell>
                        <div className="flex items-center">
                          <span className="line-clamp-1">
                            {company.sicil_mudurluk || 'Bilinmiyor'}
                          </span>
                        </div>
                      </TableCell>
                      <TableCell>
                        {getStatusBadge(scrapingStatus[company.id] || 'idle')}
                      </TableCell>
                      <TableCell className="text-right">
                        <Button 
                          variant={scrapingStatus[company.id] === 'error' ? 'outline' : 'default'}
                          size="sm" 
                          onClick={() => handleScrape(company.id)}
                          disabled={scrapingStatus[company.id] === 'scraping'}
                          className="w-full sm:w-auto"
                        >
                          {scrapingStatus[company.id] === 'scraping' ? (
                            <>
                              <Loader2 className="mr-2 h-3.5 w-3.5 animate-spin" />
                              İşleniyor
                            </>
                          ) : scrapingStatus[company.id] === 'success' ? (
                            <>
                              <CheckCircle2 className="mr-2 h-3.5 w-3.5" />
                              Tamamlandı
                            </>
                          ) : scrapingStatus[company.id] === 'error' ? (
                            <>
                              <AlertTriangle className="mr-2 h-3.5 w-3.5" />
                              Tekrar Dene
                            </>
                          ) : (
                            <>
                              <Play className="mr-2 h-3.5 w-3.5" />
                              Başlat
                            </>
                          )}
                        </Button>
                      </TableCell>
                    </TableRow>
                  ))
                )}
              </TableBody>
            </Table>
          </div>
        </CardContent>

        {totalPages > 1 && (
          <CardFooter className="border-t pt-4">
             <div className="flex items-center justify-between w-full">
                <div className="text-sm text-muted-foreground">
                  Toplam {filteredCompanies.length} sonuçtan {indexOfFirstItem + 1}-{Math.min(indexOfLastItem, filteredCompanies.length)} arası gösteriliyor
                </div>
                <div className="flex items-center space-x-1">
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={firstPage}
                    disabled={currentPage === 1}
                    className="h-8 w-8 p-0"
                  >
                    <ChevronsLeft className="h-4 w-4" />
                  </Button>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={prevPage}
                    disabled={currentPage === 1}
                    className="h-8 w-8 p-0"
                  >
                    <ChevronLeft className="h-4 w-4" />
                  </Button>
                  <div className="flex items-center justify-center w-10 text-sm">
                    {currentPage}/{totalPages || 1}
                  </div>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={nextPage}
                    disabled={currentPage >= totalPages}
                    className="h-8 w-8 p-0"
                  >
                    <ChevronRight className="h-4 w-4" />
                  </Button>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={lastPage}
                    disabled={currentPage >= totalPages}
                    className="h-8 w-8 p-0"
                  >
                    <ChevronsRight className="h-4 w-4" />
                  </Button>
                </div>
              </div>
          </CardFooter>
        )}
      </Card>
    </div>
  );
}