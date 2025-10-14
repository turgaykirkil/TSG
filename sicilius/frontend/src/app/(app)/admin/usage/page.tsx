'use client';

import React, { useEffect, useState, useCallback } from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { toast } from 'sonner';

interface TableUsage {
  table: string;
  total_bytes: number;
  approx_rows: number;
}

interface UsageResponse {
  db: {
    database_size_bytes: number | null;
    tables: TableUsage[];
  };
  storage: {
    bucket: string;
    total_files: number;
    total_bytes: number;
  };
}

interface DbTableRow {
  schema: string;
  table: string;
  approx_rows: number;
  size_bytes: number;
  size: string;
}

export default function SupabaseUsagePage() {
  const [data, setData] = useState<UsageResponse | null>(null);
  const [dbTables, setDbTables] = useState<DbTableRow[] | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const getApiUrl = useCallback(() => `/api/v1`, []);

  const humanBytes = (bytes?: number | null) => {
    if (!bytes || bytes <= 0) return '0 B';
    const units = ['B', 'KB', 'MB', 'GB', 'TB'];
    let i = 0;
    let val = bytes;
    while (val >= 1024 && i < units.length - 1) {
      val /= 1024;
      i++;
    }
    return `${val.toFixed(2)} ${units[i]}`;
  };

  const fetchUsage = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const apiUrl = getApiUrl();
      const res = await fetch(`${apiUrl}/usage/supabase-overview`, { credentials: 'include' });
      if (!res.ok) {
        const e = await res.json().catch(() => ({}));
        throw new Error(e.detail || `Sunucu hatası: ${res.status}`);
      }
      const json = (await res.json()) as UsageResponse;
      setData(json);
      // Fetch full table list (app/public, physical tables)
      const resTables = await fetch(`${apiUrl}/stats/db-tables`, { credentials: 'include' });
      if (resTables.ok) {
        const tjson = await resTables.json();
        const rows: DbTableRow[] = Array.isArray(tjson?.tables) ? tjson.tables : [];
        setDbTables(rows);
      }
    } catch (e: any) {
      setError(e.message);
      toast.error(e.message || 'Kullanım bilgisi alınamadı');
    } finally {
      setLoading(false);
    }
  }, [getApiUrl]);

  useEffect(() => {
    fetchUsage();
  }, [fetchUsage]);

  const topTables = (data?.db.tables || []).slice(0, 10);
  const tableRows: { name: string; approx_rows: number; sizeText: string; sizeBytes: number }[] =
    (dbTables && dbTables.length > 0)
      ? dbTables.map(r => ({
          name: `${r.schema}.${r.table}`,
          approx_rows: r.approx_rows ?? 0,
          sizeText: r.size ?? '',
          sizeBytes: r.size_bytes ?? 0,
        }))
      : topTables.map(t => ({
          name: t.table,
          approx_rows: t.approx_rows ?? 0,
          sizeText: humanBytes(t.total_bytes ?? 0),
          sizeBytes: t.total_bytes ?? 0,
        }));

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>Supabase Kullanımı</CardTitle>
          <CardDescription>Veritabanı ve Storage kullanım özetiniz</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex items-center justify-between mb-4">
            <div className="text-sm text-muted-foreground">Ücretsiz kota limitlerini aşmamak için düzenli kontrol önerilir.</div>
            <Button size="sm" variant="secondary" onClick={fetchUsage} disabled={loading}>
              Yenile
            </Button>
          </div>

          {error && (
            <div className="mb-4 rounded-md border border-destructive bg-destructive/10 p-3 text-sm text-destructive">
              Hata: {error}
            </div>
          )}

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="rounded bg-slate-100 dark:bg-slate-900/40 p-4">
              <div className="text-xs text-muted-foreground">DB Toplam Boyut</div>
              <div className="text-lg font-semibold">{humanBytes(data?.db.database_size_bytes ?? 0)}</div>
            </div>
            <div className="rounded bg-slate-100 dark:bg-slate-900/40 p-4">
              <div className="text-xs text-muted-foreground">Storage Toplam Dosya</div>
              <div className="text-lg font-semibold">{data?.storage.total_files ?? 0}</div>
            </div>
            <div className="rounded bg-slate-100 dark:bg-slate-900/40 p-4">
              <div className="text-xs text-muted-foreground">Storage Toplam Boyut</div>
              <div className="text-lg font-semibold">{humanBytes(data?.storage.total_bytes ?? 0)}</div>
            </div>
          </div>

          <div className="mt-6">
            <div className="font-medium mb-2">Tablo Ölçüleri</div>
            <div className="overflow-auto rounded border">
              <table className="w-full text-sm">
                <thead>
                  <tr className="bg-slate-50 dark:bg-slate-800/50 text-left">
                    <th className="px-3 py-2">Tablo</th>
                    <th className="px-3 py-2">Satır (yaklaşık)</th>
                    <th className="px-3 py-2">Boyut</th>
                  </tr>
                </thead>
                <tbody>
                  {tableRows.length === 0 && (
                    <tr>
                      <td colSpan={3} className="px-3 py-4 text-center text-muted-foreground">
                        Veri bulunamadı.
                      </td>
                    </tr>
                  )}
                  {tableRows.map((t) => (
                    <tr key={t.name} className="border-t">
                      <td className="px-3 py-2 font-mono">{t.name}</td>
                      <td className="px-3 py-2">{(t.approx_rows ?? 0).toLocaleString('tr-TR')}</td>
                      <td className="px-3 py-2">{t.sizeText}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
