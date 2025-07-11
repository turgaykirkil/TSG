

'use client';

import { useState } from 'react';
import Link from 'next/link';
import { usePathname, useRouter } from 'next/navigation';
import { Bell, Search, Menu, User, Settings, LogOut, CreditCard, LifeBuoy } from 'lucide-react';

import { Button } from '@/components/ui/button';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { Input } from '@/components/ui/input';
import { useAuth } from '@/contexts/AuthContext';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuGroup,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';



export function AppHeader() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const pathname = usePathname();
  const router = useRouter();
    const { session, logout } = useAuth();
  const user = session?.user;

  const navigation = [
    { name: 'Genel Bakış', href: '/dashboard' },
    { name: 'Arama', href: '/search' },
    { name: 'Raporlar', href: '/reports' },
    { name: 'Kaydedilenler', href: '/favorites' },
    { name: 'Ayarlar', href: '/settings' },
  ];

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchTerm.trim()) {
      router.push(`/search?q=${encodeURIComponent(searchTerm)}`);
    }
  };

  return (
    <header className="sticky top-0 z-10 flex-shrink-0 flex h-16 bg-white shadow">
      <div className="flex-1 px-4 flex justify-between">
        <div className="flex items-center">
          <Button
            variant="ghost"
            size="icon"
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="md:hidden"
          >
            <span className="sr-only">Menüyü aç</span>
            <Menu className="h-6 w-6" aria-hidden="true" />
          </Button>
        </div>

        <div className="flex-1 flex items-center justify-center px-2 lg:ml-6 lg:justify-end">
          <form onSubmit={handleSearch} className="w-full max-w-lg lg:max-w-xs">
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <Search className="h-5 w-5 text-gray-400" aria-hidden="true" />
              </div>
              <Input
                id="search"
                name="search"
                className="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md leading-5 bg-white placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:ring-1 focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
                placeholder="Şirket, sicil no veya vergi no ile ara..."
                type="search"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
              />
            </div>
          </form>
        </div>

        <div className="flex items-center">
          <Button variant="ghost" size="icon" className="ml-2">
            <span className="sr-only">Bildirimler</span>
            <Bell className="h-6 w-6" aria-hidden="true" />
          </Button>

          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="ghost" className="relative h-8 w-8 rounded-full">
                <Avatar className="h-8 w-8">
                  <AvatarImage src={user?.image || ''} alt={user?.name || 'Kullanıcı'} />
                  <AvatarFallback className="bg-primary/10 text-primary font-semibold">
                    {user?.name?.charAt(0).toUpperCase() || 'U'}
                  </AvatarFallback>
                </Avatar>
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent className="w-56" align="end" forceMount>
              <DropdownMenuLabel className="font-normal">
                <div className="flex items-center gap-3">
                  <Avatar className="h-10 w-10">
                    <AvatarImage src={user?.image || ''} alt={user?.name || 'Kullanıcı'} />
                    <AvatarFallback className="bg-primary/10 text-primary font-semibold">
                      {user?.name?.charAt(0).toUpperCase() || 'U'}
                    </AvatarFallback>
                  </Avatar>
                  <div className="flex flex-col space-y-1">
                    <p className="text-sm font-medium leading-none">{user?.name || 'Kullanıcı'}</p>
                    <p className="text-xs leading-none text-muted-foreground">
                      {user?.email}
                    </p>
                    {user?.role && (
                      <p className="text-xs leading-none text-muted-foreground capitalize">
                        {user.role.toLowerCase()}
                      </p>
                    )}
                  </div>
                </div>
              </DropdownMenuLabel>
              <DropdownMenuSeparator />
              <DropdownMenuGroup>
                <DropdownMenuItem onClick={() => router.push('/profile')}>
                  <User className="mr-2 h-4 w-4" />
                  <span>Profil</span>
                </DropdownMenuItem>
                <DropdownMenuItem onClick={() => router.push('/settings')}>
                  <Settings className="mr-2 h-4 w-4" />
                  <span>Ayarlar</span>
                </DropdownMenuItem>
              </DropdownMenuGroup>
              <DropdownMenuSeparator />
              <DropdownMenuItem
                onClick={async () => {
                  await logout();
                  router.push('/login');
                }}
                className="text-red-600 focus:text-red-600"
              >
                <LogOut className="mr-2 h-4 w-4" />
                <span>Çıkış Yap</span>
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </div>
      </div>

      {/* Mobile menu */}
      {mobileMenuOpen && (
        <div className="md:hidden">
          <div className="pt-2 pb-3 space-y-1">
            {navigation.map((item) => {
              const isActive = pathname === item.href;
              return (
                <Link
                  key={item.name}
                  href={item.href}
                  className={`block pl-3 pr-4 py-2 border-l-4 text-base font-medium ${
                    isActive
                      ? 'bg-indigo-50 border-indigo-500 text-indigo-700'
                      : 'border-transparent text-gray-600 hover:bg-gray-50 hover:border-gray-300 hover:text-gray-800'
                  }`}
                  onClick={() => setMobileMenuOpen(false)}
                >
                  {item.name}
                </Link>
              );
            })}
          </div>
        </div>
      )}
    </header>
  );
}
