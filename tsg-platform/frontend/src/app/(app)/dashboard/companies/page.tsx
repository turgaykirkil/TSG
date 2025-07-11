import type { Metadata } from 'next';
import { cookies } from 'next/headers';
import { redirect } from 'next/navigation';
import Link from 'next/link';
import { API_BASE_URL, API_ENDPOINTS } from '@/lib/constants';

export const metadata: Metadata = {
  title: 'Şirketler | Sicilius',
  description: 'Kayıtlı tüm şirketlerin listesi',
};

type Company = {
  id: string; // Changed from number to string to match UUID
  name: string;
  type: string;
  city: string;
};

async function getSession() {
  const cookieStore = cookies();
  const token = cookieStore.get('auth_token')?.value;
  
  if (!token) {
    return null;
  }

  try {
    const response = await fetch(`${API_BASE_URL}${API_ENDPOINTS.AUTH.ME}`, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
      cache: 'no-store',
    });

    if (!response.ok) {
      return null;
    }

    return await response.json();
  } catch (error) {
    console.error('Session check failed:', error);
    return null;
  }
}

export default async function CompaniesPage() {
  const session = await getSession();
  
  if (!session) { // Corrected session check
    redirect('/login');
  }

  // Fetch companies from API
  let companies: Company[] = [];
  try {
    const response = await fetch(`${API_BASE_URL}${API_ENDPOINTS.COMPANIES.BASE}`, {
      headers: {
        'Authorization': `Bearer ${cookies().get('auth_token')?.value}`,
        'Content-Type': 'application/json',
      },
      cache: 'no-store',
    });

    if (response.ok) {
      companies = await response.json();
    } else {
      console.error('Failed to fetch companies:', await response.text());
    }
  } catch (error) {
    console.error('Error fetching companies:', error);
  }

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
