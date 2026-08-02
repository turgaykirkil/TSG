'use client';

import { useState } from 'react';
import { 
  Building2, 
  Key, 
  ShieldCheck, 
  Activity, 
  CreditCard, 
  Download, 
  PlusCircle, 
  Zap, 
  CheckCircle2, 
  Copy, 
  ExternalLink,
  Lock,
  Clock,
  HelpCircle,
  FileText
} from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';

export default function ClientPortalPage() {
  const [copiedKey, setCopiedKey] = useState(false);
  const [extraQuotaRequested, setExtraQuotaRequested] = useState(false);

  const customerInfo = {
    title: 'Garanti BBVA A.Ş.',
    vkn: '3880023451',
    packageName: 'Enterprise Paket',
    monthlyQuota: 50000,
    usedQuota: 14250,
    remainingQuota: 35750,
    renewDate: '2026-08-01',
    livePrefix: 'sk_live_garanti_982f...a12c',
    sandboxPrefix: 'sk_test_garanti_33ff...89ba',
  };

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
    setCopiedKey(true);
    setTimeout(() => setCopiedKey(false), 2000);
  };

  const usagePercent = Math.round((customerInfo.usedQuota / customerInfo.monthlyQuota) * 100);

  return (
    <div className="min-h-screen bg-background text-foreground py-10 px-4 md:px-8">
      <div className="max-w-6xl mx-auto space-y-8">
        {/* Header */}
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-border pb-6">
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-3xl font-bold tracking-tight">Sicilius B2B Müşteri Portalı</h1>
              <span className="bg-emerald-500/10 text-emerald-500 text-xs font-semibold px-2.5 py-0.5 rounded-full border border-emerald-500/20">
                Canlı Bağlantı
              </span>
            </div>
            <p className="text-muted-foreground text-sm mt-1">
              Hoş geldiniz, <strong className="text-foreground">{customerInfo.title}</strong> — VKN: {customerInfo.vkn}
            </p>
          </div>
          <div className="flex items-center gap-3">
            <a 
              href="https://docs.sicilius.com.tr" 
              target="_blank" 
              rel="noopener noreferrer"
              className="inline-flex items-center gap-2 text-sm text-primary hover:underline"
            >
              <FileText className="h-4 w-4" /> API Dokümantasyonu <ExternalLink className="h-3 w-3" />
            </a>
          </div>
        </div>

        {/* Quota & Usage Overview */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <Card className="bg-card/50 backdrop-blur border shadow-sm">
            <CardHeader className="pb-2">
              <CardTitle className="text-sm text-muted-foreground font-medium">Aylık Kota Durumu</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              <div className="flex justify-between items-baseline">
                <span className="text-3xl font-extrabold">{customerInfo.remainingQuota.toLocaleString()}</span>
                <span className="text-xs text-muted-foreground">Kalan Sorgu / {customerInfo.monthlyQuota.toLocaleString()}</span>
              </div>
              <div className="h-2 w-full bg-secondary rounded-full overflow-hidden">
                <div 
                  className="h-full bg-primary rounded-full transition-all"
                  style={{ width: `${usagePercent}%` }}
                />
              </div>
              <p className="text-xs text-muted-foreground">
                Kotanız <strong className="text-foreground">{customerInfo.renewDate}</strong> tarihinde otomatik yenilenecektir.
              </p>
            </CardContent>
          </Card>

          <Card className="bg-card/50 backdrop-blur border shadow-sm">
            <CardHeader className="pb-2">
              <CardTitle className="text-sm text-muted-foreground font-medium">Aktif Sözleşme Paketi</CardTitle>
            </CardHeader>
            <CardContent className="space-y-2">
              <div className="text-2xl font-bold text-primary">{customerInfo.packageName}</div>
              <p className="text-xs text-muted-foreground">
                Sınırsız Nexus Fraud sorgusu & Signal Engine Webhook desteği dahildir.
              </p>
              <Button 
                size="sm" 
                variant="outline" 
                onClick={() => setExtraQuotaRequested(true)}
                className="w-full mt-2 gap-1.5"
              >
                <Zap className="h-3.5 w-3.5 text-amber-500" /> İlave Kota / Paket Yükselt
              </Button>
              {extraQuotaRequested && (
                <p className="text-[11px] text-emerald-500 font-medium text-center">
                  ✓ Ek kota talebiniz müşteri temsilcinize iletildi.
                </p>
              )}
            </CardContent>
          </Card>

          <Card className="bg-card/50 backdrop-blur border shadow-sm">
            <CardHeader className="pb-2">
              <CardTitle className="text-sm text-muted-foreground font-medium">API Çalışma Saatleri</CardTitle>
            </CardHeader>
            <CardContent className="space-y-2">
              <div className="flex items-center gap-2 text-2xl font-bold text-emerald-500">
                <Clock className="h-5 w-5" /> 08:00 — 20:00 (TR)
              </div>
              <p className="text-xs text-muted-foreground">
                Gece suistimallerine karşı API sistemimiz mesai saatleri dışına kapalıdır.
              </p>
            </CardContent>
          </Card>
        </div>

        {/* API Keys Section */}
        <Card>
          <CardHeader>
            <CardTitle className="text-lg flex items-center gap-2">
              <Key className="h-5 w-5 text-primary" /> API Anahtarlarınız (HMAC Secrets)
            </CardTitle>
            <CardDescription className="text-xs">
              Sistemlerinizin Sicilius API'ye güvenli bağlanması için gereken HMAC imzalama anahtarlarınız.
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            {/* Live Key */}
            <div className="p-4 border rounded-lg bg-card/60 space-y-2">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <span className="bg-emerald-500/10 text-emerald-500 border border-emerald-500/20 text-xs font-bold px-2 py-0.5 rounded">
                    CANLI (LIVE) KEY
                  </span>
                  <span className="text-xs text-muted-foreground">https://api.sicilius.com.tr</span>
                </div>
                <Button size="sm" variant="outline" onClick={() => copyToClipboard(customerInfo.livePrefix)} className="h-8 gap-1 text-xs">
                  <Copy className="h-3 w-3" /> {copiedKey ? 'Kopyalandı!' : 'Key Kopyala'}
                </Button>
              </div>
              <code className="block p-2.5 bg-muted rounded font-mono text-sm border text-foreground">
                {customerInfo.livePrefix}
              </code>
              <p className="text-[11px] text-muted-foreground">
                * Bu key'in geçerlilik süresi 90 gündür. Süre dolmadan 14 gün önce e-posta ile bilgilendirilirsiniz.
              </p>
            </div>

            {/* Sandbox Key */}
            <div className="p-4 border rounded-lg bg-card/60 space-y-2">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <span className="bg-amber-500/10 text-amber-500 border border-amber-500/20 text-xs font-bold px-2 py-0.5 rounded">
                    SANDBOX (TEST) KEY
                  </span>
                  <span className="text-xs text-muted-foreground">https://test-api.sicilius.com.tr</span>
                </div>
                <Button size="sm" variant="outline" onClick={() => copyToClipboard(customerInfo.sandboxPrefix)} className="h-8 gap-1 text-xs">
                  <Copy className="h-3 w-3" /> Key Kopyala
                </Button>
              </div>
              <code className="block p-2.5 bg-muted rounded font-mono text-sm border text-foreground">
                {customerInfo.sandboxPrefix}
              </code>
              <p className="text-[11px] text-muted-foreground">
                * Test ortamında yalnızca izole edilmiş anonim veri kullanılır. Canlı veritabanı sorgulanmaz.
              </p>
            </div>
          </CardContent>
        </Card>

        {/* Invoices & Past Usage */}
        <Card>
          <CardHeader>
            <CardTitle className="text-lg flex items-center gap-2">
              <CreditCard className="h-5 w-5 text-primary" /> Fatura & Kullanım Dökümü
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="border rounded-lg overflow-x-auto">
              <table className="w-full text-sm text-left">
                <thead className="bg-muted text-xs uppercase text-muted-foreground border-b">
                  <tr>
                    <th className="p-3">Dönem</th>
                    <th className="p-3">Paket / Hizmet</th>
                    <th className="p-3">Toplam Çağrı</th>
                    <th className="p-3">Fatura Tutarı</th>
                    <th className="p-3 text-right">Fatura PDF</th>
                  </tr>
                </thead>
                <tbody className="divide-y border-b">
                  <tr>
                    <td className="p-3 font-medium">Haziran 2026</td>
                    <td className="p-3 text-muted-foreground">Enterprise Paket (50.000 Sorgu)</td>
                    <td className="p-3 font-mono">48,200</td>
                    <td className="p-3 font-semibold text-emerald-500">Ödendi</td>
                    <td className="p-3 text-right">
                      <Button size="sm" variant="ghost" className="h-7 text-xs">
                        <Download className="h-3.5 w-3.5 mr-1" /> İndir
                      </Button>
                    </td>
                  </tr>
                  <tr>
                    <td className="p-3 font-medium">Mayıs 2026</td>
                    <td className="p-3 text-muted-foreground">Enterprise Paket (50.000 Sorgu)</td>
                    <td className="p-3 font-mono">41,900</td>
                    <td className="p-3 font-semibold text-emerald-500">Ödendi</td>
                    <td className="p-3 text-right">
                      <Button size="sm" variant="ghost" className="h-7 text-xs">
                        <Download className="h-3.5 w-3.5 mr-1" /> İndir
                      </Button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
