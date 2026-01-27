'use client';

import { useEffect, useState } from 'react';
import { Activity, Database, HardDrive, Users } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Skeleton } from '@/components/ui/skeleton';

export function AdminStats() {
    const [stats, setStats] = useState<any>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        async function fetchStats() {
            try {
                const res = await fetch('/api/v1/stats/dashboard', { credentials: 'include' });
                if (res.ok) {
                    const data = await res.json();
                    setStats(data);
                }
            } catch (error) {
                console.error('Failed to fetch admin stats', error);
            } finally {
                setLoading(false);
            }
        }
        fetchStats();
    }, []);

    if (loading) {
        return (
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4 mb-8">
                {[...Array(4)].map((_, i) => (
                    <Skeleton key={i} className="h-32 rounded-xl" />
                ))}
            </div>
        );
    }

    const items = [
        {
            title: 'Toplam Kullanıcı',
            value: stats?.total_users || 0,
            description: 'Kayıtlı hesap',
            icon: Users,
        },
        {
            title: 'Aktif Oturumlar',
            value: stats?.active_sessions || 0,
            description: 'Son 24s aktif',
            icon: Activity,
        },
        {
            title: 'Veritabanı Boyutu',
            value: stats?.db_size || '0 B',
            description: 'Postgres kullanımı',
            icon: Database,
        },
        {
            title: 'Dosya Depolama',
            value: stats?.storage_usage || '0 B',
            description: 'Static/Media files',
            icon: HardDrive,
        },
    ];

    return (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4 mb-8">
            {items.map((stat) => (
                <Card key={stat.title}>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">
                            {stat.title}
                        </CardTitle>
                        <stat.icon className="h-4 w-4 text-muted-foreground" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">{stat.value}</div>
                        <p className="text-xs text-muted-foreground">
                            {stat.description}
                        </p>
                    </CardContent>
                </Card>
            ))}
        </div>
    );
}
