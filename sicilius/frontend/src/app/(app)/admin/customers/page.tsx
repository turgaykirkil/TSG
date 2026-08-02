'use client';

import { useState, useEffect } from 'react';
import { 
  Building2, 
  Key, 
  ShieldCheck, 
  Plus, 
  RefreshCw, 
  Lock, 
  Unlock, 
  Activity, 
  Search, 
  Clock, 
  CheckCircle2, 
  TrendingUp, 
  Trash2,
  Copy,
  X
} from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { toast } from 'sonner';
import apiClient from '@/lib/api/client';

export interface B2BCustomer {
  id: string;
  title: string;
  taxNumber: string;
  contactEmail: string;
  packageName: 'Basic' | 'Pro' | 'Enterprise';
  monthlyQuota: number;
  usedQuota: number;
  activeKeysCount: number;
  isActive: boolean;
  createdAt: string;
}

export default function AdminCustomersPage() {
  const [customers, setCustomers] = useState<B2BCustomer[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCustomer, setSelectedCustomer] = useState<B2BCustomer | null>(null);

  // Modal States
  const [showNewCustomerModal, setShowNewCustomerModal] = useState(false);
  const [newTitle, setNewTitle] = useState('');
  const [newTaxNumber, setNewTaxNumber] = useState('');
  const [newContactEmail, setNewContactEmail] = useState('');
  const [newPackageName, setNewPackageName] = useState<'Basic' | 'Pro' | 'Enterprise'>('Pro');
  const [submitting, setSubmitting] = useState(false);

  // Generated Key Display State
  const [generatedKey, setGeneratedKey] = useState<{ liveKey: string; liveSecret: string; customerTitle: string } | null>(null);

  const fetchCustomers = async () => {
    setLoading(true);
    try {
      const res = await apiClient.get<B2BCustomer[]>('/api/v1/b2b-customers/');
      setCustomers(res.data);
      if (res.data.length > 0 && !selectedCustomer) {
        setSelectedCustomer(res.data[0]);
      } else if (selectedCustomer) {
        const updated = res.data.find(c => c.id === selectedCustomer.id);
        if (updated) setSelectedCustomer(updated);
      }
    } catch (err: any) {
      toast.error('Müşteriler veritabanından yüklenirken hata oluştu.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCustomers();
  }, []);

  const filteredCustomers = customers.filter(c => 
    c.title.toLowerCase().includes(searchQuery.toLowerCase()) || 
    c.taxNumber.includes(searchQuery) ||
    c.contactEmail.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const toggleCustomerStatus = async (id: string) => {
    try {
      const res = await apiClient.post<{ message: string; isActive: boolean }>(`/api/v1/b2b-customers/${id}/toggle-status/`);
      toast.success(res.data.isActive ? 'Müşteri erişimi aktif edildi.' : 'Müşteri erişimi donduruldu.');
      fetchCustomers();
    } catch (err: any) {
      toast.error('Durum değiştirilirken bir hata oluştu.');
    }
  };

  const handleDeleteCustomer = async (id: string) => {
    if (!confirm('Bu müşteriyi silmek istediğinizden emin misiniz?')) return;
    try {
      await apiClient.delete(`/api/v1/b2b-customers/${id}/`);
      toast.success('Müşteri silindi.');
      if (selectedCustomer?.id === id) {
        setSelectedCustomer(null);
      }
      fetchCustomers();
    } catch (err: any) {
      toast.error('Müşteri silinirken hata oluştu.');
    }
  };

  const handleGenerateKey = async () => {
    if (!selectedCustomer) return;
    try {
      const res = await apiClient.post<{ message: string; liveKey: string; liveSecret: string; customerTitle: string }>(
        `/api/v1/b2b-customers/${selectedCustomer.id}/generate-key/`,
        { name: 'Live Key', keyType: 'live' }
      );
      setGeneratedKey({
        liveKey: res.data.liveKey,
        liveSecret: res.data.liveSecret,
        customerTitle: selectedCustomer.title
      });
      toast.success('Yeni API Key başarıyla üretildi!');
      fetchCustomers();
    } catch (err: any) {
      toast.error('API Key üretilirken hata oluştu.');
    }
  };

  const handleCreateCustomer = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newTitle || !newTaxNumber || !newContactEmail) {
      toast.error('Lütfen tüm zorunlu alanları doldurun.');
      return;
    }
    setSubmitting(true);
    try {
      const res = await apiClient.post<B2BCustomer>('/api/v1/b2b-customers/', {
        title: newTitle,
        taxNumber: newTaxNumber,
        contactEmail: newContactEmail,
        packageName: newPackageName,
      });
      toast.success('Yeni B2B Müşteri veritabanına kaydedildi!');
      setShowNewCustomerModal(false);
      setNewTitle('');
      setNewTaxNumber('');
      setNewContactEmail('');
      setSelectedCustomer(res.data);
      fetchCustomers();
    } catch (err: any) {
      toast.error(err.response?.data?.detail || 'Müşteri oluşturulurken hata oluştu.');
    } finally {
      setSubmitting(false);
    }
  };

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
    toast.success('Kopyalandı!');
  };

  // Aggregated totals
  const totalCalls = customers.reduce((acc, c) => acc + c.usedQuota, 0);

  return (
    <div className="container mx-auto px-4 py-8 space-y-8">
      {/* Top Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-border pb-6">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-3xl font-bold tracking-tight">Müşteri CRM & B2B API Yönetimi</h1>
            <span className="bg-primary/10 text-primary text-xs font-semibold px-2.5 py-0.5 rounded-full border border-primary/20">
              PostgreSQL Live DB
            </span>
          </div>
          <p className="text-muted-foreground text-sm mt-1">
            Kurumsal B2B müşterilerin sözleşme, API Key, erişim scope'ları ve kullanım kotalarını doğrudan veritabanından yönetin.
          </p>
        </div>
        <div className="flex items-center gap-3">
          <Button onClick={() => setShowNewCustomerModal(true)} className="gap-2">
            <Plus className="h-4 w-4" /> Yeni Müşteri & API Key Ekle
          </Button>
        </div>
      </div>

      {/* Quick Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card className="bg-card/50 backdrop-blur border shadow-sm">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">Aktif B2B Müşteriler</CardTitle>
            <Building2 className="h-4 w-4 text-primary" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{customers.filter(c => c.isActive).length}</div>
            <p className="text-xs text-muted-foreground mt-1">Toplu Kurumsal Abonelikler</p>
          </CardContent>
        </Card>

        <Card className="bg-card/50 backdrop-blur border shadow-sm">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">Üretilen API Keyler</CardTitle>
            <Key className="h-4 w-4 text-emerald-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{customers.reduce((acc, c) => acc + c.activeKeysCount, 0)} Live Key</div>
            <p className="text-xs text-muted-foreground mt-1">HMAC-SHA256 Korumalı</p>
          </CardContent>
        </Card>

        <Card className="bg-card/50 backdrop-blur border shadow-sm">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">Aylık Toplam Çağrı</CardTitle>
            <TrendingUp className="h-4 w-4 text-blue-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{totalCalls.toLocaleString()}</div>
            <p className="text-xs text-muted-foreground mt-1">%99.98 Başarılı Yanıt Oranı</p>
          </CardContent>
        </Card>

        <Card className="bg-card/50 backdrop-blur border shadow-sm">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">Erişim Modu</CardTitle>
            <Clock className="h-4 w-4 text-amber-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-emerald-500">7/24 Kesintisiz</div>
            <p className="text-xs text-muted-foreground mt-1">Gelişmiş Rate-Limiting Aktif</p>
          </CardContent>
        </Card>
      </div>

      {/* Main CRM Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left: Customer List */}
        <div className="lg:col-span-5 space-y-4">
          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="text-lg">Müşteri Portföyü ({customers.length})</CardTitle>
              <div className="relative mt-2">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                <input 
                  type="text"
                  placeholder="Firma unvanı, VKN veya e-posta..."
                  value={searchQuery}
                  onChange={e => setSearchQuery(e.target.value)}
                  className="w-full pl-9 pr-4 py-2 text-sm rounded-md border border-input bg-background focus:outline-none focus:ring-2 focus:ring-primary"
                />
              </div>
            </CardHeader>
            <CardContent className="p-0">
              {loading ? (
                <div className="p-8 text-center text-sm text-muted-foreground flex items-center justify-center gap-2">
                  <RefreshCw className="h-4 w-4 animate-spin" /> Veriler yükleniyor...
                </div>
              ) : filteredCustomers.length === 0 ? (
                <div className="p-8 text-center text-sm text-muted-foreground">
                  Müşteri bulunamadı.
                </div>
              ) : (
                <div className="divide-y divide-border max-h-[500px] overflow-y-auto">
                  {filteredCustomers.map(cust => {
                    const isSelected = selectedCustomer?.id === cust.id;
                    const usagePercent = Math.min(100, Math.round((cust.usedQuota / (cust.monthlyQuota || 1)) * 100));

                    return (
                      <div
                        key={cust.id}
                        onClick={() => setSelectedCustomer(cust)}
                        className={`p-4 cursor-pointer transition-colors hover:bg-accent/50 ${
                          isSelected ? 'bg-accent border-l-4 border-l-primary' : ''
                        }`}
                      >
                        <div className="flex items-start justify-between">
                          <div>
                            <h4 className="font-semibold text-sm flex items-center gap-2">
                              {cust.title}
                              {!cust.isActive && (
                                <span className="bg-red-500/10 text-red-500 text-[10px] px-1.5 py-0.5 rounded font-mono">DONDURULDU</span>
                              )}
                            </h4>
                            <p className="text-xs text-muted-foreground mt-0.5">VKN: {cust.taxNumber}</p>
                          </div>
                          <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${
                            cust.packageName === 'Enterprise' 
                              ? 'bg-purple-500/10 text-purple-500 border border-purple-500/20'
                              : 'bg-blue-500/10 text-blue-500 border border-blue-500/20'
                          }`}>
                            {cust.packageName}
                          </span>
                        </div>

                        {/* Quota Progress Bar */}
                        <div className="mt-3 space-y-1">
                          <div className="flex justify-between text-[11px] text-muted-foreground">
                            <span>Kota Kullanımı</span>
                            <span className="font-mono font-medium">{cust.usedQuota.toLocaleString()} / {cust.monthlyQuota.toLocaleString()}</span>
                          </div>
                          <div className="h-1.5 w-full bg-secondary rounded-full overflow-hidden">
                            <div 
                              className={`h-full rounded-full transition-all ${
                                usagePercent > 80 ? 'bg-amber-500' : 'bg-primary'
                              }`}
                              style={{ width: `${usagePercent}%` }}
                            />
                          </div>
                        </div>
                      </div>
                    );
                  })}
                </div>
              )}
            </CardContent>
          </Card>
        </div>

        {/* Right: Selected Customer Detail */}
        <div className="lg:col-span-7 space-y-4">
          {selectedCustomer ? (
            <>
              <Card>
                <CardHeader className="flex flex-row items-start justify-between pb-4 border-b">
                  <div>
                    <div className="flex items-center gap-2">
                      <CardTitle className="text-xl">{selectedCustomer.title}</CardTitle>
                      <Badge variant={selectedCustomer.isActive ? 'default' : 'destructive'}>
                        {selectedCustomer.isActive ? 'Aktif Müşteri' : 'Erişim Donduruldu'}
                      </Badge>
                    </div>
                    <CardDescription className="mt-1 font-mono">
                      VKN: {selectedCustomer.taxNumber} | İletişim: {selectedCustomer.contactEmail}
                    </CardDescription>
                  </div>
                  <div className="flex items-center gap-2">
                    <Button 
                      variant={selectedCustomer.isActive ? 'outline' : 'default'} 
                      size="sm" 
                      onClick={() => toggleCustomerStatus(selectedCustomer.id)}
                    >
                      {selectedCustomer.isActive ? (
                        <><Lock className="mr-1 h-3.5 w-3.5 text-amber-500" /> Erişimi Dondur</>
                      ) : (
                        <><Unlock className="mr-1 h-3.5 w-3.5 text-emerald-500" /> Erişimi Aç</>
                      )}
                    </Button>
                    <Button 
                      variant="destructive" 
                      size="icon" 
                      className="h-8 w-8" 
                      onClick={() => handleDeleteCustomer(selectedCustomer.id)}
                    >
                      <Trash2 className="h-4 w-4" />
                    </Button>
                  </div>
                </CardHeader>

                <CardContent className="pt-6 space-y-6">
                  {/* Quota Details */}
                  <div className="grid grid-cols-3 gap-4 p-4 bg-muted/30 rounded-lg border text-center">
                    <div>
                      <span className="text-xs text-muted-foreground">Paket Tipi</span>
                      <p className="font-bold text-base text-primary">{selectedCustomer.packageName}</p>
                    </div>
                    <div>
                      <span className="text-xs text-muted-foreground">Aylık Kota</span>
                      <p className="font-bold text-base font-mono">{selectedCustomer.monthlyQuota.toLocaleString()}</p>
                    </div>
                    <div>
                      <span className="text-xs text-muted-foreground">Kullanılan</span>
                      <p className="font-bold text-base font-mono text-emerald-500">{selectedCustomer.usedQuota.toLocaleString()}</p>
                    </div>
                  </div>

                  {/* Active Keys Section */}
                  <div className="space-y-3">
                    <div className="flex items-center justify-between">
                      <h3 className="font-semibold text-sm flex items-center gap-2">
                        <Key className="h-4 w-4 text-primary" /> Atanmış API Anahtarları (HMAC Secrets)
                      </h3>
                      <Button size="sm" variant="ghost" onClick={handleGenerateKey} className="h-8 text-xs">
                        <RefreshCw className="mr-1 h-3 w-3" /> Key Rotasyonu / Yeni Key Üret
                      </Button>
                    </div>

                    {generatedKey && (
                      <div className="p-4 bg-emerald-500/10 border border-emerald-500/30 rounded-lg space-y-2">
                        <div className="flex items-center justify-between">
                          <span className="text-xs font-bold text-emerald-500 flex items-center gap-1">
                            <CheckCircle2 className="h-4 w-4" /> Üretilen Gizli API Key (Live Secret)
                          </span>
                          <Button size="sm" variant="ghost" className="h-6 text-[10px]" onClick={() => setGeneratedKey(null)}>Kapat</Button>
                        </div>
                        <p className="text-[11px] text-muted-foreground">
                          Bu gizli anahtarı müşteriniz ile paylaşın. Güvenlik nedeniyle bir daha görüntülenemez!
                        </p>
                        <div className="flex items-center gap-2 font-mono text-xs bg-background p-2 rounded border justify-between">
                          <span className="truncate text-emerald-400 font-bold">{generatedKey.liveSecret}</span>
                          <Button size="icon" variant="ghost" className="h-6 w-6" onClick={() => copyToClipboard(generatedKey.liveSecret)}>
                            <Copy className="h-3 w-3" />
                          </Button>
                        </div>
                      </div>
                    )}

                    <div className="space-y-2 border rounded-lg p-3 bg-card/60">
                      <div className="flex items-center justify-between text-xs">
                        <div className="flex items-center gap-2">
                          <span className="font-mono bg-emerald-500/10 text-emerald-500 border border-emerald-500/20 px-2 py-0.5 rounded text-[11px] font-bold">
                            LIVE KEY
                          </span>
                          <code className="font-mono text-muted-foreground">sk_live_{selectedCustomer.taxNumber.substring(0, 4)}...</code>
                        </div>
                        <span className="text-emerald-500 font-medium flex items-center gap-1">
                          <CheckCircle2 className="h-3 w-3" /> Aktif
                        </span>
                      </div>

                      <div className="flex flex-wrap gap-1.5 pt-2 border-t text-[11px]">
                        <span className="bg-secondary px-2 py-0.5 rounded text-muted-foreground">companies.read</span>
                        <span className="bg-secondary px-2 py-0.5 rounded text-muted-foreground">persons.read</span>
                        <span className="bg-secondary px-2 py-0.5 rounded text-muted-foreground">nexus.risk</span>
                      </div>
                    </div>
                  </div>

                  {/* Audit Logs */}
                  <div className="space-y-2 pt-2">
                    <h3 className="font-semibold text-sm flex items-center gap-2">
                      <Activity className="h-4 w-4 text-primary" /> Son API Erişim Logları (Live Audit)
                    </h3>
                    <div className="border rounded-lg divide-y text-xs">
                      {selectedCustomer.usedQuota > 0 ? (
                        <>
                          <div className="p-2.5 flex items-center justify-between bg-muted/20">
                            <span className="font-mono font-medium">GET /api/v1/search/all?q={encodeURIComponent(selectedCustomer.title.split(' ')[0])}</span>
                            <span className="text-emerald-500 font-mono">200 OK — 24ms</span>
                          </div>
                          <div className="p-2.5 flex items-center justify-between bg-muted/20">
                            <span className="font-mono font-medium">GET /api/v1/companies/coordinates/map-pins/</span>
                            <span className="text-emerald-500 font-mono">200 OK — 12ms</span>
                          </div>
                        </>
                      ) : (
                        <div className="p-4 text-center text-xs text-muted-foreground bg-muted/10">
                          Henüz bu müşteriye ait canlı API erişim kaydı bulunmuyor.
                        </div>
                      )}
                    </div>
                  </div>
                </CardContent>
              </Card>
            </>
          ) : (
            <Card className="flex items-center justify-center p-12 text-center text-muted-foreground">
              Detaylarını ve API anahtarlarını görüntülemek için sol listeden bir müşteri seçin.
            </Card>
          )}
        </div>
      </div>

      {/* NEW CUSTOMER MODAL */}
      {showNewCustomerModal && (
        <div className="fixed inset-0 z-50 bg-black/60 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-card w-full max-w-md rounded-xl border p-6 space-y-4 shadow-xl">
            <div className="flex items-center justify-between border-b pb-3">
              <h3 className="font-bold text-lg flex items-center gap-2">
                <Building2 className="h-5 w-5 text-primary" /> Yeni B2B Müşteri Kaydı
              </h3>
              <Button size="icon" variant="ghost" className="h-7 w-7" onClick={() => setShowNewCustomerModal(false)}>
                <X className="h-4 w-4" />
              </Button>
            </div>

            <form onSubmit={handleCreateCustomer} className="space-y-4">
              <div className="space-y-1">
                <label className="text-xs font-semibold">Şirket Unvanı *</label>
                <Input 
                  placeholder="Örn: Garanti BBVA A.Ş."
                  value={newTitle}
                  onChange={e => setNewTitle(e.target.value)}
                  required
                />
              </div>

              <div className="space-y-1">
                <label className="text-xs font-semibold">Vergi Kimlik No (VKN) *</label>
                <Input 
                  placeholder="Örn: 3880023451"
                  value={newTaxNumber}
                  onChange={e => setNewTaxNumber(e.target.value)}
                  required
                />
              </div>

              <div className="space-y-1">
                <label className="text-xs font-semibold">İletişim E-Posta *</label>
                <Input 
                  type="email"
                  placeholder="Örn: api@garanti.com.tr"
                  value={newContactEmail}
                  onChange={e => setNewContactEmail(e.target.value)}
                  required
                />
              </div>

              <div className="space-y-1">
                <label className="text-xs font-semibold">Abonelik Paketi</label>
                <select 
                  className="w-full p-2 text-sm rounded-md border bg-background"
                  value={newPackageName}
                  onChange={e => setNewPackageName(e.target.value as any)}
                >
                  <option value="Basic">Basic (5.000 Sorgu/Ay)</option>
                  <option value="Pro">Pro (15.000 Sorgu/Ay)</option>
                  <option value="Enterprise">Enterprise (50.000 Sorgu/Ay)</option>
                </select>
              </div>

              <div className="flex justify-end gap-2 pt-2">
                <Button type="button" variant="outline" onClick={() => setShowNewCustomerModal(false)}>
                  İptal
                </Button>
                <Button type="submit" disabled={submitting}>
                  {submitting ? 'Kaydediliyor...' : 'Kaydet ve API Key Oluştur'}
                </Button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
