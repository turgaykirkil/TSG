"use client";

import React from "react";
import EmailSettingsForm from "@/app/(app)/admin/components/settings/EmailSettingsForm";

export default function AdminEmailSettingsPage() {
  return (
    <div className="max-w-3xl">
      <h1 className="text-2xl font-bold mb-1">E-posta Ayarları</h1>
      <p className="text-sm text-muted-foreground mb-6">Oracle Email Delivery / SMTP bilgilerinizi burada yönetin.</p>

      <EmailSettingsForm />
    </div>
  );
}
