'use client';

import FileUploadSection from '@/app/admin/components/file-upload-section';
import { useSession } from 'next-auth/react';
import { redirect } from 'next/navigation';

export default function UploadPage() {
  const { data: session, status } = useSession();

  if (status === 'loading') {
    return <div className="flex items-center justify-center h-screen">Yükleniyor...</div>;
  }

  if (!session) {
    redirect('/login?callbackUrl=/upload');
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-6">Dosya Yükle</h1>
      <FileUploadSection />
    </div>
  );
}
