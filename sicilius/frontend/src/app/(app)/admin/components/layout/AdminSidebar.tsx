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
  ArrowLeft,
  type LucideIcon,
  ScanText,
  ArrowRight,
  Database,
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
  target?: string;
};



const userNavigation: NavItem[] = [
  { name: 'Dashboard', href: '/dashboard', icon: Home },
  { name: 'Arama', href: '/search', icon: Search },
  { name: 'Profil', href: '/profile', icon: Settings },
  { name: 'Yükle', href: '/upload', icon: UploadCloud },
];

const adminNavigation: NavItem[] = [
  { name: 'Admin Paneli', href: '/admin', icon: Home },
  { name: 'OCR Yönetimi', href: '/admin/ocr', icon: ScanText },
  { name: 'Raporlar', href: '/admin/reports', icon: BarChart3 },
  { name: 'Supabase Kullanımı', href: '/admin/usage', icon: Database },
  { name: 'Kaydedilenler', href: '/admin/favorites', icon: Bookmark },
  { name: 'Ayarlar', href: '/admin/settings', icon: Settings },
];

export function AppSidebar({ onLinkClick }: AppSidebarProps) {
  const pathname = usePathname();
  const { session, logout } = useAuth();
  const user = session?.user;
  const isAdmin = user?.role === 'admin';

  const navigation: NavItem[] = isAdmin ? adminNavigation : userNavigation;

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
          const isActive = pathname === item.href;
          return (
            <Link
              key={item.name}
              href={item.href}
              onClick={onLinkClick}
              target={item.target}
              rel={item.target === '_blank' ? 'noopener noreferrer' : ''}
              className={cn(
                'flex items-center gap-3 rounded-lg px-3 py-2 transition-colors text-foreground/80 hover:bg-accent hover:text-accent-foreground',
                isActive && 'bg-primary/15 text-primary hover:bg-primary/20'
              )}
            >
              <item.icon className="h-5 w-5" aria-hidden="true" />
              <span className="text-sm font-medium">{item.name}</span>
            </Link>
          );
        })}
      </nav>

      <div className="mt-auto border-t p-4">
        <Link
          href="/dashboard"
          target="_blank"
          rel="noopener noreferrer"
          className="flex w-full items-center gap-3 rounded-lg px-3 py-2 text-slate-700 transition-all hover:bg-slate-100 hover:text-slate-900 dark:text-slate-300 dark:hover:bg-slate-800 dark:hover:text-slate-50"
        >
          <ArrowRight className="h-5 w-5" />
          <span className="text-sm font-medium">Siteye Git</span>
        </Link>
      </div>
    </div>
  );
}
