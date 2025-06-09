import * as React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Icons } from '@/components/icons';
import { cn } from '@/lib/utils';

const navigation = [
  { name: 'Anasayfa', href: '/' },
  { name: 'Hakkında', href: '/about' },
  { name: 'İletişim', href: '/contact' },
];

type HeaderProps = {
  className?: string;
};

export function Header({ className }: HeaderProps) {
  const location = useLocation();
  const [mobileMenuOpen, setMobileMenuOpen] = React.useState(false);

  return (
    <header className={cn('sticky top-0 z-40 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60', className)}>
      <div className="container flex h-16 items-center justify-between">
        <div className="flex items-center gap-6 md:gap-10">
          <Link to="/" className="flex items-center space-x-2">
            <Icons.logo className="h-6 w-6" />
            <span className="font-bold inline-block">TSG Platform</span>
          </Link>
          
          <nav className="hidden md:flex gap-6">
            {navigation.map((item) => (
              <Link
                key={item.href}
                to={item.href}
                className={cn(
                  'flex items-center text-sm font-medium text-muted-foreground transition-colors hover:text-foreground',
                  location.pathname === item.href && 'text-foreground'
                )}
              >
                {item.name}
              </Link>
            ))}
          </nav>
        </div>

        <div className="flex items-center gap-2">
          <Button variant="ghost" size="sm" asChild>
            <Link to="/auth/login">Giriş Yap</Link>
          </Button>
          <Button size="sm" asChild>
            <Link to="/auth/register">Kayıt Ol</Link>
          </Button>
          
          <Button
            variant="ghost"
            size="icon"
            className="md:hidden"
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          >
            <Icons.menu className="h-5 w-5" />
            <span className="sr-only">Menüyü Aç</span>
          </Button>
        </div>
      </div>
      
      {/* Mobile Menu */}
      <div className={cn(
        'md:hidden border-t bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60',
        mobileMenuOpen ? 'block' : 'hidden'
      )}>
        <div className="container py-2">
          <nav className="flex flex-col gap-2">
            {navigation.map((item) => (
              <Link
                key={item.href}
                to={item.href}
                className={cn(
                  'block px-4 py-2 text-sm font-medium rounded-md transition-colors',
                  location.pathname === item.href
                    ? 'bg-accent text-accent-foreground'
                    : 'text-muted-foreground hover:bg-accent hover:text-accent-foreground'
                )}
                onClick={() => setMobileMenuOpen(false)}
              >
                {item.name}
              </Link>
            ))}
          </nav>
        </div>
      </div>
    </header>
  );
}
