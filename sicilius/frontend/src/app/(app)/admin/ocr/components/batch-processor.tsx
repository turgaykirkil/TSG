'use client';

import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { useToast } from '@/components/ui/use-toast';
import api from '@/lib/axios';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { RocketIcon } from '@radix-ui/react-icons';

export default function BatchProcessor() {
  const [limit, setLimit] = useState(10);
  const [isLoading, setIsLoading] = useState(false);
  const { toast } = useToast();

  const handleStartBatch = async () => {
    setIsLoading(true);
    try {
            const response = await api.post('/ocr/process-batch', { limit });
      toast({
        title: 'Başarılı',
        description: response.data.message || 'Toplu OCR işlemi başarıyla başlatıldı.',
        variant: 'default',
      });
    } catch (error: any) {
      toast({
        title: 'Hata',
        description: error.response?.data?.detail || 'Toplu OCR işlemi başlatılırken bir hata oluştu.',
        variant: 'destructive',
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>Toplu OCR İşlemi</CardTitle>
        <CardDescription>
          Beklemedeki ilanlar için toplu OCR işlemini başlatın.
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div className="grid w-full max-w-sm items-center gap-1.5">
          <Label htmlFor="limit">İşlenecek İlan Sayısı</Label>
          <Input
            type="number"
            id="limit"
            placeholder="10"
            value={limit}
            onChange={(e) => setLimit(Number(e.target.value))}
            min={1}
            max={100}
            disabled={isLoading}
          />
        </div>
      </CardContent>
      <CardFooter>
        <Button onClick={handleStartBatch} disabled={isLoading}>
          {isLoading ? (
            <>
              <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              İşleniyor...
            </>
          ) : (
            <>
              <RocketIcon className="mr-2 h-4 w-4" /> Toplu İşlemi Başlat
            </>
          )}
        </Button>
      </CardFooter>
    </Card>
  );
}
