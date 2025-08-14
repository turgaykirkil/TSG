import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Building2, Users2, History, Activity } from 'lucide-react';

export function KpiSection() {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      <Card className="hover:shadow-lg transition-shadow duration-300" aria-label="Toplam Şirketler: 1,234; bu ay yüzde 3.4 artış">
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">Toplam Şirketler</CardTitle>
          <Building2 className="h-4 w-4 text-muted-foreground" aria-hidden="true" focusable="false" />
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">1,234</div>
          <p className="text-xs text-muted-foreground">+3.4% bu ay</p>
        </CardContent>
      </Card>

      <Card className="hover:shadow-lg transition-shadow duration-300" aria-label="Toplam Kişiler: 8,902; bu ay yüzde 1.1 artış">
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">Toplam Kişiler</CardTitle>
          <Users2 className="h-4 w-4 text-muted-foreground" aria-hidden="true" focusable="false" />
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">8,902</div>
          <p className="text-xs text-muted-foreground">+1.1% bu ay</p>
        </CardContent>
      </Card>

      <Card className="hover:shadow-lg transition-shadow duration-300" aria-label="Geçmiş Kayıtları: 42,118; son 24 saatte 312">
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">Geçmiş Kayıtları</CardTitle>
          <History className="h-4 w-4 text-muted-foreground" aria-hidden="true" focusable="false" />
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">42,118</div>
          <p className="text-xs text-muted-foreground">Son 24 saatte 312</p>
        </CardContent>
      </Card>

      <Card className="hover:shadow-lg transition-shadow duration-300" aria-label="Anlık İşlemler: 12; şu an işleniyor">
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">Anlık İşlemler</CardTitle>
          <Activity className="h-4 w-4 text-muted-foreground" aria-hidden="true" focusable="false" />
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">12</div>
          <p className="text-xs text-muted-foreground">Şu an işleniyor</p>
        </CardContent>
      </Card>
    </div>
  );
}
