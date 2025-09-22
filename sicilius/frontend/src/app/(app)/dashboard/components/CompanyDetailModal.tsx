"use client";

import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { useCompanyDetail } from '@/hooks/useCompanyDetail';
import { useNearbyCompanies } from '@/hooks/useNearbyCompanies';
import dynamic from 'next/dynamic';
import { useEffect, useMemo, useRef, useState } from 'react';
import { FileText, Users, Clock, MapPin } from 'lucide-react';

const MiniMap = dynamic(() => import('@/components/maps/MiniMap').then(m => m.MiniMap), { ssr: false });

interface CompanyDetailModalProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  companyId?: string;
  onOpenCompany?: (companyId: string) => void; // ilişkili şirketi anında açmak için opsiyonel callback
  onLimitReached?: () => void; // günlük limit uyarısı için üst bileşeni bilgilendir
}

export default function CompanyDetailModal({ open, onOpenChange, companyId, onOpenCompany, onLimitReached }: CompanyDetailModalProps) {
  const { data, isFetching, isError, error } = useCompanyDetail(companyId, open);
  const [annOpenAll, setAnnOpenAll] = useState(false);
  const company: any = data?.company ?? null;
  const personsCount = Array.isArray(data?.persons) ? data!.persons.length : 0;
  const annCount = Array.isArray(data?.announcements) ? data!.announcements.length : 0;
  const histCount = Array.isArray(data?.history) ? data!.history.length : 0;

  const centerLatLon = useMemo(() => {
    const c = company?.koordinat;
    if (!c) return null;
    // Accept both PostGIS-like {x, y} and API-like {lat, lon}
    if (typeof c?.x === 'number' && typeof c?.y === 'number') {
      return { lat: c.y as number, lon: c.x as number };
    }
    if (typeof c?.lat === 'number' && typeof c?.lon === 'number') {
      return { lat: c.lat as number, lon: c.lon as number };
    }
    return null;
  }, [company?.koordinat]);

  const [radiusKM, setRadiusKM] = useState<number>(5);
  // Persist radius across sessions
  useEffect(() => {
    if (!open) return;
    try {
      const raw = localStorage.getItem('sicilius.company_modal.radius_km');
      const n = raw ? parseInt(raw, 10) : NaN;
      if ([1, 5, 10].includes(n)) setRadiusKM(n);
    } catch {}
  }, [open]);
  useEffect(() => {
    try {
      localStorage.setItem('sicilius.company_modal.radius_km', String(radiusKM));
    } catch {}
  }, [radiusKM]);
  const { data: nearby, isFetching: isNearbyFetching } = useNearbyCompanies(companyId, {
    enabled: !!open && !!companyId && !!centerLatLon,
    max_km: radiusKM,
    limit: 10,
  });

  // Şirket detayı başarıyla yüklendiğinde günlük kullanım bilgisini yenile (badge güncelleme)
  const lastRefreshedId = useRef<string | null>(null);
  useEffect(() => {
    if (!open) {
      lastRefreshedId.current = null;
      return;
    }
    const cid = (data as any)?.company?.id || null;
    if (!isFetching && !isError && cid && lastRefreshedId.current !== cid) {
      lastRefreshedId.current = cid;
      try {
        if (typeof window !== 'undefined') {
          window.dispatchEvent(new Event('daily-usage:refresh'));
        }
      } catch {}
    }
  }, [open, isFetching, isError, (data as any)?.company?.id]);

  // Günlük limit aşıldığında (429), modal'ı kapat ve üst bileşeni bilgilendir
  useEffect(() => {
    const status = (error as any)?.status;
    if (open && isError && status === 429) {
      onOpenChange(false);
      if (typeof window !== 'undefined') {
        // küçük bir gecikmeyle user-friendly modal açılır
        setTimeout(() => onLimitReached && onLimitReached(), 50);
      } else {
        onLimitReached && onLimitReached();
      }
    }
  }, [open, isError, error, onOpenChange, onLimitReached]);

  // If there are no nearby results, auto-expand radius once (e.g., 1 -> 5 -> 10)
  const expandedRef = useRef(false);
  useEffect(() => {
    if (!open || !centerLatLon || isNearbyFetching) return;
    if (!Array.isArray(nearby)) return;
    if (nearby.length > 0) return;
    if (expandedRef.current) return;
    if (radiusKM < 10) {
      expandedRef.current = true;
      setRadiusKM(radiusKM === 1 ? 5 : 10);
    }
  }, [open, centerLatLon, nearby, isNearbyFetching, radiusKM]);

  const formatDateTime = (value?: string | null): string => {
    if (!value || value === '-') return '-';
    let d = new Date(value);
    if (isNaN(d.getTime())) {
      const base = String(value).slice(0, 19); // YYYY-MM-DDTHH:mm:ss
      const tryDate = new Date(base);
      if (!isNaN(tryDate.getTime())) d = tryDate;
    }
    if (isNaN(d.getTime())) return String(value);
    return d.toLocaleString('tr-TR', { year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit' });
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-5xl w-[min(92vw,1100px)] max-h-[85vh] bg-white dark:bg-slate-900 text-slate-900 dark:text-slate-100 p-0 overflow-y-auto">
        <DialogHeader className="px-4 pt-4">
          <DialogTitle className="text-slate-900 dark:text-slate-100">{company?.firma_unvani || company?.unvan || 'Şirket Detayı'}</DialogTitle>
          <DialogDescription className="text-slate-600 dark:text-slate-300">
            Bu içerik yalnızca bilgilendirme amaçlıdır; ayrıntılı hükümler ve koşullar için{' '}
            <a href="/kullanici-sozlesmesi" target="_blank" rel="noopener noreferrer" className="underline text-primary">Kullanıcı Sözleşmesi</a>
            'ni inceleyiniz.
          </DialogDescription>
        </DialogHeader>

        {/* Sticky summary chips */}
        <div className="sticky top-0 z-10 bg-white/75 dark:bg-slate-900/75 backdrop-blur border-b border-slate-200/70 dark:border-slate-700/70">
          <div className="px-4 py-2 flex items-center gap-2 text-xs">
            <span className="inline-flex items-center gap-1 rounded-full border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 px-2.5 py-1 text-slate-700 dark:text-slate-200"><Users size={14} /> {personsCount} kişi</span>
            <span className="inline-flex items-center gap-1 rounded-full border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 px-2.5 py-1 text-slate-700 dark:text-slate-200"><FileText size={14} /> {annCount} ilan</span>
            <span className="inline-flex items-center gap-1 rounded-full border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 px-2.5 py-1 text-slate-700 dark:text-slate-200"><Clock size={14} /> {histCount} geçmiş</span>
          </div>
        </div>

        {isFetching && (
          <div className="p-4 space-y-4">
            <div className="h-4 bg-slate-200 dark:bg-slate-700 rounded w-1/2 animate-pulse" />
            <div className="grid grid-cols-2 gap-3">
              <div className="h-24 bg-slate-100 dark:bg-slate-800 rounded animate-pulse" />
              <div className="h-24 bg-slate-100 dark:bg-slate-800 rounded animate-pulse" />
            </div>
            <div className="h-4 bg-slate-200 dark:bg-slate-700 rounded w-1/3 animate-pulse" />
            <div className="space-y-2">
              {Array.from({ length: 3 }).map((_, i) => (
                <div key={i} className="h-16 bg-slate-100 dark:bg-slate-800 rounded animate-pulse" />
              ))}
            </div>
          </div>
        )}
        {isError && ((error as any)?.status !== 429) && (
          <div className="text-sm text-red-600" role="alert">{(error as Error)?.message || 'Detaylar alınamadı.'}</div>
        )}

        {!isFetching && !isError && company && (
          <div className="space-y-6 p-4">
            <section>
              <h3 className="text-sm font-semibold text-slate-700 dark:text-slate-200">Şirket Bilgileri</h3>
              <div className="mt-2 space-y-1 text-sm">
                <div><span className="text-slate-500 dark:text-slate-400">Sicil No:</span> {company.sicil_no || '-'}</div>
                <div><span className="text-slate-500 dark:text-slate-400">MERSİS No:</span> {company.mersis_number || company.mersis_number_ocr || '-'}</div>
                <div><span className="text-slate-500 dark:text-slate-400">Müdürlük:</span> {company.sicil_mudurluk || '-'}</div>
                <div><span className="text-slate-500 dark:text-slate-400">Adres:</span> {company.adres || company.address || '-'}</div>
                <div><span className="text-slate-500 dark:text-slate-400">Son Güncelleme:</span> {formatDateTime(company.updated_at || company.last_scraped_at || company.created_at || '-')}</div>
              </div>
            </section>

            {/* Konum & Yakın Şirketler */}
            <section>
              <div className="flex items-center justify-between">
                <h3 className="text-sm font-semibold text-slate-700 dark:text-slate-200 flex items-center gap-2"><MapPin size={16}/> Konum ve Yakın Şirketler</h3>
                {centerLatLon ? (
                  <a
                    href={`https://www.openstreetmap.org/?mlat=${centerLatLon.lat}&mlon=${centerLatLon.lon}#map=14/${centerLatLon.lat}/${centerLatLon.lon}`}
                    target="_blank"
                    rel="noreferrer"
                    className="text-xs underline text-blue-600 hover:text-blue-700 dark:text-blue-400"
                    data-testid="open-osm"
                  >
                    Haritada Aç
                  </a>
                ) : null}
              </div>
              <div className="flex items-center gap-2 text-xs">
                <span className="text-slate-500 dark:text-slate-400">Yarıçap:</span>
                {[1, 5, 10].map(v => (
                  <Button
                    key={v}
                    type="button"
                    size="sm"
                    variant={radiusKM === v ? 'gradient' : 'outline'}
                    className="h-auto px-2 py-1"
                    onClick={() => setRadiusKM(v)}
                    aria-pressed={radiusKM === v}
                    data-testid={`radius-${v}`}
                  >
                    {v} km
                  </Button>
                ))}
              </div>
              <div className="mt-2 grid grid-cols-1 md:grid-cols-2 gap-3">
                <div>
                  {centerLatLon ? (
                    <div data-testid="company-minimap">
                      <MiniMap
                        center={centerLatLon}
                        pins={(nearby || []).filter(n => n.koordinat && typeof n.koordinat.lat === 'number' && typeof n.koordinat.lon === 'number').map(n => ({
                          id: n.id,
                          lat: n.koordinat!.lat,
                          lon: n.koordinat!.lon,
                          label: n.unvan || n.title || 'Şirket',
                          distance_km: n.distance_km,
                        }))}
                        height={260}
                        zoom={13}
                      />
                    </div>
                  ) : (
                    <div className="text-xs text-muted-foreground dark:text-slate-400 border rounded p-3">
                      Harita için koordinat bulunamadı.
                    </div>
                  )}
                </div>
                <div>
                  {centerLatLon ? (
                    Array.isArray(nearby) && nearby.length > 0 ? (
                      <ul className="space-y-2 text-sm max-h-[260px] overflow-auto pr-1" data-testid="nearby-list">
                        {nearby.map((c: any) => {
                          const title = c.unvan || c.title || 'Şirket';
                          const dist = typeof c.distance_km === 'number' ? `${c.distance_km.toFixed(2)} km` : '';
                          const click = () => { if (onOpenCompany && c.id) onOpenCompany(c.id); };
                          return (
                            <li
                              key={c.id}
                              className="border rounded p-2 bg-white dark:bg-slate-900 dark:border-slate-700 transition-colors hover:bg-slate-50 dark:hover:bg-slate-800 cursor-pointer"
                              role="button"
                              onClick={click}
                            >
                              <div className="flex items-center justify-between">
                                <div>
                                  <div className="font-medium truncate max-w-[16rem]" title={title}>{title}</div>
                                  <div className="text-[11px] text-slate-500 dark:text-slate-400 mt-0.5 truncate max-w-[18rem]">
                                    {c.address || '-'}
                                  </div>
                                </div>
                                <Badge variant="outline" className="shrink-0 dark:border-slate-700 dark:text-slate-300">{dist}</Badge>
                              </div>
                            </li>
                          );
                        })}
                      </ul>
                    ) : (
                      <div className="text-xs text-muted-foreground dark:text-slate-400 border rounded p-3">
                        {isNearbyFetching ? 'Yakın şirketler yükleniyor...' : 'Yakında şirket bulunamadı.'}
                      </div>
                    )
                  ) : null}
                </div>
              </div>
            </section>

            <section>
              <h3 className="text-sm font-semibold text-slate-700 dark:text-slate-200">Kişiler</h3>
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
                          {mids.length ? (
                            <span className="ml-2 inline-flex flex-wrap gap-1 align-middle">
                              {mids.map((m, mi) => (
                                <Badge key={`${p.id}-mid-${mi}`} variant="outline" className="dark:border-slate-700 dark:text-slate-300">Kimlik: {m}</Badge>
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
                <h3 className="text-sm font-semibold text-slate-700 dark:text-slate-200">İlanlar</h3>
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
                      <details key={a.id || idx} className="rounded border bg-white dark:bg-slate-900 dark:border-slate-700 p-3" open={annOpenAll}>
                        <summary className="cursor-pointer select-none list-none">
                          <div className="flex items-center justify-between">
                            <div className="min-w-0 pr-2">
                              <div className="font-medium truncate" title={a.title || 'Başlık yok'}>{a.title || 'Başlık yok'}</div>
                              <div className="text-xs text-slate-500 dark:text-slate-400 mt-0.5">
                                {a.announcement_type ? `${a.announcement_type} • ` : ''}
                                {a.issue_number ? `Sayı: ${a.issue_number} • ` : ''}
                                {a.page_number ? `Sayfa: ${a.page_number} • ` : ''}
                                {date}
                              </div>
                            </div>
                            {a.newspaper_name ? <Badge variant="outline" className="shrink-0 dark:border-slate-700 dark:text-slate-300">{a.newspaper_name}</Badge> : null}
                          </div>
                        </summary>
                        <div className="mt-3 text-sm">
                          <div className="whitespace-pre-wrap leading-relaxed text-slate-700 dark:text-slate-200">
                            {a.original_text || 'İlan metni bulunamadı.'}
                          </div>
                        </div>
                      </details>
                    );
                  })}
                </div>
              ) : (
                <div className="mt-2 text-xs text-muted-foreground dark:text-slate-400">İlan bulunamadı.</div>
              )}
            </section>

            {Array.isArray(data?.history) && (
              <section>
                <h3 className="text-sm font-semibold text-slate-700 dark:text-slate-200">Gazete Hareketleri</h3>
                {data.history.length ? (
                  <ul className="mt-2 space-y-2 text-sm max-h-60 overflow-auto pr-1">
                    {data.history.map((h: any) => {
                      const date = h.entry_date ? new Date(h.entry_date).toLocaleDateString('tr-TR') : '';
                      const title = (h.processed_text || '').toString().split('\n')[0] || 'Başlık yok';
                      return (
                        <li key={h.id} className="border rounded p-2 bg-white dark:bg-slate-900 dark:border-slate-700">
                          <div className="flex items-center justify-between">
                            <span className="font-medium">{title}</span>
                            <span className="text-xs text-slate-500 dark:text-slate-400">{date}</span>
                          </div>
                        </li>
                      );
                    })}
                  </ul>
                ) : (
                  <div className="mt-2 text-xs text-muted-foreground dark:text-slate-400">Geçmiş kaydı bulunamadı.</div>
                )}
              </section>
            )}
            
            {Array.isArray((data as any)?.same_address_companies) && (
              <section>
                <h3 className="text-sm font-semibold text-slate-700 dark:text-slate-200">İlişkiler (Aynı Adres)</h3>
                {(data as any).same_address_companies.length ? (
                  <ul className="mt-2 space-y-2 text-sm max-h-60 overflow-auto pr-1">
                    {(data as any).same_address_companies.map((c: any) => {
                      const title = c.firma_unvani || c.unvan || 'Bilinmeyen Firma';
                      const mersis = c.mersis_number || c.mersis_number_ocr || '';
                      const addr = c.adres || c.address || 'Adres yok';
                      const handleClick = () => {
                        if (onOpenCompany && c.id) onOpenCompany(c.id);
                      };
                      return (
                        <li
                          key={c.id}
                          className="border rounded p-2 bg-white dark:bg-slate-900 dark:border-slate-700 transition-colors hover:bg-slate-50 dark:hover:bg-slate-800 cursor-pointer"
                          role="button"
                          onClick={handleClick}
                        >
                          <div className="font-medium">{title}</div>
                          <div className="text-xs text-slate-500 dark:text-slate-400 mt-1">MERSİS: {mersis || '-'}</div>
                          <div className="text-xs text-slate-500 dark:text-slate-400 mt-1">{addr}</div>
                        </li>
                      );
                    })}
                  </ul>
                ) : (
                  <div className="mt-2 text-xs text-muted-foreground dark:text-slate-400">Aynı adreste başka şirket bulunamadı.</div>
                )}
              </section>
            )}

            {Array.isArray((data as any)?.related_companies) && (
              <section>
                <h3 className="text-sm font-semibold text-slate-700 dark:text-slate-200">İlişkiler (Ortak Kişiler)</h3>
                {(data as any).related_companies.length ? (
                  <div className="mt-2 space-y-4">
                    {(() => {
                      const related = (data as any).related_companies as any[];
                      const isNameMatch = (rc: any) => {
                        const persons: any[] = Array.isArray(rc.shared_persons) ? rc.shared_persons : [];
                        return persons.some((sp) => (
                          (sp?.relation_type === 'OCR_ORTAK') ||
                          ((sp?.full_name && String(sp.full_name).trim().length > 0) && Array.isArray(sp?.masked_ids) && sp.masked_ids.length > 0)
                        ));
                      };
                      const strong = related.filter(isNameMatch);
                      const weak = related.filter((rc) => !isNameMatch(rc));

                      const renderList = (arr: any[]) => (
                        <ul className="space-y-2 text-sm max-h-72 overflow-auto pr-1">
                          {arr.map((rc) => {
                            const title = rc.firma_unvani || rc.unvan || 'Şirket';
                            const sub = rc.sicil_no || '';
                            const mersis = rc.mersis_number || rc.mersis_number_ocr || '';
                            const persons: any[] = Array.isArray(rc.shared_persons) ? rc.shared_persons : [];
                            const handleClick = () => {
                              if (onOpenCompany && rc.id) onOpenCompany(rc.id);
                            };
                            return (
                              <li
                                key={rc.id}
                                className="border rounded p-2 bg-white dark:bg-slate-900 dark:border-slate-700 transition-colors hover:bg-slate-50 dark:hover:bg-slate-800 cursor-pointer"
                                role="button"
                                onClick={handleClick}
                              >
                                <div className="flex items-center justify-between">
                                  <div>
                                    <span className="font-medium">{title}</span>
                                    {sub ? <span className="ml-2 text-xs text-slate-500 dark:text-slate-400">{sub}</span> : null}
                                    {mersis ? <Badge variant="outline" className="ml-2 align-middle dark:border-slate-700 dark:text-slate-300">MERSİS: {mersis}</Badge> : null}
                                  </div>
                                  <span className="text-xs text-slate-500 dark:text-slate-400">{persons.length} ortak kişi</span>
                                </div>
                                {persons.length ? (
                                  <ul className="mt-1 grid grid-cols-1 gap-1">
                                    {persons.map((sp: any, idx: number) => {
                                      const nmRaw = sp.full_name || `${sp.first_name || ''} ${sp.last_name || ''}`.trim();
                                      const nm = nmRaw && nmRaw.length > 0 ? nmRaw : '';
                                      const mids: string[] = Array.isArray(sp.masked_ids) ? sp.masked_ids : (nm && nm.includes('*') ? [nm] : []);
                                      const showName = nm && !nm.includes('*');
                                      return (
                                        <li key={`${rc.id}-sp-${idx}`} className="text-xs text-slate-600 dark:text-slate-300">
                                          {showName ? <span className="font-medium">{nm}</span> : null}
                                          {mids.length ? (
                                            <span className="ml-1 inline-flex flex-wrap gap-1 align-middle">
                                              {mids.map((m, mi) => (
                                                <Badge key={`${rc.id}-sp-${idx}-mid-${mi}`} variant="outline" className="dark:border-slate-700 dark:text-slate-300">Kimlik: {m}</Badge>
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
                      );

                      return (
                        <>
                          {strong.length > 0 && (
                            <div>
                              <h4 className="text-xs font-semibold text-emerald-600 dark:text-emerald-400">İsim + Kimlik ile eşleşenler (yüksek güven)</h4>
                              <div className="mt-2">{renderList(strong)}</div>
                            </div>
                          )}
                          {weak.length > 0 && (
                            <div>
                              <h4 className="text-xs font-semibold text-slate-700 dark:text-slate-200">Sadece Kimlik ile eşleşenler</h4>
                              <div className="mt-2">{renderList(weak)}</div>
                            </div>
                          )}
                        </>
                      );
                    })()}
                  </div>
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
