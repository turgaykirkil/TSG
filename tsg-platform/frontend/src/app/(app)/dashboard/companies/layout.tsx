import type { ReactNode } from 'react';

type CompaniesLayoutProps = {
  children: ReactNode;
};

export default function CompaniesLayout({ children }: CompaniesLayoutProps) {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold tracking-tight">Şirketler</h1>
          <p className="text-muted-foreground">
            Şirket bilgilerini görüntüleyin ve yönetin
          </p>
        </div>
      </div>
      {children}
    </div>
  );
}
