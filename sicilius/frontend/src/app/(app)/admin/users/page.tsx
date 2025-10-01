"use client";

import React from "react";
import { API_BASE_URL, API_ENDPOINTS } from "@/config/constants";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useToast } from "@/components/ui/use-toast";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";

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

  const load = React.useCallback(async () => {
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE_URL}${API_ENDPOINTS.USERS.BASE}?skip=0&limit=200`, { credentials: "include" });
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
      const res = await fetch(`${API_BASE_URL}${API_ENDPOINTS.USERS.BASE}/${encodeURIComponent(id)}`, {
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

  return (
    <div className="max-w-6xl">
      <h1 className="text-2xl font-bold mb-1">Kullanıcılar</h1>
      <p className="text-sm text-muted-foreground mb-4">Kullanıcıları görüntüleyin, rollerini değiştirin ve erişimlerini yönetin.</p>

      <div className="flex items-center gap-3 mb-4">
        <div className="grid gap-1">
          <Label htmlFor="q">Ara</Label>
          <Input id="q" placeholder="İsim ya da e-posta" value={q} onChange={(e) => setQ(e.target.value)} />
        </div>
        <div className="mt-6">
          <Button variant="outline" onClick={load} disabled={loading}>{loading ? "Yükleniyor..." : "Yenile"}</Button>
        </div>
      </div>

      <div className="rounded border">
        <Table>
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
    </div>
  );
}
