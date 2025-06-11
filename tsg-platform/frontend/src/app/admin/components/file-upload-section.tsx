'use client';

import { type FC, useState, useCallback } from 'react';
import { useDropzone, type FileRejection } from 'react-dropzone';
import { batchCreateCompanies } from '@/lib/api/companyScrape';
import { toast } from 'sonner';
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { MUDURLUKLER } from "@/lib/constants/mudurlukler";
import { processExcelFile, type ExcelProcessResult, type ExcelSheetResult } from '@/lib/file-utils';
import type { CustomFile } from '@/lib/types/file.types';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { ColumnTypeModal } from './column-type-modal';

// Dosya boyutunu formatlayan yardımcı fonksiyon
function formatFileSize(bytes: number): string {
  if (bytes === 0) return '0 Bytes';
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

type HeaderSelection = {
  sheetName: string;
  columnName: string;
  columnType: 'sicil_no' | 'firma_unvani' | 'none';
};

const FileUploadSection: FC = () => {
  const [files, setFiles] = useState<CustomFile[]>([]);
  const [isProcessing, setIsProcessing] = useState(false);
  const [selectedHeader, setSelectedHeader] = useState<{sheetName: string; columnName: string} | null>(null);
  const [headerSelections, setHeaderSelections] = useState<Record<string, HeaderSelection[]>>({});

  // Seçili sütun türünü döndür
  const getColumnType = (sheetName: string, columnName: string): string => {
    const selection = headerSelections[sheetName]?.find(
      sel => sel.columnName === columnName
    );
    return selection?.columnType || 'none';
  };

  // Başlık için stil sınıfını döndür
  const getHeaderClassName = (sheetName: string, columnName: string): string => {
    const type = getColumnType(sheetName, columnName);
    const baseClasses = 'px-4 py-2 text-left text-xs font-medium uppercase tracking-wider cursor-pointer transition-colors duration-200';
    
    if (type === 'sicil_no') {
      return `${baseClasses} bg-blue-50 text-blue-700 hover:bg-blue-100 dark:bg-blue-900/30 dark:text-blue-300 dark:hover:bg-blue-900/50`;
    } else if (type === 'firma_unvani') {
      return `${baseClasses} bg-green-50 text-green-700 hover:bg-green-100 dark:bg-green-900/30 dark:text-green-300 dark:hover:bg-green-900/50`;
    }
    
    return `${baseClasses} text-gray-500 hover:bg-gray-100 dark:text-gray-400 dark:hover:bg-gray-700`;
  };

  // Seçilen başlıklardaki değerleri işle ve veritabanına kaydet
  const processAndSaveSelectedColumns = async () => {
    if (!files.length || isProcessing) return;
    
    let totalSaved = 0;
    
    try {
      setIsProcessing(true);
      
      for (const file of files) {
        const sheets = file.previewData?.sheets || [];
        const combinedSheet = sheets.length > 1 ? combineAllSheets(sheets) : sheets[0];
        
        if (!combinedSheet || !combinedSheet.rows?.length) continue;
        
        // Seçili başlıkları bul
        const selectedColumns = headerSelections[combinedSheet.sheetName] || [];
        if (selectedColumns.length === 0) continue;
        
        // Sicil No ve Firma Ünvanı sütunlarını ayırt et
        const sicilNoColumn = selectedColumns.find(col => col.columnType === 'sicil_no');
        const firmaUnvaniColumn = selectedColumns.find(col => col.columnType === 'firma_unvani');
        
        if (!sicilNoColumn) {
          console.warn('Sicil No sütunu seçili değil');
          continue;
        }
        
        // Verileri hazırla
        const companiesToSave = [];
        
        for (const row of combinedSheet.rows) {
          const sicilNo = row[sicilNoColumn.columnName]?.toString().trim();
          
          if (!sicilNo) continue; // Boş sicil numaralarını atla
          
          const companyData = {
            sicil_no: sicilNo,
            firma_unvani: firmaUnvaniColumn ? row[firmaUnvaniColumn.columnName]?.toString().trim() : null,
            is_scraped: false,
            last_scraped_at: null
          };
          
          companiesToSave.push(companyData);
        }
        
        // Veritabanına kaydet
        if (companiesToSave.length > 0) {
          try {
            await batchCreateCompanies(companiesToSave);
            totalSaved += companiesToSave.length;
            console.log(`${companiesToSave.length} adet şirket kaydedildi`);
          } catch (error) {
            console.error('Toplu kayıt sırasında hata oluştu:', error);
            throw error;
          }
        }
      }
      
      // Kullanıcıya başarılı kayıt sayısını göster
      if (totalSaved > 0) {
        toast.success(`Toplam ${totalSaved} adet şirket başarıyla kaydedildi`);
      } else {
        toast.info('Kaydedilecek yeni veri bulunamadı');
      }
      
    } catch (error) {
      console.error('Veri kaydedilirken hata oluştu:', error);
      toast.error('Veri kaydedilirken bir hata oluştu. Lütfen tekrar deneyin.');
    } finally {
      setIsProcessing(false);
    }
  };

  // Başlık tıklandığında çalışır
  const handleHeaderClick = (sheetName: string, columnName: string) => {
    console.log('Seçilen başlık:', { sheetName, columnName });
    
    // Mevcut seçimi kontrol et
    const currentType = getColumnType(sheetName, columnName);
    console.log('Mevcut seçim:', currentType);
    
    // Modal'ı aç ve seçimi yap
    setSelectedHeader({ sheetName, columnName });
  };

  // Başlık tipi seçildiğinde çalışır
  const handleHeaderTypeSelect = (type: 'sicil_no' | 'firma_unvani' | 'none') => {
    if (!selectedHeader) return;
    
    const { sheetName, columnName } = selectedHeader;
    console.log('Seçilen tip:', { sheetName, columnName, type });
    
    setHeaderSelections(prev => {
      const sheetSelections = [...(prev[sheetName] || [])];
      const existingIndex = sheetSelections.findIndex(s => s.columnName === columnName);
      
      if (type === 'none') {
        // Seçimi kaldır
        if (existingIndex >= 0) {
          sheetSelections.splice(existingIndex, 1);
        }
      } else {
        // Yeni seçim ekle veya güncelle
        const newSelection = { sheetName, columnName, columnType: type };
        if (existingIndex >= 0) {
          sheetSelections[existingIndex] = newSelection;
        } else {
          sheetSelections.push(newSelection);
        }
      }
      
      // Seçim yapıldıktan sonra verileri işle
      setTimeout(() => {
        processAndSaveSelectedColumns();
      }, 100);
      
      return {
        ...prev,
        [sheetName]: sheetSelections
      };
    });
    
    setSelectedHeader(null);
  };

  // Tüm sayfaları birleştir
  const combineAllSheets = (sheets: ExcelSheetResult[]): ExcelSheetResult | null => {
    try {
      if (!sheets?.length) return null;
      
      const combinedHeaders = new Set<string>();
      const combinedRows: Record<string, any>[] = [];
      let totalRows = 0;

      // 1. Tüm başlıkları topla
      sheets.forEach(sheet => {
        if (!sheet?.headers) return;
        
        sheet.headers.forEach(header => {
          const headerStr = String(header || '').trim();
          if (headerStr) {
            combinedHeaders.add(headerStr);
          }
        });
      });

      // 2. Her sayfayı işle
      sheets.forEach(sheet => {
        if (!sheet?.rows?.length) return;
        
        sheet.rows.forEach(row => {
          if (!row || typeof row !== 'object') return;
          
          const newRow: Record<string, any> = { __sheetName: sheet.sheetName };
          
          // Mevcut satırdaki tüm değerleri kopyala
          Object.entries(row).forEach(([key, value]) => {
            if (key && value !== undefined && value !== null) {
              newRow[String(key).trim()] = String(value).trim();
            }
          });
          
          // Eksik başlıklar için boş değer ata
          combinedHeaders.forEach(header => {
            if (!(header in newRow)) {
              newRow[header] = '';
            }
          });
          
          combinedRows.push(newRow);
        });
        
        totalRows += sheet.rows.length;
      });

      // 3. Sonuçları döndür
      const headers = Array.from(combinedHeaders);
      
      // Boş satırları filtrele
      const filteredRows = combinedRows.filter(row => 
        Object.values(row).some(val => val && String(val).trim() !== '')
      );

      return {
        sheetName: 'Tüm Sayfalar',
        headers,
        rows: filteredRows.length > 0 ? filteredRows : combinedRows,
        isCombined: true,
        totalRows: filteredRows.length > 0 ? filteredRows.length : totalRows
      };
    } catch (error) {
      console.error('Sayfalar birleştirilirken hata oluştu:', error);
      return null;
    }
  };

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

  // Tablo satırlarını oluştur
  const renderTableRows = (sheet: ExcelSheetResult, fileId: string) => {
    if (!sheet?.rows?.length) return null;
    
    return sheet.rows.slice(0, 5).map((row, rowIndex) => (
      <tr key={`${fileId}-${rowIndex}`} className="border-t dark:border-gray-700">
        {sheet.headers?.map((header, colIndex) => {
          const cellValue = row[header] !== undefined ? String(row[header]) : '';
          return (
            <td 
              key={`${fileId}-${rowIndex}-${colIndex}`} 
              className="px-4 py-2 text-sm dark:text-gray-200"
            >
              {cellValue}
            </td>
          );
        })}
      </tr>
    ));
  };

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
      {/* Sütun Tipi Seçim Modalı */}
      {selectedHeader && (
        <ColumnTypeModal
          isOpen={!!selectedHeader}
          onClose={() => setSelectedHeader(null)}
          columnName={selectedHeader.columnName}
          onSelectType={handleHeaderTypeSelect}
        />
      )}
      
      <div 
        {...getRootProps()} 
        className={`border-2 border-dashed rounded-lg p-6 text-center cursor-pointer transition-colors ${
          isDragActive ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20' : 'border-gray-300 dark:border-gray-700 hover:border-blue-400 dark:hover:border-blue-600'
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
                className="border rounded-lg p-4 hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors"
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
                      {file.status === 'error' && file.error && (
                        <p className="mt-1 text-sm text-red-600">{file.error}</p>
                      )}
                    </div>
                    
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
                      className="text-red-600 hover:bg-red-50 dark:text-red-400 dark:hover:bg-red-900/30"
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
      {files.map((file) => {
        const sheets = file.previewData?.sheets || [];
        const combinedSheet = sheets.length > 1 ? combineAllSheets(sheets) : sheets[0];
        
        return (
          <div key={file.id} className="mt-6">
            <div className="flex justify-between items-center mb-2">
              <h3 className="text-lg font-medium">{file.name} - Önizleme</h3>
              {sheets.length > 1 && (
                <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                  {sheets.length} sayfa birleştirildi
                </span>
              )}
            </div>
            
            {combinedSheet && combinedSheet.rows && combinedSheet.rows.length > 0 ? (
              <div className="border rounded-md overflow-hidden">
                <div className="bg-gray-50 dark:bg-gray-800 px-4 py-2 border-b dark:border-gray-700">
                  <h4 className="text-md font-medium text-gray-900 dark:text-gray-100">
                    {combinedSheet.sheetName} (Toplam {combinedSheet.rows.length} satır, {combinedSheet.headers?.length || 0} sütun)
                  </h4>
                </div>
                <div className="overflow-auto max-h-96 bg-white dark:bg-gray-900/30 rounded-b-md">
                  <table className="w-full text-sm">
                    <thead>
                      <tr className="bg-gray-100 dark:bg-gray-800">
                        {combinedSheet.headers?.map((header, headerIndex) => (
                          <th 
                            key={`${file.id}-${headerIndex}`} 
                            className={getHeaderClassName(combinedSheet.sheetName, header)}
                            onClick={() => handleHeaderClick(combinedSheet.sheetName, header)}
                            title="Sütun türünü seçmek için tıklayın"
                          >
                            <div className="flex items-center space-x-2">
                              <span className="font-semibold">{header}</span>
                              {getColumnType(combinedSheet.sheetName, header) !== 'none' && (
                                <Badge 
                                  variant="default"
                                  className={`text-xs px-1.5 py-0.5 ${
                                    getColumnType(combinedSheet.sheetName, header) === 'sicil_no' 
                                      ? 'bg-blue-100 text-blue-700 hover:bg-blue-200 dark:bg-blue-700 dark:text-white dark:hover:bg-blue-600' 
                                      : 'bg-green-100 text-green-700 hover:bg-green-200 dark:bg-green-700 dark:text-white dark:hover:bg-green-600'
                                  }`}
                                >
                                  {getColumnType(combinedSheet.sheetName, header) === 'sicil_no' ? 'Sicil No' : 'Firma Ünvanı'}
                                </Badge>
                              )}
                            </div>
                          </th>
                        )) || null}
                      </tr>
                    </thead>
                    <tbody>
                      {renderTableRows(combinedSheet, file.id)}
                      {combinedSheet.rows.length > 5 && (
                        <tr>
                          <td 
                            colSpan={combinedSheet.headers?.length || 1} 
                            className="px-4 py-2 text-center text-xs text-gray-500"
                          >
                            Toplam {combinedSheet.rows.length} satırdan ilk 5 gösteriliyor
                          </td>
                        </tr>
                      )}
                    </tbody>
                  </table>
                </div>
              </div>
            ) : (
              <p className="text-sm text-gray-500">Önizleme mevcut değil</p>
            )}
          </div>
        );
      })}
    </div>
  );
};

export default FileUploadSection;