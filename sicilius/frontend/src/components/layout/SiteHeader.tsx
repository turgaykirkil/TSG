"use client";

import Link from 'next/link';
import { SiciliusLogo as Logo } from '@/components/icons/SiciliusLogo';
import { Button } from '@/components/ui/button';

export function SiteHeader() {
  return (
    <header className="fixed top-0 left-0 w-full bg-white/80 backdrop-blur-sm z-50 border-b border-gray-200">
      <div className="container mx-auto px-6 h-16 flex justify-between items-center">
        <Link href="/" className="flex items-center" aria-label="Sicilius Ana Sayfa">
          <Logo className="h-8 w-auto text-gray-900" />
        </Link>
        <nav className="hidden md:flex items-center space-x-8">
          <Link href="/#features" className="text-sm text-gray-600 hover:text-blue-600">Özellikler</Link>
          <Link href="/#why-sicilius" className="text-sm text-gray-600 hover:text-blue-600">Neden Sicilius?</Link>
          <Link href="/#policies" className="text-sm text-gray-600 hover:text-blue-600">İlkeler</Link>
          <Link href="/sss" className="text-sm text-gray-600 hover:text-blue-600">SSS</Link>
        </nav>
        <div className="flex items-center space-x-4">
          <Button asChild variant="gradient" className="px-4 py-2 text-sm font-medium rounded-full">
            <Link href="/login">Giriş Yap</Link>
          </Button>
        </div>
      </div>
    </header>
  );
}
