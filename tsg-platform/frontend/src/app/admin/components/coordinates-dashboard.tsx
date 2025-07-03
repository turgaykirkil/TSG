'use client';

import { useState, useCallback, useEffect } from 'react';
import { supabase } from '@/lib/supabaseClient';
import { Progress } from '@/components/ui/progress';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';

// Type definitions
type Stats = {
  coordinated: number;
  uncoordinated: number;
  conflicts: number;
};

type CompanyData = {
  id: string;
  sicil_no: string;
  sicil_mudurluk: string;
  address: string;
  koordinat?: string;
  geocode_attempted_at: string;
  created_at: string;
};

const CoordinatesDashboard = () => {
  const [stats, setStats] = useState<Stats>({ coordinated: 0, uncoordinated: 0, conflicts: 0 });
  const [isLoading, setIsLoading] = useState(false);
  const [isResolving, setIsResolving] = useState(false);
  const [message, setMessage] = useState<{ type: 'success' | 'error' | 'info'; text: string } | null>(null);
  const [progress, setProgress] = useState(0);
  const [limit, setLimit] = useState(100);

  const fetchStats = useCallback(async () => {
    try {
      const { data, error } = await supabase.rpc('get_coordinate_stats');
      if (error) throw error;
      if (data && data.length > 0) {
        setStats(data[0]);
      } else {
        throw new Error("RPC 'get_coordinate_stats' returned no data.");
      }
    } catch (error: any) {
      console.warn('get_coordinate_stats RPC failed, falling back to client-side calculation.', error.message);
      try {
        const { count: coordinated, error: coordError } = await supabase.from('companies').select('*', { count: 'exact', head: true }).not('koordinat', 'is', null);
        const { count: uncoordinated, error: uncoordError } = await supabase.from('companies').select('*', { count: 'exact', head: true }).is('koordinat', null);
        
        if (coordError || uncoordError) {
            throw new Error(coordError?.message || uncoordError?.message);
        }

        setStats({ coordinated: coordinated ?? 0, uncoordinated: uncoordinated ?? 0, conflicts: 0 });
        setMessage({ type: 'info', text: 'İstatistikler sunucudan alınamadığı için istemcide hesaplandı (çakışmalar hariç).' });

      } catch (fallbackError: any) {
        console.error('Error fetching stats with fallback:', fallbackError);
        setMessage({ type: 'error', text: `İstatistikler yüklenemedi: ${fallbackError.message}` });
      }
    }
  }, []);

  useEffect(() => {
    fetchStats();
  }, [fetchStats]);

  const handleFetchCoordinates = useCallback(async (fetchLimit: number) => {
    if (!fetchLimit || fetchLimit <= 0) {
      setMessage({ type: 'error', text: "Lütfen 0'dan büyük geçerli bir sayı girin." });
      return;
    }
    setIsLoading(true);
    setMessage(null);
    setProgress(0);

    try {
      const { data: companiesToFetch, error: fetchError } = await supabase
        .from('companies')
        .select('id, address, sicil_mudurluk')
        .is('koordinat', null)
        .limit(fetchLimit);

      if (fetchError) throw fetchError;

      if (!companiesToFetch || companiesToFetch.length === 0) {
        setMessage({ type: 'info', text: 'Koordinatı alınacak yeni firma bulunamadı.' });
        setIsLoading(false);
        return;
      }

      const addressMap = companiesToFetch.reduce((acc, company) => {
        if (company.address) {
          const cleanAddress = company.address.trim();
          if (cleanAddress) {
            if (!acc[cleanAddress]) {
              acc[cleanAddress] = { ids: [], sicil_mudurluk: company.sicil_mudurluk };
            }
            acc[cleanAddress].ids.push(company.id);
          }
        }
        return acc;
      }, {} as Record<string, { ids: string[], sicil_mudurluk: string }>);

      const uniqueAddresses = Object.keys(addressMap);
      const totalUniqueAddresses = uniqueAddresses.length;
      let successfulGeocodes = 0;

      for (let i = 0; i < totalUniqueAddresses; i++) {
        const address = uniqueAddresses[i];
        const { ids: companyIds, sicil_mudurluk } = addressMap[address];
        const now = new Date().toISOString();

        await new Promise(resolve => setTimeout(resolve, 2000)); // 2 saniye bekle

        try {
          const apiKey = process.env.NEXT_PUBLIC_LOCATIONIQ_API_KEY;
          if (!apiKey) throw new Error('LocationIQ API anahtarı (NEXT_PUBLIC_LOCATIONIQ_API_KEY) bulunamadı.');

          // Şehir bilgisini 'sicil_mudurluk'ten çıkar, varsayılan olarak İzmir kullan
          const city = sicil_mudurluk?.split(' ')[0] || 'İzmir';
          const country = 'Turkey';

          const mainAddress = address.split('/')[0];
          const cleanedAddress = mainAddress
            .replace(/MAHALLESİ|MAH\.|CADDE|CAD\.|SOKAK|SOK\.|SK\.|BULVARI|BUL\.|BLOK|NO:|İÇ KAPI NO:|PLAZA|İŞ MERKEZİ|SİTESİ|GALERİA|APT/gi, ' ')
            .replace(/\d+[a-zA-Z]?\/\d+[a-zA-Z]?/g, ' ') // 1/A, 10/2B gibi kapı nolarını temizle
            .replace(/[^a-zA-Z0-9ğüşıöçĞÜŞİÖÇ\s]/g, ' ') // Özel karakterleri temizle
            .replace(/\s\s+/g, ' ') // Çoklu boşlukları teke indir
            .trim();
          
          const fullQuery = `${cleanedAddress}, ${city}, ${country}`;

          const response = await fetch(`https://us1.locationiq.com/v1/search?key=${apiKey}&q=${encodeURIComponent(fullQuery)}&format=json`);

          if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`LocationIQ API error (${response.status}): ${errorText}`);
          }

          const geoData = await response.json();

          if (geoData && geoData.length > 0) {
            const { lat, lon } = geoData[0];
            const coordinate = `POINT(${lon} ${lat})`;
            const { error: updateError } = await supabase
              .from('companies')
              .update({ koordinat: coordinate, geocode_attempted_at: now })
              .in('id', companyIds);
            if (updateError) throw updateError;
            successfulGeocodes++;
          } else {
            const { error: updateError } = await supabase.from('companies').update({ geocode_attempted_at: now }).in('id', companyIds);
            if (updateError) throw updateError;
          }
        } catch (err: any) {
          console.error(`Adres işlenemedi: ${address}:`, err.message);
        }
        setProgress(((i + 1) / totalUniqueAddresses) * 100);
      }

      setMessage({ type: 'success', text: `${totalUniqueAddresses} adresten ${successfulGeocodes} tanesi başarıyla koordinatlandırıldı.` });
      await fetchStats();

    } catch (err: any) {
      console.error('Koordinat getirme hatası:', err);
      setMessage({ type: 'error', text: `Bir hata oluştu: ${err.message}` });
    } finally {
      setIsLoading(false);
    }
  }, [fetchStats]);

  const handleResolveConflicts = useCallback(async () => {
    setIsResolving(true);
    setMessage(null);
    try {
      const { data, error } = await supabase.rpc('resolve_coordinate_conflicts');

      if (error) throw error;

      const resultMessage = data?.message || `${data?.count || 0} çakışma çözüldü.`;
      setMessage({ type: 'success', text: resultMessage });
      await fetchStats();

    } catch (err: any) {
      console.error('Çakışma çözme hatası:', err);
      setMessage({ type: 'error', text: `Bir hata oluştu: ${err.message}` });
    } finally {
      setIsResolving(false);
    }
  }, [fetchStats]);

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>Koordinat İstatistikleri</CardTitle>
        </CardHeader>
        <CardContent>
          {stats ? (
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
              <div>
                <p className="text-2xl font-bold">{(stats.coordinated || 0) + (stats.uncoordinated || 0)}</p>
                <p className="text-sm text-muted-foreground">Toplam Firma</p>
              </div>
              <div>
                <p className="text-2xl font-bold text-green-600">{stats.coordinated || 0}</p>
                <p className="text-sm text-muted-foreground">Koordinatlı</p>
              </div>
              <div>
                <p className="text-2xl font-bold text-red-600">{stats.uncoordinated || 0}</p>
                <p className="text-sm text-muted-foreground">Koordinatsız</p>
              </div>
              <div>
                <p className="text-2xl font-bold text-orange-500">{stats.conflicts || 0}</p>
                <p className="text-sm text-muted-foreground">Çakışan</p>
              </div>
            </div>
          ) : (
            <p>İstatistikler yükleniyor...</p>
          )}
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Koordinat İşlemleri</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-4 p-4 border rounded-lg">
            <h4 className="font-medium">Kontrollü Koordinat Getirme</h4>
            <p className="text-sm text-muted-foreground">
              API limitlerini aşmamak için, bir seferde kaç firmanın koordinatının getirileceğini belirtin. Bu işlem, koordinatı olmayan ve daha önce denenmemiş firmaları getirecektir.
            </p>
            <div className="flex flex-col sm:flex-row items-center gap-4">
              <Input
                type="number"
                value={limit}
                onChange={(e) => setLimit(Math.max(0, Number(e.target.value)))}
                placeholder="Sayı girin"
                className="max-w-[150px]"
              />
              <Button onClick={() => handleFetchCoordinates(limit)} disabled={isLoading || isResolving} className="flex-1">
                {isLoading ? 'Koordinatlar Getiriliyor...' : `Sıradaki ${limit} Firmanın Koordinatını Getir`}
              </Button>
            </div>
          </div>

          <div className="space-y-4 p-4 border rounded-lg">
             <h4 className="font-medium">Toplu Çakışma Çözme</h4>
            <p className="text-sm text-muted-foreground">
              Aynı koordinata sahip ancak farklı adresleri olan firmaları tespit edip yeniden konumlandırır. Bu işlem tüm veritabanını tarar ve uzun sürebilir.
            </p>
            <Button onClick={handleResolveConflicts} disabled={isLoading || isResolving} variant="destructive" className="w-full">
              {isResolving ? 'Çakışmalar Çözülüyor...' : 'Tüm Çakışmaları Çöz'}
            </Button>
          </div>
          {(isLoading || isResolving) && (
            <div className="space-y-2">
              <Progress value={progress} />
              <p className="text-sm text-center text-muted-foreground">
                İşleniyor... {Math.round(progress)}%
              </p>
            </div>
          )}
          {message && (
            <div className={`p-4 rounded-md text-sm ${
              message.type === 'success' ? 'bg-green-100 text-green-800' :
              message.type === 'error' ? 'bg-red-100 text-red-800' :
              'bg-blue-100 text-blue-800'
            }`}>
              {message.text}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
};

export default CoordinatesDashboard;