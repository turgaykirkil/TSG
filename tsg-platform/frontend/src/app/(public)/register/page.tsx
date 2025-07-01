"use client";

import Link from 'next/link';
import { useSession } from 'next-auth/react';
import { useRouter } from 'next/navigation';
import { useEffect } from 'react';

import { UserAuthForm } from '@/components/auth/user-auth-form';
import AuthLayout from '@/layouts/AuthLayout';
import { Icons } from '@/components/icons';

export default function RegisterPage() {
  const { status } = useSession();
  const router = useRouter();

  useEffect(() => {
    if (status === 'authenticated') {
      router.push('/dashboard');
    }
  }, [status, router]);

  if (status === 'loading') {
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
          Hesap Oluştur
        </h1>
        <p className="text-balance text-sm text-muted-foreground">
          Başlamak için aşağıya bilgilerinizi girin.
        </p>
      </div>
      <UserAuthForm mode="register" />
      <p className="mt-4 text-center text-sm text-muted-foreground">
        Zaten bir hesabın var mı?{' '}
        <Link
          href="/login"
          className="font-semibold text-[#1e3a8a] hover:underline"
        >
          Giriş Yap
        </Link>
      </p>
    </AuthLayout>
  );
}

