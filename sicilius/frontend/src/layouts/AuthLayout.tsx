import React from 'react';
import { Icons } from '@/components/icons';

interface AuthLayoutProps {
  children: React.ReactNode;
}

export default function AuthLayout({ children }: AuthLayoutProps) {
  return (
    <div className="min-h-screen w-full lg:grid lg:grid-cols-2">
      <div className="relative hidden h-full flex-col bg-muted p-10 text-white lg:flex dark:border-r">
        {/* Background with gradient */}
        <div className="absolute inset-0 bg-gradient-to-br from-[#1e3a8a] to-[#1e3a8a]/90" />
        
        {/* Logo and Brand Name */}
        <div className="relative z-20 flex items-center text-lg font-medium">
          <Icons.logo className="mr-2 h-8 w-8" />
          Sicilius
        </div>
        
        {/* Main Quote/Message */}
        <div className="relative z-20 mt-auto">
          <blockquote className="space-y-2">
            <p className="text-lg">
              &ldquo;Verinin karmaşıklığını sadelikle çözüyoruz. Sicilius, iş zekanızın yeni merkezi.&rdquo;
            </p>
            <footer className="text-sm">Sicilius Ekibi</footer>
          </blockquote>
        </div>
      </div>
      <div className="flex items-center justify-center py-12 bg-background text-foreground">
        <div className="mx-auto grid w-[380px] gap-6 p-6 sm:p-0">
          {children}
        </div>
      </div>
    </div>
  );
}
