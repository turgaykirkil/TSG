"use client";

import { motion, Variants } from 'framer-motion';
import Link from 'next/link';
import { useSession } from 'next-auth/react';
import { useRouter } from 'next/navigation';
import { useEffect, useState } from 'react';
import { Icons } from '@/components/icons';
import { UserAuthForm } from '@/components/auth/user-auth-form';

export default function LoginPage() {
  const { status } = useSession();
  const router = useRouter();
  const [isMounted, setIsMounted] = useState(false);

  useEffect(() => {
    setIsMounted(true);
  }, []);

  useEffect(() => {
    if (status === 'authenticated') {
      router.push('/dashboard');
    }
  }, [status, router]);

  const containerVariants: Variants = {
    hidden: { opacity: 0, scale: 0.95 },
    visible: {
      opacity: 1,
      scale: 1,
      transition: {
        duration: 0.5,
      },
    },
  };

  if (!isMounted || status === 'loading') {
    return (
      <div className="flex h-screen w-screen items-center justify-center bg-gradient-to-br from-gray-900 via-gray-800 to-slate-900">
        <Icons.spinner className="h-10 w-10 animate-spin text-white" />
      </div>
    );
  }

  return (
    <div className="container relative flex h-screen w-screen flex-col items-center justify-center bg-gradient-to-br from-slate-50 to-gray-100">
      <motion.div
        className="mx-auto flex w-full max-w-md flex-col justify-center space-y-6 rounded-xl bg-white/60 p-10 shadow-xl backdrop-blur-lg border border-gray-200/50"
        variants={containerVariants}
        initial="hidden"
        animate="visible"
      >
        <div className="flex flex-col space-y-4 text-center">
          <div className="mx-auto mb-4">
            <Icons.logo className="h-12 w-12 text-gray-900" />
          </div>
          <h1 className="text-3xl font-bold tracking-tight text-gray-900">
            Sicilius&apos;a Hoş Geldiniz
          </h1>
          <p className="text-md text-gray-600">
            Hesabınıza erişmek için bilgilerinizi girin.
          </p>
        </div>
        <UserAuthForm mode="login" />
        <p className="px-8 text-center text-sm text-gray-600">
          <Link
            href="/register"
            className="text-primary hover:underline"
          >
            Hesabınız yok mu? Kayıt Olun
          </Link>
        </p>
      </motion.div>
    </div>
  );
}
