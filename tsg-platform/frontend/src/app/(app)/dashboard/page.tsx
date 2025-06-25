'use client';

import { useSession } from 'next-auth/react';
import { motion, type Variants } from 'framer-motion';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Users, Building2, Activity, DollarSign, type LucideIcon } from 'lucide-react';
import { Icons } from '@/components/icons';

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

const fadeIn = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0 },
};

export default function DashboardPage() {
  const { data: session, status } = useSession();

  if (status === 'loading') {
    return (
      <div className="flex h-full w-full items-center justify-center">
        <Icons.spinner className="h-8 w-8 animate-spin text-primary" />
      </div>
    );
  }

  const userName = session?.user?.name || 'Kullanıcı';

  return (
    <motion.div
      className="space-y-8 p-4 md:p-8"
      initial="hidden"
      animate="visible"
      variants={{ visible: { transition: { staggerChildren: 0.1 } } }}
    >
      <motion.div variants={fadeIn}>
                <h1 className="text-2xl md:text-3xl font-bold tracking-tight text-gray-900 dark:text-gray-100">
          Hoş Geldiniz, {userName}!
        </h1>
        <p className="text-muted-foreground mt-1">
          İşte işletmenizin bugünkü anlık görüntüsü.
        </p>
      </motion.div>

            <motion.div
        className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-4"
        variants={{ visible: { transition: { staggerChildren: 0.1 } } }}
      >
        <StatCard title="Toplam Gelir" value="₺45,231.89" icon={DollarSign} change="+20.1%" variants={fadeIn} />
        <StatCard title="Aktif Kullanıcılar" value="+2350" icon={Users} change="+180.1%" variants={fadeIn} />
        <StatCard title="Toplam Şirket" value="+12,234" icon={Building2} change="+19%" variants={fadeIn} />
        <StatCard title="Yeni Aktiviteler" value="+573" icon={Activity} change="+201" variants={fadeIn} />
      </motion.div>

      <div className="grid grid-cols-1 gap-8 lg:grid-cols-3">
        <motion.div className="lg:col-span-2" variants={fadeIn}>
          <Card className="shadow-lg hover:shadow-xl transition-shadow duration-300">
            <CardHeader>
              <CardTitle>Büyüme Analizi</CardTitle>
            </CardHeader>
            <CardContent className="pl-2 pt-4">
              <ResponsiveContainer width="100%" height={350}>
                <AreaChart data={chartData}>
                  <defs>
                    <linearGradient id="colorUv" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#8884d8" stopOpacity={0.8} />
                      <stop offset="95%" stopColor="#8884d8" stopOpacity={0} />
                    </linearGradient>
                  </defs>
                  <XAxis dataKey="name" stroke="#888888" fontSize={12} tickLine={false} axisLine={false} />
                  <YAxis stroke="#888888" fontSize={12} tickLine={false} axisLine={false} tickFormatter={(value) => `₺${value}`} />
                  <CartesianGrid strokeDasharray="3 3" className="opacity-20" />
                  <Tooltip formatter={(value) => [`₺${value}`, 'Toplam']}/>
                  <Area type="monotone" dataKey="total" stroke="#8884d8" fillOpacity={1} fill="url(#colorUv)" />
                </AreaChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </motion.div>

        <motion.div variants={fadeIn}>
          <Card className="shadow-lg hover:shadow-xl transition-shadow duration-300">
            <CardHeader>
              <CardTitle>Son Etkinlikler</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              {recentActivities.map((activity, index) => (
                <div key={index} className="flex items-center">
                  <div className="flex h-9 w-9 items-center justify-center rounded-full bg-muted-foreground/10">
                    <Users className="h-4 w-4 text-muted-foreground" />
                  </div>
                  <div className="ml-4 space-y-1">
                                        <p className="text-sm font-medium leading-snug">
                      <span className="font-semibold">{activity.user}</span> {activity.action}
                    </p>
                    <p className="text-xs text-muted-foreground">{activity.time}</p>
                  </div>
                </div>
              ))}
            </CardContent>
          </Card>
        </motion.div>
      </div>
    </motion.div>
  );
}

interface StatCardProps {
  title: string;
  value: string;
  icon: LucideIcon;
  change: string;
  variants: Variants;
}

function StatCard({ title, value, icon: Icon, change, variants }: StatCardProps) {
  return (
    <motion.div variants={variants} whileHover={{ scale: 1.05, transition: { duration: 0.2 } }}>
      <Card className="shadow-md hover:shadow-lg transition-shadow duration-300">
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">{title}</CardTitle>
          <Icon className="h-4 w-4 text-muted-foreground" />
        </CardHeader>
        <CardContent>
                    <div className="text-xl font-bold lg:text-2xl">{value}</div>
          <p className="text-xs text-muted-foreground">geçen aydan beri {change}</p>
        </CardContent>
      </Card>
    </motion.div>
  );
}

