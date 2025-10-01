"use client";

import React, { useEffect, useState } from "react";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { useToast } from "@/components/ui/use-toast";
import { API_BASE_URL, API_ENDPOINTS } from "@/config/constants";

export default function UserSettingsForm() {
  const { toast } = useToast();
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);

  const [form, setForm] = useState({
    registrationMode: "invite_only",
    allowedEmailDomains: "",
    blockedEmailDomains: "",
    defaultUserRole: "user",
    inviteEnabled: true as boolean,
    inviteTokenTtlHours: 72 as number | string,
    monthlyInviteLimitPerAdmin: 1 as number | string,
    dailyQueryLimit: 20 as number | string,
  });

  const onChange = (key: string) => (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const value = e.target.type === 'checkbox' ? (e.target as HTMLInputElement).checked : e.target.value;
    setForm((f) => ({ ...f, [key]: value }));
  };

  useEffect(() => {
    const run = async () => {
      setLoading(true);
      try {
        const res = await fetch(`${API_BASE_URL}${API_ENDPOINTS.SETTINGS.USER}`, { credentials: "include" });
        if (!res.ok) throw new Error("Ayarlar alınamadı");
        const data = await res.json();
        setForm({
          registrationMode: data.registration_mode || "invite_only",
          allowedEmailDomains: (data.allowed_email_domains || []).join(","),
          blockedEmailDomains: (data.blocked_email_domains || []).join(","),
          defaultUserRole: data.default_user_role || "user",
          inviteEnabled: Boolean(data.invite_enabled ?? true),
          inviteTokenTtlHours: String(data.invite_token_ttl_hours ?? 72),
          monthlyInviteLimitPerAdmin: String(data.monthly_invite_limit_per_admin ?? 1),
          dailyQueryLimit: String(data.daily_query_limit ?? 20),
        });
      } catch (e: any) {
        toast({ title: "Hata", description: e.message || String(e), variant: "destructive" });
      } finally {
        setLoading(false);
      }
    };
    run();
  }, [toast]);

  const save = async () => {
    setSaving(true);
    try {
      const payload: any = {
        registration_mode: form.registrationMode,
        allowed_email_domains: form.allowedEmailDomains.split(",").map(s => s.trim()).filter(Boolean),
        blocked_email_domains: form.blockedEmailDomains.split(",").map(s => s.trim()).filter(Boolean),
        default_user_role: form.defaultUserRole,
        invite_enabled: form.inviteEnabled,
        invite_token_ttl_hours: Number(form.inviteTokenTtlHours),
        monthly_invite_limit_per_admin: Number(form.monthlyInviteLimitPerAdmin),
        daily_query_limit: Number(form.dailyQueryLimit),
      };
      const res = await fetch(`${API_BASE_URL}${API_ENDPOINTS.SETTINGS.USER}`, {
        method: "PUT",
        credentials: "include",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      if (!res.ok) {
        const data = await res.json().catch(() => ({}));
        throw new Error(data?.detail || "Kaydetme başarısız");
      }
      toast({ title: "Ayarlar kaydedildi" });
    } catch (e: any) {
      toast({ title: "Hata", description: e.message || String(e), variant: "destructive" });
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="grid gap-4">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="grid gap-2">
          <Label htmlFor="registration_mode">Kayıt Modu</Label>
          <select id="registration_mode" className="h-10 rounded-md border bg-background px-3 text-sm" value={form.registrationMode} onChange={onChange("registrationMode")}>
            <option value="open">Açık Kayıt</option>
            <option value="invite_only">Sadece Davet</option>
          </select>
        </div>
        <div className="grid gap-2">
          <Label htmlFor="default_user_role">Varsayılan Rol</Label>
          <select id="default_user_role" className="h-10 rounded-md border bg-background px-3 text-sm" value={form.defaultUserRole} onChange={onChange("defaultUserRole")}>
            <option value="user">user</option>
            <option value="manager">manager</option>
            <option value="admin">admin</option>
          </select>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="grid gap-2">
          <Label htmlFor="allow_domains">Domain Allowlist (virgülle)</Label>
          <Input id="allow_domains" value={form.allowedEmailDomains} onChange={onChange("allowedEmailDomains")} placeholder="example.com, company.com" />
        </div>
        <div className="grid gap-2">
          <Label htmlFor="block_domains">Domain Denylist (virgülle)</Label>
          <Input id="block_domains" value={form.blockedEmailDomains} onChange={onChange("blockedEmailDomains")} placeholder="spam.com" />
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="grid gap-2">
          <div className="flex items-center gap-2">
            <input id="invite_enabled" type="checkbox" checked={form.inviteEnabled} onChange={onChange("inviteEnabled")} />
            <Label htmlFor="invite_enabled">Davet Sistemi Açık</Label>
          </div>
        </div>
        <div className="grid gap-2">
          <Label htmlFor="invite_token_ttl">Davet Geçerlilik (saat)</Label>
          <Input id="invite_token_ttl" value={form.inviteTokenTtlHours} onChange={onChange("inviteTokenTtlHours")} />
        </div>
        <div className="grid gap-2">
          <Label htmlFor="invite_limit">Aylık Admin Davet Limiti</Label>
          <Input id="invite_limit" value={form.monthlyInviteLimitPerAdmin} onChange={onChange("monthlyInviteLimitPerAdmin")} />
        </div>
      </div>

      <div className="grid gap-2">
        <Label htmlFor="daily_limit">Günlük Sorgu Limiti</Label>
        <Input id="daily_limit" value={form.dailyQueryLimit} onChange={onChange("dailyQueryLimit")} />
      </div>

      <div className="pt-2">
        <Button onClick={save} disabled={saving || loading}>{saving ? "Kaydediliyor..." : "Kaydet"}</Button>
      </div>
    </div>
  );
}
