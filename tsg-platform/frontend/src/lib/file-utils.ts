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

      // 5. Başlık satırını belirle (İlk sheet ve Ankara ise 2. satır, diğerleri 1. satır)
      const isFirstSheet = sheetName === workbook.SheetNames[0];
      const isAnkara = file.name.toLowerCase().includes('ankara');
      const headerRowIndex = (isFirstSheet && isAnkara) ? 1 : 0;
      const dataStartIndex = (isFirstSheet && isAnkara) ? 2 : 1;

      // 6. Başlıkları al ve temizle
      const headers = (jsonData[headerRowIndex] || [])
        .map((header: any) => String(header || '').trim())
        .filter(Boolean);
      
      if (headers.length === 0) continue;

      // 7. Veri satırlarını işle
      const rows: Record<string, any>[] = [];
      for (let i = dataStartIndex; i < jsonData.length; i++) {
        const row = jsonData[i] || [];
        if (!Array.isArray(row)) continue;

        const rowData: Record<string, any> = {};
        headers.forEach((header: string, index: number) => {
          const value = row[index];
          rowData[header] = value !== undefined && value !== null ? String(value).trim() : '';
        });
        
        // Boş olmayan en az bir hücre içeren satırları ekle
        if (Object.values(rowData).some(val => val && val.trim() !== '')) {
          rows.push(rowData);
        }
      }

      if (rows.length > 0) {
        result.sheets.push({
          sheetName,
          headers,
          rows
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