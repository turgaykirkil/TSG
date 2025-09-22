"use client";

import { useEffect, useMemo, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { API_BASE_URL } from "@/config/constants";

export default function InvitePage() {
  const params = useSearchParams();
  const router = useRouter();
  const token = useMemo(() => (params?.get("token") || "").trim(), [params]);

  const [email, setEmail] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [password, setPassword] = useState<string>("");
  const [busy, setBusy] = useState<boolean>(false);

  useEffect(() => {
    const run = async () => {
      if (!token) {
        setError("Geçersiz davet bağlantısı (token eksik)");
        setLoading(false);
        return;
      }
      try {
        setLoading(true);
        setError(null);
        const res = await fetch(`${API_BASE_URL}/api/v1/auth/invite/accept`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ token }),
          credentials: 'include',
        });
        const json = await res.json();
        if (!res.ok) throw new Error(json?.detail || 'Davet doğrulanamadı');
        setEmail(json?.email || "");
      } catch (e: any) {
        setError(e?.message || 'Bilinmeyen hata');
      } finally {
        setLoading(false);
      }
    };
    run();
  }, [token]);

  const complete = async () => {
    try {
      setBusy(true);
      setError(null);
      const res = await fetch(`${API_BASE_URL}/api/v1/auth/invite/complete`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ token, password }),
        credentials: 'include',
      });
      const json = await res.json();
      if (!res.ok) throw new Error(json?.detail || 'Davet tamamlanamadı');
      // Cookie ayarlandı, dashboard'a yönlendir
      router.replace('/dashboard');
    } catch (e: any) {
      setError(e?.message || 'Bilinmeyen hata');
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="container mx-auto px-6 py-16 max-w-xl">
      <Card>
        <CardHeader>
          <CardTitle>Davet ile Katıl</CardTitle>
          <CardDescription>
            Sicilius, davetle üyelik sistemine sahiptir. Aşağıdan şifrenizi belirleyerek hesabınızı oluşturabilirsiniz.
          </CardDescription>
        </CardHeader>
        <CardContent>
          {loading ? (
            <div>Doğrulanıyor…</div>
          ) : error ? (
            <div className="text-sm text-red-600" role="alert">{error}</div>
          ) : (
            <div className="space-y-4">
              <div>
                <label className="block text-sm mb-1">E-posta</label>
                <Input value={email} readOnly aria-readonly />
              </div>
              <div>
                <label className="block text-sm mb-1">Şifre</label>
                <Input
                  type="password"
                  placeholder="En az 8 karakter"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                />
              </div>
              <div className="flex justify-end">
                <Button variant="gradient" onClick={complete} disabled={!password || busy}>
                  {busy ? 'Tamamlanıyor…' : 'Davet Tamamla ve Giriş Yap'}
                </Button>
              </div>
              <p className="text-xs text-slate-500">
                Hesabınız oluşturulduğunda, günlük 20 sorgu limiti uygulanır. Ayrıntılar için
                {' '}<a className="underline" href="/kullanici-sozlesmesi" target="_blank" rel="noreferrer">Kullanıcı Sözleşmesi</a>.
              </p>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
