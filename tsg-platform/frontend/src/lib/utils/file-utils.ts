import * as XLSX from 'xlsx';
import { v4 as uuidv4 } from 'uuid';
import type { CustomFile, ExcelProcessResult, ExcelSheetResult } from '../types/file.types';

/**
 * Excel dosyasını işler ve sonuçları döndürür
 */
export async function processExcelFile(file: File): Promise<ExcelProcessResult> {
  try {
    const arrayBuffer = await file.arrayBuffer();
    const workbook = XLSX.read(arrayBuffer, { type: 'array' });
    const result: ExcelProcessResult = { 
      success: true, 
      fileName: file.name,
      sheets: []
    };

    // Tüm sayfaları işle
    for (const sheetName of workbook.SheetNames) {
      const worksheet = workbook.Sheets[sheetName];
      const jsonData = XLSX.utils.sheet_to_json(worksheet, { header: 1, defval: '' }) as any[][];
      
      if (jsonData.length === 0) continue;
      
      // Ankara dosyalarında başlık ikinci satırda
      const isAnkara = file.name.toLowerCase().includes('ankara');
      const headerRowIndex = isAnkara ? 1 : 0;
      const dataStartIndex = isAnkara ? 2 : 1;
      
      const headers = (jsonData[headerRowIndex] || [])
        .map((header: any) => String(header).trim())
        .filter(Boolean);
      
      if (headers.length === 0) continue;
      
      const rows: Record<string, any>[] = [];
      
      // Veri satırlarını işle
      for (let i = dataStartIndex; i < jsonData.length; i++) {
        const row = jsonData[i] || [];
        const rowData: Record<string, any> = {};
        
        // Sadece dolu satırları ekle
        if (!row.some(cell => cell !== '')) continue;
        
        // Sütunları başlıklara göre eşleştir
        headers.forEach((header, colIndex) => {
          rowData[header] = row[colIndex] !== undefined ? String(row[colIndex]).trim() : '';
        });
        
        rows.push(rowData);
      }
      
      if (rows.length > 0) {
        const sheetResult: ExcelSheetResult = {
          sheetName,
          headers,
          rows
        };
        
        result.sheets.push(sheetResult);
      }
    }
    
    if (result.sheets.length === 0) {
      throw new Error('İşlenebilir veri bulunamadı');
    }
    
    return result;
    
  } catch (error) {
    return {
      success: false,
      fileName: file.name,
      sheets: [],
      error: error instanceof Error ? error.message : 'Bilinmeyen bir hata oluştu'
    };
  }
}

/**
 * Dosya boyutunu okunabilir formata çevirir
 */
export function formatFileSize(bytes?: number): string {
  if (!bytes && bytes !== 0) return 'Boyut bilinmiyor';
  if (bytes === 0) return '0 Byte';
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

/**
 * Özel bir dosya nesnesi oluşturur
 */
export function createCustomFile(file: File): CustomFile {
  return {
    ...file,
    id: uuidv4(),
    status: 'waiting' as const,
    progress: 0,
    error: undefined,
    previewData: undefined,
    müdürlük: '',
    uploadedAt: new Date(),
    formattedSize: formatFileSize(file.size)
  };
}
