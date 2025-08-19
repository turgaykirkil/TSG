"use client";

import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { useCompanyDetail } from '@/hooks/useCompanyDetail';

interface CompanyDetailModalProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  companyId?: string;
}

export default function CompanyDetailModal({ open, onOpenChange, companyId }: CompanyDetailModalProps) {
  const { data, isFetching, isError, error } = useCompanyDetail(companyId, open);
  const company: any = data?.company ?? null;

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-3xl">
        <DialogHeader>
          <DialogTitle>{company?.firma_unvani || company?.unvan || 'Şirket Detayı'}</DialogTitle>
          <DialogDescription>
            Şirket ve ilişkili veriler (kişiler, ilanlar, geçmiş) basit görünümde listelenir.
          </DialogDescription>
        </DialogHeader>

        {isFetching && (
          <div className="text-sm text-muted-foreground">Yükleniyor…</div>
        )}
        {isError && (
          <div className="text-sm text-red-600" role="alert">{(error as Error)?.message || 'Detaylar alınamadı.'}</div>
        )}

        {!isFetching && !isError && company && (
          <div className="space-y-6">
            <section>
              <h3 className="text-sm font-semibold text-slate-700">Şirket Bilgileri</h3>
              <div className="mt-2 space-y-1 text-sm">
                <div><span className="text-slate-500">Sicil No:</span> {company.sicil_no || '-'}</div>
                <div><span className="text-slate-500">Müdürlük:</span> {company.sicil_mudurluk || '-'}</div>
                <div><span className="text-slate-500">Adres:</span> {company.adres || company.address || '-'}</div>
              </div>
            </section>

            <section>
              <h3 className="text-sm font-semibold text-slate-700">Kişiler</h3>
              {data?.persons?.filter(p => 
                (p.full_name || '').includes('***') || 
                (p.first_name || '').includes('***') || 
                (p.last_name || '').includes('***')
              ).length ? (
                <ul className="mt-2 space-y-1 text-sm">
                  {data.persons
                    .filter(p => 
                      (p.full_name || '').includes('***') || 
                      (p.first_name || '').includes('***') || 
                      (p.last_name || '').includes('***')
                    )
                    .map((p, i) => (
                      <li key={`${p.id}-${i}`} className="flex items-center justify-between">
                        <div>
                          <span className="font-medium">{p.full_name || `${p.first_name || ''} ${p.last_name || ''}`.trim() || 'Ad Soyad Yok'}</span>
                          <span className="ml-2 text-xs text-slate-500">{p.relation_type || p.position || ''}</span>
                        </div>
                        <div className="text-xs text-slate-500">{p.is_current ? 'Aktif' : 'Geçmiş'}</div>
                      </li>
                    ))}
                </ul>
              ) : (
                <div className="mt-2 text-xs text-muted-foreground">Yıldızlı kişi bulunamadı.</div>
              )}
            </section>

            {Array.isArray(data?.history) && (
              <section>
                <h3 className="text-sm font-semibold text-slate-700">Gazete Hareketleri</h3>
                {data.history.length ? (
                  <ul className="mt-2 space-y-2 text-sm max-h-60 overflow-auto pr-1">
                    {data.history.map((h: any) => {
                      const date = h.entry_date ? new Date(h.entry_date).toLocaleDateString('tr-TR') : '';
                      const title = (h.processed_text || '').toString().split('\n')[0] || 'Başlık yok';
                      return (
                        <li key={h.id} className="border rounded p-2 bg-white">
                          <div className="flex items-center justify-between">
                            <span className="font-medium">{title}</span>
                            <span className="text-xs text-slate-500">{date}</span>
                          </div>
                        </li>
                      );
                    })}
                  </ul>
                ) : (
                  <div className="mt-2 text-xs text-muted-foreground">Geçmiş kaydı bulunamadı.</div>
                )}
              </section>
            )}
            
            {Array.isArray((data as any)?.same_address_companies) && (
              <section>
                <h3 className="text-sm font-semibold text-slate-700">İlişkiler (Aynı Adres)</h3>
                {(data as any).same_address_companies.length ? (
                  <ul className="mt-2 space-y-2 text-sm max-h-60 overflow-auto pr-1">
                    {(data as any).same_address_companies.map((c: any) => (
                      <li key={c.id} className="border rounded p-2 bg-white">
                        <div className="font-medium">{c.firma_unvani || c.unvan || 'Bilinmeyen Firma'}</div>
                        <div className="text-xs text-slate-500 mt-1">{c.adres || c.address || 'Adres yok'}</div>
                      </li>
                    ))}
                  </ul>
                ) : (
                  <div className="mt-2 text-xs text-muted-foreground">Aynı adreste başka şirket bulunamadı.</div>
                )}
              </section>
            )}

            {Array.isArray((data as any)?.related_companies) && (
              <section>
                <h3 className="text-sm font-semibold text-slate-700">İlişkiler (Ortak Kişiler - Yıldızlı)</h3>
                {(data as any).related_companies.length ? (
                  <ul className="mt-2 space-y-2 text-sm max-h-60 overflow-auto pr-1">
                    {(data as any).related_companies.map((rc: any) => {
                      const title = rc.firma_unvani || rc.unvan || 'Şirket';
                      const sub = rc.sicil_no || '';
                      const persons: any[] = Array.isArray(rc.shared_persons) ? rc.shared_persons : [];
                      return (
                        <li key={rc.id} className="border rounded p-2 bg-white">
                          <div className="flex items-center justify-between">
                            <div>
                              <span className="font-medium">{title}</span>
                              {sub ? <span className="ml-2 text-xs text-slate-500">{sub}</span> : null}
                            </div>
                            <span className="text-xs text-slate-500">{persons.length} ortak kişi</span>
                          </div>
                          {persons.length ? (
                            <ul className="mt-1 grid grid-cols-1 gap-1">
                              {persons.map((sp: any, idx: number) => (
                                <li key={`${rc.id}-sp-${idx}`} className="text-xs text-slate-600">
                                  <span className="font-medium">{sp.full_name || `${sp.first_name || ''} ${sp.last_name || ''}`.trim() || 'Ad Soyad Yok'}</span>
                                  {sp.relation_type || sp.position ? (
                                    <span className="ml-1 text-slate-500">— {sp.relation_type || sp.position}</span>
                                  ) : null}
                                  {sp.is_current !== undefined && (
                                    <span className="ml-1 text-slate-400">({sp.is_current ? 'Aktif' : 'Geçmiş'})</span>
                                  )}
                                </li>
                              ))}
                            </ul>
                          ) : null}
                        </li>
                      );
                    })}
                  </ul>
                ) : (
                  <div className="mt-2 text-xs text-muted-foreground">Yıldızlı kişi üzerinden ilişkili şirket bulunamadı.</div>
                )}
              </section>
            )}
          </div>
        )}
      </DialogContent>
    </Dialog>
  );
}
