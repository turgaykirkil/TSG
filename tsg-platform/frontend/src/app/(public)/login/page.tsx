"use client";

import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { useEffect } from 'react';

import { UserAuthForm } from '@/components/auth/user-auth-form';
import AuthLayout from '@/layouts/AuthLayout';
import { Icons } from '@/components/icons';
import { useAuth } from '@/contexts/AuthContext';

export default function LoginPage() {
  const { isAuthenticated, loading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (isAuthenticated) {
      router.push('/dashboard');
    }
  }, [isAuthenticated, router]);

  if (loading) {
    return (
      <div className="flex h-screen w-screen items-center justify-center bg-gray-900">
        <Icons.spinner className="h-10 w-10 animate-spin text-white" />
      </div>
    );
  }

  return (
    <AuthLayout>
      <div className="grid gap-2 text-center">
        <h1 className="text-3xl font-bold tracking-tight text-gray-900">
          Giriş Yap
        </h1>
        <p className="text-balance text-sm text-muted-foreground">
          Hesabınıza erişmek için bilgilerinizi girin.
        </p>
      </div>
      <UserAuthForm mode="login" />
      <p className="mt-4 text-center text-sm text-muted-foreground">
        Hesabın yok mu?{' '}
        <Link
          href="/register"
          className="font-semibold text-[#1e3a8a] hover:underline"
        >
          Kayıt Ol
        </Link>
      </p>
    </AuthLayout>
  );
}
