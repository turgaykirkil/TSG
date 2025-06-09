import { type ReactNode } from 'react';
import { Header } from '@/components/Header';
import { Footer } from '@/components/Footer';
import { Toaster } from 'react-hot-toast';
import { useTheme } from '@/contexts/ThemeContext';
import { cn } from '@/lib/utils';

interface MainLayoutProps {
  children: ReactNode;
  className?: string;
  hideHeader?: boolean;
  hideFooter?: boolean;
  containerClassName?: string;
}

export function MainLayout({
  children, 
  className, 
  hideHeader = false,
  hideFooter = false,
  containerClassName = 'container mx-auto px-4 py-8',
}: MainLayoutProps) {
  const { theme } = useTheme();

  return (
    <div className={cn(
      'min-h-screen bg-background font-sans antialiased flex flex-col',
      'transition-colors duration-200',
      {
        'dark': theme === 'dark',
      },
      className
    )}>
      {!hideHeader && <Header />}
      
      <main className={cn("flex-1", {
        'pt-16': !hideHeader, // Header yüksekliği kadar padding ekler
      })}>
        <div className={containerClassName}>
          {children}
        </div>
      </main>
      
      {!hideFooter && <Footer />}
      
      {/* Toast Notifications */}
      <Toaster
        position="top-right"
        toastOptions={{
          duration: 5000,
          className: '!bg-background !text-foreground !border !border-border',
          success: {
            iconTheme: {
              primary: 'hsl(142.1 76.2% 36.3%)',
              secondary: 'hsl(0 0% 100%)',
            },
          },
          error: {
            iconTheme: {
              primary: 'hsl(0 84.2% 60.2%)',
              secondary: 'hsl(0 0% 100%)',
            },
          },
        }}
      />
    </div>
  );
}
