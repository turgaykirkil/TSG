// Force re-render to clear stale cache
'use client';

import { useState, useCallback } from 'react';
import { supabase } from '@/lib/supabaseClient';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Icons } from '@/components/icons';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import { Input } from '@/components/ui/input';
import LoadingSpinner from '@/components/ui/loading-spinner';
import { geocodeAddress, GeocodeResult } from '@/lib/geocode';

// Define the props for the component
interface CoordinatesDashboardProps {
  stats: {
    totalCompanies: number;
    withCoordinates: number;
  };
  refreshStats: () => void;
}

// The GeocodeResult interface is now defined in @/lib/geocode.ts

/**
 * Cleans and simplifies a raw address string to improve geocoding accuracy.
 * This function applies a multi-step process:
 * 1. Normalizes Turkish characters and converts to lowercase.
 * 2. Strips common company type suffixes (e.g., 'anonim şirketi') and other noise words.
 * 3. Removes generic address-related keywords (e.g., 'mahallesi', 'caddesi', 'sokak').
 * 4. Cleans up punctuation and consolidates whitespace.
 * 5. Adds a country context for the final query.
 */
const simplifyAddress = (address: string): string => {
  if (!address) return '';

  // 1. Use Unicode normalization to decompose combined characters (like 'i̇') and remove diacritics.
  // This is more robust than simple character replacement.
  let simplified = address
    .toLowerCase()
    .normalize('NFD') // Decompose characters (e.g., 'ö' -> 'o' + '¨')
    .replace(/[\u0300-\u036f]/g, ''); // Remove diacritical marks

  // 2. Remove common company type suffixes (using the normalized form)
  const companyNoise = /\b(a\.s\.|anonim sirketi|as|ltd\. sti\.|limited sirketi|ltd sti|sanayi ve ticaret|ticaret|sanayi|kuyumculuk|insaat|otomotiv|turizm|gida|tekstil|ithalat|ihracat|danismanlik|yonetim|gayrimenkul|emlak|mucevherat|pazarlama)\b/gi;
  simplified = simplified.replace(companyNoise, '');

  // 3. Remove generic address keywords (noise, using the normalized form)
  const addressNoise = /\b(apt|apartmani|mah|mahallesi|cad|caddesi|sok|sokak|sk|bulvari|blv|is merkezi|hani|han|sitesi|ic kapi|dis kapi|koyu|ilcesi|no|kat|daire)\b/gi;
  simplified = simplified.replace(addressNoise, '');

  // 4. Remove punctuation and special characters, then clean up whitespace
  simplified = simplified.replace(/[.,:;]/g, ' '); // Replace punctuation with space
  simplified = simplified.replace(/[/]/g, ' '); // Treat slashes as spaces
  simplified = simplified.replace(/\s+/g, ' ').trim();

  // 5. Add country context if not present
  if (!/turkey|türkiye/i.test(simplified)) {
    simplified = `${simplified}, turkey`;
  }

  return simplified;
};

const CoordinatesDashboard = ({ stats, refreshStats }: CoordinatesDashboardProps) => {
  const [isLoading, setIsLoading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [totalToFetch, setTotalToFetch] = useState(0);
  const [message, setMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null);
  const [fetchLimit, setFetchLimit] = useState(100);

  const withoutCoordinates = stats.totalCompanies - stats.withCoordinates;

  const handleFetchCoordinates = useCallback(async () => {
    setIsLoading(true);
    setMessage(null);
    setProgress(0);

    try {
      // 1. SORGUNUN GÜNCELLENMESİ: Sadece koordinatı ve deneme zamanı olmayanları getir
      const { data: companies, error: fetchError } = await supabase
        .from('companies')
        .select('id, firma_unvani, adres')
        .is('koordinat', null)
        .is('geocode_attempted_at', null) // Yeni koşul
        .limit(fetchLimit);

      if (fetchError) throw fetchError;

      if (!companies || companies.length === 0) {
        setMessage({
          type: 'success',
          text: 'Koordinat getirilecek yeni firma bulunmuyor. Tüm firmalar işlenmiş veya koordinatları mevcut.',
        });
        setIsLoading(false);
        return;
      }

      console.log('[GEO-DEBUG] Veritabanından çekilecek firma sayısı:', companies.length);
      setTotalToFetch(companies.length);
      let successCount = 0;
      let notFoundCount = 0;
      let skippedCount = 0;
      let errorCount = 0;

      for (let i = 0; i < companies.length; i++) {
        const company = companies[i];
        const now = new Date().toISOString();

        if (!company.adres || company.adres.trim() === '') {
          console.log(`[GEO-SKIP] ID ${company.id}: Adres boş, denendi olarak işaretleniyor.`);
          skippedCount++;
          // Adres boş olsa bile denendi olarak işaretle ki tekrar sorgulanmasın
          await supabase.from('companies').update({ geocode_attempted_at: now }).eq('id', company.id);
          setProgress(i + 1);
          continue;
        }

        const simplifiedAddress = simplifyAddress(company.adres);
        console.log(`[GEO-QUERY] ID ${company.id}: "${simplifiedAddress}"`);

        try {
          const result = await geocodeAddress(simplifiedAddress);

          if (result) { // Check if a result was returned (not null)
            console.log(`[GEO-SUCCESS] ID ${company.id}: Koordinatlar bulundu -> ${result.latitude}, ${result.longitude}`);
            // 2. BAŞARILI DURUM: Hem koordinatı hem de deneme zamanını kaydet
            await supabase
              .from('companies')
              .update({
                koordinat: `POINT(${result.longitude} ${result.latitude})`, // Use correct properties
                geocode_attempted_at: now,
              })
              .eq('id', company.id);
            successCount++;
          } else { // result is null, geocoding failed
            console.warn(`[GEO-NOT-FOUND] ID ${company.id}: Adres bulunamadı, denendi olarak işaretleniyor.`);
            notFoundCount++;
            // 3. BAŞARISIZ DURUM: Sadece deneme zamanını kaydet
            await supabase.from('companies').update({ geocode_attempted_at: now }).eq('id', company.id);
          }
        } catch (apiError: any) {
          console.error(`[GEO-ERROR] ID ${company.id}: API hatası. Bu kayıt daha sonra tekrar denenecek.`, apiError.message);
          // API hatası durumunda denendi olarak İŞARETLEME, sonraki çalıştırmada tekrar denensin.
          errorCount++;
        }

        setProgress(i + 1);
      }

      const summaryText = `İşlem tamamlandı. Başarılı: ${successCount}, Bulunamadı (işaretlendi): ${notFoundCount}, Atlandı (işaretlendi): ${skippedCount}, Hata (tekrar denenecek): ${errorCount}.`;
      setMessage({ type: 'success', text: summaryText });
      refreshStats();

    } catch (error: any) {
      console.error('Koordinat getirme işlemi sırasında genel bir hata oluştu:', error);
      setMessage({ type: 'error', text: `Genel Hata: ${error.message}` });
    } finally {
      setIsLoading(false);
    }
  }, [fetchLimit, refreshStats]);

  return (
    <div>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Koordinatı Olan Firmalar</CardTitle>
            <Icons.mapPin className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.withCoordinates.toLocaleString('tr-TR')}</div>
            <p className="text-xs text-muted-foreground">
              Toplam {stats.totalCompanies.toLocaleString('tr-TR')} firmanın %{stats.totalCompanies > 0 ? ((stats.withCoordinates / stats.totalCompanies) * 100).toFixed(1) : 0}
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Koordinatı Olmayan Firmalar</CardTitle>
            <Icons.mapPinOff className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{withoutCoordinates.toLocaleString('tr-TR')}</div>
             <p className="text-xs text-muted-foreground">
              Koordinat bilgisi eksik olan firmalar
            </p>
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Toplu Koordinat Ekleme</CardTitle>
          <p className="text-sm text-muted-foreground">
            Adres bilgilerini kullanarak koordinatı eksik olan firmaların coğrafi konum verilerini otomatik olarak getirin.
            Bu işlem firma sayısına göre uzun sürebilir.
          </p>
        </CardHeader>
        <CardContent>
          {message && (
            <Alert variant={message.type === 'error' ? 'destructive' : 'success'} className="mb-4">
              <AlertTitle>{message.type === 'error' ? 'Hata!' : 'Başarılı!'}</AlertTitle>
              <AlertDescription>{message.text}</AlertDescription>
            </Alert>
          )}

          {isLoading ? (
            <div className="flex flex-col items-center justify-center">
              <LoadingSpinner />
              <p className="mt-2 text-sm text-muted-foreground">
                Koordinatlar getiriliyor... ({progress} / {totalToFetch})
              </p>
              <div className="w-full bg-muted rounded-full h-2.5 mt-2">
                <div className="bg-primary h-2.5 rounded-full" style={{ width: `${totalToFetch > 0 ? (progress / totalToFetch) * 100 : 0}%` }}></div>
              </div>
            </div>
          ) : (
            <div className="flex items-center space-x-2">
              <Input
                type="number"
                value={fetchLimit}
                onChange={(e) => setFetchLimit(Math.max(1, parseInt(e.target.value, 10) || 1))}
                className="max-w-[100px]"
                min="1"
              />
              <Button onClick={handleFetchCoordinates} disabled={isLoading || withoutCoordinates === 0}>
                {isLoading ? <Icons.spinner className="mr-2 h-4 w-4 animate-spin" /> : <Icons.download className="mr-2 h-4 w-4" />}
                Getir
              </Button>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
};

export default CoordinatesDashboard;
