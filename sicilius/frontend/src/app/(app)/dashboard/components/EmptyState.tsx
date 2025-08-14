"use client";

import { Search, FolderX } from 'lucide-react';

interface EmptyStateProps {
  type: 'start' | 'no-results';
  query?: string;
}

export default function EmptyState({ type, query }: EmptyStateProps) {
  const isStart = type === 'start';
  return (
    <div className="flex flex-col items-center justify-center rounded-lg border border-dashed bg-white p-10 text-center text-slate-600">
      <div className="mb-3 rounded-full bg-slate-100 p-3 text-slate-500">
        {isStart ? <Search size={20} /> : <FolderX size={20} />}
      </div>
      <h3 className="text-sm font-semibold" style={{ color: '#0A192F' }}>
        {isStart ? 'Aramaya başlayın' : 'Sonuç bulunamadı'}
      </h3>
      <p className="mt-1 max-w-md text-xs text-slate-500">
        {isStart
          ? 'Şirket unvanı, sicil no, müdürlük, TCKN/VKN veya kişi adı yazın.'
          : `"${query ?? ''}" için eşleşme bulunamadı. Farklı anahtar sözcükler deneyin.`}
      </p>
    </div>
  );
}
