'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import {
  Home,
  Search,
  BarChart3,
  Bookmark,
  Settings,
  UploadCloud,
  LogOut,
  type LucideIcon,
} from 'lucide-react';
import { useAuth } from '@/contexts/AuthContext';
import { Logo } from '@/components/ui/logo';
import { cn } from '@/lib/utils';
import { Button } from '@/components/ui/button';

interface AppSidebarProps {
  onLinkClick?: () => void;
}

type NavItem = {
  name: string;
  href: string;
  icon: LucideIcon;
};

const baseNavigation: NavItem[] = [
  { name: 'Genel Bakış', href: '/dashboard', icon: Home },
  { name: 'Arama', href: '/dashboard/search', icon: Search },
  { name: 'Raporlar', href: '/dashboard/reports', icon: BarChart3 },
  { name: 'Kaydedilenler', href: '/dashboard/favorites', icon: Bookmark },
  { name: 'Ayarlar', href: '/dashboard/settings', icon: Settings },
];

export function AppSidebar({ onLinkClick }: AppSidebarProps) {
  const pathname = usePathname();
  const { session, logout } = useAuth();
  const user = session?.user;
  const isAdmin = user?.role === 'admin';

  const navigation: NavItem[] = isAdmin
    ? [...baseNavigation, { name: 'Admin', href: '/admin', icon: UploadCloud }]
    : baseNavigation;

  const handleLogout = () => {
    if (onLinkClick) onLinkClick();
    logout();
  };

  return (
    <div className="flex h-full flex-col bg-background">
      <div className="flex h-16 shrink-0 items-center border-b px-6">
        <Link href="/dashboard" className="flex items-center gap-2" onClick={onLinkClick}>
          <Logo className="h-7 w-7 text-primary" />
          <span className="text-xl font-bold text-foreground">Sicilius</span>
        </Link>
      </div>

      <nav className="flex-1 space-y-1 p-4">
        {navigation.map((item) => {
          const isActive =
            pathname === item.href || (item.href !== '/dashboard' && pathname.startsWith(item.href));
          return (
            <Link
              key={item.name}
              href={item.href}
              onClick={onLinkClick}
              className={cn(
                'flex items-center gap-3 rounded-lg px-3 py-2 text-slate-700 transition-all hover:bg-slate-100 hover:text-slate-900 dark:text-slate-300 dark:hover:bg-slate-800 dark:hover:text-slate-50',
                isActive &&
                  'bg-sky-100 text-sky-600 hover:bg-sky-100 hover:text-sky-600 dark:bg-sky-900/50 dark:text-sky-400 dark:hover:bg-sky-900/60 dark:hover:text-sky-400'
              )}
            >
              <item.icon className="h-5 w-5" aria-hidden="true" />
              <span className="text-sm font-medium">{item.name}</span>
            </Link>
          );
        })}
      </nav>

      <div className="mt-auto border-t p-4">
        <Button
          variant="ghost"
          onClick={handleLogout}
          className="w-full justify-start gap-3 px-3 py-2 text-slate-700 hover:bg-slate-100 hover:text-slate-900 dark:text-slate-300 dark:hover:bg-slate-800 dark:hover:text-slate-50"
        >
          <LogOut className="h-5 w-5" />
          <span className="text-sm font-medium">Çıkış Yap</span>
        </Button>
      </div>
    </div>
  );
}
