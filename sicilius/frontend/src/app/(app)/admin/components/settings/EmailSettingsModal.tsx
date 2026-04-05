"use client";

import React from "react";
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { useToast } from "@/components/ui/use-toast";

export type EmailSettings = {
  host: string;
  port: string;
  secure: "starttls" | "ssl";
  username: string;
  password: string;
  fromName: string;
  fromEmail: string;
  resetUrlBase: string;
};

interface Props {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  initial?: Partial<EmailSettings>;
}

export default function EmailSettingsModal({ open, onOpenChange, initial }: Props) {
  const { toast } = useToast();

  const [form, setForm] = React.useState<EmailSettings>({
    host: initial?.host ?? "",
    port: initial?.port ?? "587",
    secure: (initial?.secure as EmailSettings["secure"]) ?? "starttls",
    username: initial?.username ?? "",
    password: initial?.password ?? "",
    fromName: initial?.fromName ?? "Sicilius",
    fromEmail: initial?.fromEmail ?? "",
    resetUrlBase: initial?.resetUrlBase ?? "http://localhost:3000",
  });

  React.useEffect(() => {
    if (!open) return;
    setForm((f) => ({
      host: initial?.host ?? f.host,
      port: initial?.port ?? f.port,
      secure: (initial?.secure as EmailSettings["secure"]) ?? f.secure,
      username: initial?.username ?? f.username,
      password: initial?.password ?? f.password,
      fromName: initial?.fromName ?? f.fromName,
      fromEmail: initial?.fromEmail ?? f.fromEmail,
      resetUrlBase: initial?.resetUrlBase ?? f.resetUrlBase,
    }));
  }, [open, initial]);

  const onChange = (key: keyof EmailSettings) => (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const value = e.target.value;
    setForm((f) => ({ ...f, [key]: value }));
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-xl">
        <DialogHeader>
          <DialogTitle>E-posta Ayarları</DialogTitle>
          <DialogDescription>
            Oracle Email Delivery veya kullandığınız SMTP servis bilgilerini girin. Bu ayarlar lokal ve prod için aynıdır; sadece .env içerikleri farklı olabilir.
          </DialogDescription>
        </DialogHeader>

        <div className="grid gap-4 py-2">
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
              <Input id="smtp_username" value={form.username} onChange={onChange("username")} placeholder="SMTP kullanıcı adı" />
            </div>
          </div>

          <div className="grid gap-2">
            <Label htmlFor="smtp_password">SMTP Parola / Token</Label>
            <Input id="smtp_password" type="password" value={form.password} onChange={onChange("password")} placeholder="Uygulama parolası" />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="grid gap-2">
              <Label htmlFor="from_name">Gönderen Adı</Label>
              <Input id="from_name" value={form.fromName} onChange={onChange("fromName")} placeholder="Sicilius" />
            </div>
            <div className="grid gap-2">
              <Label htmlFor="from_email">Gönderen E-posta</Label>
              <Input id="from_email" value={form.fromEmail} onChange={onChange("fromEmail")} placeholder="no-reply@alanadiniz.com" />
            </div>
          </div>

          <div className="grid gap-2">
            <Label htmlFor="reset_base">Reset Linki Tabanı</Label>
            <Input id="reset_base" value={form.resetUrlBase} onChange={onChange("resetUrlBase")} placeholder="http://localhost:3000" />
          </div>
        </div>

        <DialogFooter>
          <Button
            type="button"
            variant="secondary"
            onClick={() => onOpenChange(false)}
          >
            Kapat
          </Button>
          <Button
            type="button"
            onClick={async () => {
              // TODO: Backend ayar kaydetme endpointi eklendiğinde buraya bağlanacak
              toast({ title: "Ayarlar kaydedildi", description: "Kaydetme uç noktası sonraki adımda etkinleştirilecek." });
              onOpenChange(false);
            }}
          >
            Kaydet
          </Button>
          <Button
            type="button"
            variant="outline"
            onClick={async () => {
              // TODO: Backend test e-postası uç noktası eklendiğinde çağrılacak
              toast({ title: "Test e-postası", description: "Test gönderimi bir sonraki adımda etkinleştirilecek." });
            }}
          >
            Test E-postası Gönder
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
