'use client';

import { useState, useCallback, useEffect } from 'react';
import { supabase } from '@/lib/supabaseClient';
import { Progress } from '@/components/ui/progress';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';

// Type definitions
type Stats = {
  total_companies: number;
  with_coordinates: number;
  without_coordinates: number;
  conflicts: number;
};

type CompanyData = {
  id: string;
  adres: string;
  sicil_no: string;
  sicil_mudurluk: string;
  koordinat?: string | null;
  created_at?: string;
};

type CompanyUpdatePayload = {
  id: string;
  sicil_no: string;
  sicil_mudurluk: string;
  koordinat?: string;
  geocode_attempted_at: string;
  created_at: string;
};

const CoordinatesDashboard = () => {
  const [stats, setStats] = useState<Stats | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [isResolving, setIsResolving] = useState(false);
  const [message, setMessage] = useState<{ type: 'success' | 'error' | 'info'; text: string } | null>(null);
  const [progress, setProgress] = useState(0);
  const [limit, setLimit] = useState(100); // State for the limit

  const refreshStats = useCallback(async () => {
    try {
      const { data, error } = await supabase.rpc('get_coordinate_stats');
      if (error) throw error;
      setStats(data);
    } catch (error) {
      console.error('Error fetching stats:', error);
      setMessage({ type: 'error', text: 'İstatistikler yüklenemedi.' });
    }
  }, []);

  useEffect(() => {
    refreshStats();
  }, [refreshStats]);

  const geocodeAddress = async (address: string): Promise<{ latitude: number; longitude: number } | null> => {
    if (!address) return null;
    const apiKey = process.env.NEXT_PUBLIC_LOCATIONIQ_API_KEY;
    const url = `https://us1.locationiq.com/v1/search?key=${apiKey}&q=${encodeURIComponent(address)}&format=json`;

    try {
      const response = await fetch(url);
      if (!response.ok) {
        console.error(`Geocoding API error for address '${address}': ${response.statusText}`);
        return null;
      }
      const data = await response.json();
      if (data && data[0]) {
        return { latitude: parseFloat(data[0].lat), longitude: parseFloat(data[0].lon) };
      }
      return null;
    } catch (error) {
      console.error(`Error geocoding address '${address}':`, error);
      return null;
    }
  };

  const fetchAllFromSupabase = async (queryBuilder: any) => {
    const allData: any[] = [];
    let page = 0;
    const pageSize = 1000;
    let hasMore = true;

    console.log("Tüm veritabanı taranıyor (sayfalar halinde)...");
    while (hasMore) {
      const { data, error } = await queryBuilder.range(page * pageSize, (page + 1) * pageSize - 1);
      if (error) {
        console.error("Sayfalama sırasında hata:", error);
        throw error;
      }
      if (data && data.length > 0) {
        allData.push(...data);
        if (data.length < pageSize) {
          hasMore = false;
        } else {
          page++;
        }
      } else {
        hasMore = false;
      }
    }
    console.log(`Tarama tamamlandı. Toplam kayıt: ${allData.length}`);
    return allData;
  };

  const handleFetchCoordinates = useCallback(async (fetchLimit: number) => {
    if (!fetchLimit || fetchLimit <= 0) {
      setMessage({ type: 'error', text: "Lütfen 0'dan büyük geçerli bir sayı girin." });
      return;
    }
    setIsLoading(true);
    setMessage(null);
    setProgress(0);
    console.log(`--- Koordinat Getirme İşlemi Başladı (Limit: ${fetchLimit}) ---`);

    try {
      const { data: companiesToFetch, error: fetchError } = await supabase
        .from('companies')
        .select('id, adres, sicil_no, sicil_mudurluk')
        .is('koordinat', null)
        .is('geocode_attempted_at', null)
        .limit(fetchLimit);

      if (fetchError) throw fetchError;

      if (!companiesToFetch || companiesToFetch.length === 0) {
        setMessage({ type: 'info', text: 'Tüm firmaların koordinatları mevcut veya daha önce denenmiş.' });
        setIsLoading(false);
        return;
      }
      console.log(`1. Toplam ${companiesToFetch.length} adet konumlandırılacak şirket bulundu.`);

      const addressMap = new Map<string, CompanyData[]>();
      for (const company of companiesToFetch) {
        const address = company.adres?.trim().toLowerCase();
        if (address) {
          if (!addressMap.has(address)) {
            addressMap.set(address, []);
          }
          addressMap.get(address)!.push(company);
        }
      }
      console.log(`2. Şirketler ${addressMap.size} adet benzersiz adrese göre gruplandırıldı.`);

      let addressesProcessed = 0;
      const allUpdates: CompanyUpdatePayload[] = [];
      const delay = (ms: number) => new Promise(res => setTimeout(res, ms));

      console.log('3. Benzersiz adresler için konumlandırma başlıyor (Sıralı ve Gecikmeli)...');
      for (const [address, companies] of addressMap.entries()) {
        const geocodeResult = await geocodeAddress(address);
        const now = new Date().toISOString();

        const updatePayloads = companies.map((company: CompanyData) => ({
          id: company.id,
          sicil_no: company.sicil_no,
          sicil_mudurluk: company.sicil_mudurluk,
          koordinat: geocodeResult ? `POINT(${geocodeResult.longitude} ${geocodeResult.latitude})` : undefined,
          geocode_attempted_at: now,
          created_at: company.created_at || now, // Preserve existing created_at or set new one
        }));

        allUpdates.push(...updatePayloads);
        addressesProcessed++;
        setProgress((addressesProcessed / addressMap.size) * 100);

        // Rate limit'e uymak için 500ms bekle (saniyede 2 istek)
        await delay(500);
      }

      const successfulUpdates = allUpdates.filter(u => u.koordinat);
      const failedAttempts = allUpdates.filter(u => !u.koordinat);

      console.log(`4. Konumlandırma tamamlandı. ${successfulUpdates.length} şirket için konum bulundu, ${failedAttempts.length} şirket için denendi.`);

      if (allUpdates.length > 0) {
        console.log('5. Veritabanı güncelleniyor...');
        const { error: updateError } = await supabase.from('companies').upsert(allUpdates);
        if (updateError) throw updateError;
        console.log('6. Veritabanı başarıyla güncellendi.');
      }

      setMessage({ type: 'success', text: `${successfulUpdates.length} firma başarıyla konumlandırıldı. ${failedAttempts.length} firma için konum bulunamadı.` });
      refreshStats();

    } catch (error) {
      console.error('Error fetching coordinates:', error);
      const errorMessage = error instanceof Error ? error.message : 'Bilinmeyen bir hata oluştu.';
      setMessage({ type: 'error', text: `Hata: ${errorMessage}` });
    } finally {
      setIsLoading(false);
      console.log('--- Koordinat Getirme İşlemi Tamamlandı ---');
    }
  }, [refreshStats]);

  const handleResolveConflicts = async () => {
    setIsResolving(true);
    setMessage(null);
    setProgress(0);
    console.log('--- Çakışma Çözme İşlemi Başladı (Tüm Veritabanı) ---');

    try {
      const queryBuilder = supabase
        .from('companies')
        .select('id, koordinat, sicil_no, sicil_mudurluk, adres')
        .not('koordinat', 'is', null);
      
      const companies: CompanyData[] = await fetchAllFromSupabase(queryBuilder);
      console.log(`1. Veritabanından ${companies.length} adet koordinatlı şirket çekildi.`);

      const coordsMap = new Map<string, CompanyData[]>();
      companies.forEach((c) => {
        if (c.koordinat) {
          if (!coordsMap.has(c.koordinat)) {
            coordsMap.set(c.koordinat, []);
          }
          coordsMap.get(c.koordinat)!.push(c);
        }
      });
      console.log(`2. Şirketler ${coordsMap.size} farklı koordinata göre gruplandırıldı.`);

      const companiesToReGeocode: CompanyData[] = [];
      let conflictLocationCount = 0;

      console.log('3. Çakışmalar kontrol ediliyor...');
      coordsMap.forEach((conflictingCompanies) => {
        if (conflictingCompanies.length > 1) {
          const uniqueAddresses = new Set(conflictingCompanies.map(c => c.adres?.trim().toLowerCase()));
          if (uniqueAddresses.size > 1) {
            conflictLocationCount++;
            companiesToReGeocode.push(...conflictingCompanies);
          }
        }
      });

      console.log(`4. Toplam ${conflictLocationCount} çakışma noktasında ${companiesToReGeocode.length} şirket yeniden konumlandırılacak.`);

      if (companiesToReGeocode.length === 0) {
        setMessage({ type: 'info', text: 'Farklı adreslere sahip çakışan koordinat bulunamadı.' });
        setIsResolving(false);
        return;
      }

      let companiesProcessed = 0;
      const allUpdates: CompanyUpdatePayload[] = [];
      const delay = (ms: number) => new Promise(res => setTimeout(res, ms));

      console.log('5. Yeniden konumlandırma başlıyor (Sıralı ve Gecikmeli)...');
      for (const company of companiesToReGeocode) {
        const geocodeResult = await geocodeAddress(company.adres);
        const now = new Date().toISOString();

        allUpdates.push({
          id: company.id,
          sicil_no: company.sicil_no,
          sicil_mudurluk: company.sicil_mudurluk,
          koordinat: geocodeResult ? `POINT(${geocodeResult.longitude} ${geocodeResult.latitude})` : undefined,
          geocode_attempted_at: now,
          created_at: company.created_at || now, // Preserve existing created_at or set new one
        });

        companiesProcessed++;
        setProgress((companiesProcessed / companiesToReGeocode.length) * 100);

        // Rate limit'e uymak için 500ms bekle (saniyede 2 istek)
        await delay(500);
      }
      
      const successfulUpdates = allUpdates.filter(u => u.koordinat);
      console.log(`6. Yeniden konumlandırma tamamlandı. ${successfulUpdates.length} başarılı.`);

      if (allUpdates.length > 0) {
        console.log('7. Veritabanı güncelleniyor...');
        const { error: updateError } = await supabase.from('companies').upsert(allUpdates);
        if (updateError) throw updateError;
        console.log('8. Veritabanı başarıyla güncellendi.');
      }

      setMessage({ type: 'success', text: `${conflictLocationCount} çakışma noktasında ${successfulUpdates.length} şirket başarıyla yeniden konumlandırıldı.` });
      refreshStats();

    } catch (error: any) {
      console.error('Error resolving conflicts:', error);
      setMessage({ type: 'error', text: `Çakışma çözülürken hata: ${error.message}` });
    } finally {
      setIsResolving(false);
      setProgress(0);
    }
  };

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
                <p className="text-2xl font-bold">{stats.total_companies}</p>
                <p className="text-sm text-muted-foreground">Toplam Firma</p>
              </div>
              <div>
                <p className="text-2xl font-bold text-green-600">{stats.with_coordinates}</p>
                <p className="text-sm text-muted-foreground">Koordinatlı</p>
              </div>
              <div>
                <p className="text-2xl font-bold text-red-600">{stats.without_coordinates}</p>
                <p className="text-sm text-muted-foreground">Koordinatsız</p>
              </div>
              <div>
                <p className="text-2xl font-bold text-orange-500">{stats.conflicts}</p>
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