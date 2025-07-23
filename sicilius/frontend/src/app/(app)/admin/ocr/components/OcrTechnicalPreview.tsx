'use client';

import { useState } from 'react';
import axios from 'axios';
import { Icons } from '@/components/icons';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

interface OcrResult {
  announcement_id: string;
  ocr_text: string;
  pdf_image_base64: string | null;
}

export default function OcrTechnicalPreview() {
  const [batchSize, setBatchSize] = useState(10);
  const [results, setResults] = useState<OcrResult[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const startOCR = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await axios.post('/api/v1/batch_ocr/process-and-preview', { limit: batchSize });
      setResults(response.data);
    } catch (err) {
      setError('OCR işlemi sırasında bir hata oluştu.');
      console.error(err);
    }
    setIsLoading(false);
  };

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>Teknik OCR Önizleme</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div>
              <label htmlFor="batch-size" className="block text-sm font-medium text-gray-700">İşlenecek İlan Sayısı</label>
              <input
                type="number"
                id="batch-size"
                value={batchSize}
                onChange={(e) => setBatchSize(parseInt(e.target.value, 10))}
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
              />
            </div>
            <Button onClick={startOCR} disabled={isLoading}>
              {isLoading ? (
                <>
                  <Icons.spinner className="mr-2 h-4 w-4 animate-spin" />
                  İşleniyor...
                </>
              ) : 'Önizlemeyi Başlat'}
            </Button>
            {error && <p className="text-sm text-red-600">{error}</p>}
          </div>
        </CardContent>
      </Card>

      {results.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle>OCR Sonuçları</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {results.map((result) => (
                <div key={result.announcement_id} className="grid grid-cols-1 md:grid-cols-2 gap-6 border-b pb-4 last:border-b-0">
                  <div>
                    <h4 className="font-bold mb-2">PDF Görüntüsü (İlk Sayfa)</h4>
                    {result.pdf_image_base64 ? (
                      <img src={`data:image/jpeg;base64,${result.pdf_image_base64}`} alt={`PDF preview for ${result.announcement_id}`} className="rounded-md border" />
                    ) : (
                      <div className="flex items-center justify-center h-48 bg-gray-100 rounded-md">
                        <p className="text-gray-500">Görüntü oluşturulamadı.</p>
                      </div>
                    )}
                  </div>
                  <div>
                    <h4 className="font-bold mb-2">OCR Metni</h4>
                    <pre className="whitespace-pre-wrap text-sm bg-gray-50 p-3 rounded-md h-48 overflow-auto">{result.ocr_text || 'Metin bulunamadı.'}</pre>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
