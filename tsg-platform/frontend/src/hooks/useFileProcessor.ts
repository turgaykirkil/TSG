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
  const [currentFile, setCurrentFile] = useState<File | null>(null);

  const reset = useCallback(() => {
    setExcelData(null);
    setIsProcessingExcel(false);
    setExcelProgress(0);
    pdfParser.reset();
    setError(null);
    setCurrentFile(null);
  }, [pdfParser]);

  const onDrop = useCallback(
    async (acceptedFiles: File[]) => {
      if (acceptedFiles.length === 0) return;
      const file = acceptedFiles[0];

      reset();
      setCurrentFile(file);

      const fileType = file.type;
      const fileName = file.name.toLowerCase();

      // --- PDF Processing Path ---
      if (fileType === 'application/pdf' || fileName.endsWith('.pdf')) {
        pdfParser.parsePdf(file);
        return;
      }

      // --- Excel Processing Path ---
      if (
        fileType === 'application/vnd.ms-excel' ||
        fileType === 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' ||
        fileName.endsWith('.xls') ||
        fileName.endsWith('.xlsx')
      ) {
        setIsProcessingExcel(true);
        try {
          const progressInterval = setInterval(() => {
            setExcelProgress((prev) => (prev >= 95 ? 95 : prev + 5));
          }, 300);

          const result = await processExcelFile(file);
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
      
      // Should not happen if dropzone config is correct
      toast.error('Desteklenmeyen dosya türü.');

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
    multiple: false,
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
    currentFile,

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
