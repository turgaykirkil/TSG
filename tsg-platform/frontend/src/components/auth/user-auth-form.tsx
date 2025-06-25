'use client';

import * as React from 'react';
import { useSearchParams, useRouter } from 'next/navigation';
import { zodResolver } from '@hookform/resolvers/zod';
import { signIn } from 'next-auth/react';
import { useForm } from 'react-hook-form';
import * as z from 'zod';

import { cn } from '@/lib/utils';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { toast } from '@/components/ui/use-toast';
import { Icons } from '@/components/icons';
import { useAuth } from '@/hooks/useAuth';

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
  const { register: registerUser } = useAuth();
  const router = useRouter();
  const searchParams = useSearchParams();

  const isLogin = mode === 'login';

  const { 
    register, 
    handleSubmit, 
    formState: { errors } 
  } = useForm<RegisterFormData | LoginFormData>({
      resolver: zodResolver(isLogin ? loginSchema : registerSchema),
      defaultValues: isLogin
        ? { email: '', password: '' }
        : { name: '', email: '', password: '' },
    });

  const [isLoading, setIsLoading] = React.useState<boolean>(false);

  const onSubmit = async (data: RegisterFormData | LoginFormData) => {
    setIsLoading(true);

    if (mode === 'register' && 'name' in data) {
      try {
        await registerUser(data.name, data.email, data.password);
        toast({
          title: 'Kayıt Başarılı',
          description: 'Giriş sayfasına yönlendiriliyorsunuz.',
        });
        router.push('/login');
      } catch (error) {
        toast({
          variant: 'destructive',
          title: 'Kayıt Başarısız',
          description: error instanceof Error ? error.message : 'Bir hata oluştu. Lütfen tekrar deneyin.',
        });
      }
    } else if (mode === 'login') {
      const result = await signIn('credentials', {
        redirect: false,
        email: data.email,
        password: (data as LoginFormData).password,
        callbackUrl: searchParams?.get('from') || '/dashboard',
      });

      if (result?.error) {
        toast({
          variant: 'destructive',
          title: 'Giriş Başarısız',
          description: 'E-posta veya şifreniz yanlış.',
        });
      } else {
        toast({
          title: 'Giriş Başarılı',
          description: 'Yönlendiriliyorsunuz...',
        });
        // We use a full page reload to ensure the session is updated and middleware redirects correctly.
        // This is more robust than router.push() which can cause a race condition with session updates.
        window.location.href = searchParams?.get('from') || '/dashboard';
      }
    }

    setIsLoading(false);
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
                disabled={isLoading}
                {...register('name')}
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
              E-posta
            </Label>
            <Input
              id="email"
              placeholder="ornek@eposta.com"
              type="email"
              autoCapitalize="none"
              autoComplete="email"
              autoCorrect="off"
              disabled={isLoading}
              {...register('email')}
            />
            {errors.email && (
              <p className="px-1 text-xs text-red-600">{errors.email.message}</p>
            )}
          </div>
          <div className="grid gap-1">
            <Label className="sr-only" htmlFor="password">
              Şifre
            </Label>
            <Input
              id="password"
              placeholder="Şifre"
              type="password"
              autoCapitalize="none"
              autoComplete="current-password"
              autoCorrect="off"
              disabled={isLoading}
              {...register('password')}
            />
            {errors.password && (
              <p className="px-1 text-xs text-red-600">
                {errors.password.message}
              </p>
            )}
          </div>
          <Button disabled={isLoading}>
            {isLoading && <Icons.spinner className="mr-2 h-4 w-4 animate-spin" />} 
            {mode === 'login' ? 'Giriş Yap' : 'Kayıt Ol'}
          </Button>
        </div>
      </form>


    </div>
  );
}
