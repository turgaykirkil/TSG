'use client';

import { useEffect, useState } from 'react';
import { Area, AreaChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Activity, Building2, DollarSign, type LucideIcon, Users, Loader2 } from 'lucide-react';
import { Avatar, AvatarFallback } from '@/components/ui/avatar';

// Static data that doesn't depend on the API for now
const chartData = [
  { name: 'Ocak', total: 1200 },
  { name: 'Şubat', total: 2100 },
  { name: 'Mart', total: 1400 },
  { name: 'Nisan', total: 2780 },
  { name: 'Mayıs', total: 1890 },
  { name: 'Haziran', total: 2390 },
];

const recentActivities = [
  { user: 'Ahmet Yılmaz', action: 'yeni bir şirket ekledi.', time: '15 dakika önce' },
  { user: 'Ayşe Kaya', action: 'bir rapor indirdi.', time: '1 saat önce' },
  { user: 'Mehmet Can', action: 'bir arama sorgusu çalıştırdı.', time: '3 saat önce' },
];

interface StatsData {
  totalCompanies: number;
  scrapedCompanies: number;
  withCoordinates: number;
}

export default function DashboardPage() {
  const [stats, setStats] = useState<StatsData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        setLoading(true);
        const apiUrl = process.env.NEXT_PUBLIC_API_URL;
        if (!apiUrl) {
          throw new Error('API URL is not configured in environment variables.');
        }

        const response = await fetch(`${apiUrl}/stats`);
        if (!response.ok) {
          throw new Error(`API isteği başarısız oldu: ${response.status}`);
        }
        const data: StatsData = await response.json();
        setStats(data);
      } catch (err: any) {
        console.error('İstatistikler yüklenirken hata oluştu:', err);
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchStats();
  }, []);

  const formatNumber = (num: number | undefined) => {
    if (num === undefined || num === null) return '...';
    return new Intl.NumberFormat('tr-TR').format(num);
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="flex items-center justify-between mb-8">
        <h1 className="text-3xl font-bold">Dashboard</h1>
      </div>

      {error && (
        <Card className="mb-8 bg-destructive/10 border-destructive">
          <CardHeader>
            <CardTitle className="text-destructive">Bir Hata Oluştu</CardTitle>
          </CardHeader>
          <CardContent>
            <p>{`Hata: ${error}`}</p>
          </CardContent>
        </Card>
      )}

      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4 mb-8">
        <StatCard title="Toplam Gelir" value="₺45,231.89" icon={DollarSign} change="+20.1%" isLoading={false} />
        <StatCard title="Taranan Şirketler" value={formatNumber(stats?.scrapedCompanies)} icon={Activity} change="Veritabanı" isLoading={loading} />
        <StatCard title="Toplam Şirket" value={formatNumber(stats?.totalCompanies)} icon={Building2} change="Veritabanı" isLoading={loading} />
        <StatCard title="Koordinatlı Şirket" value={formatNumber(stats?.withCoordinates)} icon={Users} change="Veritabanı" isLoading={loading} />
      </div>

      <div className="grid grid-cols-1 gap-8 lg:grid-cols-3">
        <Card className="lg:col-span-2">
          <CardHeader>
            <CardTitle>Büyüme Analizi</CardTitle>
          </CardHeader>
          <CardContent className="pl-2">
            <ResponsiveContainer width="100%" height={350}>
              <AreaChart data={chartData}>
                <defs>
                  <linearGradient id="colorUv" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="hsl(var(--primary))" stopOpacity={0.8} />
                    <stop offset="95%" stopColor="hsl(var(--primary))" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <XAxis dataKey="name" stroke="hsl(var(--muted-foreground))" fontSize={12} tickLine={false} axisLine={false} />
                <YAxis stroke="hsl(var(--muted-foreground))" fontSize={12} tickLine={false} axisLine={false} tickFormatter={(value) => `₺${value}`} />
                <CartesianGrid strokeDasharray="3 3" className="stroke-border/20" />
                <Tooltip
                  contentStyle={{
                    backgroundColor: 'hsl(var(--background))',
                    border: '1px solid hsl(var(--border))',
                    borderRadius: 'var(--radius)',
                  }}
                />
                <Area type="monotone" dataKey="total" stroke="hsl(var(--primary))" fillOpacity={1} fill="url(#colorUv)" />
              </AreaChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        <Card className="lg:col-span-1">
          <CardHeader>
            <CardTitle>Son Etkinlikler</CardTitle>
          </CardHeader>
          <CardContent className="space-y-6">
            {recentActivities.map((activity, index) => (
              <div key={index} className="flex items-center space-x-4">
                <Avatar className="h-10 w-10">
                  <AvatarFallback>{activity.user.charAt(0)}</AvatarFallback>
                </Avatar>
                <div>
                  <p className="text-sm font-medium leading-none">
                    <span className="font-semibold text-foreground">{activity.user}</span>{' '}
                    <span className="text-muted-foreground">{activity.action}</span>
                  </p>
                  <p className="text-xs text-muted-foreground pt-1">{activity.time}</p>
                </div>
              </div>
            ))}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

interface StatCardProps {
  title: string;
  value: string;
  icon: LucideIcon;
  change: string;
  isLoading?: boolean;
}

function StatCard({ title, value, icon: Icon, change, isLoading }: StatCardProps) {
  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle className="text-sm font-medium">{title}</CardTitle>
        <Icon className="h-4 w-4 text-muted-foreground" />
      </CardHeader>
      <CardContent>
        {isLoading ? (
          <div className="flex items-center justify-start h-8">
            <Loader2 className="h-6 w-6 animate-spin text-muted-foreground" />
          </div>
        ) : (
          <>
            <div className="text-2xl font-bold">{value}</div>
            <p className="text-xs text-muted-foreground">{change}</p>
          </>
        )}
      </CardContent>
    </Card>
  );
}
