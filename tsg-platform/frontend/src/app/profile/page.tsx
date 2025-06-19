'use client';

import { useSession, signOut } from 'next-auth/react';
import { redirect } from 'next/navigation';
import { Button } from '@/components/ui/button';

export default function ProfilePage() {
  const { data: session, status } = useSession();

  if (status === 'loading') {
    return <div className="flex items-center justify-center h-screen">Yükleniyor...</div>;
  }

  if (!session) {
    redirect('/login?callbackUrl=/profile');
  }

  const { user } = session;

  return (
    <div className="container mx-auto px-4 py-8 max-w-2xl">
      <h1 className="text-3xl font-bold mb-6">Profil</h1>

      <div className="space-y-4 bg-card p-6 rounded-lg shadow">
        <div>
          <h2 className="text-sm font-medium text-muted-foreground">Ad Soyad</h2>
          <p className="text-lg font-semibold">{user.name || '—'}</p>
        </div>
        <div>
          <h2 className="text-sm font-medium text-muted-foreground">E-posta</h2>
          <p className="text-lg font-semibold">{user.email}</p>
        </div>
        {user.role && (
          <div>
            <h2 className="text-sm font-medium text-muted-foreground">Rol</h2>
            <p className="text-lg font-semibold capitalize">{user.role}</p>
          </div>
        )}
      </div>

      <div className="mt-8">
        <Button variant="destructive" onClick={() => signOut({ callbackUrl: '/login' })}>
          Çıkış Yap
        </Button>
      </div>
    </div>
  );
}
