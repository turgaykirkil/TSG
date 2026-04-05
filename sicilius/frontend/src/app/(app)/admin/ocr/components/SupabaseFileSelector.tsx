'use client';

import { useState, useEffect } from 'react';
import api from '@/lib/axios';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Loader2, AlertCircle } from 'lucide-react';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';

// A simple type for the file objects returned by our new backend endpoint
interface StorageFile {
  id: string;
  name: string;
  created_at: string;
}

interface FileSelectorProps {
  onFileSelect: (filePath: string) => void;
  isProcessing: boolean;
}

const SupabaseFileSelector = ({ onFileSelect, isProcessing }: FileSelectorProps) => {
  const [files, setFiles] = useState<StorageFile[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchFiles = async () => {
      setLoading(true);
      setError(null);
      try {
        // This endpoint needs to be created on the backend
        const response = await api.get('/api/v1/storage/list-announcement-files');
        const pdfFiles = response.data.filter((file: StorageFile) => file.name.endsWith('.pdf'));
        setFiles(pdfFiles);
      } catch (err: any) {
        console.error('Error fetching files from backend:', err);
        setError('Depodaki dosyalar alınamadı. Backend servisi çalışıyor mu?');
      } finally {
        setLoading(false);
      }
    };

    fetchFiles();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center p-4">
        <Loader2 className="mr-2 h-4 w-4 animate-spin" />
        <span>Dosyalar yükleniyor...</span>
      </div>
    );
  }

  if (error) {
    return (
      <Alert variant="destructive">
        <AlertCircle className="h-4 w-4" />
        <AlertTitle>Hata</AlertTitle>
        <AlertDescription>{error}</AlertDescription>
      </Alert>
    );
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Analiz Edilecek Belgeyi Seçin</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="max-h-96 overflow-y-auto">
          <ul className="space-y-2">
            {files.length > 0 ? files.map((file: StorageFile) => (
              <li key={file.id} className="flex justify-between items-center p-2 hover:bg-muted/50 rounded-md transition-colors">
                <span className="font-mono text-sm">{file.name}</span>
                <Button variant="outline" size="sm" onClick={() => onFileSelect(file.name)} disabled={isProcessing}>
                  Analiz Et
                </Button>
              </li>
            )) : (
              <p className="text-sm text-muted-foreground text-center p-4">Depoda analiz edilecek PDF dosyası bulunamadı.</p>
            )}
          </ul>
        </div>
      </CardContent>
    </Card>
  );
};

export default SupabaseFileSelector;
