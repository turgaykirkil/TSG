'use client';

import React from 'react';
import OcrTechnicalPreview from './components/OcrTechnicalPreview';

const OcrAdminPage = () => {
  return (
    <div className="space-y-4 p-8">
        <h1 className="text-2xl font-bold">OCR Teknik Önizleme</h1>
        <p className="text-muted-foreground">
            Bu sayfa, OCR motorunun PDF belgelerinden metinleri ve konumlarını ne kadar doğru çıkardığını görsel olarak incelemek için bir geliştirici aracıdır.
        </p>
        <OcrTechnicalPreview />
    </div>
  );
};

export default OcrAdminPage;
