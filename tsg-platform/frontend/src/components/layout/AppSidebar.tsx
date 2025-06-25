'use client';

import Image from 'next/image';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Home, Search, BarChart3, Bookmark, Settings, UploadCloud, LogOut } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { useAuth } from '@/hooks/useAuth';

type NavItem = {
  name: string;
  href: string;
  icon: React.ComponentType<{ className?: string }>;
};

const baseNavigation: NavItem[] = [
  { name: 'Genel Bakış', href: '/dashboard', icon: Home },
  { name: 'Arama', href: '/dashboard/search', icon: Search },
  { name: 'Raporlar', href: '/dashboard/reports', icon: BarChart3 },
  { name: 'Kaydedilenler', href: '/dashboard/favorites', icon: Bookmark },
  { name: 'Ayarlar', href: '/dashboard/settings', icon: Settings },
];

export function AppSidebar() {
  const pathname = usePathname();
  const { user, logout } = useAuth();
  const isAdmin = user?.role === 'admin';
  const navigation: NavItem[] = isAdmin
    ? [...baseNavigation, { name: 'Dosya İşlemleri', href: '/admin', icon: UploadCloud }]
    : baseNavigation;
  

  return (
    <div className="hidden md:flex md:flex-shrink-0">
      <div className="flex flex-col w-64 border-r border-gray-200 bg-white">
        <div className="flex flex-col flex-grow pt-5 pb-4 overflow-y-auto">
                    <div className="flex items-center flex-shrink-0 px-6">
                        <Link href="/dashboard" className="flex items-center gap-2">
              <Image src="/sicilius-logo.svg" alt="Sicilius Logo" width={32} height={32} />
              <span className="text-xl font-bold text-primary">Sicilius</span>
            </Link>
          </div>
          <div className="mt-5 flex-grow flex flex-col">
            <nav className="flex-1 px-2 space-y-1">
              {navigation.map((item) => {
                const isActive = pathname === item.href;
                return (
                  <Link
                    key={item.name}
                    href={item.href}
                    className={`group flex items-center px-2 py-2 text-sm font-medium rounded-md ${
                      isActive
                        ? 'bg-primary/10 text-primary'
                        : 'text-muted-foreground hover:text-primary hover:bg-primary/5'
                    }`}
                  >
                    <item.icon
                      className={`mr-3 flex-shrink-0 h-6 w-6 ${
                        isActive ? 'text-primary' : 'text-muted-foreground group-hover:text-primary/80'
                      }`}
                      aria-hidden="true"
                    />
                    {item.name}
                  </Link>
                );
              })}
            </nav>
            <div className="mt-auto px-2 pb-4">
              <Button
                variant="ghost"
                onClick={logout}
                className="w-full justify-start group flex items-center px-2 py-2 text-sm font-medium rounded-md text-muted-foreground hover:text-primary hover:bg-primary/5"
              >
                <LogOut className="mr-3 h-6 w-6" />
                <span>Çıkış Yap</span>
              </Button>
            </div>
          </div>

        </div>
      </div>
    </div>
  );
}
