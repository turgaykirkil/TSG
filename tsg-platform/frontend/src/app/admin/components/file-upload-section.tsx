'use client';

import { useState, useMemo, FC, useCallback } from 'react';
import { UploadCloud, Loader2, FileText, X, AlertTriangle, ChevronsUpDown } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import { toast } from 'sonner';
import { useFileProcessor, type ProcessedFileData, type ParsedTable } from '@/hooks/useFileProcessor';
import { useColumnMapper, type ColumnType } from '@/hooks/useColumnMapper';
import { useCompanyUploader } from '@/hooks/useCompanyUploader';
import type { ExcelSheetResult } from '@/lib/file-utils';
import type { CompanyData } from '@/types/company.types';
import { ColumnTypeModal } from './column-type-modal';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';

const FileDropzone: FC<{
  getRootProps: (props?: object) => object;
  getInputProps: (props?: object) => object;
  isDragActive: boolean;
}> = ({ getRootProps, getInputProps, isDragActive }) => (
  <div
    {...getRootProps()}
    className={`relative flex flex-col items-center justify-center w-full p-8 border-2 border-dashed rounded-lg cursor-pointer transition-colors duration-300 ease-in-out ${
      isDragActive
        ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/10'
        : 'border-gray-300 dark:border-gray-600 hover:border-blue-400 dark:hover:border-blue-500'
    }`}
  >
    <input {...getInputProps()} />
    <UploadCloud className="w-16 h-16 text-gray-400 dark:text-gray-500 mb-4" />
    <p className="text-lg font-semibold text-gray-700 dark:text-gray-300">Sürükleyip bırakın veya tıklayarak dosya seçin</p>
    <p className="text-sm text-gray-500 dark:text-gray-400">Sadece .xlsx, .xls veya .pdf dosyaları kabul edilir</p>
  </div>
);

const ProcessingState: FC<{ progress: number }> = ({ progress }) => (
  <div className="w-full text-center p-8">
    <Loader2 className="w-12 h-12 text-blue-500 animate-spin mx-auto mb-4" />
    <p className="text-lg font-semibold mb-2">Dosya işleniyor...</p>
    <Progress value={progress} className="w-1/2 mx-auto" />
    <p className="text-sm text-gray-500 mt-2">Lütfen bekleyin, bu işlem biraz zaman alabilir.</p>
  </div>
);

const DataMapping: FC<{
  headers: string[];
  rows: Record<string, unknown>[];
  onHeaderClick: (header: string) => void;
  getColumnType: (header: string) => ColumnType | undefined;
}> = ({ headers, rows, onHeaderClick, getColumnType }) => (
  <div className="relative w-full overflow-auto h-[400px] rounded-md border">
    <Table className="min-w-full">
      <TableHeader className="sticky top-0 bg-background z-10">
        <TableRow>
          {headers.map((header) => {
            const columnType = getColumnType(header);
            return (
              <TableHead key={header}>
                <Button
                  variant="ghost"
                  onClick={() => onHeaderClick(header)}
                  className="w-full justify-start p-2 text-left h-auto whitespace-normal"
                >
                  <span className="font-bold break-words">{header}</span>
                  {columnType && columnType !== 'none' && (
                    <span className="ml-2 mt-1 px-2 py-0.5 text-xs rounded-full bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200 block">
                      {columnType}
                    </span>
                  )}
                </Button>
              </TableHead>
            );
          })}
        </TableRow>
      </TableHeader>
      <TableBody>
        {rows.slice(0, 100).map((row, rowIndex) => (
          <TableRow key={rowIndex}>
            {headers.map((header) => (
              <TableCell key={header} className="whitespace-nowrap max-w-[200px] truncate">
                {String(row[header] ?? '')}
              </TableCell>
            ))}
          </TableRow>
        ))}
      </TableBody>
    </Table>
  </div>
);

const SheetMappingInterface: FC<{ sheet: ExcelSheetResult; selectedSicilMudurluk: string; onReset: () => void; }> = ({ sheet, selectedSicilMudurluk, onReset }) => {
  const uploader = useCompanyUploader();

  const dataForMapper: (string | number | null)[][] = [
    sheet.headers,
    ...sheet.data.map(row =>
      row.map(cell => {
        if (cell === null || typeof cell === 'string' || typeof cell === 'number') {
          return cell;
        }
        return String(cell ?? '');
      })
    )
  ];

  const {
    headers,
    rows,
    isModalOpen,
    selectedHeader,
    mappedColumns,
    getColumnType,
    handleHeaderClick,
    handleMapColumn,
    closeModal,
    getMappedData,
    reset: resetMapper,
  } = useColumnMapper(dataForMapper);

  const handleUploadSuccess = useCallback(() => {
    toast.info('Yükleme tamamlandı, arayüz sıfırlanıyor.');
    onReset();
  }, [onReset]);

  const handleUpload = useCallback(async () => {
    console.log('[SheetMapping] Handle upload called.');
    if (!selectedSicilMudurluk) {
      toast.error('Lütfen Sicil Müdürlüğü seçin.');
      console.error('[SheetMapping] Sicil Müdürlüğü not selected.');
      return;
    }

    const result = getMappedData();
    console.log('[SheetMapping] Mapped data result:', result);

    if (!result.isValid) {
      toast.error('Eksik zorunlu alanlar var.', {
        description: `Lütfen şu alanları eşleştirin: ${result.missingColumns.join(', ')}`,
      });
      console.error(`[SheetMapping] Missing required columns: ${result.missingColumns.join(', ')}`);
      return;
    }

    console.log(`[SheetMapping] Attempting to upload ${result.data.length} companies.`);
    await uploader.upload(result.data, selectedSicilMudurluk, handleUploadSuccess);
  }, [getMappedData, uploader, selectedSicilMudurluk, handleUploadSuccess]);

  return (
    <div className="space-y-4">
      <ColumnTypeModal
        isOpen={isModalOpen}
        onClose={closeModal}
        columnName={selectedHeader || ''}
        onSelectType={handleMapColumn}
      />

      <DataMapping
        headers={headers}
        rows={rows}
        onHeaderClick={handleHeaderClick}
        getColumnType={getColumnType}
      />

      {mappedColumns.missing.length > 0 && !uploader.isUploading && (
        <Alert variant="default">
          <AlertTriangle className="h-4 w-4" />
          <AlertTitle>Eksik Eşleştirme</AlertTitle>
          <AlertDescription>
            Yüklemeye devam etmek için lütfen şu zorunlu alanları eşleştirin: <strong>{mappedColumns.missing.join(', ')}</strong>
          </AlertDescription>
        </Alert>
      )}
      
      {uploader.error && (
          <Alert variant="destructive">
              <AlertTriangle className="h-4 w-4" />
              <AlertTitle>Yükleme Hatası</AlertTitle>
              <AlertDescription>{uploader.error}</AlertDescription>
          </Alert>
      )}

      {uploader.isUploading ? (
        <div className="space-y-2">
            <p className="text-sm font-medium text-center">Firmalar yükleniyor...</p>
            <Progress value={uploader.progress} />
        </div>
      ) : (
        <div className="flex justify-end space-x-2">
          <Button variant="outline" onClick={resetMapper}>Sıfırla</Button>
          <Button
            onClick={handleUpload}
            disabled={!selectedSicilMudurluk || mappedColumns.missing.length > 0}
          >
            Firmaları Yükle
          </Button>
        </div>
      )}
    </div>
  );
};

const FileProcessedState: FC<{ fileData: ProcessedFileData; onReset: () => void }> = ({ fileData, onReset }) => {
  const [selectedSicilMudurluk, setSelectedSicilMudurluk] = useState<string>('');

  return (
    <Card className="w-full max-w-4xl mx-auto">
      <CardHeader>
        <div className="flex justify-between items-start">
          <div>
            <CardTitle>Veri Eşleştirme</CardTitle>
            <CardDescription>{fileData.fileName}</CardDescription>
          </div>
          <Button variant="ghost" size="sm" onClick={onReset}><X className="h-4 w-4 mr-2" />İptal</Button>
        </div>
      </CardHeader>
      <CardContent className="space-y-4">
        <div>
          <label htmlFor="sicil-mudurlugu" className="block text-sm font-medium text-gray-700 mb-1">Sicil Müdürlüğü</label>
          <Select onValueChange={setSelectedSicilMudurluk} value={selectedSicilMudurluk}>
            <SelectTrigger className="w-[320px]" id="sicil-mudurlugu">
              <SelectValue placeholder="Lütfen bir Sicil Müdürlüğü seçin..." />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="İSTANBUL TİCARET SİCİLİ MÜDÜRLÜĞÜ">İSTANBUL TİCARET SİCİLİ MÜDÜRLÜĞÜ</SelectItem>
              <SelectItem value="ANKARA TİCARET SİCİLİ MÜDÜRLÜĞÜ">ANKARA TİCARET SİCİLİ MÜDÜRLÜĞÜ</SelectItem>
              <SelectItem value="İZMİR TİCARET SİCİLİ MÜDÜRLÜĞÜ">İZMİR TİCARET SİCİLİ MÜDÜRLÜĞÜ</SelectItem>
              {/* Diğer müdürlükler buraya eklenebilir */}
            </SelectContent>
          </Select>
        </div>

        {fileData.sheets.length === 1 ? (
          <SheetMappingInterface sheet={fileData.sheets[0]} selectedSicilMudurluk={selectedSicilMudurluk} onReset={onReset} />
        ) : (
          <Tabs defaultValue={fileData.sheets[0].sheetName} className="w-full">
            <TabsList>
              {fileData.sheets.map(sheet => (
                <TabsTrigger key={sheet.sheetName} value={sheet.sheetName}>{sheet.sheetName}</TabsTrigger>
              ))}
            </TabsList>
            {fileData.sheets.map(sheet => (
              <TabsContent key={sheet.sheetName} value={sheet.sheetName}>
                <SheetMappingInterface sheet={sheet} selectedSicilMudurluk={selectedSicilMudurluk} onReset={onReset} />
              </TabsContent>
            ))}
          </Tabs>
        )}
      </CardContent>
    </Card>
  );
};

const PdfTableSelector: FC<{ 
  tables: ParsedTable[]; 
  fileName: string;
  onSelectTable: (table: ParsedTable) => void; 
  onReset: () => void;
}> = ({ tables, fileName, onSelectTable, onReset }) => {
  const [selectedValue, setSelectedValue] = useState<string>('');

  const handleSelect = () => {
    const selected = tables.find(t => t.table_name === selectedValue);
    if (selected) {
      onSelectTable(selected);
    }
  };

  return (
    <Card className="w-full max-w-2xl mx-auto">
      <CardHeader className="flex flex-row justify-between items-start">
        <div>
          <CardTitle>PDF Tablo Seçimi</CardTitle>
          <CardDescription>{fileName}</CardDescription>
        </div>
        <Button variant="ghost" size="sm" onClick={onReset}>
            <X className="h-4 w-4 mr-2" />
            İptal
        </Button>
      </CardHeader>
      <CardContent className="space-y-4">
        <Select onValueChange={setSelectedValue} value={selectedValue}>
          <SelectTrigger>
            <SelectValue placeholder="Bir tablo seçin..." />
          </SelectTrigger>
          <SelectContent>
            {tables.map(table => (
              <SelectItem key={table.table_name} value={table.table_name}>
                {table.table_name}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
        <Button onClick={handleSelect} disabled={!selectedValue} className="w-full">
          Seçili Tabloyla Devam Et
        </Button>
      </CardContent>
    </Card>
  );
};

export default function FileUploadSection() {
  const processor = useFileProcessor();
  const [selectedPdfTable, setSelectedPdfTable] = useState<ParsedTable | null>(null);

  const handleReset = useCallback(() => {
    processor.reset();
    setSelectedPdfTable(null);
  }, [processor]);

  // 1. Show processing state
  if (processor.isProcessing) {
    return (
      <Card className="w-full max-w-2xl mx-auto">
        <CardHeader>
          <CardTitle>Dosya İşleniyor</CardTitle>
          <CardDescription>{processor.currentFile?.name || 'Lütfen bekleyin...'}</CardDescription>
        </CardHeader>
        <CardContent>
          <ProcessingState progress={processor.isProcessingExcel ? processor.excelProgress : 50} />
        </CardContent>
      </Card>
    );
  }

  // 2. Show error state
  if (processor.error) {
    return (
      <Card className="w-full max-w-2xl mx-auto">
        <CardHeader><CardTitle>Hata</CardTitle></CardHeader>
        <CardContent>
          <Alert variant="destructive">
            <AlertTriangle className="h-4 w-4" />
            <AlertTitle>Dosya işlenemedi!</AlertTitle>
            <AlertDescription>{processor.error}</AlertDescription>
          </Alert>
          <Button onClick={handleReset} className="mt-4">Tekrar Dene</Button>
        </CardContent>
      </Card>
    );
  }

  // 3. Show PDF table selector if PDF is processed
  if (processor.isPdfSuccess && processor.pdfData.length > 0 && !selectedPdfTable) {
    return (
      <PdfTableSelector
        tables={processor.pdfData}
        fileName={processor.currentFile?.name || 'PDF Dosyası'}
        onSelectTable={setSelectedPdfTable}
        onReset={handleReset}
      />
    );
  }

  // 4. Show data mapping for a selected PDF table
  if (selectedPdfTable && processor.currentFile) {
    const sheetResult: ExcelSheetResult = {
      sheetName: selectedPdfTable.table_name,
      headers: selectedPdfTable.headers,
      data: selectedPdfTable.rows.map((row) =>
        selectedPdfTable.headers.map((header) => {
          const value = row[header];
          if (typeof value === 'string' || typeof value === 'number' || value === null) {
            return value;
          }
          return String(value ?? '');
        })
      ),
      totalRows: selectedPdfTable.rows.length,
    };

    const fileData: ProcessedFileData = {
      fileName: processor.currentFile.name,
      sheets: [sheetResult],
    };

    return <FileProcessedState fileData={fileData} onReset={handleReset} />;
  }

  // 5. Show data mapping for a processed Excel file
  if (processor.excelData && processor.excelData.sheets.length > 0) {
    return <FileProcessedState fileData={processor.excelData} onReset={handleReset} />;
  }

  // 6. Show initial dropzone
  return (
    <Card className="w-full max-w-2xl mx-auto">
      <CardHeader>
        <CardTitle>Dosyadan Firma Aktarımı</CardTitle>
        <CardDescription>Toplu firma verisi yüklemek için bir XLSX, XLS veya PDF dosyası seçin.</CardDescription>
      </CardHeader>
      <CardContent>
        <FileDropzone
          getRootProps={processor.getRootProps}
          getInputProps={processor.getInputProps}
          isDragActive={processor.isDragActive}
        />
      </CardContent>
    </Card>
  );
}