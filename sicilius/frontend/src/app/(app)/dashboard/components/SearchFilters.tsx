"use client";

import { cn } from '@/lib/utils';

type FilterKey = 'all' | 'companies' | 'people' | 'history';

interface SearchFiltersProps {
  value: FilterKey;
  onChange: (val: FilterKey) => void;
}

export default function SearchFilters({ value, onChange }: SearchFiltersProps) {
  const items: { key: FilterKey; label: string; disabled?: boolean }[] = [
    { key: 'all', label: 'Hepsi' },
    { key: 'companies', label: 'Şirketler' },
    { key: 'people', label: 'Kişiler', disabled: true },
    { key: 'history', label: 'Geçmiş', disabled: true },
  ];

  return (
    <div className="flex flex-wrap items-center gap-2">
      {items.map((it) => (
        <button
          key={it.key}
          type="button"
          disabled={it.disabled}
          onClick={() => !it.disabled && onChange(it.key)}
          className={cn(
            'rounded-full border px-3.5 py-1.5 text-xs font-medium transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#0A192F] focus-visible:ring-offset-2',
            value === it.key
              ? 'bg-gradient-to-r from-[#0A192F] to-[#1E3A8A] text-white border-transparent shadow'
              : 'bg-white text-slate-700 hover:bg-slate-50 border-slate-200',
            it.disabled && 'opacity-50 cursor-not-allowed'
          )}
          aria-pressed={value === it.key}
        >
          {it.label}
        </button>
      ))}
    </div>
  );
}
