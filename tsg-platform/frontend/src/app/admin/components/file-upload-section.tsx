"use client";

import { useCallback, useEffect, useState } from "react";
import { useDropzone } from "react-dropzone";
import { Button } from "@/components/ui/button";
import { toast } from "sonner";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Icons } from "@/components/icons";
import type { FilePreviewData } from "@/lib/file-utils";
import { MÜDÜRLÜKLER, readExcelFile, type ExcelProcessResult, type TableHeader } from '@/lib/file-utils';

// Dosya durum türleri
type FileStatus = 'waiting' | 'processing' | 'completed' | 'error';

// Özel dosya tipi
type CustomFile = {
  file: File;
  müdürlük: string;
  formattedSize: string;
  status: FileStatus;
  error?: string;
  previewData?: ExcelProcessResult;
};

// Tablo başlık tipi
type TableHeaderType = {
  key: string;
  name: string;
  sortable: boolean;
  resizable: boolean;
  minWidth: number;
};

// Tablo satır tipi
type TableRowType = {
  id: number;
  [key: string]: string | number | boolean | null;
};

// Dosya boyutunu formatlama fonksiyonu
const formatFileSize = (bytes?: number): string => {
  if (!bytes && bytes !== 0) return 'Boyut bilinmiyor';
  if (bytes === 0) return '0 B';
  const k = 1024;
  const sizes = ['B', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

export default function FileUploadSection() {
  const [files, setFiles] = useState<CustomFile[]>([]);
  const [isUploading, setIsUploading] = useState(false);
  const [previewData, setPreviewData] = useState<Record<string, FilePreviewData>>({});
  const [selectedMudurluk, setSelectedMudurluk] = useState<string>("");

  const onDrop = useCallback((acceptedFiles: File[]) => {
    if (!selectedMudurluk) {
      toast.error('Lütfen önce bir müdürlük seçin');
      return;
    }
    
    // Yeni dosyaları ekle
    const newFiles: CustomFile[] = acceptedFiles.map(file => {
      // Dosya uzantısını kontrol et
      const fileName = file.name || '';
      const fileExt = (fileName.split('.').pop() || '').toLowerCase();
      
      // Desteklenen uzantıları kontrol et
      const isValidFile = ['xlsx', 'xls', 'pdf'].includes(fileExt);
      
      return {
        file,
        müdürlük: selectedMudurluk,
        formattedSize: formatFileSize(file.size),
        status: isValidFile ? 'waiting' : 'error' as const,
        error: isValidFile ? undefined : 'Desteklenmeyen dosya türü. Sadece Excel (.xlsx, .xls) veya PDF (.pdf) dosyaları yükleyebilirsiniz.'
      };
    });
    
    setFiles(prevFiles => [...prevFiles, ...newFiles]);
  }, [selectedMudurluk]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['.xlsx'],
      'application/vnd.ms-excel': ['.xls']
    },
    multiple: true,
    disabled: !selectedMudurluk,
    noClick: false,
    noKeyboard: false,
    noDrag: false,
    noDragEventsBubbling: false,
    validator: (file) => {
      const fileName = file.name || '';
      const fileExt = (fileName.split('.').pop() || '').toLowerCase();
      if (!['xlsx', 'xls', 'pdf'].includes(fileExt)) {
        return {
          code: 'invalid-file-type',
          message: 'Sadece Excel (.xlsx, .xls) veya PDF (.pdf) dosyaları yükleyebilirsiniz'
        };
      }
      return null;
    }
  });

  // Dosya işleme fonksiyonu
  const processFiles = useCallback(async () => {
    if (!selectedMudurluk) {
      toast.error('Lütfen önce bir müdürlük seçin');
      return;
    }

    const updatedFiles = [...files];
    let hasError = false;

    for (let i = 0; i < updatedFiles.length; i++) {
      const fileObj = updatedFiles[i];
      
      if (fileObj.status === 'waiting') {
        try {
          updatedFiles[i] = { ...fileObj, status: 'processing' as const };
          setFiles([...updatedFiles]);
          
          // Excel dosyasını işle
          const excelData = await readExcelFile(fileObj.file);
          
          if (excelData.rows.length === 0) {
            throw new Error('Excel dosyasında veri bulunamadı');
          }
          
// Başlıkları sütunlara dönüştür
          const tableHeaders = excelData.headers.map((header, index) => ({
            key: `col${index}`,
            name: header || `Sütun ${index + 1}`,
            sortable: true,
            resizable: true,
            minWidth: 150
          }));
          
          // Satır verilerini oluştur
          const tableRows = excelData.rows.map((row, rowIndex) => {
            const rowData: Record<string, any> = { id: rowIndex };
            row.forEach((cell, cellIndex) => {
              rowData[`col${cellIndex}`] = cell;
            });
            return rowData;
          });
          
          // Önizleme verisini oluştur
          const previewData: ExcelProcessResult = {
            headers: tableHeaders,
            rows: tableRows.slice(0, 10),
            allRows: tableRows,
            currentPage: 1,
            pageSize: 10,
            hasMore: tableRows.length > 10,
            total: tableRows.length,
            sheetName: excelData.sheetName,
            sheetNames: excelData.sheetNames,
            totalRows: excelData.totalRows,
            totalColumns: excelData.totalColumns
          };
          
          // Başarılı işlem durumunu güncelle
          updatedFiles[i] = { ...fileObj, status: 'completed' as const, previewData };
          
          // Önizleme verisini güncelle
          setPreviewData(prev => ({
            ...prev,
            [i]: {
    
              data: previewData
            }
          }));
          
          toast.success(`${fileObj.file.name} başarıyla yüklendi. Toplam ${tableRows.length} satır bulundu.`);
          
        } catch (error) {
          console.error('Excel işleme hatası:', error);
          const errorMessage = error instanceof Error ? error.message : 'Bilinmeyen hata';
          
          updatedFiles[i] = { 
            ...fileObj, 
            status: 'error' as const,
            error: errorMessage,
            previewData: {
              headers: [],
              rows: [],
              allRows: [],
              currentPage: 1,
              pageSize: 10,
              hasMore: false,
              total: 0,
              sheetName: '',
              sheetNames: [],
              totalRows: 0,
              totalColumns: 0,
              error: errorMessage,
              meta: {
                fileName: fileObj.file.name,
                fileSize: fileObj.file.size,
                fileType: fileObj.file.type,
                mudurluk: selectedMudurluk,
                processedAt: new Date().toISOString()
              }
            }
          };
          
          setPreviewData(prev => ({
            ...prev,
            [i]: {
              success: false,
              error: errorMessage
            }
          }));
          
          toast.error(`Hata: ${errorMessage}`);
          hasError = true;
        }
      }
    }
    
    setFiles(updatedFiles);
    return !hasError;
  }, [files, selectedMudurluk]);

  useEffect(() => {
    if (files.length > 0) {
      processFiles();
    }
  }, [files, selectedMudurluk]);

  // Dosya kaldırma işlemi
  const removeFile = (index: number) => {
    const updatedFiles = [...files];
    updatedFiles.splice(index, 1);
    setFiles(updatedFiles);
    
    // İlgili önizleme verilerini de temizle
    setPreviewData(prev => {
      const newPreviewData = { ...prev };
      delete newPreviewData[index];
      return newPreviewData;
    });
  };

  // Dosya yükleme işlemi
  const uploadFiles = async () => {
    if (!selectedMudurluk) {
      toast.error('Lütfen önce bir müdürlük seçin');
      return;
    }
    
    if (files.length === 0) {
      toast.error('Yüklenecek dosya bulunamadı');
      return;
    }
    
    setIsUploading(true);
    
    try {
      const formData = new FormData();
      files.forEach(fileObj => {
        formData.append('files', fileObj.file);
      });
      formData.append('mudurluk', selectedMudurluk);
      
      const response = await fetch('/api/upload', {
        method: 'POST',
        body: formData,
      });
      
      if (!response.ok) {
        throw new Error('Sunucu hatası');
      }
      
      const result = await response.json();
      
      // Başarılı yükleme sonrası dosyaları temizle
      setFiles([]);
      setPreviewData({});
      
      toast.success(`${files.length} dosya başarıyla yüklendi`);
      return result;
    } catch (error) {
      console.error('Dosya yükleme hatası:', error);
      toast.error('Dosya yüklenirken bir hata oluştu');
      throw error;
    } finally {
      setIsUploading(false);
    }
  };

  const handlePageChange = (fileId: string, page: number) => {
    setPreviewData(prev => {
      const currentData = prev[fileId]?.data;
      if (!currentData) return prev;
      
      const { allRows, pageSize } = currentData;
      const startIndex = (page - 1) * pageSize;
      const endIndex = startIndex + pageSize;
      
      return {
        ...prev,
        [fileId]: {
          ...prev[fileId],
          data: {
            ...currentData,
            currentPage: page,
            rows: allRows.slice(0, endIndex),
            hasMore: endIndex < allRows.length
          }
        }
      };
    });
  };

  const loadMoreRows = (fileId: string) => {
    setPreviewData(prev => {
      const currentData = prev[fileId]?.data;
      if (!currentData) return prev;
      
      const nextPage = (currentData.currentPage || 1) + 1;
      const startIdx = 0;
      const endIdx = nextPage * (currentData.pageSize || 10);
      const newRows = currentData.allRows.slice(0, endIdx);
      
      return {
        ...prev,
        [fileId]: {
          ...prev[fileId],
          data: {
            ...currentData,
            rows: newRows,
            currentPage: nextPage,
            hasMore: newRows.length < currentData.allRows.length
          }
        }
      };
    });
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center space-x-4">
        <div className="w-64">
          <Select 
            value={selectedMudurluk} 
            onValueChange={setSelectedMudurluk}
          >
            <SelectTrigger>
              <SelectValue placeholder="Müdürlük Seçin" />
            </SelectTrigger>
            <SelectContent>
              {MÜDÜRLÜKLER.map((mudurluk) => (
                <SelectItem key={mudurluk.value} value={mudurluk.value}>
                  {mudurluk.label}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>
        
        <div className="text-sm text-muted-foreground">
          {selectedMudurluk 
            ? `${MÜDÜRLÜKLER.find(m => m.value === selectedMudurluk)?.label} Müdürlüğü seçildi` 
            : 'Lütfen bir müdürlük seçin'}
        </div>
      </div>

      <Card className="w-full">
        <CardHeader>
          <CardTitle>Dosya Yükle</CardTitle>
          <CardDescription>
            PDF veya Excel dosyalarınızı sürükleyip bırakın veya tıklayarak seçin.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div 
            {...getRootProps()} 
            className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors ${
              isDragActive 
                ? 'border-primary bg-accent/50' 
                : !selectedMudurluk 
                  ? 'bg-muted/50 border-muted-foreground/25 cursor-not-allowed' 
                  : 'border-muted-foreground/25 hover:bg-accent/50'
            }`}
          >
            <input {...getInputProps()} />
            <div className="flex flex-col items-center justify-center space-y-2">
              <Icons.upload className="h-10 w-10 text-muted-foreground" />
              {!selectedMudurluk ? (
                <p className="text-sm text-muted-foreground">
                  Lütfen önce bir müdürlük seçin
                </p>
              ) : (
                <>
                  <p className="text-sm text-muted-foreground">
                    {isDragActive 
                      ? 'Dosyaları buraya bırakın...' 
                      : 'Dosya sürükleyip bırakın veya tıklayarak seçin'}
                  </p>
                  <p className="text-xs text-muted-foreground">
                    PDF veya Excel dosyaları kabul edilir
                  </p>
                </>
              )}
            </div>
          </div>

          {files.length > 0 && (
            <div className="mt-6">
              <h3 className="text-lg font-medium mb-4">Seçilen Dosyalar</h3>
              <div className="rounded-md border mb-6">
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Dosya Adı</TableHead>
                      <TableHead>Müdürlük</TableHead>
                      <TableHead>Boyut</TableHead>
                      <TableHead>Durum</TableHead>
                      <TableHead className="text-right">İşlemler</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {files.map((fileObj, index) => (
                      <TableRow key={index}>
                        <TableCell className="font-medium">{fileObj.file.name}</TableCell>
                        <TableCell>
                          {fileObj.müdürlük ? 
                            MÜDÜRLÜKLER.find(m => m.value === fileObj.müdürlük)?.label : 
                            'Belirtilmedi'}
                        </TableCell>
                        <TableCell>{fileObj.formattedSize || formatFileSize(fileObj.file.size || 0)}</TableCell>
                        <TableCell>
                          <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                            fileObj.status === 'waiting' ? 'bg-yellow-100 text-yellow-800' :
                            fileObj.status === 'processing' ? 'bg-blue-100 text-blue-800' :
                            fileObj.status === 'completed' ? 'bg-green-100 text-green-800' :
                            'bg-red-100 text-red-800'
                          }`}>
                            {fileObj.status === 'waiting' ? 'Bekliyor' :
                             fileObj.status === 'processing' ? 'İşleniyor' :
                             fileObj.status === 'completed' ? 'Tamamlandı' : 
                             fileObj.error || 'Hata'}
                          </span>
                        </TableCell>
                        <TableCell className="text-right">
                          <Button
                            variant="ghost"
                            size="sm"
                            className="text-red-600 hover:text-red-800"
                            onClick={(e) => {
                              e.stopPropagation();
                              removeFile(index);
                            }}
                          >
                            <Icons.trash className="h-4 w-4" />
                          </Button>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </div>

              {/* Önizleme Tabloları */}
              {Object.entries(previewData).map(([indexStr, data]) => {
                if (!data || !data.success) return null;
                
                const fileIndex = parseInt(indexStr, 10);
                if (isNaN(fileIndex)) return null;
                
                const file = files[fileIndex]?.file; // Access the underlying File object
                if (!file) return null;

                // Tablo verilerini al
                const tableData = data.data || {};
                const allRows = Array.isArray(tableData.allRows) ? tableData.allRows : 
                               Array.isArray(tableData.rows) ? tableData.rows : [];
                
                // Başlıkları oluştur (eğer yoksa ilk satırdan oluştur)
                let headers: TableHeaderType[] = [];
                if (Array.isArray(tableData.headers) && tableData.headers.length > 0) {
                  headers = tableData.headers;
                } else if (allRows.length > 0) {
                  // İlk satırdan başlık oluştur
                  headers = Object.keys(allRows[0] || {}).map(key => ({
                    key,
                    name: key,
                    sortable: true,
                    resizable: true,
                    minWidth: 150
                  }));
                }
                
                // Gösterilecek satırları al
                const currentPage = tableData.currentPage || 1;
                const pageSize = tableData.pageSize || 10;
                const startIndex = 0; // Her zaman baştan göster
                const endIndex = currentPage * pageSize;
                const displayRows = allRows.slice(startIndex, endIndex);
                const totalRows = allRows.length;
                
                // Toplam kayıt sayısını al
                const totalRecords = data.data?.total || totalRows;
                
                // Sayfalama bilgilerini al (zaten yukarıda tanımlandı)
                const totalPages = Math.ceil(totalRecords / pageSize);
                const startRecord = (currentPage - 1) * pageSize + 1;
                const endRecord = Math.min(currentPage * pageSize, totalRecords);
                
                // Sayfalama bilgisi metni oluştur
                const paginationInfo = totalPages > 1 ? (
                  <div className="mt-2 text-sm text-muted-foreground">
                    <div>Toplam {totalRecords} kayıt</div>
                    <div>
                      Gösterilen: {startRecord}-{endRecord} / {totalRecords} kayıt
                      <span className="mx-2">|</span>
                      Sayfa: {currentPage}/{totalPages}
                    </div>
                  </div>
                ) : (
                  <div className="mt-2 text-sm text-muted-foreground">
                    {file.data?.total || 0} kayıt
                  </div>
                );

                return (
                  <div key={fileIndex} className="mb-8">
                    <div className="flex justify-between items-center mb-2">
                      <h4 className="text-md font-medium">
                        {file?.name || 'Bilinmeyen Dosya'}
                      </h4>
                      <div className="flex flex-col items-end">
                        <span className="text-sm text-muted-foreground">
                          {formatFileSize(file?.size || 0)}
                        </span>
                        <span className="text-xs text-muted-foreground">
                          {MÜDÜRLÜKLER.find(m => m.value === files[fileIndex]?.müdürlük)?.label || 'Müdürlük belirtilmemiş'}
                        </span>
                      </div>
                    </div>
                    
                    {/* Sayfalama bilgisi */}
                    {paginationInfo}
                    
                    {data.meta?.sheetNames && data.meta.sheetNames.length > 1 && (
                      <div className="mb-2 text-sm text-muted-foreground">
                        Sayfalar: {data.meta.sheetNames.join(', ')}
                      </div>
                    )}
                    
                    <div className="rounded-md border overflow-hidden">
                      <div className="overflow-x-auto">
                        <Table>
                          <TableHeader>
                            <TableRow>
                              {headers.map((header) => {
                                // Başlık adını güvenli bir şekilde al
                                let headerName = header?.name || header?.key || '';
                                
                                // Özel başlık formatlamaları
                                if (typeof headerName === 'string') {
                                  const lowerName = headerName.toLowerCase();
                                  if (lowerName.includes('sicil')) headerName = 'Sicil No';
                                  else if (lowerName.includes('unvan')) headerName = 'Firma Ünvanı';
                                  else if (lowerName.includes('adres')) headerName = 'Adres';
                                }
                                
                                return (
                                  <TableHead key={header.key} className="whitespace-nowrap">
                                    {headerName}
                                  </TableHead>
                                );
                              })}
                            </TableRow>
                          </TableHeader>
                          <TableBody>
                            {displayRows.length > 0 ? (
                              displayRows.map((row: TableRowType, rowIndex: number) => (
                                <TableRow key={rowIndex}>
                                  {headers.map((header: TableHeaderType) => {
                                    const value = row[header.key];
                                    let displayValue = value !== null && value !== undefined ? String(value) : '-';
                                    
                                    // Uzun metinleri kısalt
                                    if (displayValue.length > 50) {
                                      displayValue = displayValue.substring(0, 50) + '...';
                                    }
                                    
                                    return (
                                      <TableCell 
                                        key={`${rowIndex}-${header.key}`}
                                        className="max-w-xs truncate"
                                        title={String(value || '')}
                                      >
                                        {displayValue}
                                      </TableCell>
                                    );
                                  })}
                                </TableRow>
                              ))
                            ) : (
                              <TableRow>
                                <TableCell colSpan={headers.length} className="text-center text-muted-foreground">
                                  Gösterilecek veri bulunamadı
                                </TableCell>
                              </TableRow>
                            )}
                            
                            {totalRows > 5 && (
                              <TableRow>
                                <TableCell colSpan={headers.length} className="text-center">
                                  <Button 
                                    variant="outline" 
                                    size="sm"
                                    onClick={() => loadMoreRows(fileIndex)}
                                    disabled={isUploading}
                                    className="mt-2"
                                  >
                                    Daha Fazla Yükle ({totalRows - displayRows.length} kayıt daha)
                                  </Button>
                                </TableCell>
                              </TableRow>
                            )}
                          </TableBody>
                        </Table>
                      </div>
                    </div>
                  </div>
                );
              })}

              <div className="mt-4 flex justify-end">
                <Button 
                  onClick={uploadFiles}
                  disabled={isUploading || files.length === 0 || !selectedMudurluk}
                  className="gap-2"
                >
                  {isUploading ? (
                    <>
                      <Icons.spinner className="h-4 w-4 animate-spin" />
                      Yükleniyor...
                    </>
                  ) : (
                    <>
                      <Icons.upload className="h-4 w-4" />
                      Yükle ({files.length} dosya)
                    </>
                  )}
                </Button>
              </div>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
