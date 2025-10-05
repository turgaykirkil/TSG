'use client';

import * as React from 'react';
import { zodResolver } from '@hookform/resolvers/zod';
import { useForm } from 'react-hook-form';
import * as z from 'zod';

import { cn } from '@/lib/utils';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Icons } from '@/components/icons';
import { useAuth } from '@/contexts/AuthContext';
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog';
import { useToast } from '@/components/ui/use-toast';
import { API_ENDPOINTS } from '@/config/constants';

interface UserAuthFormProps extends React.HTMLAttributes<HTMLDivElement> {
  mode: 'login' | 'register';
}

// Schema for registration
const registerSchema = z.object({
  name: z.string().min(2, { message: 'Ad en az 2 karakter olmalıdır.' }),
  email: z.string().email({ message: 'Lütfen geçerli bir e-posta adresi girin.' }),
  password: z.string().min(8, { message: 'Şifre en az 8 karakter olmalıdır.' }),
});

// Schema for login
const loginSchema = z.object({
  email: z.string().email({ message: 'Lütfen geçerli bir e-posta adresi girin.' }),
  password: z.string().min(1, { message: 'Şifre boş bırakılamaz.' }),
});

// Union type for form data
type RegisterFormData = z.infer<typeof registerSchema>;
type LoginFormData = z.infer<typeof loginSchema>;

export function UserAuthForm({ className, mode, ...props }: UserAuthFormProps) {
  const { login, register: registerUser, loading } = useAuth();
  const isLogin = mode === 'login';
  const { toast } = useToast();

  const {
    register: registerField,
    handleSubmit,
    formState: { errors },
    watch,
  } = useForm<RegisterFormData | LoginFormData>({
    resolver: zodResolver(isLogin ? loginSchema : registerSchema),
    defaultValues: isLogin
      ? { email: '', password: '' }
      : { name: '', email: '', password: '' },
  });

  // Forgot Password Modal state
  const [forgotOpen, setForgotOpen] = React.useState(false);
  const [forgotEmail, setForgotEmail] = React.useState('');
  const [fpSubmitting, setFpSubmitting] = React.useState(false);

  const onSubmit = async (formData: RegisterFormData | LoginFormData) => {
    if (isLogin) {
      const { email, password } = formData as LoginFormData;
      await login(email, password);
    } else {
      const { name, email, password } = formData as RegisterFormData;
      await registerUser({ name, email, password });
    }
  };

  return (
    <div className={cn('grid gap-6', className)} {...props}>
      <form onSubmit={handleSubmit(onSubmit)}>
        <div className="grid gap-4">
          {mode === 'register' && (
            <div className="grid gap-1">
              <Label className="sr-only" htmlFor="name">
                Ad Soyad
              </Label>
              <Input
                id="name"
                placeholder="Ad Soyad"
                type="text"
                autoCapitalize="words"
                autoComplete="name"
                autoCorrect="off"
                disabled={loading}
                {...registerField('name')}
              />
              {'name' in errors && errors.name && (
                <p className="px-1 text-xs text-red-600">
                  {errors.name.message}
                </p>
              )}
            </div>
          )}
          <div className="grid gap-1">
            <Label className="sr-only" htmlFor="email">
              Email
            </Label>
            <Input
              id="email"
              placeholder="name@example.com"
              type="email"
              autoCapitalize="none"
              autoComplete="email"
              autoCorrect="off"
              disabled={loading}
              {...registerField('email')}
            />
            {'email' in errors && errors.email && (
              <p className="px-1 text-xs text-red-600">
                {errors.email.message}
              </p>
            )}
          </div>
          <div className="grid gap-1">
            <Label className="sr-only" htmlFor="password">
              Şifre
            </Label>
            <Input
              id="password"
              placeholder="••••••••"
              type="password"
              autoComplete={isLogin ? 'current-password' : 'new-password'}
              disabled={loading}
              {...registerField('password')}
            />
            {'password' in errors && errors.password && (
              <p className="px-1 text-xs text-red-600">
                {errors.password.message}
              </p>
            )}
          </div>
          <Button disabled={loading} variant="gradient">
            {loading && (
              <Icons.spinner className="mr-2 h-4 w-4 animate-spin" />
            )}
            {isLogin ? 'Giriş Yap' : 'Kayıt Ol'}
          </Button>
          {isLogin && (
            <div className="mt-3 text-center">
              <Dialog open={forgotOpen} onOpenChange={(o) => { setForgotOpen(o); if (o) { try { const v = (watch('email') as string) || ''; setForgotEmail(v); } catch { /* noop */ } } }}>
                <DialogTrigger asChild>
                  <button type="button" className="text-sm font-medium text-primary hover:underline">
                    Şifremi Unuttum
                  </button>
                </DialogTrigger>
                <DialogContent>
                  <DialogHeader>
                    <DialogTitle>Şifre Sıfırlama</DialogTitle>
                    <DialogDescription>
                      E-posta adresinizi doğrulayın. Size şifre sıfırlama bağlantısı göndereceğiz.
                    </DialogDescription>
                  </DialogHeader>
                  <div className="grid gap-2 py-2">
                    <Label htmlFor="forgot_email">E-posta</Label>
                    <Input
                      id="forgot_email"
                      type="email"
                      value={forgotEmail}
                      onChange={(e) => setForgotEmail(e.target.value)}
                      placeholder="name@example.com"
                    />
                  </div>
                  <DialogFooter>
                    <Button
                      type="button"
                      variant="secondary"
                      onClick={() => setForgotOpen(false)}
                      disabled={fpSubmitting}
                    >
                      İptal
                    </Button>
                    <Button
                      type="button"
                      onClick={async () => {
                        if (!forgotEmail) {
                          toast({ title: 'E-posta gerekli', description: 'Lütfen e-posta adresinizi girin.', variant: 'destructive' });
                          return;
                        }
                        try {
                          setFpSubmitting(true);
                          const endpoint = API_ENDPOINTS.AUTH.FORGOT_PASSWORD(forgotEmail);
                          const res = await fetch(endpoint, {
                            method: 'POST',
                            credentials: 'include',
                          });
                          if (!res.ok) {
                            let detail = 'İstek başarısız';
                            try { const data = await res.json(); detail = data?.detail || data?.msg || detail; } catch {}
                            toast({ title: 'Hata', description: String(detail), variant: 'destructive' });
                            return;
                          }
                          toast({ title: 'E-posta gönderildi', description: 'Eğer kayıtlı iseniz, şifre sıfırlama talimatları gönderildi.' });
                          setForgotOpen(false);
                        } catch (e) {
                          toast({ title: 'Bağlantı hatası', description: 'Lütfen daha sonra tekrar deneyin.', variant: 'destructive' });
                        } finally {
                          setFpSubmitting(false);
                        }
                      }}
                      disabled={fpSubmitting}
                    >
                      {fpSubmitting ? 'Gönderiliyor...' : 'Gönder'}
                    </Button>
                  </DialogFooter>
                </DialogContent>
              </Dialog>
            </div>
          )}
        </div>
      </form>
    </div>
  );
}
