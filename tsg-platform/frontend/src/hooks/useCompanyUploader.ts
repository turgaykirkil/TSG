import { useState, useCallback } from 'react';
import { toast } from 'sonner';
import { supabase } from '@/lib/supabaseClient';
import { type CompanyData } from '@/types/company.types';

export const useCompanyUploader = () => {
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [progress, setProgress] = useState(0);
  const [isSuccess, setIsSuccess] = useState(false);

  const upload = useCallback(async (companies: CompanyData[], sicilMudurluk: string, onSuccess?: () => void) => {
    console.log(`[Uploader] Upload started. Companies count: ${companies.length}, Directorate: ${sicilMudurluk}`);
    if (!companies || companies.length === 0) {
      toast.warning('Yüklenecek şirket verisi bulunamadı.');
      console.warn('[Uploader] Upload function called with no companies.');
      return;
    }
    if (!sicilMudurluk) {
        toast.warning('Lütfen bir Sicil Müdürlüğü seçin.');
        console.warn('[Uploader] Upload function called with no directorate.');
        setIsUploading(false); // Yükleme durumunu sıfırla
        return;
    }

    setIsUploading(true);
    setError(null);
    setProgress(0);
    setIsSuccess(false);

    try {
      setProgress(10);
      
      const companiesToUpload = companies.map(company => ({
        ...company,
        sicil_mudurluk: sicilMudurluk,
        created_at: company.created_at || new Date().toISOString(),
      }));

      console.log('[Uploader] Connecting to Supabase for upsert...');
      const { data, error: uploadError } = await supabase
        .from('companies')
        .upsert(companiesToUpload, { onConflict: 'sicil_no' })
        .select();
      
      setProgress(80);
      console.log('[Uploader] Supabase upsert operation completed.');

      if (uploadError) {
        console.error('[Uploader] Supabase error object:', uploadError);
        throw uploadError;
      }

      setProgress(100);
      setIsSuccess(true);
      toast.success(`${companies.length} şirket verisi başarıyla yüklendi/güncellendi.`);
      console.log('[Uploader] Upload successful.');

      if (onSuccess) {
        console.log('[Uploader] Executing onSuccess callback.');
        onSuccess();
      }

    } catch (e: unknown) {
      console.error('[Uploader] Full error during Supabase upload:', e);
      let errorMessage = 'Veri yüklenirken bir hata oluştu.';
      if (e instanceof Error) {
        if (e.message.includes('violates not-null constraint')) {
            errorMessage = 'Veritabanı hatası: Gerekli bir alan eksik. Lütfen tekrar deneyin.';
        } else if (e.message.includes('check constraint')) {
            errorMessage = 'Veri doğrulama hatası. Lütfen girdiğiniz verileri kontrol edin.';
        }
      }
      setError(errorMessage);
      toast.error(`Yükleme Başarısız: ${errorMessage}`);
    } finally {
      console.log('[Uploader] Upload process finished. Resetting isUploading state.');
      setIsUploading(false);
    }
  }, []);
  
  const resetUploader = useCallback(() => {
      console.log('[Uploader] Resetting uploader state.');
      setIsUploading(false);
      setError(null);
      setProgress(0);
      setIsSuccess(false);
  }, []);

  return {
    upload,
    isUploading,
    error,
    progress,
    isSuccess,
    resetUploader,
  };
};
