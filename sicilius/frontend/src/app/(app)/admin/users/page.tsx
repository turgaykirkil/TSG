"use client";

import React from "react";
import { API_ENDPOINTS } from "@/config/constants";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useToast } from "@/components/ui/use-toast";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle } from "@/components/ui/dialog";

type UserItem = {
  id: string;
  email: string;
  full_name?: string | null;
  is_active: boolean;
  role: "admin" | "manager" | "user";
};

export default function AdminUsersPage() {
  const { toast } = useToast();
  const [loading, setLoading] = React.useState(false);
  const [list, setList] = React.useState<UserItem[]>([]);
  const [q, setQ] = React.useState("");

  // Invite modal state
  const [inviteOpen, setInviteOpen] = React.useState(false);
  const [inviteEmail, setInviteEmail] = React.useState("");
  const [inviteSubmitting, setInviteSubmitting] = React.useState(false);
  const [inviteLink, setInviteLink] = React.useState<string | null>(null);

  const load = React.useCallback(async () => {
    setLoading(true);
    try {
      const res = await fetch(`${API_ENDPOINTS.USERS.BASE}?skip=0&limit=200`, { credentials: "include" });
      if (!res.ok) throw new Error("Kullanıcılar alınamadı");
      const data = await res.json();
      setList(data as UserItem[]);
    } catch (e: any) {
      toast({ title: "Hata", description: e.message || String(e), variant: "destructive" });
    } finally {
      setLoading(false);
    }
  }, [toast]);

  React.useEffect(() => { load(); }, [load]);

  const filtered = React.useMemo(() => {
    const term = q.trim().toLowerCase();
    if (!term) return list;
    return list.filter(u => (u.email?.toLowerCase().includes(term)) || (u.full_name || "").toLowerCase().includes(term));
  }, [q, list]);

  const updateUser = async (id: string, patch: Partial<UserItem>) => {
    try {
      const res = await fetch(`${API_ENDPOINTS.USERS.BASE}/${encodeURIComponent(id)}`, {
        method: "PUT",
        credentials: "include",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(patch),
      });
      const data = await res.json().catch(() => ({}));
      if (!res.ok) throw new Error(data?.detail || "Güncellenemedi");
      toast({ title: "Güncellendi" });
      await load();
    } catch (e: any) {
      toast({ title: "Hata", description: e.message || String(e), variant: "destructive" });
    }
  };

  const fetchInviteBase = async (): Promise<string | null> => {
    try {
      const res = await fetch(API_ENDPOINTS.SETTINGS.EMAIL, { credentials: "include" });
      if (!res.ok) return null;
      const data = await res.json();
      return data?.invite_url_base || null;
    } catch {
      return null;
    }
  };

  const createInvite = async () => {
    const email = inviteEmail.trim();
    if (!email) {
      toast({ title: "E-posta gerekli", description: "Lütfen davet etmek istediğiniz e-posta adresini girin.", variant: "destructive" });
      return;
    }
    setInviteSubmitting(true);
    try {
      const res = await fetch(API_ENDPOINTS.AUTH.INVITE_CREATE, {
        method: "POST",
        credentials: "include",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email }),
      });
      const data = await res.json().catch(() => ({}));
      if (!res.ok) throw new Error(data?.detail || "Davet oluşturulamadı");
      const token: string | undefined = data?.token;
      if (!token) throw new Error("Sunucudan token alınamadı");

      const base = await fetchInviteBase();
      const link = `${base || "http://localhost:3000/davet"}?token=${encodeURIComponent(token)}`;
      setInviteLink(link);
      toast({
        title: data?.email_sent !== false ? "Davet Oluşturuldu" : "Davet Oluşturuldu (E-posta Hatası)",
        description: data?.msg || "Davet bağlantısı başarıyla üretildi.",
        variant: data?.email_sent !== false ? "default" : "destructive"
      });
    } catch (e: any) {
      toast({ title: "Hata", description: e.message || String(e), variant: "destructive" });
    } finally {
      setInviteSubmitting(false);
    }
  };

  return (
    <div className="max-w-6xl">
      <h1 className="text-2xl font-bold mb-1">Kullanıcılar</h1>
      <p className="text-sm text-muted-foreground mb-4">Kullanıcıları görüntüleyin, rollerini değiştirin ve erişimlerini yönetin.</p>

      <div className="flex flex-col md:flex-row md:items-center gap-3 mb-4">
        <div className="grid gap-1 w-full md:w-auto">
          <Label htmlFor="q">Ara</Label>
          <Input id="q" placeholder="İsim ya da e-posta" value={q} onChange={(e) => setQ(e.target.value)} />
        </div>
        <div className="flex mt-6 md:mt-6 gap-2">
          <Button variant="outline" onClick={load} disabled={loading}>{loading ? "Yükleniyor..." : "Yenile"}</Button>
        </div>
        <div className="mt-2 md:mt-6 md:ml-auto w-full md:w-auto">
          <Button className="w-full md:w-auto" onClick={() => { setInviteOpen(true); setInviteLink(null); }}>Kullanıcı Davet Et</Button>
        </div>
      </div>

      <div className="rounded border overflow-x-auto">
        <Table className="min-w-[800px]">
          <TableHeader>
            <TableRow>
              <TableHead>E-posta</TableHead>
              <TableHead>Ad Soyad</TableHead>
              <TableHead>Rol</TableHead>
              <TableHead>Durum</TableHead>
              <TableHead className="text-right">İşlemler</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {filtered.map(u => (
              <TableRow key={u.id}>
                <TableCell className="font-medium">{u.email}</TableCell>
                <TableCell>{u.full_name || "—"}</TableCell>
                <TableCell>
                  <select
                    className="h-9 rounded-md border bg-background px-2 text-sm"
                    value={u.role}
                    onChange={(e) => updateUser(u.id, { role: e.target.value as UserItem["role"] })}
                  >
                    <option value="user">user</option>
                    <option value="manager">manager</option>
                    <option value="admin">admin</option>
                  </select>
                </TableCell>
                <TableCell>
                  {u.is_active ? <span className="text-green-600">Aktif</span> : <span className="text-red-600">Pasif</span>}
                </TableCell>
                <TableCell className="text-right space-x-2">
                  {u.is_active ? (
                    <Button variant="outline" onClick={() => updateUser(u.id, { is_active: false })}>Banla</Button>
                  ) : (
                    <Button variant="outline" onClick={() => updateUser(u.id, { is_active: true })}>Ban Kaldır</Button>
                  )}
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>

      {/* Invite Modal */}
      <Dialog open={inviteOpen} onOpenChange={(o) => { setInviteOpen(o); if (!o) { setInviteEmail(""); setInviteLink(null); } }}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Kullanıcı Davet Et</DialogTitle>
            <DialogDescription>Yeni bir kullanıcıyı e-posta ile davet edin. Davet bağlantısını kopyalayabilirsiniz.</DialogDescription>
          </DialogHeader>
          <div className="grid gap-3">
            <div className="grid gap-2">
              <Label htmlFor="invite_email">E-posta</Label>
              <Input id="invite_email" placeholder="kisi@ornek.com" value={inviteEmail} onChange={(e) => setInviteEmail(e.target.value)} />
            </div>
            <div className="flex gap-2">
              <Button onClick={createInvite} disabled={inviteSubmitting}>{inviteSubmitting ? "Oluşturuluyor..." : "Davet Oluştur"}</Button>
              <Button variant="outline" onClick={() => setInviteOpen(false)}>Kapat</Button>
            </div>
            {inviteLink && (
              <div className="grid gap-2">
                <Label>Oluşturulan Davet Bağlantısı</Label>
                <div className="flex items-center gap-2">
                  <Input readOnly value={inviteLink} />
                  <Button
                    variant="outline"
                    onClick={async () => {
                      try {
                        await navigator.clipboard.writeText(inviteLink);
                        toast({ title: "Kopyalandı" });
                      } catch {
                        toast({ title: "Kopyalanamadı", variant: "destructive" });
                      }
                    }}
                  >Kopyala</Button>
                </div>
              </div>
            )}
          </div>
        </DialogContent>
      </Dialog>
    </div>
  );
}
