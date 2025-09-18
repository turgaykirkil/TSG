"use client";

import { Menu } from "lucide-react";

interface HeaderProps {
  onOpenHistory: () => void;
  loading?: boolean;
}

export default function Header({ onOpenHistory, loading = false }: HeaderProps) {
  return (
    <header className="sticky top-0 z-50 bg-white/80 dark:bg-slate-900/80 backdrop-blur border-b border-slate-200/60 dark:border-slate-700/60">
      <div className="mx-auto w-full max-w-screen-2xl h-14 px-4 flex items-center justify-between">
        <div className="flex items-center gap-2 select-none">
          <span className="text-2xl font-semibold tracking-tight text-slate-900 dark:text-slate-100">Sicilius</span>
        </div>
        <div className="flex items-center gap-2">
          <button
            type="button"
            className="inline-flex items-center gap-2 rounded-full bg-white/80 dark:bg-slate-900/80 px-3 py-2 shadow border border-slate-200 dark:border-slate-700 text-slate-700 dark:text-slate-200 hover:bg-white dark:hover:bg-slate-900"
            onClick={onOpenHistory}
            aria-label="Geçmişi aç"
          >
            <Menu size={18} className="inline" /> Geçmiş
          </button>
        </div>
      </div>
      {loading && (
        <div className="loading-bar" aria-hidden />
      )}
    </header>
  );
}
