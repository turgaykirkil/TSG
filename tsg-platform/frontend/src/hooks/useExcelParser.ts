import { useState, useCallback } from 'react';
import { useDropzone, type FileRejection } from 'react-dropzone';
import { toast } from 'sonner';
import type { ExcelProcessResult } from '@/lib/file-utils';

// Web worker'ın sunucu tarafında çalışmasını engellemek için kontrol
const isBrowser = typeof window !== 'undefined';

/**
 * Excel dosyalarını işlemek için `react-dropzone` ve bir Web Worker kullanan özel hook.
 * Dosya seçme, işleme durumunu yönetme ve sonuçları döndürme mantığını kapsar.
 */
export const useExcelParser = () => {
  const [processedData, setProcessedData] = useState<(ExcelProcessResult & { fileId: string }) | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const parseExcelViaWorker = useCallback((file: File, fileId: string): Promise<ExcelProcessResult> => {
    return new Promise((resolve) => {
      if (!isBrowser) {
        resolve({ success: false, fileName: file.name, sheets: [], error: 'Web Worker bu ortamda mevcut değil.' });
        return;
      }
      
      const worker = new Worker(new URL('../workers/excelParser.worker.ts', import.meta.url));
      worker.postMessage({ fileId, file });
      
      worker.onmessage = (event: MessageEvent<{ fileId: string; result: ExcelProcessResult }>) => {
        const { result } = event.data;
        worker.terminate();
        resolve(result);
      };
      
      worker.onerror = (err) => {
        worker.terminate();
        resolve({ success: false, fileName: file.name, sheets: [], error: err.message });
      };
    });
  }, []);

  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    if (acceptedFiles.length === 0) return;
    
    const file = acceptedFiles[0];
    const fileId = `${file.name}-${file.lastModified}`;

    setIsProcessing(true);
    setError(null);
    setProcessedData(null);
    
    toast.info(`'${file.name}' işleniyor...`);

    const result = await parseExcelViaWorker(file, fileId);

    if (result.success) {
      toast.success(`'${file.name}' başarıyla işlendi.`);
      setProcessedData({ ...result, fileId });
    } else {
      const errorMessage = result.error || 'Bilinmeyen bir hata oluştu.';
      toast.error(`'${file.name}' işlenirken hata oluştu: ${errorMessage}`);
      setError(errorMessage);
    }
    
    setIsProcessing(false);
  }, [parseExcelViaWorker]);

  const onDropRejected = useCallback((fileRejections: FileRejection[]) => {
    fileRejections.forEach(({ file, errors }) => {
      errors.forEach(err => {
        if (err.code === 'file-too-large') {
          toast.error(`Dosya çok büyük: ${file.name}. Maksimum boyut 10MB.`);
        } else {
          toast.error(`${file.name}: ${err.message}`);
        }
      });
    });
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    onDropRejected,
    accept: {
      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['.xlsx'],
      'application/vnd.ms-excel': ['.xls'],
    },
    maxSize: 10 * 1024 * 1024, // 10MB
    multiple: false,
  });

  const reset = useCallback(() => {
    setProcessedData(null);
    setIsProcessing(false);
    setError(null);
  }, []);

  return {
    isProcessing,
    processedData,
    error,
    getRootProps,
    getInputProps,
    isDragActive,
    reset,
  };
};
