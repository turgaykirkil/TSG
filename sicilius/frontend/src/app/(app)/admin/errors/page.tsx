"use client";

import React, { useEffect, useState } from 'react';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { useToast } from '@/components/ui/use-toast';
import { Loader2, CheckCircle, AlertCircle } from 'lucide-react';

interface CompanyError {
    id: string;
    company_id: string;
    company_name?: string;
    user_id: string;
    description: string;
    status: 'OPEN' | 'RESOLVED';
    created_at: string;
    resolved_at?: string;
}

export default function AdminErrorsPage() {
    const [errors, setErrors] = useState<CompanyError[]>([]);
    const [loading, setLoading] = useState(true);
    const [fetchError, setFetchError] = useState<string | null>(null);
    const [filter, setFilter] = useState<'ALL' | 'OPEN' | 'RESOLVED'>('OPEN');
    const { toast } = useToast();

    const fetchErrors = async () => {
        setLoading(true);
        setFetchError(null);
        try {
            const res = await fetch('/api/v1/errors/', {
                credentials: 'include',
            });
            if (!res.ok) {
                if (res.status === 401 || res.status === 403) {
                    throw new Error('Bu sayfayı görüntüleme yetkiniz yok.');
                }
                throw new Error('Hatalar yüklenemedi');
            }
            const data = await res.json();
            setErrors(Array.isArray(data) ? data : []);
        } catch (error: any) {
            const errorMessage = error?.message || 'Hata raporları alınırken bir sorun oluştu.';
            setFetchError(errorMessage);
            toast({
                title: 'Hata',
                description: errorMessage,
                variant: 'destructive',
            });
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchErrors();
    }, []);

    const handleResolve = async (id: string) => {
        try {
            const res = await fetch(`/api/v1/errors/${id}/resolve`, {
                method: 'PATCH',
                credentials: 'include',
            });
            if (!res.ok) throw new Error('Hata çözülemedi');

            toast({
                title: 'Başarılı',
                description: 'Hata raporu çözüldü olarak işaretlendi.',
            });

            // Listeyi güncelle
            setErrors(prev => prev.map(e => e.id === id ? { ...e, status: 'RESOLVED', resolved_at: new Date().toISOString() } : e));
        } catch (error) {
            toast({
                title: 'İşlem Başarısız',
                description: 'Hata durumu güncellenemedi.',
                variant: 'destructive',
            });
        }
    };

    const filteredErrors = errors.filter(e => {
        if (filter === 'ALL') return true;
        return e.status === filter;
    });

    const formatDate = (dateStr: string) => {
        return new Date(dateStr).toLocaleString('tr-TR');
    };

    return (
        <div className="container mx-auto py-8 space-y-6">
            <div className="flex items-center justify-between">
                <h1 className="text-2xl font-bold">Hata Bildirimleri</h1>
                <div className="flex gap-2">
                    <Button variant={filter === 'OPEN' ? 'default' : 'outline'} onClick={() => setFilter('OPEN')}>
                        Açık
                    </Button>
                    <Button variant={filter === 'RESOLVED' ? 'default' : 'outline'} onClick={() => setFilter('RESOLVED')}>
                        Çözülenler
                    </Button>
                    <Button variant={filter === 'ALL' ? 'default' : 'outline'} onClick={() => setFilter('ALL')}>
                        Tümü
                    </Button>
                </div>
            </div>

            {loading ? (
                <div className="flex justify-center p-12">
                    <Loader2 className="h-8 w-8 animate-spin text-slate-400" />
                </div>
            ) : fetchError ? (
                <div className="text-center p-12 text-red-500 bg-red-50 dark:bg-red-900/20 rounded-lg border border-red-200 dark:border-red-800">
                    <AlertCircle className="h-12 w-12 mx-auto mb-4" />
                    <p className="font-medium">{fetchError}</p>
                    <Button variant="outline" className="mt-4" onClick={fetchErrors}>
                        Tekrar Dene
                    </Button>
                </div>
            ) : (
                <div className="grid gap-4">
                    {filteredErrors.length === 0 ? (
                        <div className="text-center p-12 text-slate-500 bg-slate-50 dark:bg-slate-900 rounded-lg border border-dashed">
                            {filter === 'OPEN' && 'Açık hata bildirimi bulunmuyor. 🎉'}
                            {filter === 'RESOLVED' && 'Çözülmüş hata bildirimi bulunmuyor.'}
                            {filter === 'ALL' && 'Henüz hiç hata bildirimi yapılmamış.'}
                        </div>
                    ) : (
                        filteredErrors.map((error) => (
                            <Card key={error.id} className="overflow-hidden">
                                <CardHeader className="bg-slate-50 dark:bg-slate-900/50 py-3 flex flex-row items-center justify-between space-y-0">
                                    <div className="flex items-center gap-2">
                                        {error.status === 'OPEN' ? (
                                            <Badge variant="destructive" className="flex gap-1 items-center"><AlertCircle size={12} /> Açık</Badge>
                                        ) : (
                                            <Badge variant="secondary" className="bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-100 flex gap-1 items-center"><CheckCircle size={12} /> Çözüldü</Badge>
                                        )}
                                        <span className="text-xs text-slate-500">{formatDate(error.created_at)}</span>
                                    </div>
                                    {error.status === 'OPEN' && (
                                        <Button size="sm" variant="outline" onClick={() => handleResolve(error.id)}>
                                            Çözüldü İşaretle
                                        </Button>
                                    )}
                                </CardHeader>
                                <CardContent className="pt-4">
                                    <div className="grid gap-2">
                                        <div className="text-sm font-medium text-slate-500">
                                            Şirket: <span className="text-slate-900 dark:text-slate-100">{error.company_name || 'Bilinmiyor'}</span>
                                        </div>
                                        <div className="mt-2 p-3 bg-slate-50 dark:bg-slate-900 rounded-md text-sm whitespace-pre-wrap">
                                            {error.description}
                                        </div>
                                        {error.resolved_at && (
                                            <div className="text-xs text-slate-400 mt-2 text-right">
                                                Çözüm Tarihi: {formatDate(error.resolved_at)}
                                            </div>
                                        )}
                                    </div>
                                </CardContent>
                            </Card>
                        ))
                    )}
                </div>
            )}
        </div>
    );
}
