import { useState, useCallback } from 'react';
import { toast } from 'sonner';
import { supabase } from '@/lib/supabaseClient';
import { type Company } from '@/types/company.types';

export const useCompanyUploader = () => {
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [progress, setProgress] = useState(0);
  const [isSuccess, setIsSuccess] = useState(false);

  const upload = useCallback(async (companies: Company[], sicilMudurluk: string, onSuccess?: () => void) => {
    console.log(`[Uploader] Upload started. Companies count: ${companies.length}, Directorate: ${sicilMudurluk}`);
    if (!companies || companies.length === 0) {
      toast.warning('Yüklenecek şirket verisi bulunamadı.');
      return;
    }
    if (!sicilMudurluk) {
      toast.warning('Lütfen bir Sicil Müdürlüğü seçin.');
      return;
    }

    setIsUploading(true);
    setError(null);
    setProgress(0);
    setIsSuccess(false);

    const BATCH_SIZE = 100;
    let totalUploaded = 0;
    let totalFailed = 0;

    try {
      for (let i = 0; i < companies.length; i += BATCH_SIZE) {
        const batch = companies.slice(i, i + BATCH_SIZE).map(company => ({
          ...company,
          sicil_mudurluk: sicilMudurluk,
          created_at: company.created_at || new Date().toISOString(),
        }));

        try {
          const { error: batchError } = await supabase
            .from('companies')
            .upsert(batch, { onConflict: 'sicil_no' });

          if (batchError) {
            console.warn(`[Uploader] Batch (from index ${i}) failed. Retrying individually.`, batchError);
            toast.warning(`Bir grup veri yüklenemedi, tek tek deneniyor... (Kayıt ${i})`);
            // Retry individually
            for (const company of batch) {
              const { error: individualError } = await supabase
                .from('companies')
                .upsert(company, { onConflict: 'sicil_no' });

              if (individualError) {
                console.error(`[Uploader] Failed to upload individual company: ${company.sicil_no}`, individualError);
                totalFailed++;
              } else {
                totalUploaded++;
              }
            }
          } else {
            totalUploaded += batch.length;
          }

        } catch (e) {
            console.error(`[Uploader] Critical error during batch (from index ${i}).`, e);
            totalFailed += batch.length; // Assume whole batch failed on critical error
        }

        setProgress(Math.round(((i + batch.length) / companies.length) * 100));
      }

      setIsSuccess(true);
      toast.success(`Yükleme tamamlandı. Başarılı: ${totalUploaded}, Başarısız: ${totalFailed}`);
      if (onSuccess) onSuccess();

    } catch (e: unknown) {
      const errorMessage = 'Yükleme sırasında beklenmedik bir hata oluştu.';
      console.error('[Uploader] Unrecoverable error during upload process:', e);
      setError(errorMessage);
      toast.error(errorMessage);
    } finally {
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
