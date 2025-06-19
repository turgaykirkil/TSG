import * as XLSX from 'xlsx';

export interface ExcelSheetResult {
  sheetName: string;
  headers: string[];
  rows: Record<string, any>[];
  isCombined?: boolean;
  totalRows?: number;
}

export interface ExcelProcessResult {
  success: boolean;
  fileName: string;
  sheets: ExcelSheetResult[];
  error?: string;
}

export async function processExcelFile(file: File): Promise<ExcelProcessResult> {
  try {
    // 1. Dosyayı oku
    const arrayBuffer = await file.arrayBuffer();
    if (!arrayBuffer?.byteLength) {
      throw new Error('Dosya boş veya okunamadı');
    }

    // 2. Workbook'u oku
    const workbook = XLSX.read(arrayBuffer, { type: 'array' });
    if (!workbook.SheetNames?.length) {
      throw new Error('Excel dosyasında çalışma sayfası bulunamadı');
    }

    const result: ExcelProcessResult = {
      success: true,
      fileName: file.name,
      sheets: []
    };

    // 3. Tüm sayfaları işle
    for (const sheetName of workbook.SheetNames) {
      const worksheet = workbook.Sheets[sheetName];
      if (!worksheet) continue;

      // 4. JSON'a dönüştür
      const jsonData = XLSX.utils.sheet_to_json<any>(worksheet, { header: 1, defval: '' });
      if (!jsonData?.length) continue;

      // 5. Başlıkları al (Her zaman ilk satır başlık olarak alınacak)
      const headers = jsonData[0]?.map((cell: any) => String(cell || '').trim()) || [];
      if (!headers?.length) continue;

      // 6. Veri satırlarını işle
      const rows: Record<string, any>[] = [];
      for (let i = 1; i < jsonData.length; i++) {
        const rowData = jsonData[i];
        if (!Array.isArray(rowData)) continue;
        
        const row: Record<string, any> = {};
        rowData.forEach((cell: any, index: number) => {
          if (index < headers.length) {
            row[headers[index]] = cell !== undefined && cell !== null ? String(cell).trim() : '';
          }
        });
        
        // Boş olmayan en az bir hücre içeren satırları ekle
        if (Object.values(row).some(val => val && val.trim() !== '')) {
          rows.push(row);
        }
      }

      // 7. Sonuçları ekle
      if (rows.length > 0) {
        result.sheets.push({
          sheetName,
          headers,
          rows,
          isCombined: false,
          totalRows: rows.length
        });
      }
    }

    if (result.sheets.length === 0) {
      throw new Error('İşlenebilir veri bulunamadı');
    }

    return result;
  } catch (error) {
    console.error('Excel işleme hatası:', error);
    return {
      success: false,
      fileName: file.name,
      sheets: [],
      error: error instanceof Error ? error.message : 'Bilinmeyen bir hata oluştu'
    };
  }
}