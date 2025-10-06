"use client";

import React, { useEffect, useState } from "react";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { useToast } from "@/components/ui/use-toast";
import { API_ENDPOINTS } from "@/config/constants";

export default function EmailSettingsForm() {
  const { toast } = useToast();
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [testing, setTesting] = useState(false);

  const [form, setForm] = useState({
    host: "",
    port: "587",
    secure: "starttls",
    username: "",
    password: "",
    fromName: "Sicilius",
    fromEmail: "",
    resetUrlBase: "http://localhost:3000",
    inviteUrlBase: "http://localhost:3000/davet/",
  });

  const onChange = (key: string) => (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    setForm((f) => ({ ...f, [key]: e.target.value }));
  };

  useEffect(() => {
    const run = async () => {
      setLoading(true);
      try {
        const res = await fetch(API_ENDPOINTS.SETTINGS.EMAIL, { credentials: "include" });
        if (!res.ok) throw new Error("Ayarlar alınamadı");
        const data = await res.json();
        setForm((f) => ({
          ...f,
          host: data.host || "",
          port: String(data.port ?? "587"),
          secure: data.secure || "starttls",
          username: data.username || "",
          fromName: data.from_name || data.fromName || "Sicilius",
          fromEmail: data.from_email || data.fromEmail || "",
          resetUrlBase: data.reset_url_base || data.resetUrlBase || "http://localhost:3000",
          inviteUrlBase: data.invite_url_base || data.inviteUrlBase || "http://localhost:3000/davet/",
        }));
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
      const payload = {
        host: form.host,
        port: Number(form.port),
        secure: form.secure as "starttls" | "ssl",
        username: form.username,
        password: form.password || undefined,
        from_name: form.fromName,
        from_email: form.fromEmail,
        reset_url_base: form.resetUrlBase,
        invite_url_base: form.inviteUrlBase,
      } as any;
      const res = await fetch(API_ENDPOINTS.SETTINGS.EMAIL, {
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
      setForm((f) => ({ ...f, password: "" }));
    } catch (e: any) {
      toast({ title: "Hata", description: e.message || String(e), variant: "destructive" });
    } finally {
      setSaving(false);
    }
  };

  const sendTest = async () => {
    const to = prompt("Test e-postası adresi:", form.fromEmail || "");
    if (!to) return;
    setTesting(true);
    try {
      const res = await fetch(API_ENDPOINTS.SETTINGS.EMAIL_TEST, {
        method: "POST",
        credentials: "include",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ to }),
      });
      if (!res.ok) {
        const data = await res.json().catch(() => ({}));
        throw new Error(data?.detail || "Test e-postası gönderilemedi");
      }
      toast({ title: "Test e-postası gönderildi" });
    } catch (e: any) {
      toast({ title: "Hata", description: e.message || String(e), variant: "destructive" });
    } finally {
      setTesting(false);
    }
  };

  return (
    <div className="grid gap-4">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="grid gap-2">
          <Label htmlFor="smtp_host">SMTP Sunucusu</Label>
          <Input id="smtp_host" value={form.host} onChange={onChange("host")} placeholder="smtp.email.<region>.oci.oraclecloud.com" />
        </div>
        <div className="grid gap-2">
          <Label htmlFor="smtp_port">Port</Label>
          <Input id="smtp_port" value={form.port} onChange={onChange("port")} placeholder="587" />
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="grid gap-2">
          <Label htmlFor="smtp_secure">Güvenlik</Label>
          <select
            id="smtp_secure"
            className="h-10 rounded-md border bg-background px-3 text-sm"
            value={form.secure}
            onChange={onChange("secure")}
          >
            <option value="starttls">STARTTLS (587)</option>
            <option value="ssl">SSL/TLS (465)</option>
          </select>
        </div>
        <div className="grid gap-2">
          <Label htmlFor="smtp_username">SMTP Kullanıcı Adı</Label>
          <Input id="smtp_username" value={form.username} onChange={onChange("username")} />
        </div>
      </div>

      <div className="grid gap-2">
        <Label htmlFor="smtp_password">SMTP Parola / Token</Label>
        <Input id="smtp_password" type="password" value={form.password} onChange={onChange("password")} />
        <p className="text-xs text-muted-foreground">Boş bırakırsanız mevcut parola korunur.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="grid gap-2">
          <Label htmlFor="from_name">Gönderen Adı</Label>
          <Input id="from_name" value={form.fromName} onChange={onChange("fromName")} />
        </div>
        <div className="grid gap-2">
          <Label htmlFor="from_email">Gönderen E-posta</Label>
          <Input id="from_email" value={form.fromEmail} onChange={onChange("fromEmail")} />
        </div>
      </div>

      <div className="grid gap-2">
        <Label htmlFor="reset_base">Reset Linki Tabanı</Label>
        <Input id="reset_base" value={form.resetUrlBase} onChange={onChange("resetUrlBase")} placeholder="http://localhost:3000" />
      </div>

      <div className="grid gap-2">
        <Label htmlFor="invite_base">Davet Linki Tabanı</Label>
        <Input id="invite_base" value={form.inviteUrlBase} onChange={onChange("inviteUrlBase")} placeholder="https://sicilius.com.tr/davet/" />
      </div>

      <div className="flex gap-3 pt-2">
        <Button onClick={save} disabled={saving || loading}>
          {saving ? "Kaydediliyor..." : "Kaydet"}
        </Button>
        <Button variant="outline" onClick={sendTest} disabled={testing || loading}>
          {testing ? "Gönderiliyor..." : "Test E-postası Gönder"}
        </Button>
      </div>
    </div>
  );
}
