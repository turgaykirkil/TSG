import type { Metadata } from 'next';
import { getServerSession } from 'next-auth';
import { redirect } from 'next/navigation';
import { authOptions } from '@/lib/auth';
import Link from 'next/link';

export const metadata: Metadata = {
  title: 'Şirketler | Sicilius',
  description: 'Kayıtlı tüm şirketlerin listesi',
};

type Company = {
  id: number;
  name: string;
  type: string;
  city: string;
};

export default async function CompaniesPage() {
  const session = await getServerSession(authOptions);

  // Redirect to login if not authenticated
  if (!session) {
    redirect('/auth/login');
  }

  // This would typically come from an API
  const companies: Company[] = [
    { id: 1, name: 'ABC Teknoloji A.Ş.', type: 'Anonim Şirket', city: 'İstanbul' },
    { id: 2, name: 'XYZ Danışmanlık Ltd. Şti.', type: 'Limited Şirket', city: 'Ankara' },
    { id: 3, name: '123 İnşaat A.Ş.', type: 'Anonim Şirket', city: 'İzmir' },
  ];

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold tracking-tight">Şirketler</h1>
        <p className="text-muted-foreground">
          Kayıtlı tüm şirketlerin listesi
        </p>
      </div>
      
      <div className="rounded-lg border bg-card text-card-foreground shadow-sm">
        <div className="p-6">
          <div className="flex items-center justify-between mb-6">
            <div className="flex-1 max-w-md">
              <input
                type="text"
                placeholder="Şirket adı ile ara..."
                className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
              />
            </div>
            <Link 
              href="/dashboard/companies/new"
              className="inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 bg-primary text-primary-foreground hover:bg-primary/90 h-10 px-4 py-2"
            >
              Yeni Şirket Ekle
            </Link>
          </div>
          
          <div className="rounded-md border">
            <table className="w-full">
              <thead>
                <tr className="border-b">
                  <th className="h-12 px-4 text-left align-middle font-medium text-muted-foreground">ID</th>
                  <th className="h-12 px-4 text-left align-middle font-medium text-muted-foreground">Şirket Adı</th>
                  <th className="h-12 px-4 text-left align-middle font-medium text-muted-foreground">Tür</th>
                  <th className="h-12 px-4 text-left align-middle font-medium text-muted-foreground">Şehir</th>
                  <th className="h-12 px-4 text-right align-middle font-medium text-muted-foreground">İşlemler</th>
                </tr>
              </thead>
              <tbody>
                {companies.map((company) => (
                  <tr key={company.id} className="border-b hover:bg-muted/50">
                    <td className="p-4 align-middle">{company.id}</td>
                    <td className="p-4 align-middle font-medium">
                      <Link 
                        href={`/dashboard/companies/${company.id}`}
                        className="hover:underline hover:text-primary"
                      >
                        {company.name}
                      </Link>
                    </td>
                    <td className="p-4 align-middle">{company.type}</td>
                    <td className="p-4 align-middle">{company.city}</td>
                    <td className="p-4 align-middle text-right">
                      <Link 
                        href={`/dashboard/companies/${company.id}`}
                        className="text-primary hover:underline"
                      >
                        Detay
                      </Link>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          
          <div className="flex items-center justify-between px-2 py-4">
            <div className="text-sm text-muted-foreground">
              Toplam {companies.length} şirket listeleniyor
            </div>
            <div className="flex items-center space-x-2">
              <button 
                className="inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 border border-input bg-background hover:bg-accent hover:text-accent-foreground h-9 w-9"
                disabled
              >
                &lt;
              </button>
              <button 
                className="inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 border border-input bg-background hover:bg-accent hover:text-accent-foreground h-9 w-9"
                disabled
              >
                &gt;
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
