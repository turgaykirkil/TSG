import * as XLSX from 'xlsx';

// ========== TİP TANIMLAMALARI ==========

/** Excel'den okunan ham veri yapısı */
export interface ExcelRawData {
  headers: string[];
  rows: any[][];
  sheetName: string;
  sheetNames: string[];
  totalRows: number;
  totalColumns: number;
}

/** Tablo başlık tanımı */
export interface TableHeader {
  key: string;
  name: string;
  sortable: boolean;
  resizable: boolean;
  minWidth: number;
}

/** Excel işleme sonucu tipi */
export interface ExcelProcessResult {
  headers: TableHeader[];
  rows: Array<Record<string, any>>;
  allRows: Array<Record<string, any>>;
  currentPage: number;
  pageSize: number;
  hasMore: boolean;
  total: number;
  sheetName: string;
  sheetNames: string[];
  totalRows: number;
  totalColumns: number;
}

// Excel okuma seçenekleri
interface ExcelReadOptions extends XLSX.ParsingOptions {
  cellDates?: boolean;
  cellStyles?: boolean;
  sheetStubs?: boolean;
}

// Excel yazma seçenekleri
interface ExcelWriteOptions extends XLSX.WritingOptions {
  bookType?: XLSX.BookType;
  bookSST?: boolean;
  type?: 'base64' | 'binary' | 'buffer' | 'file' | 'array' | 'string';
}

// Excel dosyasını işleme sonucu
type ProcessExcelResult = {
  success: boolean;
  data?: ExcelProcessResult;
  error?: string;
  file: File;
  fileName: string;
  fileSize: number;
  fileType: string;
  uploadedAt: Date;
};

// ========== FONKSİYONLAR ==========

/**
 * Excel dosyasından ham veriyi okur
 * @param file - Okunacak Excel dosyası
 * @returns Excel'den okunan ham veri
 */
export async function readExcelFile(file: File): Promise<ExcelRawData> {
  const arrayBuffer = await file.arrayBuffer();
  const workbook = XLSX.read(arrayBuffer, { type: 'array' });
  
  const result: ExcelRawData = {
    headers: [],
    rows: [],
    sheetName: '',
    sheetNames: [],
    totalRows: 0,
    totalColumns: 0
  };

  // Tüm sayfa isimlerini kaydet
  result.sheetNames = [...workbook.SheetNames];
  
  // Sadece ilk sayfayı oku
  result.sheetName = workbook.SheetNames[0] || '';
  if (!result.sheetName) return result;

  const worksheet = workbook.Sheets[result.sheetName];
  const jsonData = XLSX.utils.sheet_to_json<any[]>(worksheet, {
    header: 1,
    defval: '',
  });

  if (jsonData.length === 0) return result;

  // İlk satırı başlık olarak al
  result.headers = (jsonData[0] || []).map((cell: any) => 
    cell !== null && cell !== undefined ? cell.toString().trim() : ''
  );

  // Diğer satırları veri olarak al
  result.rows = jsonData.slice(1)
    .map(row => 
      Array.isArray(row) 
        ? row.map(cell => cell !== null && cell !== undefined ? cell.toString().trim() : '')
        : []
    )
    .filter(row => row.length > 0); // Boş satırları filtrele

  // Toplam satır ve sütun sayılarını hesapla
  result.totalRows = result.rows.length;
  result.totalColumns = result.headers.length || (result.rows[0]?.length || 0);

  return result;
}

/**
 * Excel dosyasını işler ve sonuçları döndürür
 */
export async function processExcelFile(file: File): Promise<ProcessExcelResult> {
  try {
    const excelData = await readExcelFile(file);
    
    if (excelData.rows.length === 0) {
      throw new Error('Excel dosyası boş veya okunamadı');
    }
    
    // Başlıkları işle
    const headers: TableHeader[] = excelData.headers.map((header, index) => ({
      key: `col${index}`,
      name: header || `Sütun ${index + 1}`,
      sortable: true,
      resizable: true,
      minWidth: 150
    }));
    
    // Tüm satırları işle
    const allRows = excelData.rows.map((row, rowIndex) => {
      const rowData: Record<string, any> = { id: rowIndex };
      row.forEach((cell, cellIndex) => {
        rowData[`col${cellIndex}`] = cell;
      });
      return rowData;
    });
    
    // Sayfalama için ilk 10 satırı al
    const pageSize = 10;
    const rows = allRows.slice(0, pageSize);
    
    const result: ExcelProcessResult = {
      headers,
      rows,
      allRows,
      currentPage: 1,
      pageSize,
      hasMore: allRows.length > pageSize,
      total: allRows.length,
      sheetName: excelData.sheetName,
      sheetNames: excelData.sheetNames,
      totalRows: excelData.totalRows,
      totalColumns: excelData.totalColumns
    };
    
    return {
      success: true,
      data: result,
      file,
      fileName: file.name,
      fileSize: file.size,
      fileType: file.type,
      uploadedAt: new Date()
    };
  } catch (error) {
    return {
      success: false,
      error: error instanceof Error ? error.message : 'Bilinmeyen bir hata oluştu',
      file,
      fileName: file.name,
      fileSize: file.size,
      fileType: file.type,
      uploadedAt: new Date()
    };
  }
}

// ========== SABİTLER ==========

/** Müdürlük listesi */
export const MÜDÜRLÜKLER = [
  { value: 'ankara', label: 'Ankara' },
  { value: 'istanbul', label: 'İstanbul' },
  { value: 'izmir', label: 'İzmir' },
];

// Dosya durum tipleri
export type FileStatus = 'waiting' | 'processing' | 'completed' | 'error';

// Dosya önizleme veri yapısı
export interface FilePreviewData {
  id: string;
  name: string;
  type: string;
  size: number;
  status: FileStatus;
  progress: number;
  error?: string;
  previewData?: ExcelProcessResult;
  uploadedAt: Date;
  file: File;
  data: Record<string, any>;
}

// ========== YARDIMCI FONKSİYONLAR ==========

/**
      type: 'array',
      cellDates: true,
      cellText: false,
      cellNF: false
    };
    
    const workbook = XLSX.read(arrayBuffer, readOptions);
    const sheetNames = workbook.SheetNames;
    
    if (sheetNames.length === 0) {
      throw new Error('Excel dosyasında sayfa bulunamadı');
    }
    
    // İlk sayfayı işle
    const firstSheet = workbook.Sheets[sheetNames[0]];
    
    // JSON'a dönüştürme seçenekleri
    const jsonOptions: SheetToJsonOptions = {
      header: 1,
      defval: '',
      blankrows: false,
      raw: false,
      dateNF: 'dd.mm.yyyy',
      cellDates: true
    };
    
    const jsonData = XLSX.utils.sheet_to_json<Record<string, any>>(firstSheet, jsonOptions);
    
    if (jsonData.length === 0) {
      throw new Error('Excel sayfası boş görünüyor');
    }
    
    // Başlıkları al (boş olmayan hücreleri filtrele)
    const firstRow = jsonData[0];
    if (!Array.isArray(firstRow)) {
      throw new Error('Geçersiz Excel formatı: İlk satır başlık bilgisi içermiyor');
    }
    
    const headers = firstRow
      .map((header: any) => {
        if (header === null || header === undefined) return '';
        return String(header).trim();
      })
      .filter(Boolean);
    
    if (headers.length === 0) {
      throw new Error('Excel dosyasında geçerli başlık bulunamadı');
    }
    
    // Veri satırlarını işle
    const rows: ExcelRowData[] = [];
    
    for (let i = 1; i < jsonData.length; i++) {
      const row = jsonData[i];
      if (!row || !Array.isArray(row)) continue;
      
      const rowData: ExcelRowData = { id: i };
      let hasData = false;
      
      // Sütun sayısı kadar döngü yap
      for (let j = 0; j < headers.length; j++) {
        const header = headers[j];
        const cellValue = j < row.length ? row[j] : null;
        
        // Değeri temizle ve dönüştür
        if (cellValue !== null && cellValue !== undefined && cellValue !== '') {
          let processedValue: string | number | boolean | null = cellValue;
          
          // Değer tipine göre işle
          if (cellValue instanceof Date) {
            // Tarih değerini ISO formatına çevir
            processedValue = cellValue.toISOString().split('T')[0];
          } else if (typeof cellValue === 'object') {
            // Nesne ise stringe çevir
            processedValue = JSON.stringify(cellValue);
          } else if (typeof cellValue === 'string') {
            // String ise trim yap
            processedValue = cellValue.trim();
          }
          
          // Eğer işlenmiş değer boş değilse ekle
          if (processedValue !== '' && processedValue !== null) {
            rowData[header] = processedValue;
            hasData = true;
          } else {
            rowData[header] = null;
          }
        } else {
          rowData[header] = null;
        }
      }
      
      // Eğer satırda en az bir veri varsa ekle
      if (hasData) {
        rows.push(rowData);
      }
    }
    
    if (rows.length === 0) {
      console.warn('Excel dosyasında işlenebilir veri bulunamadı');
    }
    
    return {
      rows,
      headers,
      sheetName: sheetNames[0],
      sheetNames,
      totalRows: rows.length,
      totalColumns: headers.length
    };
    
  } catch (error) {
    console.error('Excel okuma hatası:', error);
    throw new Error(`Excel dosyası işlenirken bir hata oluştu: ${error instanceof Error ? error.message : String(error)}`);
  }
};

/**
 * PDF dosyasını işler (şimdilik örnek veri döndürür)
 */
const processPdfFile = async (file: File, mudurluk?: string): Promise<PdfProcessResult> => {
  console.log('PDF işleniyor:', file.name, 'Müdürlük:', mudurluk);
  
  // Gerçek bir PDF işleme mantığı buraya gelecek
  // Şimdilik örnek veri döndürüyoruz
  return {
    rows: [
      { id: 1, belgeNo: 'PDF-001', konu: 'Örnek PDF Belgesi', tarih: '2023-01-01' },
      { id: 2, belgeNo: 'PDF-002', konu: 'Başka Bir Belge', tarih: '2023-01-02' },
    ],
    headers: ['id', 'belgeNo', 'konu', 'tarih'],
    total: 2
  };
};

/**
 * Excel dosyasını işler
 */
export const processExcelFile = async (file: File, mudurluk?: string): Promise<ExcelProcessResult> => {
  console.log('Excel işleniyor:', file.name, 'Müdürlük:', mudurluk);
  return await readExcelFile(file);
};

/**
 * Veriyi tablo formatına dönüştürür
 */
export const convertToTableData = (data: ExcelProcessResult | PdfProcessResult): any => {
  // Ortak tablo başlıklarını oluştur
  const createTableHeaders = (headers: string[]): TableHeader[] => 
    headers.map(header => ({
      key: header,
      name: header,
      sortable: true,
      resizable: true,
      minWidth: 100
    }));

  if ('sheetName' in data) {
    // Excel verisi
    const tableData = {
      headers: createTableHeaders(data.headers),
      rows: data.rows.slice(0, 10), // İlk 10 satırı göster
      allRows: data.rows, // Tüm satırların bir kopyasını tut
      total: data.rows.length,
      currentPage: 1,
      pageSize: 10,
      hasMore: data.rows.length > 10,
      meta: {
        sheetName: data.sheetName,
        sheetNames: data.sheetNames,
        totalRows: data.totalRows,
        totalColumns: data.totalColumns
      }
    };
    
    return tableData;
  } else {
    // PDF verisi
    const tableData = {
      headers: createTableHeaders(data.headers),
      rows: data.rows.slice(0, 10), // İlk 10 satırı göster
      allRows: data.rows, // Tüm satırların bir kopyasını tut
      total: data.total,
      currentPage: 1,
      pageSize: 10,
      hasMore: data.rows.length > 10,
      meta: {
        total: data.total
      }
    };
    
    return tableData;
  }
};

/**
 * Dosya işleme ana fonksiyonu
 */
export const processFile = async (file: File, mudurluk?: string): Promise<FilePreviewData> => {
  // Varsayılan meta veri
  const defaultMeta = {
    fileName: file?.name || 'Bilinmeyen dosya',
    fileSize: file?.size || 0,
    fileType: file?.type || 'application/octet-stream',
    mudurluk: mudurluk || 'Belirtilmemiş',
    processedAt: new Date().toISOString()
  };

  try {
    // Temel dosya doğrulaması
    if (!file) {
      throw new Error('Dosya seçilmedi');
    }

    // Dosya adı ve uzantı kontrolü
    const fileName = file.name || '';
    const fileExt = (fileName.split('.').pop() || '').toLowerCase();
    
    // Desteklenen uzantıları kontrol et
    if (!['xlsx', 'xls', 'pdf'].includes(fileExt)) {
      throw new Error('Sadece Excel (.xlsx, .xls) veya PDF (.pdf) dosyaları yükleyebilirsiniz');
    }
    
    // Dosya türüne göre işlem yap
    let processedData;
    
    if (fileExt === 'pdf') {
      processedData = await processPdfFile(file, mudurluk);
    } else {
      processedData = await processExcelFile(file, mudurluk);
    }
    
    // Veriyi tablo formatına dönüştür
    const tableData = convertToTableData(processedData);
    
    return {
      success: true,
      data: tableData,
      meta: {
        ...defaultMeta,
        ...tableData.meta
      }
    };
    
  } catch (error) {
    console.error('Dosya işleme hatası:', error);
    const errorMessage = error instanceof Error ? error.message : 'Bilinmeyen bir hata oluştu';
    
    return {
      success: false,
      error: errorMessage,
      meta: {
        ...defaultMeta,
        error: errorMessage
      },
      data: {
        headers: [],
        rows: [],
        total: 0
      }
    };
  }
};
