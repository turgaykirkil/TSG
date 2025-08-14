'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Home, Upload, Search, Settings, Bot } from 'lucide-react';

import { cn } from '@/lib/utils';
import { Icons } from '@/components/icons';

const navItems = [
  { href: '/dashboard', label: 'Dashboard', icon: Home },
  { href: '/dashboard/search', label: 'Veri Arama', icon: Search },
  { href: '/dashboard/settings', label: 'Ayarlar', icon: Settings },
];

interface SidebarProps {
  isOpen?: boolean;
  onClose?: () => void;
}

export function Sidebar({ isOpen = false, onClose }: SidebarProps) {
  const pathname = usePathname();

  return (
    <div 
      className={cn(
        'fixed inset-y-0 left-0 z-30 w-64 border-r bg-muted/40 transition-transform duration-300 ease-in-out md:relative md:translate-x-0',
        isOpen ? 'translate-x-0' : '-translate-x-full md:translate-x-0',
        'md:block',
        !isOpen && 'hidden'
      )}
    >
      {/* Overlay for mobile */}
      <div 
        className="fixed inset-0 z-10 bg-black/50 md:hidden"
        onClick={onClose}
      />
      <div className="flex h-full max-h-screen flex-col gap-2">
        <div className="flex h-14 items-center border-b px-4 lg:h-[60px] lg:px-6">
          <Link href="/" className="flex items-center gap-2 font-semibold">
            <Icons.logo className="h-6 w-6 text-[#1e3a8a]" />
            <span className="">Sicilius</span>
          </Link>
        </div>
        <div className="flex-1">
          <nav
            className="grid items-start px-2 text-sm font-medium lg:px-4"
            role="navigation"
            aria-label="Kullanıcı menüsü"
          >
            {navItems.map(({ href, label, icon: Icon }) => (
              <Link
                key={label}
                href={href}
                className={cn(
                  'flex items-center gap-3 rounded-lg px-3 py-2 text-muted-foreground transition-all hover:text-primary',
                  pathname === href && 'bg-muted text-primary'
                )}
                aria-current={pathname === href ? 'page' : undefined}
              >
                <Icon className="h-4 w-4" aria-hidden="true" />
                {label}
              </Link>
            ))}
          </nav>
        </div>
      </div>
    </div>
  );
}
