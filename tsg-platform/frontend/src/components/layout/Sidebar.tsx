'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Home, Upload, Search, Settings, Bot } from 'lucide-react';

import { cn } from '@/lib/utils';
import { Icons } from '@/components/icons';

const navItems = [
  { href: '/dashboard', label: 'Dashboard', icon: Home },
  { href: '/dashboard/upload', label: 'Dosya Yükle', icon: Upload },
  { href: '/dashboard/search', label: 'Veri Arama', icon: Search },
  { href: '/dashboard/scraping', label: 'Veri Kazıma', icon: Bot },
  { href: '/dashboard/settings', label: 'Ayarlar', icon: Settings },
];

export function Sidebar() {
  const pathname = usePathname();

  return (
    <div className="hidden border-r bg-muted/40 md:block">
      <div className="flex h-full max-h-screen flex-col gap-2">
        <div className="flex h-14 items-center border-b px-4 lg:h-[60px] lg:px-6">
          <Link href="/" className="flex items-center gap-2 font-semibold">
            <Icons.logo className="h-6 w-6 text-[#1e3a8a]" />
            <span className="">Sicilius</span>
          </Link>
        </div>
        <div className="flex-1">
          <nav className="grid items-start px-2 text-sm font-medium lg:px-4">
            {navItems.map(({ href, label, icon: Icon }) => (
              <Link
                key={label}
                href={href}
                className={cn(
                  'flex items-center gap-3 rounded-lg px-3 py-2 text-muted-foreground transition-all hover:text-primary',
                  pathname === href && 'bg-muted text-primary'
                )}
              >
                <Icon className="h-4 w-4" />
                {label}
              </Link>
            ))}
          </nav>
        </div>
      </div>
    </div>
  );
}
