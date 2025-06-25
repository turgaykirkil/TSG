import { type ReactNode, useState, useEffect } from 'react';
import { useSession } from 'next-auth/react';
import Link from 'next/link';
import { usePathname, useRouter } from 'next/navigation';
import { cn } from '@/lib/utils';
import { useTheme } from '@/contexts/ThemeContext';
import { Button } from '@/components/ui/button';
import { toast } from 'sonner';
import { Icons } from '@/components/icons';
import { UserNav } from '@/components/user-nav';
import { FullScreenLoader } from '@/components/ui/loading-spinner';


interface DashboardLayoutProps {
  children: ReactNode;
  className?: string;
}

type NavItem = {
  title: string;
  href: string;
  icon: keyof typeof Icons;
  disabled?: boolean;
};

const baseSidebarNavItems: NavItem[] = [
  {
    title: 'Genel Bakış',
    href: '/dashboard',
    icon: 'layoutDashboard',
  },
  {
    title: 'Şirketler',
    href: '/dashboard/companies',
    icon: 'building2',
  },
  {
    title: 'İlanlar',
    href: '/dashboard/announcements',
    icon: 'newspaper',
  },
  {
    title: 'Ayarlar',
    href: '/dashboard/settings',
    icon: 'settings',
  },
];

export function DashboardLayout({ children, className }: DashboardLayoutProps) {
  const { data: session, status } = useSession();
  const router = useRouter();
  const pathname = usePathname();
  const { theme, setTheme } = useTheme();

  const [isSidebarOpen, setIsSidebarOpen] = useState(false);

  const user = session?.user;
  const isAdmin = user?.role === 'admin';

  const sidebarNavItems: NavItem[] = isAdmin
    ? [...baseSidebarNavItems, { title: 'Dosya İşlemleri', href: '/admin', icon: 'upload' } as NavItem]
    : baseSidebarNavItems;

  useEffect(() => {
    if (status === 'unauthenticated') {
      // Redirect immediately without showing a toast, as the user will be on the login page.
      router.push('/auth/login');
    }
  }, [status, router]);

  const toggleTheme = () => {
    const newTheme = theme === 'dark' ? 'light' : 'dark';
    setTheme(newTheme);
    document.documentElement.classList.toggle('dark', newTheme === 'dark');
    localStorage.setItem('theme', newTheme);
    const metaThemeColor = document.querySelector('meta[name="theme-color"]');
    if (metaThemeColor) {
      metaThemeColor.setAttribute(
        'content',
        newTheme === 'dark' ? '#0f172a' : '#ffffff'
      );
    }
  };

  if (status === 'loading') {
    return <FullScreenLoader />;
  }

  if (status === 'unauthenticated') {
    // Yönlendirme sırasında içeriğin görünmesini engelle
    return null;
  }

  return (
    <div className={cn('min-h-screen bg-background font-sans antialiased flex')}>
      {/* Mobile sidebar */}
      <div
        className={cn(
          'fixed inset-0 z-40 lg:hidden',
          isSidebarOpen ? 'block' : 'hidden',
          'transition-opacity duration-300',
          'bg-background/80 backdrop-blur-sm',
          'lg:bg-transparent lg:backdrop-blur-0',
        )}
        onClick={() => setIsSidebarOpen(false)}
      >
        <div
          className={cn(
            'fixed inset-y-0 left-0 z-50 w-64 bg-background shadow-lg transition-all duration-300 ease-in-out',
            isSidebarOpen ? 'translate-x-0' : '-translate-x-full',
            'lg:translate-x-0',
            'border-r border-border',
          )}
          onClick={(e) => e.stopPropagation()}
        >
          <div className="flex h-16 items-center justify-between border-b border-border px-6">
            <Link href="/dashboard" className="flex items-center space-x-2">
              <Icons.logo className="h-8 w-8" />
              <span className="text-xl font-bold">Sicilius</span>
            </Link>
            <Button
              variant="ghost"
              size="icon"
              onClick={() => setIsSidebarOpen(false)}
              className="lg:hidden"
            >
              <Icons.x className="h-5 w-5" />
              <span className="sr-only">Menüyü kapat</span>
            </Button>
          </div>
          <nav className="space-y-1 p-4">
            {sidebarNavItems.map((item) => {
              const Icon = Icons[item.icon];
              const isActive = pathname === item.href;

              return (
                <Link
                  key={item.href}
                  href={item.href}
                  className={cn(
                    'flex items-center rounded-md px-3 py-2 text-sm font-medium transition-colors',
                    isActive
                      ? 'bg-primary/10 text-primary'
                      : 'text-muted-foreground hover:bg-accent hover:text-accent-foreground',
                    item.disabled && 'cursor-not-allowed opacity-50',
                  )}
                  onClick={() => setIsSidebarOpen(false)}
                >
                  <Icon className="mr-3 h-5 w-5" />
                  {item.title}
                </Link>
              );
            })}
          </nav>
        </div>
      </div>

      {/* Desktop sidebar */}
      <div className="hidden lg:fixed lg:inset-y-0 lg:flex lg:w-64 lg:flex-col lg:border-r lg:border-border">
        <div className="flex h-16 flex-shrink-0 items-center border-b border-border px-6">
          <Link href="/dashboard" className="flex items-center space-x-2">
            <Icons.logo className="h-8 w-8" />
            <span className="text-xl font-bold">Sicilius</span>
          </Link>
        </div>
        <div className="flex flex-1 flex-col overflow-y-auto">
          <nav className="flex-1 space-y-1 px-2 py-4">
            {sidebarNavItems.map((item) => {
              const Icon = Icons[item.icon];
              const isActive = pathname === item.href;

              return (
                <Link
                  key={item.href}
                  href={item.href}
                  className={cn(
                    'group flex items-center rounded-md px-3 py-2 text-sm font-medium transition-colors',
                    isActive
                      ? 'bg-primary/10 text-primary'
                      : 'text-muted-foreground hover:bg-accent hover:text-accent-foreground',
                    item.disabled && 'cursor-not-allowed opacity-50',
                  )}
                >
                  <Icon className="mr-3 h-5 w-5" />
                  {item.title}
                </Link>
              );
            })}
          </nav>

          <div className="border-t border-border p-4">
            <div className="flex items-center justify-between">
              <button
                onClick={toggleTheme}
                className="flex items-center space-x-2 rounded-md p-2 text-sm font-medium text-muted-foreground transition-colors hover:bg-accent hover:text-accent-foreground"
                aria-label={theme === 'dark' ? 'Açık temaya geç' : 'Koyu temaya geç'}
              >
                {theme === 'dark' ? (
                  <>
                    <Icons.sun className="h-5 w-5" />
                    <span className="sr-only lg:not-sr-only">Açık Tema</span>
                  </>
                ) : (
                  <>
                    <Icons.moon className="h-5 w-5" />
                    <span className="sr-only lg:not-sr-only">Koyu Tema</span>
                  </>
                )}
              </button>
              <UserNav />
            </div>
          </div>
        </div>
      </div>

      <div className="flex flex-1 flex-col lg:pl-64">
        <header className="sticky top-0 z-10 flex h-16 flex-shrink-0 items-center justify-between border-b border-border bg-background/95 px-4 backdrop-blur supports-[backdrop-filter]:bg-background/60 lg:px-6">
          <div className="flex items-center">
            <Button
              variant="ghost"
              size="icon"
              className="lg:hidden"
              onClick={() => setIsSidebarOpen(true)}
              aria-label="Menüyü aç"
            >
              <Icons.menu className="h-6 w-6" />
              <span className="sr-only">Menüyü aç</span>
            </Button>
            <h1 className="ml-2 text-lg font-semibold">
              {sidebarNavItems.find((item) => item.href === pathname)?.title || 'Panel'}
            </h1>
          </div>
          <div className="flex items-center space-x-4">
            <Button
              variant="ghost"
              size="icon"
              className="lg:hidden"
              onClick={toggleTheme}
              aria-label={theme === 'dark' ? 'Açık temaya geç' : 'Koyu temaya geç'}
            >
              {theme === 'dark' ? (
                <Icons.sun className="h-5 w-5" />
              ) : (
                <Icons.moon className="h-5 w-5" />
              )}
              <span className="sr-only">Temayı değiştir</span>
            </Button>
            <div className="lg:hidden">
              <UserNav />
            </div>
          </div>
        </header>

        <main className={cn('flex-1', className)}>
          <div className="mx-auto max-w-7xl p-4 sm:p-6 lg:p-8">
            {children}
          </div>
        </main>
      </div>
    </div>
  );
}
