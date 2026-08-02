'use client';

import { useState } from 'react';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Search, MapPin, RefreshCw, CheckCircle2, AlertCircle } from 'lucide-react';
import { toast } from 'sonner';
import apiClient from '@/lib/api/client';

export interface CompanyRow {
  id: string;
  unvan: string;
  sicil_no?: string;
  address?: string;
  city?: string;
  district?: string;
  lat?: number | null;
  lon?: number | null;
  has_coordinate: boolean;
}

export interface CoordinateStats {
  coordinated: number;
  uncoordinated: number;
  conflicts: number;
}

interface CoordinatesTableProps {
  companies: CompanyRow[];
  stats?: CoordinateStats;
  onRefresh: () => void;
  onSelectOnMap?: (company: CompanyRow) => void;
}

export function CoordinatesTable({ companies, stats, onRefresh, onSelectOnMap }: CoordinatesTableProps) {
  const [searchTerm, setSearchTerm] = useState('');
  const [filterType, setFilterType] = useState<'all' | 'coordinated' | 'uncoordinated'>('all');
  const [geocodingId, setGeocodingId] = useState<string | null>(null);

  const totalCoordinated = stats ? stats.coordinated : companies.filter((c) => c.has_coordinate).length;
  const totalUncoordinated = stats ? stats.uncoordinated : companies.filter((c) => !c.has_coordinate).length;
  const totalAll = stats ? (stats.coordinated + stats.uncoordinated) : companies.length;

  const filteredCompanies = companies.filter((c) => {
    const searchLower = searchTerm.toLowerCase();
    const unvanMatch = c.unvan ? c.unvan.toLowerCase().includes(searchLower) : false;
    const addressMatch = c.address ? c.address.toLowerCase().includes(searchLower) : false;
    const matchesSearch = unvanMatch || addressMatch;

    if (filterType === 'coordinated') return matchesSearch && c.has_coordinate;
    if (filterType === 'uncoordinated') return matchesSearch && !c.has_coordinate;
    return matchesSearch;
  });

  const handleGeocodeSingle = async (companyId: string, address?: string) => {
    if (!address) {
      toast.error('Bu şirkete ait adres bulunmuyor.');
      return;
    }
    setGeocodingId(companyId);
    try {
      const res = await apiClient.post('/api/v1/processing/process-coordinates/', { limit: 1 });
      toast.success('Koordinat arama işlemi tamamlandı.');
      onRefresh();
    } catch (err: any) {
      toast.error('Koordinat arama işlemi sırasında hata oluştu.');
    } finally {
      setGeocodingId(null);
    }
  };

  return (
    <div className="space-y-4 bg-card p-6 rounded-xl border border-border shadow-sm">
      {/* Search & Filter Bar */}
      <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
        <div className="relative w-full sm:w-96">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
          <Input
            placeholder="Şirket unvanı veya adres ara..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="pl-9"
          />
        </div>

        <div className="flex items-center gap-2 w-full sm:w-auto justify-end">
          <Button
            variant={filterType === 'all' ? 'default' : 'outline'}
            size="sm"
            onClick={() => setFilterType('all')}
          >
            Tümü ({totalAll.toLocaleString('tr-TR')})
          </Button>
          <Button
            variant={filterType === 'coordinated' ? 'default' : 'outline'}
            size="sm"
            onClick={() => setFilterType('coordinated')}
          >
            Koordinatlı ({totalCoordinated.toLocaleString('tr-TR')})
          </Button>
          <Button
            variant={filterType === 'uncoordinated' ? 'default' : 'outline'}
            size="sm"
            onClick={() => setFilterType('uncoordinated')}
          >
            Bekleyenler ({totalUncoordinated.toLocaleString('tr-TR')})
          </Button>
        </div>
      </div>

      {/* Datatable */}
      <div className="rounded-lg border overflow-hidden">
        <Table>
          <TableHeader className="bg-muted/50">
            <TableRow>
              <TableHead>Şirket Unvanı</TableHead>
              <TableHead>Adres / Şehir</TableHead>
              <TableHead>Koordinat</TableHead>
              <TableHead>Durum</TableHead>
              <TableHead className="text-right">İşlemler</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {filteredCompanies.length === 0 ? (
              <TableRow>
                <TableCell colSpan={5} className="text-center py-8 text-muted-foreground">
                  Arama kriterlerine uygun şirket bulunamadı.
                </TableCell>
              </TableRow>
            ) : (
              filteredCompanies.slice(0, 50).map((c) => (
                <TableRow key={c.id}>
                  <TableCell className="font-semibold text-foreground max-w-[240px] truncate">
                    {c.unvan || 'İsimsiz Şirket'}
                  </TableCell>
                  <TableCell className="max-w-[300px] truncate text-xs text-muted-foreground">
                    {c.address || 'Adres bilgisi yok'}
                  </TableCell>
                  <TableCell className="font-mono text-xs">
                    {c.lat && c.lon ? (
                      <span className="text-emerald-600 dark:text-emerald-400 font-semibold">
                        {c.lat.toFixed(5)}, {c.lon.toFixed(5)}
                      </span>
                    ) : (
                      <span className="text-muted-foreground">-</span>
                    )}
                  </TableCell>
                  <TableCell>
                    {c.has_coordinate ? (
                      <Badge variant="outline" className="bg-emerald-500/10 text-emerald-600 border-emerald-500/20 gap-1">
                        <CheckCircle2 className="h-3 w-3" /> Eşleşti
                      </Badge>
                    ) : (
                      <Badge variant="outline" className="bg-amber-500/10 text-amber-600 border-amber-500/20 gap-1">
                        <AlertCircle className="h-3 w-3" /> Bekliyor
                      </Badge>
                    )}
                  </TableCell>
                  <TableCell className="text-right space-x-2">
                    {c.has_coordinate && onSelectOnMap && (
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => onSelectOnMap(c)}
                        className="gap-1 text-xs"
                      >
                        <MapPin className="h-3.5 w-3.5" /> Harita
                      </Button>
                    )}
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => handleGeocodeSingle(c.id, c.address)}
                      disabled={geocodingId === c.id}
                      className="gap-1 text-xs"
                    >
                      <RefreshCw className={`h-3.5 w-3.5 ${geocodingId === c.id ? 'animate-spin' : ''}`} />
                      {geocodingId === c.id ? 'Aranıyor...' : 'Koordinat Al'}
                    </Button>
                  </TableCell>
                </TableRow>
              ))
            )}
          </TableBody>
        </Table>
      </div>
    </div>
  );
}
