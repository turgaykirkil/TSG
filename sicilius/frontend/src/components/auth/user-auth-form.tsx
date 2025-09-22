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

  const {
    register: registerField,
    handleSubmit,
    formState: { errors },
  } = useForm<RegisterFormData | LoginFormData>({
    resolver: zodResolver(isLogin ? loginSchema : registerSchema),
    defaultValues: isLogin
      ? { email: '', password: '' }
      : { name: '', email: '', password: '' },
  });

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
        </div>
      </form>
    </div>
  );
}
