import { useState, useCallback, useMemo } from 'react';
import { companySchema, CompanyData } from '@/types/company.types';

export type ColumnType = 'sicil_no' | 'firma_unvani' | 'sicil_mudurluk' | 'adres' | 'none';

const REQUIRED_COLUMNS: ColumnType[] = ['sicil_no', 'firma_unvani'];

export interface MappedDataResult {
  isValid: boolean;
  data: CompanyData[];
  missingColumns: ColumnType[];
  errorCount: number;
}

/**
 * Excel ve PDF'ten gelen verileri işleme, sütunları eşleştirme ve doğrulama mantığını yöneten kapsamlı hook.
 * @param initialData - İlk satırı başlık olan, ham veri dizisi.
 */
export const useColumnMapper = (initialData: (string | number | null)[][]) => {
  const { headers, rows } = useMemo(() => {
    if (!initialData || initialData.length < 1) {
      return { headers: [], rows: [] };
    }
    const headerRow = initialData[0].map(String);
    const dataRows = initialData.slice(1).map(row => {
      const rowObject: Record<string, unknown> = {};
      headerRow.forEach((header, index) => {
        rowObject[header] = row[index];
      });
      return rowObject;
    });
    return { headers: headerRow, rows: dataRows };
  }, [initialData]);

  const [selections, setSelections] = useState<Record<string, ColumnType>>({});
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedHeader, setSelectedHeader] = useState<string | null>(null);

  const reset = useCallback(() => {
    setSelections({});
    setIsModalOpen(false);
    setSelectedHeader(null);
  }, []);

  const handleHeaderClick = useCallback((header: string) => {
    setSelectedHeader(header);
    setIsModalOpen(true);
  }, []);

  const closeModal = useCallback(() => {
    setIsModalOpen(false);
    setSelectedHeader(null);
  }, []);

  const handleMapColumn = useCallback((type: ColumnType) => {
    if (!selectedHeader) return;

    setSelections(prev => {
      const newSelections = { ...prev };

      // Eğer bu tip başka bir başlığa atanmışsa, o atamayı kaldır
      Object.keys(newSelections).forEach(key => {
        if (newSelections[key] === type) {
          delete newSelections[key];
        }
      });

      // Yeni tipi ata veya mevcut tipi kaldır
      if (type !== 'none' && prev[selectedHeader] !== type) {
        newSelections[selectedHeader] = type;
      } else {
        delete newSelections[selectedHeader];
      }
      
      return newSelections;
    });

    closeModal();
  }, [selectedHeader, closeModal]);

  const getColumnType = useCallback((header: string): ColumnType | undefined => selections[header], [selections]);

  const mappedColumns = useMemo(() => {
    const assignedTypes = new Set(Object.values(selections));
    const missing = REQUIRED_COLUMNS.filter(col => !assignedTypes.has(col));
    const isValid = missing.length === 0;

    return { assignedTypes, missing, isValid };
  }, [selections]);

  const getMappedData = useCallback((): MappedDataResult => {
    if (!mappedColumns.isValid) {
      return { isValid: false, data: [], missingColumns: mappedColumns.missing, errorCount: 0 };
    }

    const mappedData: CompanyData[] = [];
    let errorCount = 0;

    const reverseMapping: Partial<Record<ColumnType, string>> = {};
    for (const key in selections) {
      if (Object.prototype.hasOwnProperty.call(selections, key)) {
        reverseMapping[selections[key]] = key;
      }
    }

    rows.forEach(row => {
      const companyObject: Partial<CompanyData> = {};
      for (const type in reverseMapping) {
        const colType = type as ColumnType;
        if (colType !== 'none') {
          companyObject[colType] = String(row[reverseMapping[colType]!] ?? '');
        }
      }

      const validation = companySchema.safeParse(companyObject);
      if (validation.success) {
        mappedData.push(validation.data as CompanyData);
      } else {
        errorCount++;
      }
    });

    return { isValid: true, data: mappedData, missingColumns: [], errorCount };
  }, [selections, rows, mappedColumns]);

  return {
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
    reset,
  };
};
