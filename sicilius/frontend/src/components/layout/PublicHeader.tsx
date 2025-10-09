'use client';

import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { Menu, X } from 'lucide-react';
import { useState, useEffect } from 'react';
import { cn } from '@/lib/utils';
import { SiciliusLogo as Logo } from '@/components/icons/SiciliusLogo';
import ThemeToggle from '@/app/(app)/dashboard/components/ThemeToggle';

export function PublicHeader() {
  const [isScrolled, setIsScrolled] = useState(false);
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 10);
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const navItems = [
    { name: 'Anasayfa', href: '/' },
    { name: 'Hakkında', href: '/about' },
    { name: 'SSS', href: '/sss' },
    { name: 'İletişim', href: '/contact' },
  ];

  return (
    <header 
      data-testid="public-header"
      className={cn(
        'fixed top-0 left-0 right-0 z-50 transition-all duration-300',
        isScrolled 
          ? 'bg-background/80 backdrop-blur-md border-b border-border/50 shadow-sm' 
          : 'bg-transparent border-b border-transparent'
      )}
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16 md:h-20">
          <div className="flex items-center">
            <Link 
              href="/" 
              className="flex items-center space-x-2 group"
            >
              <Logo className="h-7 w-auto text-primary" />
              <span className="text-2xl font-bold gradient-text">Sicilius</span>
            </Link>
          </div>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center space-x-1">
            {navItems.map((item) => (
              <Link
                key={item.href}
                href={item.href}
                className={cn(
                  'px-4 py-2 text-sm font-medium rounded-lg transition-colors',
                  'text-foreground/80 hover:text-foreground hover:bg-gray-100 dark:hover:bg-slate-800',
                  'relative overflow-hidden'
                )}
              >
                {item.name}
              </Link>
            ))}
          </nav>

          <div className="hidden md:flex items-center space-x-3">
            <Button asChild variant="gradient" className="px-6">
              <Link href="/login">Giriş Yap</Link>
            </Button>
            <div className="ml-1">
              <ThemeToggle fixed={false} />
            </div>
          </div>

          {/* Mobile menu button */}
          <div className="flex items-center md:hidden">
            <button
              onClick={() => setIsMenuOpen(!isMenuOpen)}
              className="inline-flex items-center justify-center p-2 rounded-md text-foreground/70 hover:text-foreground focus:outline-none"
              data-testid="mobile-menu-button"
              aria-expanded="false"
            >
              <span className="sr-only">Menüyü aç</span>
              {isScrolled ? 
                (isMenuOpen ? <X size={24} /> : <Menu size={24} />) :
                (isMenuOpen ? <X size={24} className="text-white" /> : <Menu size={24} className="text-white" />)}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile menu */}
      <div
        data-testid="mobile-menu"
        className={cn(
          'md:hidden transition-all duration-300 ease-in-out overflow-hidden',
          isMenuOpen ? 'max-h-96' : 'max-h-0'
        )}
      >
        <div className="px-2 pt-2 pb-3 space-y-1 bg-background/95 backdrop-blur-sm border-t border-border/50">
          {navItems.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              className="block px-3 py-2 rounded-md text-base font-medium text-foreground/90 hover:bg-gray-100 dark:hover:bg-slate-800 hover:text-foreground transition-colors"
              onClick={() => setIsMenuOpen(false)}
            >
              {item.name}
            </Link>
          ))}
          <div className="pt-4 border-t border-border/30 mt-2 space-y-2">
            <Button asChild variant="gradient" className="w-full px-4 py-2 text-center" onClick={() => setIsMenuOpen(false)}>
              <Link href="/login">Giriş Yap</Link>
            </Button>
            <div className="w-full flex justify-center">
              <ThemeToggle fixed={false} />
            </div>
          </div>
        </div>
      </div>
    </header>
  );
}
