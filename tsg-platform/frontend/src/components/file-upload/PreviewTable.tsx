import type { ExcelProcessResult } from "@/lib/types/file.types";

interface PreviewTableProps {
  previewData: ExcelProcessResult;
}

export function PreviewTable({ 
  previewData 
}: PreviewTableProps) {
  // Eğer veri yoksa veya başarısızsa hiçbir şey gösterme
  if (!previewData?.success || !previewData.sheets?.length) return null;

  return (
    <div className="space-y-6">
      {previewData.sheets.map((sheet, sheetIndex) => (
        <div key={sheetIndex} className="border rounded-md overflow-hidden">
          <div className="bg-gray-50 px-4 py-2 border-b">
            <h4 className="text-md font-medium">
              Sayfa: {sheet.sheetName} (Toplam {sheet.rows.length} satır, {sheet.headers.length} sütun)
            </h4>
          </div>
          <div className="overflow-auto max-h-96">
            <table className="w-full text-sm">
              <thead>
                <tr className="bg-gray-100">
                  {sheet.headers.map((header, index) => (
                    <th 
                      key={index} 
                      className="px-4 py-2 text-left font-medium text-gray-700 whitespace-nowrap"
                    >
                      {header || `Sütun ${index + 1}`}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {sheet.rows.slice(0, 5).map((row, rowIndex) => (
                  <tr key={rowIndex} className="border-t">
                    {sheet.headers.map((header, colIndex) => (
                      <td 
                        key={colIndex} 
                        className="px-4 py-2 text-sm"
                      >
                        {row[header] !== undefined ? String(row[header]).slice(0, 100) : ''}
                      </td>
                    ))}
                  </tr>
                ))}
                {sheet.rows.length > 5 && (
                  <tr>
                    <td colSpan={sheet.headers.length} className="text-center py-2 text-sm text-gray-500">
                      Toplam {sheet.rows.length} satırdan ilk 5 gösteriliyor
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>
      ))}
    </div>
  );
}
