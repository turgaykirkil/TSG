'use client';

import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { Menu, X } from 'lucide-react';
import { useState, useEffect } from 'react';
import { cn } from '@/lib/utils';

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
    { name: 'İletişim', href: '/contact' },
  ];

  return (
    <header 
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
              <span className="text-2xl font-bold bg-gradient-to-r from-primary to-secondary bg-clip-text text-transparent">
                Sicilius
              </span>
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
                  'text-foreground/80 hover:text-primary hover:bg-accent/50',
                  'relative group overflow-hidden'
                )}
              >
                {item.name}
                <span className="absolute bottom-0 left-0 w-0 h-0.5 bg-primary transition-all duration-300 group-hover:w-full"></span>
              </Link>
            ))}
          </nav>

          <div className="hidden md:flex items-center space-x-3">
            <Link href="/login">
              <Button variant="ghost" className="px-4">
                Giriş Yap
              </Button>
            </Link>
            <Link href="/register">
              <Button className="gradient-primary px-6 hover:shadow-primary/40">
                Kayıt Ol
              </Button>
            </Link>
          </div>

          {/* Mobile menu button */}
          <div className="flex items-center md:hidden">
            <button
              onClick={() => setIsMenuOpen(!isMenuOpen)}
              className="inline-flex items-center justify-center p-2 rounded-md text-foreground/70 hover:text-foreground focus:outline-none"
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
              className="block px-3 py-2 rounded-md text-base font-medium text-foreground/90 hover:bg-accent hover:text-primary transition-colors"
              onClick={() => setIsMenuOpen(false)}
            >
              {item.name}
            </Link>
          ))}
          <div className="pt-4 border-t border-border/30 mt-2 space-y-2">
            <Link
              href="/login"
              className="block w-full px-4 py-2 text-center rounded-md bg-transparent border border-primary text-primary hover:bg-primary/10 transition-colors"
              onClick={() => setIsMenuOpen(false)}
            >
              Giriş Yap
            </Link>
            <Link
              href="/register"
              className="block w-full px-4 py-2 text-center rounded-md gradient-primary text-white hover:shadow-primary/40 transition-all"
              onClick={() => setIsMenuOpen(false)}
            >
              Kayıt Ol
            </Link>
          </div>
        </div>
      </div>
    </header>
  );
}
