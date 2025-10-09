'use client';

import { useRouter } from 'next/navigation';
import { useEffect, useState } from 'react';
import { Button } from '@/components/ui/button';
import { useAuth } from '@/contexts/AuthContext';
import { FullScreenLoader } from '@/components/ui/loading-spinner';
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { useToast } from '@/components/ui/use-toast';
import { API_ENDPOINTS } from '@/config/constants';

export default function ProfilePage() {
  const router = useRouter();
  const { session, logout, isAuthenticated, loading } = useAuth();
  const user = session?.user;
  const [isLoggingOut, setIsLoggingOut] = useState(false);
  const { toast } = useToast();

  const [open, setOpen] = useState(false);
  const [currentPassword, setCurrentPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [newPassword2, setNewPassword2] = useState('');
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    if (!loading && !isAuthenticated) {
      router.push('/login?callbackUrl=/profile');
    }
  }, [isAuthenticated, loading, router]);

  if (loading) {
    return <FullScreenLoader />;
  }

  if (!isAuthenticated || !user) {
    return null; // Redirect will happen in useEffect
  }

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
          <p className="text-lg font-semibold">{user.email || '—'}</p>
        </div>
        {user.role && (
          <div>
            <h2 className="text-sm font-medium text-muted-foreground">Rol</h2>
            <p className="text-lg font-semibold capitalize">{user.role}</p>
          </div>
        )}
      </div>

      <div className="mt-8">
        <div className="flex items-center gap-3 flex-wrap">
          <Dialog open={open} onOpenChange={setOpen}>
            <DialogTrigger asChild>
              <Button variant="secondary">Şifremi Değiştir</Button>
            </DialogTrigger>
            <DialogContent>
              <DialogHeader>
                <DialogTitle>Şifre Değiştir</DialogTitle>
                <DialogDescription>
                  Mevcut şifrenizi doğrulayın ve yeni şifrenizi belirleyin.
                </DialogDescription>
              </DialogHeader>
              <div className="space-y-4 py-2">
                <div className="grid gap-2">
                  <Label htmlFor="current_password">Mevcut Şifre</Label>
                  <Input
                    id="current_password"
                    type="password"
                    value={currentPassword}
                    onChange={(e) => setCurrentPassword(e.target.value)}
                    placeholder="Mevcut şifreniz"
                  />
                </div>
                <div className="grid gap-2">
                  <Label htmlFor="new_password">Yeni Şifre</Label>
                  <Input
                    id="new_password"
                    type="password"
                    value={newPassword}
                    onChange={(e) => setNewPassword(e.target.value)}
                    placeholder="En az 8 karakter"
                  />
                </div>
                <div className="grid gap-2">
                  <Label htmlFor="new_password2">Yeni Şifre (Tekrar)</Label>
                  <Input
                    id="new_password2"
                    type="password"
                    value={newPassword2}
                    onChange={(e) => setNewPassword2(e.target.value)}
                    placeholder="Yeni şifrenizi tekrar yazın"
                  />
                </div>
              </div>
              <DialogFooter>
                <Button
                  variant="secondary"
                  onClick={() => setOpen(false)}
                  disabled={submitting}
                >
                  İptal
                </Button>
                <Button
                  onClick={async () => {
                    if (!currentPassword || !newPassword || !newPassword2) {
                      toast({ title: 'Eksik bilgi', description: 'Lütfen tüm alanları doldurun.', variant: 'destructive' });
                      return;
                    }
                    if (newPassword.length < 8) {
                      toast({ title: 'Zayıf şifre', description: 'Yeni şifre en az 8 karakter olmalı.', variant: 'destructive' });
                      return;
                    }
                    if (newPassword !== newPassword2) {
                      toast({ title: 'Eşleşmedi', description: 'Yeni şifre ve tekrarı uyuşmuyor.', variant: 'destructive' });
                      return;
                    }
                    try {
                      setSubmitting(true);
                      const res = await fetch(`${API_ENDPOINTS.AUTH.CHANGE_PASSWORD}`,
                        {
                          method: 'POST',
                          headers: { 'Content-Type': 'application/json' },
                          credentials: 'include',
                          body: JSON.stringify({ current_password: currentPassword, new_password: newPassword })
                        }
                      );
                      if (!res.ok) {
                        let detail = 'Şifre değiştirilemedi';
                        try { const data = await res.json(); detail = data?.detail || data?.msg || detail; } catch {}
                        toast({ title: 'Hata', description: String(detail), variant: 'destructive' });
                        return;
                      }
                      toast({ title: 'Başarılı', description: 'Şifreniz güncellendi.' });
                      setOpen(false);
                      setCurrentPassword('');
                      setNewPassword('');
                      setNewPassword2('');
                    } catch (e: any) {
                      toast({ title: 'Hata', description: 'Bağlantı sağlanamadı.', variant: 'destructive' });
                    } finally {
                      setSubmitting(false);
                    }
                  }}
                  disabled={submitting}
                >
                  {submitting ? 'Gönderiliyor...' : 'Şifreyi Güncelle'}
                </Button>
              </DialogFooter>
            </DialogContent>
          </Dialog>

          <Button 
            variant="destructive" 
            onClick={async () => {
              setIsLoggingOut(true);
              await logout();
              router.push('/login');
            }}
            disabled={isLoggingOut}
          >
            Çıkış Yap
          </Button>
        </div>
      </div>
    </div>
  );
}
