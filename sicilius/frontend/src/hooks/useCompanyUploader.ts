import { useState, useCallback } from 'react';
import { toast } from 'sonner';

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

        const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5001';

    try {
      for (let i = 0; i < companies.length; i += BATCH_SIZE) {
        const batch = companies.slice(i, i + BATCH_SIZE).map(company => ({
          sicil_no: company.sicil_no,
          firma_unvani: company.firma_unvani,
          adres: company.adres,
          sicil_mudurluk: sicilMudurluk,
        }));

                const response = await fetch(`${apiUrl}/api/v1/parsing/companies/save`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ companies: batch }),
        });

        if (response.ok) {
          const result = await response.json();
          totalUploaded += result.processed_rows || batch.length;
        } else {
          const errorData = await response.json();
          console.error(`[Uploader] Batch (from index ${i}) failed.`, errorData.detail);
          toast.error(`Bir grup veri yüklenemedi: ${errorData.detail || 'Bilinmeyen hata'}`);
          totalFailed += batch.length;
        }
        
        setProgress(Math.round(((i + batch.length) / companies.length) * 100));
      }

      setIsSuccess(totalFailed === 0);
      if (totalFailed > 0) {
        toast.error(`Yükleme tamamlandı. Başarılı: ${totalUploaded}, Başarısız: ${totalFailed}`);
      } else {
        toast.success(`Yükleme başarıyla tamamlandı. Toplam ${totalUploaded} kayıt işlendi.`);
      }
      if (onSuccess && totalFailed === 0) onSuccess();

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
