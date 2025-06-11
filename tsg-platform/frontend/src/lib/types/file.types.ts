// Tablo başlık tipi
export interface TableHeader {
  key: string;
  name: string;
  label: string;
  sortable?: boolean;
  resizable?: boolean;
  minWidth?: number;
  type?: string;
  visible?: boolean;
}

// Excel sayfa sonucu tipi
export interface ExcelSheetResult {
  sheetName: string;
  headers: string[];
  rows: Record<string, any>[];
}

// Excel işleme sonucu tipi
export interface ExcelProcessResult {
  success: boolean;
  fileName: string;
  sheets: ExcelSheetResult[];
  error?: string;
}

// PDF işleme sonucu tipi
export interface PdfProcessResult {
  success: boolean;
  file: File;
  fileName: string;
  fileSize: number;
  fileType: string;
  uploadedAt: Date;
  text?: string;
  pageCount?: number;
  metadata?: Record<string, any>;
  error?: string;
  meta?: {
    processedAt?: string;
    error?: boolean;
    [key: string]: any;
  };
}

// Özel dosya tipi
export interface CustomFile extends File {
  id: string;
  status: 'waiting' | 'processing' | 'success' | 'error';
  error?: string;
  progress: number;
  previewData?: ExcelProcessResult;
  müdürlük: string;
  uploadedAt: Date;
  formattedSize: string;
}
