'use client';

import { useState } from 'react';
import api from '@/lib/axios';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import { Loader2 } from 'lucide-react';
import SupabaseFileSelector from './SupabaseFileSelector';

// Defines the structure for a single OCR text line
interface OcrLine {
  bbox: [number, number, number, number];
  text: string;
}

// Defines the structure for a single page of OCR results
interface OcrPage {
  lines: OcrLine[];
}

// Defines the structure for the entire OCR API result
interface OcrResult {
  announcement_id: number;
  pdf_image_base64: string;
  ocr_data: OcrPage[];
  ocr_text: string;
}

const OcrTechnicalPreview = () => {
  const [result, setResult] = useState<OcrResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [activeLine, setActiveLine] = useState<OcrLine | null>(null);
  const [currentFile, setCurrentFile] = useState<string | null>(null);

  const processDocument = async (fileName: string) => {
    setLoading(true);
    setError(null);
    setResult(null);
    setCurrentFile(fileName);

    try {
      const response = await api.post(`/api/v1/batch_ocr/process-specific-preview/${fileName}`);
      setResult(response.data);
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || `"${fileName}" dosyası işlenemedi.`);
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const renderContent = () => {
    if (loading) {
      return (
        <div className="flex flex-col items-center justify-center p-8 border-2 border-dashed rounded-lg h-96">
          <Loader2 className="h-12 w-12 animate-spin text-primary" />
          <span className="mt-4 text-lg font-semibold">'{currentFile}' işleniyor...</span>
          <p className="text-muted-foreground">Bu işlem birkaç dakika sürebilir.</p>
        </div>
      );
    }

    if (error) {
      return (
        <Alert variant="destructive">
          <AlertTitle>Analiz Başarısız</AlertTitle>
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      );
    }

    if (result) {
      return (
        <Card>
          <CardHeader>
            <CardTitle>Duyuru ID: {result.announcement_id}</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              {/* Image and Bounding Boxes Column */}
              <div className="relative border rounded-md overflow-hidden bg-gray-50">
                {result.pdf_image_base64 ? (
                  <>
                    <img
                      src={`data:image/jpeg;base64,${result.pdf_image_base64}`}
                      alt={`PDF Sayfa 1 - ${result.announcement_id}`}
                      className="w-full h-auto"
                    />
                    {result.ocr_data?.[0]?.lines.map((line: OcrLine, index: number) => {
                      const [x1, y1, x2, y2] = line.bbox;
                      return (
                        <div
                          key={index}
                          className="absolute border-2 border-blue-500 bg-blue-500 bg-opacity-20 hover:bg-opacity-40 cursor-pointer transition-all duration-150"
                          style={{
                            left: `${x1}px`,
                            top: `${y1}px`,
                            width: `${x2 - x1}px`,
                            height: `${y2 - y1}px`,
                          }}
                          onMouseEnter={() => setActiveLine(line)}
                          onMouseLeave={() => setActiveLine(null)}
                        />
                      );
                    })}
                  </>
                ) : (
                  <div className="flex items-center justify-center h-full">
                    <p>Görüntü oluşturulamadı.</p>
                  </div>
                )}
              </div>

              {/* Recognized Text Column */}
              <div className="p-4 border rounded-md bg-gray-50 flex flex-col">
                <h4 className="font-bold mb-4">Vurgulanan Metin</h4>
                <div className="p-4 bg-blue-100 border border-blue-200 rounded-md min-h-[80px] flex items-center justify-center">
                  {activeLine ? (
                    <p className="font-mono text-sm text-center">{activeLine.text}</p>
                  ) : (
                    <p className="text-muted-foreground text-center">Bir metin kutusunun üzerine gelin.</p>
                  )}
                </div>
                <hr className="my-4" />
                <h5 className="font-semibold mb-2">Tüm Metin (Ham)</h5>
                <pre className="text-xs whitespace-pre-wrap font-mono bg-white p-2 rounded-md flex-grow overflow-y-auto">
                  {result.ocr_text}
                </pre>
              </div>
            </div>
          </CardContent>
        </Card>
      );
    }

    // Default view: show the file selector
    return <SupabaseFileSelector onFileSelect={processDocument} isProcessing={loading} />;
  };

  return <div className="space-y-6">{renderContent()}</div>;
};

export default OcrTechnicalPreview;
