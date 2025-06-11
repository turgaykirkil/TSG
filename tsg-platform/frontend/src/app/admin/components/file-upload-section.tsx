'use client';

import { type FC, useState, useCallback } from 'react';
import { useDropzone, type FileRejection } from 'react-dropzone';
import { toast } from 'sonner';
import { Loader2 } from 'lucide-react';
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { MUDURLUKLER } from "@/lib/constants/mudurlukler";
import { processExcelFile, type ExcelProcessResult, type ExcelSheetResult } from '@/lib/file-utils';
import type { CustomFile } from '@/lib/types/file.types';
import { batchAddCompanies } from '@/lib/supabase';
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
  columnType: 'sicil_no' | 'firma_unvani' | 'sicil_mudurluk' | 'none';
};

const FileUploadSection: FC = () => {
  const [files, setFiles] = useState<CustomFile[]>([]);
  const [isProcessing, setIsProcessing] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [selectedHeader, setSelectedHeader] = useState<{sheetName: string; columnName: string} | null>(null);
  const [headerSelections, setHeaderSelections] = useState<Record<string, HeaderSelection[]>>({});
  const [selectedSicilMudurluk, setSelectedSicilMudurluk] = useState<string>(''); // Yeni state eklendi

  // Seçili sütun türünü döndür
  const getColumnType = (sheetName: string, columnName: string): string => {
    // Tüm dosyaları kontrol et
    for (const file of files) {
      const fileSelections = headerSelections[file.id] || [];
      const selection = fileSelections.find(
        sel => sel.sheetName === sheetName && sel.columnName === columnName
      );
      if (selection) {
        return selection.columnType;
      }
    }
    return 'none';
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
  const processAndSaveSelectedColumns = async (onProgress?: (progress: number) => void) => {
    console.log('processAndSaveSelectedColumns başladı');
    if (!files.length) {
      console.log('İşlenecek dosya yok');
      return 0;
    }
    if (isProcessing) {
      console.log('Zaten işlem yapılıyor');
      return 0;
    }
    
    let totalSaved = 0;
    let processedFiles = 0;
    
    try {
      console.log('İşlem başlatılıyor...');
      setIsProcessing(true);
      
      for (const file of files) {
        console.log('Dosya nesnesi:', file);
        console.log('Dosya işleniyor - ID:', file.id, 'Name:', file.name);
        
        if (!file.previewData) {
          console.error('Dosyada previewData yok:', file);
          continue;
        }
        
        const sheets = file.previewData.sheets || [];
        console.log('Sayfa sayısı:', sheets.length, 'Sayfalar:', sheets.map(s => s.sheetName || 'isimsiz'));
        
        if (sheets.length === 0) {
          console.error('Dosyada sayfa yok:', file.name);
          continue;
        }
        
        const combinedSheet = sheets.length > 1 ? combineAllSheets(sheets) : sheets[0];
        console.log('Birleştirilmiş sayfa:', combinedSheet ? 'Mevcut' : 'Yok');
        
        if (!combinedSheet?.rows?.length) {
          console.log('İşlenecek satır yok veya sayfa boş');
          continue;
        }
        
        // Seçili sütunları al
        console.log('Dosya ID:', file.id);
        console.log('Mevcut headerSelections:', headerSelections);
        const selections = headerSelections[file.id] || [];
        console.log('Bu dosya için seçimler:', selections);
        
        const sicilNoColumn = selections.find(s => s.columnType === 'sicil_no')?.columnName;
        const firmaUnvaniColumn = selections.find(s => s.columnType === 'firma_unvani')?.columnName;

        console.log('Seçili sütunlar:', { sicilNoColumn, firmaUnvaniColumn });
        
        // Eğer hiç sütun seçilmemişse devam et
        if (!sicilNoColumn && !firmaUnvaniColumn) {
          console.log('Hiç sütun seçilmemiş, atlanıyor...');
          continue;
        }
        
        // Seçilen sütunların sayfada var olduğundan emin ol
        const headers = combinedSheet.headers || [];
        if ((sicilNoColumn && !headers.includes(sicilNoColumn)) || 
            (firmaUnvaniColumn && !headers.includes(firmaUnvaniColumn))) {
          console.error('Seçilen sütunlar sayfada bulunamadı');
          toast.error('Seçilen sütunlar sayfada bulunamadı. Lütfen sütun seçimlerinizi kontrol edin.');
          continue;
        }
        
        // Verileri hazırla
        type CompanyData = {
          sicil_no: string;
          firma_unvani: string;
          sicil_mudurluk: string;  // Yeni eklenen alan
          is_scraped: boolean;
          last_scraped_at: null;
          metadata: {
            source: string;
            import_date: string;
            [key: string]: any;
          };
        };

        // Önce tüm satırları işle, sonra null olmayanları filtrele
        const allRows = combinedSheet.rows.map(row => {
          const sicilNo = sicilNoColumn ? String(row[sicilNoColumn] || '').trim() : '';
          const firmaUnvani = firmaUnvaniColumn ? String(row[firmaUnvaniColumn] || '').trim() : '';
          if (!sicilNo && !firmaUnvani) return null;
          
          return {
            sicil_no: sicilNo,
            firma_unvani: firmaUnvani,
            sicil_mudurluk: selectedSicilMudurluk,  // Seçilen sicil müdürlüğünü kullanıyoruz
            is_scraped: false,
            last_scraped_at: null,
            metadata: {
              source: 'excel_import',
              import_date: new Date().toISOString()
            }
          };
        });
        
        // Null değerleri filtrele ve tip dönüşümü yap
        const companies: CompanyData[] = allRows.filter((row): row is CompanyData => row !== null);
        
        if (!companies.length) continue;
        
        // API'ye gönder
        try {
          // Supabase'e kaydet
          const result = await batchAddCompanies(companies);
          totalSaved += result?.length || 0;
          
          // Dosya durumunu güncelle
          updateFileStatus(
            file.id, 
            'success',
            file.previewData
          );
        } catch (error) {
          console.error(`${file.name} kaydedilirken hata oluştu:`, error);
          updateFileStatus(
            file.id,
            'error',
            file.previewData,
            'Kayıt sırasında hata oluştu'
          );
          continue;
        }
        
        // İlerleme durumunu güncelle
        processedFiles++;
        if (onProgress) {
          const progress = Math.round((processedFiles / files.length) * 100);
          onProgress(progress);
        }
      }
      
      // Başarı mesajını artık burada göstermiyoruz, handleUploadClick'te gösteriyoruz
      return totalSaved;
      
    } catch (error) {
      console.error('Veri kaydedilirken hata oluştu:', error);
      toast.error('Veri kaydedilirken bir hata oluştu. Lütfen tekrar deneyin.');
      throw error;
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

  // Seçim yapıldığında sadece başlık rengini günceller, otomatik kayıt yapmaz
  const handleHeaderTypeSelect = (type: 'sicil_no' | 'firma_unvani' | 'sicil_mudurluk' | 'none') => {
    if (!selectedHeader) return;
    
    const { sheetName, columnName } = selectedHeader;
    console.log('Seçilen tip:', { sheetName, columnName, type });
    
    // Aktif dosyayı bul
    const activeFile = files.find(f => f.previewData?.sheets?.some(s => s.sheetName === sheetName));
    if (!activeFile) {
      console.error('Aktif dosya bulunamadı');
      return;
    }
    
    setHeaderSelections(prev => {
      const fileSelections = [...(prev[activeFile.id] || [])];
      const existingIndex = fileSelections.findIndex(s => 
        s.sheetName === sheetName && s.columnName === columnName
      );
      
      if (type === 'none') {
        // Seçimi kaldır
        if (existingIndex >= 0) {
          fileSelections.splice(existingIndex, 1);
        }
      } else {
        // Yeni seçim ekle veya güncelle
        const newSelection = { sheetName, columnName, columnType: type };
        if (existingIndex >= 0) {
          fileSelections[existingIndex] = newSelection;
        } else {
          fileSelections.push(newSelection);
        }
      }
      
      return {
        ...prev,
        [activeFile.id]: fileSelections
      };
    });
    
    setSelectedHeader(null);
  };

  // Yükleme butonuna tıklandığında çalışır
  const handleUploadClick = async () => {
    console.log('handleUploadClick çalıştı');
    if (isUploading) {
      console.log('Zaten yükleme yapılıyor');
      return;
    }
    
    try {
      console.log('Yükleme başlatılıyor...');
      setIsUploading(true);
      setUploadProgress(0);
      
      // Progress güncelleme fonksiyonu
      const updateProgress = (progress: number) => {
        console.log(`İlerleme: %${progress}`);
        setUploadProgress(progress);
      };
      
      // İşlemi başlat ve işlenen firma sayısını al
      console.log('processAndSaveSelectedColumns çağrılıyor...');
      const processedCount = await processAndSaveSelectedColumns(updateProgress);
      console.log(`İşlem tamamlandı. İşlenen kayıt: ${processedCount}`);
      
      // Başarı mesajını göster
      toast.success(`${processedCount} adet firma verisi işlenmiştir`);
      
      // İşlem tamamlandıktan sonra progress bar'ı sıfırla
      setTimeout(() => {
        setUploadProgress(0);
      }, 2000);
      
    } catch (error) {
      console.error('Yükleme sırasında hata oluştu:', error);
      toast.error('Yükleme sırasında bir hata oluştu. Lütfen tekrar deneyin.');
    } finally {
      console.log('Yükleme işlemi tamamlandı');
      setIsUploading(false);
    }
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
                        value={selectedSicilMudurluk}
                        onValueChange={setSelectedSicilMudurluk}
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
          
          <div className="space-y-4 pt-4">
            {/* Yükleme Çubuğu */}
            {uploadProgress > 0 && uploadProgress < 100 && (
              <div className="space-y-2">
                <div className="flex justify-between text-sm text-muted-foreground">
                  <span>Yükleniyor...</span>
                  <span>{Math.round(uploadProgress)}%</span>
                </div>
                <Progress value={uploadProgress} className="h-2" />
              </div>
            )}

            
            <div className="flex flex-col sm:flex-row justify-end space-y-2 sm:space-y-0 sm:space-x-3 pt-4">
              <Button 
                variant="outline" 
                onClick={() => {
                  toast.success('Tüm dosyalar temizlendi');
                  setFiles([]);
                }}
                disabled={isProcessing || isUploading}
                className="w-full sm:w-auto"
              >
                Tümünü Temizle
              </Button>
              <Button 
                onClick={(e) => {
                  e.preventDefault();
                  handleUploadClick();
                }}
                disabled={isProcessing || isUploading || files.length === 0 || !selectedSicilMudurluk}
                className="w-full sm:w-auto"
              >
                {isUploading ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    İşleniyor...
                  </>
                ) : (
                  'Kaydet ve İşle'
                )}
              </Button>
            </div>
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