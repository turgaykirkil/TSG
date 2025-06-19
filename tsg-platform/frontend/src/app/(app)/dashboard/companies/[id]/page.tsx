import { MapPin, FileText, Calendar, Mail, Phone, Globe, ArrowLeft, Star, Share2, Download, MoreHorizontal } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Badge } from '@/components/ui/badge';
import Link from 'next/link';

type Company = {
  id: number;
  name: string;
  taxNumber: string;
  registrationNumber: string;
  address: string;
  city: string;
  district: string;
  phone: string;
  email: string;
  website: string;
  status: 'Aktif' | 'Tasfiye' | 'İflas' | 'Fesih';
  establishmentDate: string;
  lastUpdate: string;
  industry: string;
  employees: string;
  description: string;
  isFavorite: boolean;
  executives: Array<{
    name: string;
    title: string;
    startDate: string;
  }>;
  financials: {
    year: string;
    revenue: string;
    profit: string;
    assets: string;
    equity: string;
  }[];
  documents: Array<{
    id: number;
    name: string;
    type: string;
    date: string;
    size: string;
  }>;
};

// Mock data - replace with actual API call
const getCompanyData = (_id: string): Company => ({
  id: 1,
  name: 'ABC Teknoloji A.Ş.',
  taxNumber: '1234567890',
  registrationNumber: '123456-7890',
  address: 'Levent Mah. Büyükdere Cad. No:123 Kat:5',
  city: 'İstanbul',
  district: 'Şişli',
  phone: '+90 212 123 45 67',
  email: 'info@abcteknoloji.com.tr',
  website: 'www.abcteknoloji.com.tr',
  status: 'Aktif',
  establishmentDate: '15.05.2010',
  lastUpdate: '10.06.2024',
  industry: 'Bilişim ve Teknoloji',
  employees: '50-100',
  description: 'ABC Teknoloji, yazılım geliştirme ve danışmanlık hizmetleri sunan öncü bir teknoloji şirketidir. Müşteri odaklı çözümleriyle sektöründe lider konumdadır.',
  isFavorite: true,
  executives: [
    { name: 'Ahmet Yılmaz', title: 'Genel Müdür', startDate: '15.05.2010' },
    { name: 'Mehmet Demir', title: 'Finans Müdürü', startDate: '10.03.2015' },
    { name: 'Ayşe Kaya', title: 'İnsan Kaynakları Müdürü', startDate: '22.11.2018' },
  ],
  financials: [
    { year: '2023', revenue: '25.450.000 TL', profit: '3.250.000 TL', assets: '18.750.000 TL', equity: '12.300.000 TL' },
    { year: '2022', revenue: '20.150.000 TL', profit: '2.800.000 TL', assets: '15.200.000 TL', equity: '10.500.000 TL' },
    { year: '2021', revenue: '18.300.000 TL', profit: '2.100.000 TL', assets: '13.750.000 TL', equity: '9.200.000 TL' },
  ],
  documents: [
    { id: 1, name: 'Sözleşme Örneği', type: 'PDF', date: '10.06.2024', size: '2.4 MB' },
    { id: 2, name: 'İmza Sirküleri', type: 'PDF', date: '05.06.2024', size: '1.8 MB' },
    { id: 3, name: 'Vergi Levhası', type: 'JPG', date: '01.06.2024', size: '1.2 MB' },
  ],
});

export default function CompanyDetailPage({ params }: { params: { id: string } }) {
  // Get company data based on the ID from the URL
  const company = getCompanyData(params.id);
  
  const statusVariants = {
    Aktif: 'bg-green-100 text-green-800',
    Tasfiye: 'bg-yellow-100 text-yellow-800',
    İflas: 'bg-red-100 text-red-800',
    Fesih: 'bg-gray-100 text-gray-800',
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <Link href="/dashboard/search" className="text-sm text-muted-foreground hover:text-foreground flex items-center">
            <ArrowLeft className="h-4 w-4 mr-1" />
            Geri Dön
          </Link>
          <div className="flex items-center mt-2">
            <h1 className="text-2xl font-bold tracking-tight">{company.name}</h1>
            <Badge className={`ml-3 ${statusVariants[company.status]}`}>
              {company.status}
            </Badge>
          </div>
        </div>
        <div className="flex space-x-2">
          <Button variant="outline" size="sm">
            <Star className={`mr-2 h-4 w-4 ${company.isFavorite ? 'fill-yellow-400 text-yellow-400' : ''}`} />
            {company.isFavorite ? 'Favorilerden Çıkar' : 'Favorilere Ekle'}
          </Button>
          <Button variant="outline" size="sm">
            <Share2 className="mr-2 h-4 w-4" />
            Paylaş
          </Button>
          <Button variant="outline" size="sm">
            <Download className="mr-2 h-4 w-4" />
            Dışa Aktar
          </Button>
          <Button variant="outline" size="icon">
            <MoreHorizontal className="h-4 w-4" />
            <span className="sr-only">Daha fazla</span>
          </Button>
        </div>
      </div>

      <Tabs defaultValue="overview" className="space-y-4">
        <TabsList>
          <TabsTrigger value="overview">Genel Bakış</TabsTrigger>
          <TabsTrigger value="financials">Finansal Bilgiler</TabsTrigger>
          <TabsTrigger value="documents">Belgeler</TabsTrigger>
          <TabsTrigger value="history">Tarihçe</TabsTrigger>
          <TabsTrigger value="relationships">İlişkiler</TabsTrigger>
        </TabsList>

        <TabsContent value="overview" className="space-y-6">
          <div className="grid gap-6 md:grid-cols-3">
            <div className="md:col-span-2 space-y-6">
              <div className="rounded-lg border p-6">
                <h2 className="text-lg font-semibold mb-4">Temel Bilgiler</h2>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="space-y-1">
                    <p className="text-sm text-muted-foreground">Vergi No</p>
                    <p>{company.taxNumber}</p>
                  </div>
                  <div className="space-y-1">
                    <p className="text-sm text-muted-foreground">Sicil No</p>
                    <p>{company.registrationNumber}</p>
                  </div>
                  <div className="space-y-1">
                    <p className="text-sm text-muted-foreground">Kuruluş Tarihi</p>
                    <div className="flex items-center">
                      <Calendar className="h-4 w-4 mr-2 text-muted-foreground" />
                      <span>{company.establishmentDate}</span>
                    </div>
                  </div>
                  <div className="space-y-1">
                    <p className="text-sm text-muted-foreground">Son Güncelleme</p>
                    <div className="flex items-center">
                      <Calendar className="h-4 w-4 mr-2 text-muted-foreground" />
                      <span>{company.lastUpdate}</span>
                    </div>
                  </div>
                  <div className="space-y-1">
                    <p className="text-sm text-muted-foreground">Sektör</p>
                    <p>{company.industry}</p>
                  </div>
                  <div className="space-y-1">
                    <p className="text-sm text-muted-foreground">Çalışan Sayısı</p>
                    <p>{company.employees}</p>
                  </div>
                </div>
              </div>

              <div className="rounded-lg border p-6">
                <h2 className="text-lg font-semibold mb-4">İletişim Bilgileri</h2>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="space-y-1">
                    <p className="text-sm text-muted-foreground">Adres</p>
                    <div className="flex items-start">
                      <MapPin className="h-4 w-4 mr-2 mt-0.5 text-muted-foreground flex-shrink-0" />
                      <span>
                        {company.address}\n{company.district}/{company.city}
                      </span>
                    </div>
                  </div>
                  <div className="space-y-1">
                    <p className="text-sm text-muted-foreground">Telefon</p>
                    <div className="flex items-center">
                      <Phone className="h-4 w-4 mr-2 text-muted-foreground" />
                      <a href={`tel:${company.phone.replace(/\s+/g, '')}`} className="hover:underline">
                        {company.phone}
                      </a>
                    </div>
                  </div>
                  <div className="space-y-1">
                    <p className="text-sm text-muted-foreground">E-posta</p>
                    <div className="flex items-center">
                      <Mail className="h-4 w-4 mr-2 text-muted-foreground" />
                      <a href={`mailto:${company.email}`} className="hover:underline">
                        {company.email}
                      </a>
                    </div>
                  </div>
                  <div className="space-y-1">
                    <p className="text-sm text-muted-foreground">Web Sitesi</p>
                    <div className="flex items-center">
                      <Globe className="h-4 w-4 mr-2 text-muted-foreground" />
                      <a 
                        href={`https://${company.website}`} 
                        target="_blank" 
                        rel="noopener noreferrer"
                        className="hover:underline"
                      >
                        {company.website}
                      </a>
                    </div>
                  </div>
                </div>
              </div>

              <div className="rounded-lg border p-6">
                <h2 className="text-lg font-semibold mb-4">Yöneticiler</h2>
                <div className="space-y-4">
                  {company.executives.map((executive, index) => (
                    <div key={index} className="flex items-center justify-between p-3 rounded-lg bg-muted/50">
                      <div>
                        <p className="font-medium">{executive.name}</p>
                        <p className="text-sm text-muted-foreground">{executive.title}</p>
                      </div>
                      <div className="text-sm text-muted-foreground">
                        {executive.startDate} tarihinden beri
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            <div className="space-y-6">
              <div className="rounded-lg border p-6">
                <h2 className="text-lg font-semibold mb-4">Hakkında</h2>
                <p className="text-muted-foreground">{company.description}</p>
              </div>

              <div className="rounded-lg border p-6">
                <h2 className="text-lg font-semibold mb-4">Son Faaliyetler</h2>
                <div className="space-y-4">
                  {[1, 2, 3].map((item) => (
                    <div key={item} className="flex items-start">
                      <div className="h-2 w-2 rounded-full bg-primary mt-2 mr-3" />
                      <div>
                        <p className="font-medium">Sermaye Artırımı</p>
                        <p className="text-sm text-muted-foreground">15 Mayıs 2024</p>
                        <p className="text-sm mt-1">Sermaye 1.000.000 TL'den 2.500.000 TL'ye çıkarıldı.</p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </TabsContent>

        <TabsContent value="financials">
          <div className="rounded-lg border p-6">
            <h2 className="text-lg font-semibold mb-4">Finansal Bilgiler</h2>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b">
                    <th className="text-left p-3">Yıl</th>
                    <th className="text-right p-3">Ciro</th>
                    <th className="text-right p-3">Net Kâr</th>
                    <th className="text-right p-3">Toplam Varlıklar</th>
                    <th className="text-right p-3">Özkaynaklar</th>
                  </tr>
                </thead>
                <tbody>
                  {company.financials.map((financial, index) => (
                    <tr key={index} className="border-b last:border-0 hover:bg-muted/50">
                      <td className="p-3 font-medium">{financial.year}</td>
                      <td className="p-3 text-right">{financial.revenue}</td>
                      <td className="p-3 text-right">{financial.profit}</td>
                      <td className="p-3 text-right">{financial.assets}</td>
                      <td className="p-3 text-right">{financial.equity}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </TabsContent>

        <TabsContent value="documents">
          <div className="rounded-lg border p-6">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-lg font-semibold">Belgeler</h2>
              <Button size="sm">Belge Yükle</Button>
            </div>
            <div className="space-y-2">
              {company.documents.map((doc) => (
                <div key={doc.id} className="flex items-center justify-between p-3 rounded-lg border">
                  <div className="flex items-center">
                    <FileText className="h-5 w-5 mr-3 text-muted-foreground" />
                    <div>
                      <p className="font-medium">{doc.name}</p>
                      <p className="text-xs text-muted-foreground">{doc.type} • {doc.size} • {doc.date}</p>
                    </div>
                  </div>
                  <Button variant="ghost" size="icon">
                    <Download className="h-4 w-4" />
                    <span className="sr-only">İndir</span>
                  </Button>
                </div>
              ))}
            </div>
          </div>
        </TabsContent>

        <TabsContent value="history">
          <div className="rounded-lg border p-6">
            <h2 className="text-lg font-semibold mb-4">Şirket Tarihçesi</h2>
            <div className="relative">
              <div className="absolute left-5 top-0 h-full w-0.5 bg-muted" />
              <div className="space-y-8">
                {[
                  {
                    date: '15.05.2010',
                    title: 'Kuruluş',
                    description: 'ABC Teknoloji A.Ş. 100.000 TL sermaye ile kuruldu.'
                  },
                  {
                    date: '10.03.2015',
                    title: 'Sermaye Artırımı',
                    description: 'Sermaye 500.000 TL\'ye çıkarıldı.'
                  },
                  {
                    date: '22.11.2018',
                    title: 'Yeni Ofis',
                    description: 'Levent\'deki yeni ofisimize taşındık.'
                  },
                  {
                    date: '01.01.2023',
                    title: 'Yeni Hizmet',
                    description: 'Yapay zeka çözümleri hizmetleri başlatıldı.'
                  }
                ].map((event, index) => (
                  <div key={index} className="relative pl-10">
                    <div className="absolute left-0 top-1 h-4 w-4 rounded-full bg-primary flex items-center justify-center">
                      <div className="h-2 w-2 rounded-full bg-white" />
                    </div>
                    <p className="text-sm text-muted-foreground">{event.date}</p>
                    <h3 className="font-medium">{event.title}</h3>
                    <p className="text-muted-foreground">{event.description}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </TabsContent>

        <TabsContent value="relationships">
          <div className="rounded-lg border p-6">
            <h2 className="text-lg font-semibold mb-4">İlişkili Şirketler</h2>
            <div className="grid gap-4 md:grid-cols-2">
              {[1, 2, 3].map((item) => (
                <div key={item} className="rounded-lg border p-4">
                  <div className="flex justify-between items-start">
                    <div>
                      <h3 className="font-medium">İlgili Şirket {item}</h3>
                      <p className="text-sm text-muted-foreground">Ortak Yönetici: Ahmet Yılmaz</p>
                      <p className="text-sm text-muted-foreground">İlişki Türü: Ortak Yönetim</p>
                    </div>
                    <Button variant="outline" size="sm">Detay</Button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
}
