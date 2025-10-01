"use client";

import React from 'react';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import EmailSettingsForm from '@/app/(app)/admin/components/settings/EmailSettingsForm';
import UserSettingsForm from '@/app/(app)/admin/components/settings/UserSettingsForm';
import { usePathname, useRouter, useSearchParams } from 'next/navigation';

export default function SettingsPage() {
  const router = useRouter();
  const pathname = usePathname();
  const params = useSearchParams();
  const tabParam = (params.get('tab') || 'general').toLowerCase();
  const [value, setValue] = React.useState<string>(['general','email','users','security','integrations'].includes(tabParam) ? tabParam : 'general');

  const setTab = (v: string) => {
    setValue(v);
    const sp = new URLSearchParams(params.toString());
    sp.set('tab', v);
    router.replace(`${pathname}?${sp.toString()}`);
  };

  return (
    <div className="max-w-5xl">
      <h1 className="text-2xl font-bold mb-1">Ayarlar</h1>
      <p className="text-sm text-muted-foreground mb-6">Uygulama genel ayarlarını yönetin.</p>

      <Tabs value={value} onValueChange={setTab}>
        <TabsList className="mb-4">
          <TabsTrigger value="general">Genel</TabsTrigger>
          <TabsTrigger value="email">E-posta</TabsTrigger>
          <TabsTrigger value="users">Kullanıcı Yönetimi</TabsTrigger>
          <TabsTrigger value="security">Güvenlik</TabsTrigger>
          <TabsTrigger value="integrations">Entegrasyonlar</TabsTrigger>
        </TabsList>

        <TabsContent value="general">
          <div className="text-sm text-muted-foreground">Genel ayarlar yakında.</div>
        </TabsContent>

        <TabsContent value="email">
          <EmailSettingsForm />
        </TabsContent>

        <TabsContent value="users">
          <UserSettingsForm />
        </TabsContent>

        <TabsContent value="security">
          <div className="text-sm text-muted-foreground">Güvenlik ayarları yakında.</div>
        </TabsContent>

        <TabsContent value="integrations">
          <div className="text-sm text-muted-foreground">Entegrasyon ayarları yakında.</div>
        </TabsContent>
      </Tabs>
    </div>
  );
}
