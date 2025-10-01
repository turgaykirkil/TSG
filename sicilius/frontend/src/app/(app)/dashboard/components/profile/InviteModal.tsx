"use client";

import React from "react";
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { useAlert } from "@/contexts/AlertContext";
import { API_BASE_URL, API_ENDPOINTS } from "@/config/constants";

interface Props {
  open: boolean;
  onOpenChange: (open: boolean) => void;
}

type InviteItem = {
  token: string;
  invited_email: string;
  invited_month_key: string;
  accepted_at?: string | null;
};

export default function InviteModal({ open, onOpenChange }: Props) {
  const { showAlert } = useAlert();
  const [tab, setTab] = React.useState("list");

  const [list, setList] = React.useState<InviteItem[] | null>(null);
  const [loading, setLoading] = React.useState(false);

  const [pwdSubmitting, setPwdSubmitting] = React.useState(false);
  const [currentPwd, setCurrentPwd] = React.useState("");
  const [newPwd, setNewPwd] = React.useState("");

  const load = React.useCallback(async () => {
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE_URL}${API_ENDPOINTS.AUTH.INVITE_LIST_MY}`, { credentials: "include" });
      if (!res.ok) throw new Error("Davetler alınamadı");
      const data = await res.json();
      setList(data as InviteItem[]);
    } catch (e: any) {
      showAlert({ title: "Hata", description: e.message || String(e), variant: "destructive" });
    } finally {
      setLoading(false);
    }
  }, [showAlert]);

  React.useEffect(() => {
    if (open) load();
  }, [open, load]);

  const changePassword = async () => {
    if (!currentPwd || !newPwd) {
      showAlert({ title: "Alanlar gerekli", description: "Mevcut ve yeni şifreyi girin.", variant: "destructive" });
      return;
    }
    setPwdSubmitting(true);
    try {
      const res = await fetch(`${API_BASE_URL}${API_ENDPOINTS.AUTH.CHANGE_PASSWORD}`, {
        method: "POST",
        credentials: "include",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ current_password: currentPwd, new_password: newPwd }),
      });
      const data = await res.json().catch(() => ({}));
      if (!res.ok) throw new Error(data?.detail || "Şifre değiştirilemedi");
      showAlert({ title: "Şifre değiştirildi", variant: "success" });
      setCurrentPwd("");
      setNewPwd("");
    } catch (e: any) {
      showAlert({ title: "Hata", description: e.message || String(e), variant: "destructive" });
    } finally {
      setPwdSubmitting(false);
    }
  };

  const revoke = async (token: string) => {
    if (!confirm("Bu daveti iptal etmek istediğinize emin misiniz?")) return;
    try {
      const res = await fetch(`${API_BASE_URL}${API_ENDPOINTS.AUTH.INVITE_REVOKE(token)}`, {
        method: "DELETE",
        credentials: "include",
      });
      const data = await res.json().catch(() => ({}));
      if (!res.ok) throw new Error(data?.detail || "Davet iptal edilemedi");
      showAlert({ title: "Davet iptal edildi", variant: "success" });
      await load();
    } catch (e: any) {
      showAlert({ title: "Hata", description: e.message || String(e), variant: "destructive" });
    }
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-2xl">
        <DialogHeader>
          <DialogTitle>Profil</DialogTitle>
          <DialogDescription>Davetiye oluşturun veya oluşturduğunuz davetleri yönetin.</DialogDescription>
        </DialogHeader>

        <Tabs value={tab} onValueChange={setTab}>
          <TabsList className="mb-4">
            <TabsTrigger value="list">Davetlerim</TabsTrigger>
            <TabsTrigger value="password">Şifremi Değiştir</TabsTrigger>
          </TabsList>

          <TabsContent value="list">
            <div className="grid gap-3">
              {loading ? (
                <div className="text-sm text-muted-foreground">Yükleniyor...</div>
              ) : !list || list.length === 0 ? (
                <div className="text-sm text-muted-foreground">Henüz davet bulunmuyor.</div>
              ) : (
                <div className="space-y-2">
                  {list.map((it) => (
                    <div key={it.token} className="flex items-center justify-between rounded border p-2">
                      <div className="text-sm">
                        <div className="font-medium">{it.invited_email}</div>
                        <div className="text-xs text-muted-foreground">Ay: {it.invited_month_key} {it.accepted_at ? "• Kabul edildi" : "• Bekliyor"}</div>
                      </div>
                      <div className="flex items-center gap-2">
                        {!it.accepted_at && (
                          <Button variant="outline" onClick={() => revoke(it.token)}>İptal Et</Button>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </TabsContent>

          <TabsContent value="password">
            <div className="grid gap-3">
              <div className="grid gap-2">
                <Label htmlFor="current_pwd">Mevcut Şifre</Label>
                <Input id="current_pwd" type="password" value={currentPwd} onChange={(e) => setCurrentPwd(e.target.value)} />
              </div>
              <div className="grid gap-2">
                <Label htmlFor="new_pwd">Yeni Şifre</Label>
                <Input id="new_pwd" type="password" value={newPwd} onChange={(e) => setNewPwd(e.target.value)} />
                <p className="text-xs text-muted-foreground">En az 8 karakter. Büyük harf, sayı ve sembol önerilir.</p>
              </div>
              <div>
                <Button onClick={changePassword} disabled={pwdSubmitting}>{pwdSubmitting ? "Güncelleniyor..." : "Şifreyi Güncelle"}</Button>
              </div>
            </div>
          </TabsContent>
        </Tabs>
      </DialogContent>
    </Dialog>
  );
}
