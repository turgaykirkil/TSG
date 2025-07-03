'use client';

'use client';

import { useState, useCallback } from 'react';
import { useDropzone, type Accept, type FileRejection } from 'react-dropzone';
import { toast } from 'sonner';
import { processExcelFile, type ProcessedFileData } from '@/lib/file-utils';
import { usePDFParser, type ParsedTable } from './usePDFParser';

// Re-exporting types for easier import in components
export type { ProcessedFileData, ParsedTable };

const ACCEPTED_FILE_TYPES: Accept = {
  'application/vnd.ms-excel': ['.xls'],
  'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['.xlsx'],
  'application/pdf': ['.pdf'],
};

const MAX_FILE_SIZE = 15 * 1024 * 1024; // 15MB

export const useFileProcessor = () => {
  // State for Excel processing
  const [excelData, setExcelData] = useState<ProcessedFileData | null>(null);
  const [isProcessingExcel, setIsProcessingExcel] = useState(false);
  const [excelProgress, setExcelProgress] = useState(0);
  
  // PDF Parser Hook
  const pdfParser = usePDFParser();

  // General state
  const [error, setError] = useState<string | null>(null);
  const [currentFiles, setCurrentFiles] = useState<File[]>([]);

  const reset = useCallback(() => {
    setExcelData(null);
    setIsProcessingExcel(false);
    setExcelProgress(0);
    pdfParser.reset();
    setError(null);
    setCurrentFiles([]);
  }, [pdfParser]);

  const onDrop = useCallback(
    async (acceptedFiles: File[]) => {
      if (acceptedFiles.length === 0) return;

      reset();
      setCurrentFiles(acceptedFiles);

      const pdfFiles = acceptedFiles.filter(
        (f) => f.type === 'application/pdf' || f.name.toLowerCase().endsWith('.pdf')
      );

      const excelFiles = acceptedFiles.filter(
        (f) =>
          f.type === 'application/vnd.ms-excel' ||
          f.type === 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' ||
          f.name.toLowerCase().endsWith('.xls') ||
          f.name.toLowerCase().endsWith('.xlsx')
      );

      if (pdfFiles.length > 0 && excelFiles.length > 0) {
        toast.error('Lütfen aynı anda yalnızca PDF veya yalnızca Excel dosyaları yükleyin.');
        reset();
        return;
      }

      // --- PDF Processing Path ---
      if (pdfFiles.length > 0) {
        pdfParser.parsePdf(pdfFiles);
        return;
      }

      // --- Excel Processing Path (only process the first Excel file for now) ---
      if (excelFiles.length > 0) {
        if (excelFiles.length > 1) {
          toast.info('Şu anda yalnızca ilk Excel dosyası işlenecektir.');
        }
        const fileToProcess = excelFiles[0];
        setIsProcessingExcel(true);
        try {
          const progressInterval = setInterval(() => {
            setExcelProgress((prev) => (prev >= 95 ? 95 : prev + 5));
          }, 300);

          const result = await processExcelFile(fileToProcess);
          clearInterval(progressInterval);
          setExcelProgress(100);

          if (result.success) {
            setExcelData({
              fileName: result.fileName,
              sheets: result.sheets,
            });
            toast.success(`'${result.fileName}' başarıyla işlendi.`);
          } else {
            throw new Error(result.error || 'Dosya işlenirken bilinmeyen bir hata oluştu.');
          }
        } catch (e: unknown) {
          const errorMessage = e instanceof Error ? e.message : 'Dosya işlenemedi.';
          setError(errorMessage);
          toast.error(`Hata: ${errorMessage}`);
        } finally {
          setIsProcessingExcel(false);
        }
        return;
      }
      
      toast.error('Desteklenmeyen dosya türü. Lütfen .xls, .xlsx veya .pdf dosyası seçin.');
    },
    [reset, pdfParser]
  );

  const onDropRejected = useCallback((fileRejections: FileRejection[]) => {
    const rejection = fileRejections[0];
    if (!rejection) return;

    const { errors } = rejection;
    if (errors[0].code === 'file-too-large') {
      toast.error(`Dosya boyutu çok büyük. Maksimum ${MAX_FILE_SIZE / 1024 / 1024}MB olmalıdır.`);
    } else if (errors[0].code === 'file-invalid-type') {
      toast.error('Geçersiz dosya türü. Lütfen .xls, .xlsx veya .pdf dosyası seçin.');
    } else {
      toast.error(errors[0].message);
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    onDropRejected,
    accept: ACCEPTED_FILE_TYPES,
    maxSize: MAX_FILE_SIZE,
    multiple: true,
  });

  // Consolidate processing states and errors
  const isProcessing = isProcessingExcel || pdfParser.isLoading;
  const combinedError = error || pdfParser.error?.message || null;

  return {
    // Core props
    getRootProps,
    getInputProps,
    isDragActive,
    reset,
    currentFiles,

    // Overall status
    isProcessing,
    error: combinedError,

    // Excel specific
    excelData,
    isProcessingExcel,
    excelProgress,

    // PDF specific
    pdfData: pdfParser.parsedTables,
    isProcessingPdf: pdfParser.isLoading,
    isPdfSuccess: pdfParser.isSuccess,
  };
};
