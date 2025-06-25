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
  rows: Record<string, unknown>[];
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
  metadata?: Record<string, unknown>;
  error?: string;
  meta?: {
    processedAt?: string;
    error?: boolean;
    [key: string]: unknown;
  };
}

// Özel dosya tipi
export interface CustomFile extends File {
  id: string;
  status: 'waiting' | 'processing' | 'success' | 'error' | 'partial';
  error?: string;
  info?: string; // Bilgi mesajları için
  progress: number;
  previewData?: ExcelProcessResult;
  formattedSize?: string;
  previewUrl?: string;
  fileType?: string;
  uploadedAt?: Date;
  insertedCount?: number; // Başarıyla eklenen kayıt sayısı
  meta?: Record<string, unknown>;
  müdürlük: string;
}
