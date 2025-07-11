'use client';

import { useEffect, useState } from 'react';
import { Area, AreaChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Building2, type LucideIcon, Loader2, FileSearch, FileText, Activity } from 'lucide-react';
import { Avatar, AvatarFallback } from '@/components/ui/avatar';
import { dashboardService, StatsData } from '@/lib/api/dashboard';
import { useAuth } from '@/contexts/AuthContext';

// Varsayılan grafik verileri
const defaultChartData = [
  { name: 'Ocak', total: 0 },
  { name: 'Şubat', total: 0 },
  { name: 'Mart', total: 0 },
  { name: 'Nisan', total: 0 },
  { name: 'Mayıs', total: 0 },
  { name: 'Haziran', total: 0 },
];

// Varsayılan aktiviteler
const defaultActivities = [
  { id: '1', user: 'Sistem', action: 'Hoş geldiniz!', time: 'Şimdi' },
];

export default function DashboardPage() {
  const [stats, setStats] = useState<StatsData | null>(null);
  const [chartData, setChartData] = useState(defaultChartData);
  const [recentActivities, setRecentActivities] = useState(defaultActivities);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const { session } = useAuth();
  const user = session?.user;

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        setLoading(true);
        
        // İstatistikleri çek
        const statsData = await dashboardService.getStats();
        setStats(statsData);
        
        // Grafik verilerini çek
        const chartData = await dashboardService.getChartData();
        if (chartData.length > 0) {
          setChartData(chartData);
        }
        
        // Son aktiviteleri çek
        const activities = await dashboardService.getRecentActivities();
        if (activities.length > 0) {
          setRecentActivities(activities);
        }
      } catch (error) {
        const errorMessage = error instanceof Error ? error.message : 'Beklenmeyen bir hata oluştu';
        setError(errorMessage);
        console.error('Error fetching dashboard data:', error);
      } finally {
        setLoading(false);
      }
    };

    if (user) {
      fetchDashboardData();
    }
  }, [user]);

  const formatNumber = (num: number | undefined) => {
    if (num === undefined || num === null) return '...';
    return new Intl.NumberFormat('tr-TR').format(num);
  };

  if (error) {
    return (
      <div className="rounded-md bg-red-50 p-4">
        <h3 className="text-sm font-medium text-red-800">Hata oluştu</h3>
        <p className="mt-2 text-sm text-red-700">{error}</p>
        <button
          onClick={() => window.location.reload()}
          className="mt-2 rounded-md bg-red-100 px-3 py-1 text-sm font-medium text-red-800 hover:bg-red-200"
        >
          Tekrar Dene
        </button>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="flex h-[70vh] flex-col items-center justify-center space-y-4">
        <Loader2 className="h-12 w-12 animate-spin text-gray-600" />
        <p className="text-gray-600">Yükleniyor...</p>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="flex items-center justify-between mb-8">
        <h1 className="text-3xl font-bold">Dashboard</h1>
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
                  <div className="flex-1">
                    <p className="text-sm text-gray-600">
                      <span className="font-medium">{activity.user}</span> {activity.action}
                    </p>
                    <p className="text-xs text-gray-500">{activity.time}</p>
                  </div>
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
