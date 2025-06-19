'use client';

import { useState } from 'react';
import { useDebounce } from 'use-debounce';
import {
  Search,
  Filter,
  MoreHorizontal,
  Loader2,
  Building,
  Hash,
  CalendarDays,
  ServerCrash,
  FileSearch2
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import { useCompanySearch } from '@/hooks/useCompanySearch';
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';
import { Skeleton } from '@/components/ui/skeleton';

// Arayüzde kullanılacak sıralama alanları ve yönleri için tipler.
// Not: Bu sıralama henüz arayüze tam entegre edilmemiştir, sadece altyapı olarak mevcuttur.
type SortField = 'firma_unvani' | 'sicil_no' | 'last_scraped_at';
type SortDirection = 'asc' | 'desc';

// Yükleme sırasında gösterilecek iskelet kart bileşeni
const CompanyCardSkeleton = () => (
  <Card className="flex flex-col">
    <CardHeader>
      <Skeleton className="h-6 w-3/4" />
      <Skeleton className="h-4 w-1/4 mt-2" />
    </CardHeader>
    <CardContent className="flex-grow space-y-4">
      <div className="flex items-center space-x-3">
        <Skeleton className="h-5 w-5 rounded-full" />
        <Skeleton className="h-4 w-full" />
      </div>
      <div className="flex items-center space-x-3">
        <Skeleton className="h-5 w-5 rounded-full" />
        <Skeleton className="h-4 w-1/2" />
      </div>
    </CardContent>
    <CardFooter>
      <Skeleton className="h-4 w-1/3" />
    </CardFooter>
  </Card>
);

export default function SearchPage() {
  const [searchQuery, setSearchQuery] = useState('');
  const [debouncedSearchQuery] = useDebounce(searchQuery, 500);

  const { data: companies, isLoading, isError, error } = useCompanySearch(
    debouncedSearchQuery
  );

  const renderContent = () => {
    if (isLoading) {
      return (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {Array.from({ length: 8 }).map((_, i) => (
            <CompanyCardSkeleton key={i} />
          ))}
        </div>
      );
    }

    if (isError) {
      return (
        <div className="flex flex-col items-center justify-center text-center p-12 rounded-lg bg-muted/50">
          <ServerCrash className="h-16 w-16 text-destructive mb-4" />
          <h2 className="text-xl font-semibold">Bir Hata Oluştu</h2>
          <p className="text-muted-foreground mt-2">
            Şirket verileri yüklenirken bir sorunla karşılaşıldı.
          </p>
          <p className="text-sm text-red-500 mt-1">
            {error instanceof Error ? error.message : 'Bilinmeyen bir hata.'}
          </p>
        </div>
      );
    }
    
    if (!debouncedSearchQuery) {
        return (
            <div className="flex flex-col items-center justify-center text-center p-12 rounded-lg bg-muted/50">
                <FileSearch2 className="h-16 w-16 text-muted-foreground mb-4" />
                <h2 className="text-xl font-semibold">Aramaya Başlayın</h2>
                <p className="text-muted-foreground mt-2">
                    Şirket adı, sicil no veya adres yazarak sonuçları listeleyin.
                </p>
            </div>
        );
    }

    if (companies && companies.length === 0) {
      return (
        <div className="flex flex-col items-center justify-center text-center p-12 rounded-lg bg-muted/50">
          <FileSearch2 className="h-16 w-16 text-muted-foreground mb-4" />
          <h2 className="text-xl font-semibold">Sonuç Bulunamadı</h2>
          <p className="text-muted-foreground mt-2">
            `{debouncedSearchQuery}` araması için bir sonuç bulunamadı.
          </p>
        </div>
      );
    }

    return (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        {companies?.map(company => (
          <Card
            key={company.sicil_no}
            className="flex flex-col hover:shadow-xl hover:-translate-y-1 transition-all duration-300 bg-card/80 backdrop-blur-sm"
          >
            <CardHeader>
              <CardTitle className="text-base font-bold leading-tight">
                {company.firma_unvani || 'İsim Bilgisi Yok'}
              </CardTitle>
              <CardDescription className="flex items-center pt-1 text-xs">
                <Hash className="h-3 w-3 mr-2 text-muted-foreground" />
                {company.sicil_no}
              </CardDescription>
            </CardHeader>
            <CardContent className="flex-grow">
              <div className="flex items-start space-x-3 text-sm text-muted-foreground">
                <Building className="h-5 w-5 mt-1 flex-shrink-0" />
                <span className="line-clamp-3">{company.adres || 'Adres bilgisi yok'}</span>
              </div>
            </CardContent>
            <CardFooter className="flex justify-between items-center text-xs text-muted-foreground border-t pt-3 mt-4">
              <div className="flex items-center">
                <CalendarDays className="h-4 w-4 mr-2" />
                <span>
                  {company.last_scraped_at
                    ? new Date(company.last_scraped_at).toLocaleDateString()
                    : '-'}
                </span>
              </div>
              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <Button variant="ghost" size="icon" className="h-8 w-8">
                    <MoreHorizontal className="h-4 w-4" />
                  </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent align="end">
                  <DropdownMenuItem>Detayları Görüntüle</DropdownMenuItem>
                  <DropdownMenuItem>Favorilere Ekle</DropdownMenuItem>
                </DropdownMenuContent>
              </DropdownMenu>
            </CardFooter>
          </Card>
        ))}
      </div>
    );
  };

  return (
    <div className="space-y-8">
      {/* Üst Başlık ve Arama Çubuğu */}
      <div className="p-6 rounded-lg bg-card/50 backdrop-blur-sm border shadow-sm">
        <h1 className="text-2xl font-bold tracking-tight">Şirket Veri Bankası</h1>
        <p className="text-muted-foreground mt-1">
          Türkiye genelindeki şirketleri sicil numarası, ünvanı veya adresine göre arayın.
        </p>
        <div className="relative mt-6">
          <Search className="absolute left-4 top-1/2 h-5 w-5 -translate-y-1/2 text-muted-foreground" />
          <Input
            type="search"
            placeholder="Örn: 'ABC Teknoloji' veya 'Ankara'"
            className="pl-12 h-12 text-lg"
            value={searchQuery}
            onChange={e => setSearchQuery(e.target.value)}
          />
        </div>
      </div>

      {/* Sonuçlar Bölümü */}
      <div>
        <div className="flex items-center justify-between mb-4 px-2">
            <h2 className="text-xl font-semibold tracking-tight">Arama Sonuçları</h2>
            {/* Sıralama ve Filtreleme buraya eklenebilir */}
        </div>
        {renderContent()}
      </div>
    </div>
  );
}
