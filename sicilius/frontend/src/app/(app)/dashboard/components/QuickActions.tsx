"use client";

import { Button } from '@/components/ui/button';
import { Search, Building2, BarChart3 } from 'lucide-react';

export function QuickActions() {
  return (
    <div className="flex flex-wrap gap-3">
      {/* Güvenlik/İlke: Kullanıcı tarafında veri yükleme yok; tüm sorgular backend API üzerinden yapılmalı. */}
      <Button
        className="bg-[#64FFDA] text-[#0A192F] hover:opacity-90"
        onClick={() => { /* Duyuru Ara */ }}
        aria-label="Duyuru Ara"
        title="Duyuru Ara"
      >
        <Search className="mr-2 h-4 w-4" /> Duyuru Ara
      </Button>
      <Button
        variant="ghost"
        onClick={() => { /* Şirketleri Keşfet */ }}
        aria-label="Şirketleri Keşfet"
        title="Şirketleri Keşfet"
      >
        <Building2 className="mr-2 h-4 w-4" /> Şirketleri Keşfet
      </Button>
      <Button
        variant="outline"
        onClick={() => { /* Trendler */ }}
        aria-label="Trendler"
        title="Trendler"
      >
        <BarChart3 className="mr-2 h-4 w-4" /> Trendler
      </Button>
    </div>
  );
}
