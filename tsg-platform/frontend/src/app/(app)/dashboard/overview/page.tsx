import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Search, BarChart, Clock, Bookmark, Building2, Users, FileText } from 'lucide-react';

export default function DashboardOverview() {
  // Mock data - replace with actual data from your API
  const stats = [
    { name: 'Toplam Şirket', value: '1,234', icon: Building2 },
    { name: 'Son Aramalar', value: '24', icon: Clock },
    { name: 'Kayıtlı Şirketler', value: '56', icon: Bookmark },
    { name: 'Raporlar', value: '12', icon: FileText },
  ];

  const recentSearches = [
    { id: 1, query: 'ABC Teknoloji A.Ş.', date: '14 Haz 2024, 10:30' },
    { id: 2, query: 'XYZ İnşaat Ltd. Şti.', date: '13 Haz 2024, 15:45' },
    { id: 3, query: '1234567890 (Vergi No)', date: '12 Haz 2024, 09:12' },
  ];

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold tracking-tight">Sicilius Dashboard</h1>
        <p className="text-muted-foreground">
          Sicilius ile şirket veritabanınızı yönetin ve analiz edin.
        </p>
      </div>

      {/* Stats Grid */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        {stats.map((stat, index) => {
          const Icon = stat.icon;
          return (
            <Card key={index}>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">
                  {stat.name}
                </CardTitle>
                <Icon className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{stat.value}</div>
              </CardContent>
            </Card>
          );
        })}
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-7">
        {/* Search Card */}
        <Card className="col-span-4">
          <CardHeader>
            <CardTitle>Şirket Arama</CardTitle>
            <CardDescription>
              Şirket bilgilerini Sicilius ile kolayca bulun.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="flex space-x-2">
              <div className="relative flex-1">
                <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
                <input
                  type="search"
                  placeholder="Şirket, sicil no veya vergi no ile ara..."
                  className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 pl-8 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                />
              </div>
              <Button type="submit">
                <Search className="mr-2 h-4 w-4" />
                Ara
              </Button>
            </div>
          </CardContent>
        </Card>

        {/* Recent Searches */}
        <Card className="col-span-3">
          <CardHeader>
            <CardTitle>Son Aramalar</CardTitle>
            <CardDescription>Sicilius ile yaptığınız son aramalar.</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {recentSearches.map((search) => (
                <div key={search.id} className="flex items-center justify-between">
                  <div className="space-y-1">
                    <p className="text-sm font-medium leading-none">{search.query}</p>
                    <p className="text-sm text-muted-foreground">{search.date}</p>
                  </div>
                  <Button variant="outline" size="sm">
                    Tekrar Ara
                  </Button>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Quick Actions */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">
              Şirket Karşılaştır
            </CardTitle>
            <Users className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <p className="text-sm text-muted-foreground mb-4">
              İki veya daha fazla şirketi karşılaştırın ve detaylı analiz yapın.
            </p>
            <Button variant="outline" className="w-full">
              Karşılaştırmaya Başla
            </Button>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">
              Rapor Oluştur
            </CardTitle>
            <FileText className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <p className="text-sm text-muted-foreground mb-4">
              Şirket bilgilerinizi içeren özelleştirilmiş raporlar oluşturun.
            </p>
            <Button variant="outline" className="w-full">
              Yeni Rapor
            </Button>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">
              Analiz Paneli
            </CardTitle>
            <BarChart className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <p className="text-sm text-muted-foreground mb-4">
              Şirket verilerinizi görselleştirin ve analiz edin.
            </p>
            <Button variant="outline" className="w-full">
              Analiz Et
            </Button>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
