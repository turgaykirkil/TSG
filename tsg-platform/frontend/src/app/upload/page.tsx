'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import FileUploadSection from '@/app/admin/components/file-upload-section';
import { useAuth } from '@/contexts/AuthContext';

export default function UploadPage() {
  const router = useRouter();
  const { session, loading } = useAuth();
  const user = session?.user;

  useEffect(() => {
    if (!loading && !user) {
      router.push('/login?callbackUrl=/upload');
    }
  }, [user, loading, router]);

  if (loading) {
    return <div className="flex items-center justify-center h-screen">Yükleniyor...</div>;
  }

  if (!user) {
    return null; // Redirect will happen in useEffect
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-6">Dosya Yükle</h1>
      <FileUploadSection />
    </div>
  );
}
