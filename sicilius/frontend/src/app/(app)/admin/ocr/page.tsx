'use client';

import React, { useState } from 'react';
import OcrTechnicalPreview from './components/OcrTechnicalPreview';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { api } from '@/lib/api';
import { API_ENDPOINTS } from '@/config/constants';
import { OcrPreviewResponse } from '@/lib/types';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import { Loader2 } from 'lucide-react';

const OcrAdminPage = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<OcrPreviewResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      setSelectedFile(file);
      setPreview(null);
      setError(null);
    }
  };

  const handleAnalyze = async () => {
    if (!selectedFile) return;

    setPreview(null);
    setLoading(true);
    setError(null);

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
            const response = await api.post<OcrPreviewResponse>(
        API_ENDPOINTS.OCR.PROCESS_AND_PREVIEW,
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        }
      );
      setPreview(response.data);
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || `"${selectedFile.name}" dosyası işlenemedi.`);
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6 p-4 sm:p-6 md:p-8">
      <div className="space-y-2">
        <h1 className="text-2xl font-bold">OCR Teknik Önizleme</h1>
        <p className="text-muted-foreground">
          Bu araç, OCR motorunun PDF belgelerinden metinleri ve konumlarını ne kadar doğru çıkardığını görsel olarak inceler.
        </p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>PDF Yükle ve Analiz Et</CardTitle>
          <CardDescription>Analiz için bir PDF dosyası seçin.</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex flex-col sm:flex-row items-center gap-4">
            <Input
              id="pdf-upload"
              type="file"
              accept=".pdf"
              onChange={handleFileChange}
              disabled={loading}
              className="flex-grow"
            />
            <Button 
              onClick={handleAnalyze} 
              disabled={!selectedFile || loading}
              className="w-full sm:w-auto"
            >
              {loading ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : 'Analiz Et'}
            </Button>
          </div>
        </CardContent>
      </Card>

      {loading && (
        <div className="flex flex-col items-center justify-center p-8 border-2 border-dashed rounded-lg h-96 bg-muted/50">
          <Loader2 className="h-12 w-12 animate-spin text-primary" />
          <span className="mt-4 text-lg font-semibold">'{selectedFile?.name}' işleniyor...</span>
          <p className="text-muted-foreground">Bu işlem PDF boyutuna göre biraz zaman alabilir.</p>
        </div>
      )}

      {error && (
        <Alert variant="destructive">
          <AlertTitle>Analiz Başarısız</AlertTitle>
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      {preview && !loading && (
        <OcrTechnicalPreview preview={preview} />
      )}
    </div>
  );
};

export default OcrAdminPage;
