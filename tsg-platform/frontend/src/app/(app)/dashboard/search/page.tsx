'use client';

import { useState, useEffect, useMemo } from 'react';
import { useSearchParams, useRouter } from 'next/navigation';
import { useDebounce } from 'use-debounce';
import dynamic from 'next/dynamic';
import {
  Search, MoreHorizontal, Building, Hash, CalendarDays, ServerCrash, FileSearch2, List, Map
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import {
  DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger
} from '@/components/ui/dropdown-menu';
import { useCompanySearch } from '@/hooks/useCompanySearch';
import {
  Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle
} from '@/components/ui/card';
import { Skeleton } from '@/components/ui/skeleton';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import LoadingSpinner from '@/components/ui/loading-spinner';
import type { Company } from '@/types/company.types';

export interface MarkerData {
  koordinat: { x: number; y: number };
  companies: { id: string; firma_unvani: string | null; adres: string | null }[];
}

const MapDisplay = dynamic(() => import('./components/MapDisplay'), {
  ssr: false,
  loading: () => (
    <div className="flex h-[60vh] w-full items-center justify-center rounded-lg bg-muted">
      <LoadingSpinner />
    </div>
  ),
});

const CompanyCardSkeleton = () => (
  <Card className="flex flex-col">
    <CardHeader><Skeleton className="h-6 w-3/4" /><Skeleton className="h-4 w-1/4 mt-2" /></CardHeader>
    <CardContent className="flex-grow space-y-4">
      <div className="flex items-center space-x-3"><Skeleton className="h-5 w-5 rounded-full" /><Skeleton className="h-4 w-full" /></div>
      <div className="flex items-center space-x-3"><Skeleton className="h-5 w-5 rounded-full" /><Skeleton className="h-4 w-1/2" /></div>
    </CardContent>
    <CardFooter><Skeleton className="h-4 w-1/3" /></CardFooter>
  </Card>
);

const renderInitialState = () => (
  <div className="flex flex-col items-center justify-center text-center p-12 rounded-lg bg-muted/50 h-[60vh]">
    <FileSearch2 className="h-16 w-16 text-muted-foreground mb-4" />
    <h2 className="text-xl font-semibold">Aramaya Başlayın</h2>
    <p className="text-muted-foreground mt-2">Şirket adı, sicil no veya adres yazarak sonuçları listeleyin.</p>
  </div>
);

const renderNoResults = (query: string) => (
  <div className="flex flex-col items-center justify-center text-center p-12 rounded-lg bg-muted/50 h-[60vh]">
    <FileSearch2 className="h-16 w-16 text-muted-foreground mb-4" />
    <h2 className="text-xl font-semibold">Sonuç Bulunamadı</h2>
    <p className="text-muted-foreground mt-2">`{query}` araması için bir sonuç bulunamadı.</p>
  </div>
);

const renderError = (error: Error | null) => (
  <div className="flex flex-col items-center justify-center text-center p-12 rounded-lg bg-muted/50 h-[60vh]">
    <ServerCrash className="h-16 w-16 text-destructive mb-4" />
    <h2 className="text-xl font-semibold">Bir Hata Oluştu</h2>
    <p className="text-muted-foreground mt-2">Şirket verileri yüklenirken bir sorunla karşılaşıldı.</p>
    <p className="text-sm text-red-500 mt-1">{error instanceof Error ? error.message : 'Bilinmeyen bir hata.'}</p>
  </div>
);

export default function SearchPage() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const urlQuery = searchParams.get('q') || '';

  const [inputValue, setInputValue] = useState(urlQuery);
  const [debouncedInputValue] = useDebounce(inputValue, 500);

  const { data: companies, isLoading, isError, error } = useCompanySearch(debouncedInputValue);

  useEffect(() => {
    setInputValue(urlQuery);
  }, [urlQuery]);

  useEffect(() => {
    const params = new URLSearchParams(searchParams.toString());
    if (debouncedInputValue) {
      params.set('q', debouncedInputValue);
    } else {
      params.delete('q');
    }
    router.replace(`?${params.toString()}`);
  }, [debouncedInputValue, router, searchParams]);

  const markersData: MarkerData[] = useMemo(() => {
    if (!companies) return [];

    const companiesWithCoords = companies.filter(
      (company): company is Company & { koordinat: { x: number; y: number } } =>
        company.koordinat != null
    );

    const groupedByCoords = companiesWithCoords.reduce(
      (acc, company) => {
        const key = `${company.koordinat.x},${company.koordinat.y}`;
        if (!acc[key]) {
          acc[key] = {
            koordinat: company.koordinat,
            companies: [],
          };
        }
        acc[key].companies.push({ id: company.id || '', firma_unvani: company.firma_unvani, adres: company.adres ?? null });
        return acc;
      },
      {} as Record<string, MarkerData>
    );

    return Object.values(groupedByCoords);
  }, [companies]);

  const renderContent = () => {
    if (isLoading) {
      return (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {Array.from({ length: 8 }).map((_, i) => <CompanyCardSkeleton key={i} />)}
        </div>
      );
    }
    if (isError) return renderError(error);
    if (!debouncedInputValue) return renderInitialState();
    if (companies && companies.length === 0) return renderNoResults(debouncedInputValue);

    return (
      <Tabs defaultValue="list" className="w-full">
        <TabsList className="grid w-full grid-cols-2">
          <TabsTrigger value="list"><List className="mr-2 h-4 w-4"/>Liste ({companies?.length || 0})</TabsTrigger>
          <TabsTrigger value="map"><Map className="mr-2 h-4 w-4"/>Harita ({markersData.length})</TabsTrigger>
        </TabsList>
        <TabsContent value="list" className="mt-4">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {companies?.map(company => (
              <Card key={company.sicil_no} className="flex flex-col hover:shadow-xl hover:-translate-y-1 transition-all duration-300 bg-card/80 backdrop-blur-sm">
                <CardHeader>
                  <CardTitle className="text-base font-bold leading-tight">{company.firma_unvani || 'İsim Bilgisi Yok'}</CardTitle>
                  <CardDescription className="flex items-center pt-1 text-xs"><Hash className="h-3 w-3 mr-2 text-muted-foreground" />{company.sicil_no}</CardDescription>
                </CardHeader>
                <CardContent className="flex-grow">
                  <div className="flex items-start space-x-3 text-sm text-muted-foreground"><Building className="h-5 w-5 mt-1 flex-shrink-0" /><span className="line-clamp-3">{company.adres || 'Adres bilgisi yok'}</span></div>
                </CardContent>
                <CardFooter className="flex justify-between items-center text-xs text-muted-foreground border-t pt-3 mt-4">
                  <div className="flex items-center"><CalendarDays className="h-4 w-4 mr-2" /><span>{company.last_scraped_at ? new Date(company.last_scraped_at).toLocaleDateString() : '-'}</span></div>
                  <DropdownMenu>
                    <DropdownMenuTrigger asChild><Button variant="ghost" size="icon" className="h-8 w-8"><MoreHorizontal className="h-4 w-4" /></Button></DropdownMenuTrigger>
                    <DropdownMenuContent align="end"><DropdownMenuItem>Detayları Görüntüle</DropdownMenuItem><DropdownMenuItem>Favorilere Ekle</DropdownMenuItem></DropdownMenuContent>
                  </DropdownMenu>
                </CardFooter>
              </Card>
            ))}
          </div>
        </TabsContent>
        <TabsContent value="map" className="mt-4 h-[70vh] rounded-lg overflow-hidden border">
          <MapDisplay markers={markersData} />
        </TabsContent>
      </Tabs>
    );
  };

  return (
    <div className="space-y-8">
      <div className="p-6 rounded-lg bg-card/50 backdrop-blur-sm border shadow-sm">
        <h1 className="text-2xl font-bold tracking-tight">Şirket Veri Bankası</h1>
        <p className="text-muted-foreground mt-1">Türkiye genelindeki şirketleri sicil numarası, ünvanı veya adresine göre arayın.</p>
        <div className="relative mt-6">
          <Search className="absolute left-4 top-1/2 h-5 w-5 -translate-y-1/2 text-muted-foreground" />
          <Input
            type="search"
            placeholder="Örn: 'ABC Teknoloji' veya 'Ankara'"
            className="pl-12 h-12 text-lg"
            value={inputValue}
            onChange={e => setInputValue(e.target.value)}
          />
        </div>
      </div>
      <div>
        {renderContent()}
      </div>
    </div>
  );
}
