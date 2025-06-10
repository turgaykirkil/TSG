'use client';

import { type FC, useState, useCallback } from 'react';
import { useDropzone, type FileRejection } from 'react-dropzone';
import { toast } from 'sonner';
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { MUDURLUKLER } from "@/lib/constants/mudurlukler";
import { processExcelFile, type ExcelProcessResult } from '@/lib/file-utils';
import type { CustomFile } from '@/lib/types/file.types';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';

// Dosya boyutunu formatlayan yardımcı fonksiyon
function formatFileSize(bytes: number): string {
  if (bytes === 0) return '0 Bytes';
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
};

const FileUploadSection: FC = () => {
  const [files, setFiles] = useState<CustomFile[]>([]);
  const [isProcessing, setIsProcessing] = useState(false);

  // Dosya durumunu güncelle
  const updateFileStatus = useCallback((
    fileId: string, 
    status: CustomFile['status'], 
    previewData?: ExcelProcessResult, 
    error?: string
  ) => {
    setFiles(prevFiles => 
      prevFiles.map(file => {
        if (file.id !== fileId) return file;
        
        const updatedFile = { ...file };
        updatedFile.status = status;
        updatedFile.error = error;
        updatedFile.progress = status === 'processing' ? 0 : 100;
        
        // Dosya boyutunu her zaman güncelle
        if (file.size) {
          updatedFile.formattedSize = formatFileSize(file.size);
        }
        
        if (previewData) {
          updatedFile.previewData = previewData;
        }
        
        return updatedFile;
      })
    );
  }, []);

  // Önizleme verisini güncelle
  const updateFilePreview = useCallback((fileId: string, previewData: ExcelProcessResult) => {
    setFiles(prevFiles => 
      prevFiles.map(file => 
        file.id === fileId ? { ...file, previewData } : file
      )
    );
  }, []);

  // Dosya yükleme işlemi
  const handleUpload = useCallback(async () => {
    if (files.length === 0) {
      toast.warning('Yüklenecek dosya bulunamadı');
      return;
    }

    setIsProcessing(true);
    
    try {
      // Başarılı durumdaki dosyaları filtrele
      const filesToUpload = files.filter(file => file.status === 'success');
      
      if (filesToUpload.length === 0) {
        toast.warning('Yüklenecek geçerli dosya bulunamadı');
        return;
      }
      
      // Her dosya için yükleme işlemi
      for (const file of filesToUpload) {
        try {
          // Burada API çağrısı yapılacak
          // Örnek: await api.uploadFile(file, file.müdürlük);
          
          // Simüle edilmiş yükleme
          await new Promise(resolve => setTimeout(resolve, 1000));
          
          toast.success(`${file.name} başarıyla yüklendi`);
          
          // Yükleme tamamlandıktan sonra dosyayı listeden kaldır
          setFiles(prev => prev.filter(f => f.id !== file.id));
          
        } catch (error) {
          const errorMessage = error instanceof Error ? error.message : 'Bilinmeyen bir hata oluştu';
          toast.error(`${file.name} yüklenirken hata: ${errorMessage}`);
        }
      }
      
      toast.success('Tüm dosyalar başarıyla yüklendi');
      
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Bilinmeyen bir hata oluştu';
      toast.error(`Dosya yüklenirken hata: ${errorMessage}`);
    } finally {
      setIsProcessing(false);
    }
  }, [files]);

  // Dosya işleme fonksiyonu
  const processFiles = useCallback(async (acceptedFiles: File[]) => {
    setIsProcessing(true);
    
    // Yeni dosyaları oluştur ve CustomFile tipine dönüştür
    const newFiles: CustomFile[] = acceptedFiles.map(file => {
      const customFile = Object.assign(file, {
        id: crypto.randomUUID(),
        status: 'waiting' as const,
        progress: 0,
        müdürlük: MUDURLUKLER[0]?.value || 'GENEL_MUDURLUK',
        uploadedAt: new Date(),
        formattedSize: formatFileSize(file.size),
        previewData: undefined
      }) as CustomFile;
      return customFile;
    });

    setFiles(prevFiles => [...prevFiles, ...newFiles]);

    // Her dosyayı sırayla işle
    for (const file of newFiles) {
      // Excel dosyasını işle
      const handleExcelProcessing = async (file: File): Promise<ExcelProcessResult> => {
        try {
          return await processExcelFile(file);
        } catch (error) {
          console.error('Excel işleme hatası:', error);
          throw error;
        }
      };

      try {
        updateFileStatus(file.id, 'processing');
        
        const result = await handleExcelProcessing(file);
        
        if (result.success) {
          updateFileStatus(file.id, 'success', result);
          updateFilePreview(file.id, result);
          toast.success(`${file.name} başarıyla işlendi`);
        } else {
          throw new Error(result.error || 'Dosya işlenirken bir hata oluştu');
        }
      } catch (error) {
        const errorMessage = error instanceof Error ? error.message : 'Bilinmeyen bir hata oluştu';
        updateFileStatus(file.id, 'error', undefined, errorMessage);
        toast.error(`${file.name} işlenirken hata: ${errorMessage}`);
      }
    }
    
    setIsProcessing(false);
  }, [updateFileStatus, updateFilePreview]);

  // Dropzone ayarları
  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop: (acceptedFiles: File[]) => {
      const excelFiles = acceptedFiles.filter(file => {
        const fileExt = (file.name.split('.').pop() || '').toLowerCase();
        return fileExt === 'xlsx' || fileExt === 'xls';
      });
      
      if (excelFiles.length > 0) {
        processFiles(excelFiles);
      } else if (acceptedFiles.length > 0) {
        toast.error('Lütfen sadece Excel (.xlsx, .xls) dosyaları yükleyin');
      }
    },
    accept: {
      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['.xlsx'],
      'application/vnd.ms-excel': ['.xls'],
      'application/excel': ['.xls'],
      'application/vnd.ms-office': ['.xls']
    } as const,
    multiple: true,
    disabled: isProcessing,
    noClick: false,
    noKeyboard: false,
    maxSize: 10 * 1024 * 1024, // 10MB
    onDropRejected: (fileRejections: FileRejection[]) => {
      fileRejections.forEach(({ file, errors }) => {
        errors.forEach(err => {
          if (err.code === 'file-too-large') {
            toast.error(`${file.name} dosyası çok büyük. Maksimum dosya boyutu 10MB olabilir.`);
          } else if (err.code === 'file-invalid-type') {
            toast.error(`${file.name} geçersiz dosya türü. Sadece Excel dosyaları kabul edilir.`);
          } else {
            toast.error(`${file.name} yüklenirken hata: ${err.message}`);
          }
        });
      });
    }
  });

  // Dosya kaldır
  const removeFile = useCallback((fileId: string) => {
    setFiles(prevFiles => {
      const fileToRemove = prevFiles.find(f => f.id === fileId);
      if (fileToRemove) {
        toast.success(`${fileToRemove.name} kaldırıldı`);
      }
      return prevFiles.filter(file => file.id !== fileId);
    });
  }, []);

  return (
    <div className="space-y-6">
      <div 
        {...getRootProps()} 
        className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors ${
          isDragActive ? 'border-blue-500 bg-blue-50' : 'border-gray-300 hover:border-gray-400'
        }`}
      >
        <input {...getInputProps()} />
        <div className="flex flex-col items-center justify-center space-y-2">
          <svg 
            className="h-12 w-12 text-gray-400" 
            fill="none" 
            viewBox="0 0 24 24" 
            stroke="currentColor"
          >
            <path 
              strokeLinecap="round" 
              strokeLinejoin="round" 
              strokeWidth={2} 
              d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" 
            />
          </svg>
          <p className="text-sm text-gray-600">
            {isDragActive 
              ? 'Dosyaları buraya bırakın...' 
              : 'Dosyaları sürükleyip bırakın veya tıklayarak seçin'}
          </p>
          <p className="text-xs text-gray-500">
            Sadece Excel dosyaları (.xlsx, .xls) - Maksimum 10MB
          </p>
        </div>
      </div>

      {/* Yüklenen dosyaların listesi */}
      {files.length > 0 && (
        <div className="space-y-4">
          <h3 className="text-lg font-medium">Yüklenen Dosyalar ({files.length})</h3>
          <div className="space-y-3">
            {files.map(file => (
              <div 
                key={file.id} 
                className="border rounded-lg p-4 hover:bg-gray-50 transition-colors"
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center space-x-2">
                      <span className="font-medium truncate">{file.name}</span>
                      <span className="text-xs text-gray-500">({file.formattedSize})</span>
                      {file.status === 'processing' && (
                        <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-blue-100 text-blue-800">
                          İşleniyor...
                        </span>
                      )}
                      {file.status === 'success' && (
                        <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-green-100 text-green-800">
                          Başarılı
                        </span>
                      )}
                      {file.status === 'error' && (
                        <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-red-100 text-red-800">
                          Hata
                        </span>
                      )}
                    </div>
                    
                    {file.status === 'processing' && (
                      <div className="mt-2">
                        <Progress value={file.progress} className="h-2" />
                      </div>
                    )}
                    
                    {file.status === 'error' && file.error && (
                      <p className="mt-1 text-sm text-red-600">{file.error}</p>
                    )}
                    
                    {file.previewData?.sheets && file.previewData.sheets.length > 0 && (
                      <div className="mt-2 text-sm text-gray-600">
                        <p>
                          {file.previewData.sheets.length} sayfadan toplam {
                            file.previewData.sheets.reduce((total, sheet) => {
                              const rowCount = sheet?.rows?.length ?? 0;
                              return total + (Number.isFinite(rowCount) ? rowCount : 0);
                            }, 0)
                          } satır okundu
                        </p>
                      </div>
                    )}
                  </div>
                  
                  <div className="flex flex-col sm:flex-row items-end sm:items-center space-y-2 sm:space-y-0 sm:space-x-2 ml-4">
                    {/* Müdürlük seçimi */}
                    <div className="w-full sm:w-64">
                      <Select 
                        value={file.müdürlük} 
                        onValueChange={(value) => {
                          setFiles(prev => prev.map(f => 
                            f.id === file.id ? { ...f, müdürlük: value } : f
                          ));
                        }}
                        disabled={file.status === 'processing'}
                      >
                        <SelectTrigger>
                          <SelectValue placeholder="Müdürlük seçin" />
                        </SelectTrigger>
                        <SelectContent>
                          {MUDURLUKLER.map(mudurluk => (
                            <SelectItem key={mudurluk.value} value={mudurluk.value}>
                              {mudurluk.label}
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                    </div>
                    
                    <Button 
                      variant="ghost" 
                      size="sm" 
                      onClick={(e) => {
                        e.stopPropagation();
                        removeFile(file.id);
                      }}
                      disabled={file.status === 'processing'}
                      className="text-red-600 hover:bg-red-50"
                    >
                      Kaldır
                    </Button>
                  </div>
                </div>
              </div>
            ))}
          </div>
          
          <div className="flex flex-col sm:flex-row justify-end space-y-2 sm:space-y-0 sm:space-x-3 pt-4">
            <Button 
              variant="outline" 
              onClick={() => {
                toast.success('Tüm dosyalar temizlendi');
                setFiles([]);
              }}
              disabled={isProcessing}
              className="w-full sm:w-auto"
            >
              Tümünü Temizle
            </Button>
            <Button 
              onClick={handleUpload}
              disabled={isProcessing || files.length === 0}
              className="w-full sm:w-auto"
            >
              {isProcessing ? 'Yükleniyor...' : 'Yükle'}
            </Button>
          </div>
        </div>
      )}

      {/* Dosya Önizleme */}
      {files.map((file) => (
        <div key={file.id} className="mt-6">
          <h3 className="text-lg font-medium mb-2">{file.name} - Önizleme</h3>
          {file.previewData?.success && file.previewData.sheets.length > 0 ? (
            <div className="space-y-6">
              {file.previewData.sheets.map((sheet, sheetIndex) => (
                <div key={sheetIndex} className="border rounded-md overflow-hidden">
                  <div className="bg-gray-50 px-4 py-2 border-b">
                    <h4 className="text-md font-medium">
                      Sayfa: {sheet.sheetName || 'Bilinmeyen'} (Toplam {sheet.rows?.length ?? 0} satır, {sheet.headers?.length ?? 0} sütun)
                    </h4>
                  </div>
                  <div className="overflow-auto max-h-96">
                    <table className="w-full text-sm">
                      <thead>
                        <tr className="bg-gray-100">
                          {sheet.headers.map((header, index) => (
                            <th 
                              key={index} 
                              className="px-4 py-2 text-left font-medium text-gray-700 whitespace-nowrap"
                            >
                              {header || `Sütun ${index + 1}`}
                            </th>
                          ))}
                        </tr>
                      </thead>
                      <tbody>
                        {sheet.rows.slice(0, 5).map((row, rowIndex) => (
                          <tr key={rowIndex} className="border-t">
                            {sheet.headers.map((header, colIndex) => (
                              <td key={colIndex} className="px-4 py-2 text-sm">
                                {row[header] !== undefined && row[header] !== null ? 
                                  String(row[header]).slice(0, 100) : 
                                  ''
                                }
                              </td>
                            ))}
                          </tr>
                        ))}
                        {sheet.rows.length > 5 && (
                          <tr>
                            <td colSpan={sheet.headers?.length ?? 1} className="text-center py-2 text-sm text-gray-500">
                              Toplam {sheet.rows?.length || 0} satırdan ilk 5 gösteriliyor
                            </td>
                          </tr>
                        )}
                      </tbody>
                    </table>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-sm text-gray-500">Önizleme mevcut değil</p>
          )}
        </div>
      ))}
    </div>
  );
};

export default FileUploadSection;