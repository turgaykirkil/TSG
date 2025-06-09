import { Link } from 'react-router-dom';
import { cn } from '@/lib/utils';
import { Icons } from '@/components/icons';

export function MainNav() {
  return (
    <div className="flex items-center space-x-4 lg:space-x-6">
      <Link
        to="/dashboard"
        className="text-sm font-medium transition-colors hover:text-primary"
      >
        <Icons.logo className="h-8 w-8" />
      </Link>
      <nav className="hidden items-center space-x-4 md:flex lg:space-x-6">
        <Link
          to="/dashboard"
          className={cn(
            'text-sm font-medium transition-colors hover:text-primary',
            location.pathname === '/dashboard' ? 'text-primary' : 'text-muted-foreground'
          )}
        >
          Genel Bakış
        </Link>
        <Link
          to="/dashboard/companies"
          className={cn(
            'text-sm font-medium transition-colors hover:text-primary',
            location.pathname.startsWith('/dashboard/companies')
              ? 'text-primary'
              : 'text-muted-foreground'
          )}
        >
          Şirketler
        </Link>
        <Link
          to="/dashboard/announcements"
          className={cn(
            'text-sm font-medium transition-colors hover:text-primary',
            location.pathname.startsWith('/dashboard/announcements')
              ? 'text-primary'
              : 'text-muted-foreground'
          )}
        >
          İlanlar
        </Link>
      </nav>
    </div>
  );
}
