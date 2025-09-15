"use client";

import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { useCompanyDetail } from '@/hooks/useCompanyDetail';
import { useState } from 'react';

interface CompanyDetailModalProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  companyId?: string;
}

export default function CompanyDetailModal({ open, onOpenChange, companyId }: CompanyDetailModalProps) {
  const { data, isFetching, isError, error } = useCompanyDetail(companyId, open);
  const [annOpenAll, setAnnOpenAll] = useState(false);
  const company: any = data?.company ?? null;

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-3xl max-h-[80vh] overflow-y-auto">
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
              {Array.isArray(data?.persons) && data.persons.length > 0 ? (
                <ul className="mt-2 space-y-1 text-sm">
                  {data.persons.map((p: any, i: number) => {
                    const nameRaw = p.full_name || `${p.first_name || ''} ${p.last_name || ''}`.trim();
                    const name = nameRaw && nameRaw.length > 0 ? nameRaw : 'Ad Bilinmiyor';
                    const roleRaw = p.relation_type || p.position || '';
                    const role = (roleRaw === 'MASKELI_KIMLIK' || roleRaw === 'OCR') ? '' : roleRaw;
                    const mids: string[] = Array.isArray(p.masked_ids) ? p.masked_ids : [];
                    return (
                      <li key={`${p.id}-${i}`} className="flex items-center justify-between">
                        <div className="min-w-0 pr-2">
                          <span className="font-medium truncate inline-block max-w-[16rem] align-middle" title={name}>{name}</span>
                          {role ? <span className="ml-2 text-xs text-slate-500 align-middle">{role}</span> : null}
                          {p.is_starred ? <Badge variant="secondary" className="ml-2 align-middle">Yıldızlı</Badge> : null}
                          {p.source ? <Badge variant="outline" className="ml-2 align-middle">{p.source}</Badge> : null}
                          {mids.length ? (
                            <span className="ml-2 inline-flex flex-wrap gap-1 align-middle">
                              {mids.map((m, mi) => (
                                <Badge key={`${p.id}-mid-${mi}`} variant="outline">Kimlik: {m}</Badge>
                              ))}
                            </span>
                          ) : null}
                        </div>
                        <div className="text-xs text-slate-500 shrink-0">{p.is_current === false ? 'Geçmiş' : 'Aktif'}</div>
                      </li>
                    );
                  })}
                </ul>
              ) : (
                <div className="mt-2 text-xs text-muted-foreground">Kişi bulunamadı.</div>
              )}
            </section>

            {/* İlanlar */}
            <section>
              <div className="flex items-center justify-between">
                <h3 className="text-sm font-semibold text-slate-700">İlanlar</h3>
                {Array.isArray(data?.announcements) && data.announcements.length > 0 ? (
                  <Button size="sm" variant="outline" onClick={() => setAnnOpenAll((v: boolean) => !v)}>
                    {annOpenAll ? 'Tümünü Kapat' : 'Tümünü Aç'}
                  </Button>
                ) : null}
              </div>
              {Array.isArray(data?.announcements) && data.announcements.length > 0 ? (
                <div className="mt-2 space-y-2">
                  {data.announcements.map((a: any, idx: number) => {
                    const date = a.publication_date ? new Date(a.publication_date).toLocaleDateString('tr-TR') : '-';
                    return (
                      <details key={a.id || idx} className="rounded border bg-white p-3" open={annOpenAll}>
                        <summary className="cursor-pointer select-none list-none">
                          <div className="flex items-center justify-between">
                            <div className="min-w-0 pr-2">
                              <div className="font-medium truncate" title={a.title || 'Başlık yok'}>{a.title || 'Başlık yok'}</div>
                              <div className="text-xs text-slate-500 mt-0.5">
                                {a.announcement_type ? `${a.announcement_type} • ` : ''}
                                {a.issue_number ? `Sayı: ${a.issue_number} • ` : ''}
                                {a.page_number ? `Sayfa: ${a.page_number} • ` : ''}
                                {date}
                              </div>
                            </div>
                            {a.newspaper_name ? <Badge variant="outline" className="shrink-0">{a.newspaper_name}</Badge> : null}
                          </div>
                        </summary>
                        <div className="mt-3 text-sm space-y-2">
                          {a.pdf_url ? (
                            <div>
                              <a className="text-blue-700 underline" href={a.pdf_url} target="_blank" rel="noreferrer">
                                PDF'yi Aç
                              </a>
                            </div>
                          ) : null}
                          {a.ocr_status ? (
                            <div className="text-xs text-slate-500">OCR Durumu: {a.ocr_status}</div>
                          ) : null}
                          {a.trade_registry_number ? (
                            <div className="text-xs text-slate-500">İlan Sicil No: {a.trade_registry_number}</div>
                          ) : null}
                        </div>
                      </details>
                    );
                  })}
                </div>
              ) : (
                <div className="mt-2 text-xs text-muted-foreground">İlan bulunamadı.</div>
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
                <h3 className="text-sm font-semibold text-slate-700">İlişkiler (Ortak Kişiler)</h3>
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
                              {persons.map((sp: any, idx: number) => {
                                const nmRaw = sp.full_name || `${sp.first_name || ''} ${sp.last_name || ''}`.trim();
                                const nm = nmRaw && nmRaw.length > 0 ? nmRaw : '';
                                const mids: string[] = Array.isArray(sp.masked_ids) ? sp.masked_ids : (nm && nm.includes('*') ? [nm] : []);
                                const showName = nm && !nm.includes('*');
                                return (
                                  <li key={`${rc.id}-sp-${idx}`} className="text-xs text-slate-600">
                                    {showName ? <span className="font-medium">{nm}</span> : null}
                                    {mids.length ? (
                                      <span className="ml-1 inline-flex flex-wrap gap-1 align-middle">
                                        {mids.map((m, mi) => (
                                          <Badge key={`${rc.id}-sp-${idx}-mid-${mi}`} variant="outline">Kimlik: {m}</Badge>
                                        ))}
                                      </span>
                                    ) : null}
                                  </li>
                                );
                              })}
                            </ul>
                          ) : null}
                        </li>
                      );
                    })}
                  </ul>
                ) : (
                  <div className="mt-2 text-xs text-muted-foreground">Ortak kişi üzerinden ilişkili şirket bulunamadı.</div>
                )}
              </section>
            )}
          </div>
        )}
      </DialogContent>
    </Dialog>
  );
}
