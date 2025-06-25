import * as XLSX from 'xlsx';

// Represents a single sheet from the processed Excel file.
// The first row is treated as headers, and the rest is data.
export interface ExcelSheetResult {
  sheetName: string;
  headers: string[];
  data: unknown[][]; // Data rows (excluding the header)
  totalRows: number; // Number of data rows
}

// Represents the entire processed file data.
export interface ProcessedFileData {
  fileName: string;
  sheets: ExcelSheetResult[];
}

// Represents the result of the Excel processing operation, including success status and any errors.
export interface ExcelProcessResult {
  success: boolean;
  fileName: string;
  sheets: ExcelSheetResult[];
  error?: string;
}

/**
 * Processes an Excel file and extracts the data from each sheet into a raw 2D array.
 * This function avoids any complex header detection or data manipulation, providing a "what you see is what you get" result.
 * @param file The Excel file to process.
 * @returns A promise that resolves with the processed data or an error.
 */
export async function processExcelFile(file: File): Promise<ExcelProcessResult> {
  try {
    const arrayBuffer = await file.arrayBuffer();
    if (!arrayBuffer?.byteLength) {
      throw new Error('Dosya boş veya okunamadı.');
    }

    const workbook = XLSX.read(arrayBuffer, { type: 'array' });
    if (!workbook.SheetNames?.length) {
      throw new Error('Excel dosyasında çalışma sayfası bulunamadı.');
    }

    const processedSheets: ExcelSheetResult[] = [];

    for (const sheetName of workbook.SheetNames) {
      const worksheet = workbook.Sheets[sheetName];
      if (!worksheet) continue;

      // Convert sheet to a raw array of arrays. `header: 1` ensures this format.
      // `defval: ''` ensures empty cells are represented as empty strings.
      const data: unknown[][] = XLSX.utils.sheet_to_json(worksheet, { header: 1, defval: '' });

      // Filter out rows that are completely empty.
      const filteredData = data.filter(
        (row) => Array.isArray(row) && row.some((cell) => cell !== null && cell !== undefined && String(cell).trim() !== '')
      );

      if (filteredData.length > 0) {
        // Assume the first non-empty row is the header.
        const headers = filteredData[0].map(String);
        const dataRows = filteredData.slice(1);

        if (dataRows.length > 0) {
          processedSheets.push({
            sheetName,
            headers,
            data: dataRows,
            totalRows: dataRows.length,
          });
        }
      }
    }

    if (processedSheets.length === 0) {
      throw new Error('Dosyada işlenebilir veri bulunamadı.');
    }

    return {
      success: true,
      fileName: file.name,
      sheets: processedSheets,
    };
  } catch (error) {
    console.error('Excel işleme hatası:', error);
    return {
      success: false,
      fileName: file.name,
      sheets: [],
      error: error instanceof Error ? error.message : 'Bilinmeyen bir hata oluştu',
    };
  }
}