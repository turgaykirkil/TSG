import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useAuth } from '@/hooks/useAuth';
import { cn } from '@/lib/utils';
import { Icons } from '@/components/icons';

export function MainNav() {
  const pathname = usePathname();
  const { user } = useAuth();
  const isAdmin = user?.role === 'admin';
  return (
    <div className="flex items-center space-x-4 lg:space-x-6">
      <Link
        href="/dashboard"
        className="text-sm font-medium transition-colors hover:text-primary"
      >
        <Icons.logo className="h-8 w-8" />
      </Link>
      <nav className="hidden items-center space-x-4 md:flex lg:space-x-6">
        <Link
          href="/dashboard"
          className={cn(
            'text-sm font-medium transition-colors hover:text-primary',
            pathname === '/dashboard' ? 'text-primary' : 'text-muted-foreground'
          )}
        >
          Genel Bakış
        </Link>
        <Link
          href="/dashboard/companies"
          className={cn(
            'text-sm font-medium transition-colors hover:text-primary',
            pathname.startsWith('/dashboard/companies')
              ? 'text-primary'
              : 'text-muted-foreground'
          )}
        >
          Şirketler
        </Link>
        <Link
          href="/dashboard/announcements"
          className={cn(
            'text-sm font-medium transition-colors hover:text-primary',
            pathname.startsWith('/dashboard/announcements')
              ? 'text-primary'
              : 'text-muted-foreground'
          )}
        >
          İlanlar
        </Link>
        {isAdmin && (
          <Link
            href="/admin"
            className={cn(
              'text-sm font-medium transition-colors hover:text-primary',
              pathname.startsWith('/admin')
                ? 'text-primary'
                : 'text-muted-foreground'
            )}
          >
            Dosya İşlemleri
          </Link>
        )}
      </nav>
    </div>
  );
}
