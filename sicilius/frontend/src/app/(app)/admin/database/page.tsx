'use client';

import React from 'react';
import { PageHeader } from '@/components/ui/page-header';
import DatabaseGrid from './components/DatabaseGrid';

export default function DatabaseAdminPage() {
  return (
    <div className="flex h-full flex-col">
      <PageHeader 
        title="Veritabanı Yönetimi" 
        description="Sistemdeki tüm tabloları görüntüleyin, filtreleyin ve hatalı kayıtları düzenleyin." 
      />
      <div className="flex-1 p-6 overflow-hidden flex flex-col">
        <DatabaseGrid />
      </div>
    </div>
  );
}
