"use client";

import React from 'react';
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { useCompanyDetail } from '@/hooks/useCompanyDetail';
import { useNearbyCompanies } from '@/hooks/useNearbyCompanies';
import { useAnnouncementDetail } from '@/hooks/useAnnouncementDetail';
// same-origin fetch kullanılacak
import dynamic from 'next/dynamic';
import { useEffect, useMemo, useRef, useState } from 'react';
import { FileText, Users, Clock, MapPin, FileDown, AlertTriangle } from 'lucide-react';

const MiniMap = dynamic(() => import('@/components/maps/MiniMap').then(m => m.MiniMap), { ssr: false });
import NexusAnalysisSection from './nexus/NexusAnalysisSection';
import ReportErrorModal from './ReportErrorModal';

function maskUiName(full: string): string {
  try {
    const s = String(full || '');
    if (!s.trim()) return s;
    const tokens = s.split(/\s+/);
    // Bir karakter harf mi? (Unicode uyumlu, regex flag gerektirmez)
    const isLetter = (ch: string) => {
      return ch.toLowerCase() !== ch.toUpperCase();
    };
    // Kelimenin tamamı büyük harf mi? (harf olan karakterlerin hepsi uppercase olmalı)
    const isUpperWord = (w: string) => {
      let hasLetter = false;
      for (const ch of w) {
        if (!isLetter(ch)) continue;
        hasLetter = true;
        if (ch !== ch.toUpperCase()) return false;
      }
      return hasLetter;
    };
    const upperIdx: number[] = [];
    for (let i = 0; i < tokens.length; i++) {
      if (isUpperWord(tokens[i])) upperIdx.push(i);
    }
    if (upperIdx.length === 0) return s;
    const toMask: number[] = upperIdx.length >= 3 ? upperIdx.slice(0, 2) : [upperIdx[0]];
    const maskWord = (w: string) => {
      let seen = 0;
      let out = '';
      for (const ch of w) {
        if (isLetter(ch)) {
          seen++;
          out += (seen <= 2) ? ch : '*';
        } else {
          out += ch;
        }
      }
      return out;
    };
    for (const idx of toMask) {
      tokens[idx] = maskWord(tokens[idx]);
    }
    return tokens.join(' ');
  } catch {
    return String(full || '');
  }
}

function maskMersisUi(v: any): string {
  try {
    const raw = (v === undefined || v === null) ? '' : String(v).trim();
    if (!raw) return '-';
    if (raw.includes('*')) return raw; // already masked
    const d = raw.replace(/\D+/g, '');
    if (d.length === 16 && d[0] !== '0') {
      const arr = d.split('');
      for (let i = 3; i <= 7; i++) arr[i] = '*';
      return arr.join('');
    }
    return raw;
  } catch {
    return '-';
  }
}

// İlan öğesi: tıklanınca çekmece açılır ve detay (OCR metni) lazy-load edilir
function AnnouncementItem({ ann, extractHususFn, forceOpenOnPrint = false }: { ann: any; extractHususFn: (t?: string | null) => string | null; forceOpenOnPrint?: boolean }) {
  const [open, setOpen] = useState(false);
  useEffect(() => {
    if (forceOpenOnPrint) setOpen(true);
  }, [forceOpenOnPrint]);
  const { data, isFetching, isError, error } = useAnnouncementDetail(ann?.id, ann?._ocr_id, open);
  // Normalize hususlar to a short, readable text.
  let hususlarText = '' as string;
  try {
    const h = ann?.hususlar;
    if (typeof h === 'string') {
      hususlarText = h.trim();
    } else if (Array.isArray(h)) {
      hususlarText = h.map((x: any) => String(x ?? '').trim()).filter(Boolean).join(' • ');
    } else if (h && typeof h === 'object') {
      const cand = (h.text ?? h.value ?? '') as string;
      if (typeof cand === 'string') hususlarText = cand.trim();
    }
  } catch { }

  const extractedFromText = !hususlarText ? (typeof extractHususFn === 'function' ? extractHususFn(ann?.original_text || null) : null) : null;
  const hususDisplay = hususlarText || extractedFromText;

  // Title priority: 1. Hususlar (Topic) 2. Type 3. Extracted 4. "İlan"
  // Intentionally ignoring ann.title as it often contains the full company name which is redundant
  const title = hususDisplay || ann?.announcement_type || 'İlan';

  const textSrc = (ann?.original_text || (typeof data?.original_text === 'string' ? data?.original_text : '')) as string;
  const dt = ann?.publication_date || ann?.created_at || null;
  const issue = ann?.issue_number || '';
  const page = ann?.page_number || '';

  // Metinden tarih/sayi/sayfa cikarimlari (fallback)
  const extractDate = (t?: string | null): string | null => {
    if (!t) return null;
    try {
      const m = t.match(/\b(\d{1,2})[./](\d{1,2})[./](\d{4})\b/);
      if (m) {
        const d = new Date(parseInt(m[3], 10), parseInt(m[2], 10) - 1, parseInt(m[1], 10));
        if (!isNaN(d.getTime())) return d.toLocaleDateString('tr-TR');
        return `${m[1]}.${m[2]}.${m[3]}`;
      }
    } catch { }
    return null;
  };
  const extractIssue = (t?: string | null): string | null => {
    if (!t) return null;
    try {
      const m1 = t.match(/İ?Ilan\s*Sıra\s*No\s*[:：]\s*(\d{1,8})/i);
      if (m1 && m1[1]) return m1[1];
      const m2 = t.match(/Sayı\s*[:：]\s*(\d{1,8})/i);
      if (m2 && m2[1]) return m2[1];
    } catch { }
    return null;
  };
  const extractPage = (t?: string | null): string | null => {
    if (!t) return null;
    try {
      const m = t.match(/Sayfa\s*[:：]\s*(\d{1,4})/i);
      if (m && m[1]) return m[1];
    } catch { }
    return null;
  };

  const dateText = (() => {
    if (!dt) return '-';
    let d = new Date(dt);
    if (!isNaN(d.getTime())) return d.toLocaleDateString('tr-TR');
    const m = String(dt).match(/^(\d{1,2})[./](\d{1,2})[./](\d{4})$/);
    if (m) {
      const day = parseInt(m[1], 10);
      const mon = parseInt(m[2], 10) - 1;
      const yr = parseInt(m[3], 10);
      const d2 = new Date(yr, mon, day);
      if (!isNaN(d2.getTime())) return d2.toLocaleDateString('tr-TR');
    }
    return String(dt);
  })();

  const issueText = issue || extractIssue(textSrc) || '';
  const pageText = page || extractPage(textSrc) || '';
  const dateDisplay = dateText === '-' ? (extractDate(textSrc) || '-') : dateText;

  return (
    <li className="border rounded p-2 bg-white dark:bg-slate-900 dark:border-slate-700 text-left print-avoid-break" style={{ textAlign: 'left' }}>
      <button
        type="button"
        className="w-full text-left flex justify-start items-start"
        style={{ textAlign: 'left' }}
        onClick={() => setOpen(v => !v)}
        aria-expanded={open}
      >
        <div className="flex items-start justify-start gap-2 w-full" style={{ textAlign: 'left' }}>
          <div className="min-w-0 text-left w-full flex-1" style={{ textAlign: 'left' }}>
            <div className="font-medium text-left whitespace-pre-wrap break-words" style={{ textAlign: 'left' }} title={title}>{title}</div>
            <div className="text-[11px] text-slate-500 dark:text-slate-400 mt-0.5 flex flex-wrap gap-x-3 gap-y-1">
              <span>Tarih: {dateDisplay}</span>
              {issueText ? <span>Sayı: {issueText}</span> : null}
              {pageText ? <span>Sayfa: {pageText}</span> : null}
            </div>
          </div>
          <div className="shrink-0 self-start">
            <Badge variant="outline" className="dark:border-slate-700 dark:text-slate-300">{open ? 'Kapat' : 'Aç'}</Badge>
          </div>
        </div>
      </button>
      {open && (
        <div className="mt-2 border-t pt-2 border-slate-200 dark:border-slate-700 text-sm text-left">
          {isFetching ? (
            <div className="text-xs text-muted-foreground dark:text-slate-400">Detay yükleniyor…</div>
          ) : (
            (() => {
              const text = data?.original_text || ann?.original_text || null;
              if (text) {
                return (
                  <div className="whitespace-pre-wrap text-left text-[12px] leading-5 bg-slate-50 dark:bg-slate-800 rounded p-2 overflow-auto max-h-64 print-expand">
                    {text}
                  </div>
                );
              }
              if (isError) {
                return <div className="text-xs text-red-600">{(error as any)?.message || 'Detay getirilemedi.'}</div>;
              }
              return <div className="text-xs text-muted-foreground dark:text-slate-400">Detay metni bulunamadı.</div>;
            })()
          )}
        </div>
      )}
    </li>
  );
}

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
  /* DEDUPLICATION: Merge duplicate announcements (same date + issue + page)
     Some announcements appear twice in DB due to multiple scrape passes or OCR versions.
  */
  const uniqueAnnouncements = useMemo(() => {
    const rawAnns: any[] = Array.isArray(data?.announcements) ? data!.announcements : [];
    if (rawAnns.length < 2) return rawAnns;

    const map = new Map<string, any>();

    // Helper to generate a unique key for deduplication
    const genKey = (a: any) => {
      const d = a.publication_date || a.created_at || 'nodate';
      const i = a.issue_number || 'noissue';
      const p = a.page_number || 'nopage';
      // Only dedupe if we have at least issue+page OR date+issue+page
      // If all generic, treat as distinct to avoid false merges
      if (i === 'noissue' && p === 'nopage') return `id_${a.id}`;
      return `${d}_${i}_${p}`;
    };

    rawAnns.forEach((item) => {
      const key = genKey(item);
      if (!map.has(key)) {
        map.set(key, { ...item }); // clone
      } else {
        const existing = map.get(key);
        // Merge strategy:
        // 1. Prefer longer original_text
        const textEx = existing.original_text || '';
        const textNew = item.original_text || '';
        if (textNew.length > textEx.length) {
          existing.original_text = textNew;
          existing._ocr_id = item._ocr_id || existing._ocr_id; // carry over OCR id
        }

        // 2. Merge hususlar (topics)
        const mergeHusus = (h1: any, h2: any) => {
          const arr = new Set<string>();
          const add = (h: any) => {
            if (typeof h === 'string') arr.add(h.trim());
            else if (Array.isArray(h)) h.forEach(add);
            else if (h && typeof h === 'object' && (h.text || h.value)) arr.add((h.text || h.value).trim());
          };
          add(h1);
          add(h2);
          return Array.from(arr);
        };
        existing.hususlar = mergeHusus(existing.hususlar, item.hususlar);

        // 3. Prefer defined metadata if missing in existing
        if (!existing.publication_date && item.publication_date) existing.publication_date = item.publication_date;
        if (!existing.issue_number && item.issue_number) existing.issue_number = item.issue_number;
        if (!existing.page_number && item.page_number) existing.page_number = item.page_number;
      }
    });

    // Sort by date desc
    return Array.from(map.values()).sort((a, b) => {
      const da = new Date(a.publication_date || a.created_at || 0).getTime();
      const db = new Date(b.publication_date || b.created_at || 0).getTime();
      return db - da;
    });
  }, [data?.announcements]);

  const company: any = data?.company ?? null;
  const personsCount = Array.isArray(data?.persons) ? data!.persons.length : 0;
  const annCount = uniqueAnnouncements.length; // Use unique count
  const histCount = Array.isArray((data as any)?.history) ? (data as any).history.length : 0;
  const printRef = useRef<HTMLDivElement | null>(null);
  const [printMode, setPrintMode] = useState(false);
  const [reportErrorOpen, setReportErrorOpen] = useState(false);

  // Yazdırmaya özel: modal verilerinden tek sütunluk bağımsız HTML üret
  const buildPrintHtml = () => {
    try {
      const title = (latestAnnTitle || company?.firma_unvani || company?.unvan || 'Şirket Detayı') as string;
      const oldNames = Array.isArray(oldNamesAll) ? oldNamesAll : [];
      const anns: any[] = uniqueAnnouncements; // Use deduplicated list
      const persons: any[] = Array.isArray((data as any)?.persons) ? (data as any).persons : [];
      const oldAddrs: any[] = Array.isArray((data as any)?.old_addresses) ? (data as any).old_addresses : [];
      const sameAddr: any[] = Array.isArray((data as any)?.same_address_companies) ? (data as any).same_address_companies : [];
      const regRel: any[] = Array.isArray((data as any)?.registry_related_companies) ? (data as any).registry_related_companies : [];
      const rel: any[] = Array.isArray((data as any)?.related_companies) ? (data as any).related_companies : [];

      const fmtDate = (v?: string | null) => {
        if (!v) return '-';
        const d = new Date(v);
        return isNaN(d.getTime()) ? '-' : d.toLocaleDateString('tr-TR');
      };
      const esc = (s: any) => String(s ?? '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

      const relStrong = rel.filter((rc: any) => {
        if (typeof rc?.match_strength === 'string') return rc.match_strength === 'high';
        const ps = Array.isArray(rc.shared_persons) ? rc.shared_persons : [];
        return ps.some((sp: any) => (sp?.relation_type === 'OCR_ORTAK') || ((sp?.full_name && String(sp.full_name).trim().length > 0) && Array.isArray(sp?.masked_ids) && sp.masked_ids.length > 0));
      });
      const relWeak = rel.filter((rc: any) => {
        if (typeof rc?.match_strength === 'string') return rc.match_strength !== 'high';
        return !relStrong.includes(rc);
      });
      const nearbyList: any[] = Array.isArray(nearby) ? nearby : [];

      const html = `<!doctype html>
<html lang="tr">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>${esc(title)} - PDF</title>
  <style>
    @page { size: A4; margin: 16mm; }
    html, body { padding: 0; margin: 0; }
    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Helvetica Neue', Arial, 'Noto Sans', sans-serif; color: #0f172a; }
    .container { max-width: 800px; margin: 0 auto; }
    h1 { font-size: 20px; margin: 0 0 8px 0; }
    h2 { font-size: 16px; margin: 16px 0 8px 0; }
    .muted { color: #475569; font-size: 12px; }
    .row { margin: 4px 0; font-size: 13px; }
    .section { margin-top: 14px; }
    pre { white-space: pre-wrap; font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, 'Liberation Mono', 'Courier New', monospace; font-size: 12px; line-height: 1.5; background: #f8fafc; padding: 8px; border-radius: 4px; }
    ul { margin: 6px 0; padding-left: 18px; }
    li { margin: 4px 0; }
  </style>
  <style media="print">
    .container { max-width: none; }
    body { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
  </style>
  </head>
  <body>
    <div class="container">
      <h1>${esc(title)}</h1>
      ${oldNames.length ? `<div class="row"><strong>Eski Ünvan:</strong></div>` + oldNames.map((n: string) => `<div class="row">${esc(n)}</div>`).join('') : ''}
      <div class="row muted">Bu içerik yalnızca bilgilendirme amaçlıdır; ayrıntılı hükümler ve koşullar için Kullanıcı Sözleşmesi'ni inceleyiniz.</div>

      ${company ? `
      <div class="section">
        <h2>Şirket Bilgileri</h2>
        <div class="row">Sicil No: ${esc(company.sicil_no || '-')}</div>
        <div class="row">MERSİS No: ${esc(maskMersisUi(company.mersis_number || company.mersis_number_ocr))}</div>
        <div class="row">Müdürlük: ${esc(company.sicil_office_header || company.sicil_mudurluk || '-')}</div>
        <div class="row">Adres: ${esc(company.adres || company.address || '-')}</div>
        <div class="row">Son Güncelleme: ${esc(formatDateTime(company.last_update || company.updated_at || company.last_scraped_at || company.created_at || '-'))}</div>
      </div>` : ''}

      ${anns.length ? `
      <div class="section">
        <h2>İlanlar</h2>
        ${anns.map(a => {
        const hRaw = a?.hususlar;
        let displayTitle = '';
        if (typeof hRaw === 'string') displayTitle = hRaw.trim();
        else if (Array.isArray(hRaw)) displayTitle = hRaw.join(', ');

        // Fallback to extractHusus if available in scope, otherwise type
        if (!displayTitle) displayTitle = extractHusus(a?.original_text) || a?.announcement_type || 'İlan';

        return `
          <div class="row"><strong>${esc(displayTitle)}</strong></div>
          <div class="row muted">Tarih: ${esc(fmtDate(a?.publication_date || a?.created_at))}${a?.issue_number ? ` • Sayı: ${esc(a.issue_number)}` : ''}${a?.page_number ? ` • Sayfa: ${esc(a.page_number)}` : ''}</div>
          ${a?.original_text ? `<pre>${esc(a.original_text)}</pre>` : ''}
        `}).join('')}
      </div>` : ''}

      /*
      <div class="section">
        <h2>Konum ve Yakın Şirketler</h2>
        <div class="row">Yarıçap: ${esc(String(radiusKM))} km</div>
        ${centerLatLon ? (nearbyList.length ? `<ul>${nearbyList.map(c => `<li><div><strong>${esc(c.unvan || c.title || 'Şirket')}</strong></div><div class="muted">${esc(c.address || '-')}</div></li>`).join('')}</ul>` : `<div class="row muted">${esc(isNearbyFetching ? 'Yakın şirketler yükleniyor...' : 'Yakında şirket bulunamadı.')}</div>`) : `<div class="row muted">Harita için koordinat bulunamadı.</div>`}
      </div>
      */

      ${persons.length ? `
      <div class="section">
        <h2>Kişiler</h2>
        <ul>
          ${persons.map((p: any) => {
          const nameRaw = p.full_name || `${p.first_name || ''} ${p.last_name || ''}`.trim();
          const name = nameRaw && nameRaw.length > 0 ? nameRaw : 'Ad Bilinmiyor';
          const roleRaw = p.relation_type || p.position || '';
          const role = (roleRaw === 'MASKELI_KIMLIK' || roleRaw === 'OCR') ? '' : roleRaw;
          const status = p.is_current === false ? 'Geçmiş' : 'Aktif';
          const mids: string[] = Array.isArray(p.masked_ids) ? p.masked_ids : [];
          return `<li><span><strong>${esc(maskUiName(name))}</strong></span>${role ? ` • ${esc(role)}` : ''} • ${esc(status)}${mids.length ? ` • ${mids.map(m => `Kimlik: ${esc(m)}`).join(' • ')}` : ''}</li>`;
        }).join('')}
        </ul>
      </div>` : ''}

      ${oldAddrs ? `
      <div class="section">
        <h2>Eski Adresler</h2>
        ${oldAddrs.length ? `<ul>${oldAddrs.map((oa: any) => `<li>${esc(oa?.address || '-')}</li>`).join('')}</ul>` : `<div class="row muted">Eski adres bulunamadı.</div>`}
      </div>` : ''}


      ${regRel ? `
      <div class="section">
        <h2>İlişkiler (MERSİS/Sicil)</h2>
        ${regRel.length ? `<ul>${regRel.map((c: any) => `<li><div><strong>${esc(c.firma_unvani || c.unvan || 'Bilinmeyen Firma')}</strong></div><div class="muted">MERSİS: ${esc(maskMersisUi(c.mersis_number || c.mersis_number_ocr))}</div>${(c.adres || c.address) ? `<div class="muted">${esc(c.adres || c.address)}</div>` : ''}</li>`).join('')}</ul>` : `<div class="row muted">MERSİS/Sicil üzerinden ilişki bulunamadı.</div>`}
      </div>` : ''}

    </div>
    <script>
      window.onload = function() {
        try { window.focus(); } catch(e){}
        setTimeout(function(){ try { window.print(); } catch(e){} }, 60);
      };
    </script>
  </body>
</html>`;
      return html;
    } catch {
      return '<!doctype html><html><head><meta charset="utf-8" /></head><body>Yazdırma başarısız.</body></html>';
    }
  };


  const handlePrint = () => {
    try {
      setPrintMode(true);
      const iframe = document.createElement('iframe');
      iframe.style.position = 'fixed';
      iframe.style.right = '0';
      iframe.style.bottom = '0';
      iframe.style.width = '0';
      iframe.style.height = '0';
      iframe.style.border = '0';
      document.body.appendChild(iframe);
      const doc = iframe.contentDocument || (iframe.contentWindow && iframe.contentWindow.document);
      if (!doc) throw new Error('Print iframe document not available');
      doc.open();
      doc.write(buildPrintHtml());
      doc.close();
      const cleanup = () => {
        try { document.body.removeChild(iframe); } catch { }
        setPrintMode(false);
        window.removeEventListener('focus', cleanup);
      };
      window.addEventListener('focus', cleanup);
      setTimeout(cleanup, 5000);
    } catch { }
  };

  // PNG butonu kaldırıldı; snapshot sadece yazdırma sırasında oluşturuluyor

  useEffect(() => {
    // Ensure print mode + body scoping toggles also when user invokes print via browser menu
    const before = () => {
      try { document.body.classList.add('print-company-modal'); } catch { }
      setPrintMode(true);
    };
    const after = () => {
      try { document.body.classList.remove('print-company-modal'); } catch { }
      setPrintMode(false);
    };
    window.addEventListener('beforeprint', before);
    window.addEventListener('afterprint', after);
    return () => {
      window.removeEventListener('beforeprint', before);
      window.removeEventListener('afterprint', after);
    };
  }, []);

  const centerLatLon = useMemo(() => {
    const c = company?.koordinat;
    if (!c) return null;

    // PostGIS {x, y} format
    if (typeof c?.x === 'number' && typeof c?.y === 'number') {
      return { lat: c.y as number, lon: c.x as number };
    }

    // API {lat, lon} format
    if (typeof c?.lat === 'number' && typeof c?.lon === 'number') {
      return { lat: c.lat as number, lon: c.lon as number };
    }

    // GeoJSON format: {type: "Point", coordinates: [lon, lat]}
    if (c?.type === 'Point' && Array.isArray(c?.coordinates) && c.coordinates.length === 2) {
      const [lon, lat] = c.coordinates;
      if (typeof lon === 'number' && typeof lat === 'number') {
        return { lat, lon };
      }
    }

    return null;
  }, [company?.koordinat]);

  const [radiusKM, setRadiusKM] = useState<number>(5);
  // PERFORMANCE: Lazy-load nearby companies - only fetch when user opens location section
  const [nearbyEnabled, setNearbyEnabled] = useState(false);

  // Persist radius across sessions
  useEffect(() => {
    if (!open) return;
    try {
      const raw = localStorage.getItem('sicilius.company_modal.radius_km');
      const n = raw ? parseInt(raw, 10) : NaN;
      if ([1, 5, 10].includes(n)) setRadiusKM(n);
    } catch { }
  }, [open]);
  useEffect(() => {
    try {
      localStorage.setItem('sicilius.company_modal.radius_km', String(radiusKM));
    } catch { }
  }, [radiusKM]);

  /* Nearby feature disabled
  const { data: nearby, isFetching: isNearbyFetching } = useNearbyCompanies(companyId, {
    enabled: nearbyEnabled && !!open && !!companyId && !!centerLatLon,
    max_km: radiusKM,
    limit: 10,
  });

  // Reset nearbyEnabled when modal closes
  useEffect(() => {
    if (!open) setNearbyEnabled(false);
  }, [open]);
  */
  // Dummy values to prevent errors in render
  const nearby: any[] = [];
  const isNearbyFetching = false;

  // Başlıkta kullanılmak üzere "Tescil Edilen Hususlar" metnini çıkar
  const extractHusus = (text?: string | null): string | null => {
    if (!text) return null;
    try {
      // Aynı satırda değer
      const m1 = text.match(/Tescil\s*Edilen\s*Hususlar?\s*[:\-]\s*([^\n\r]+)/i);
      if (m1 && m1[1]) return m1[1].trim();
      // Etiketi bul, bir sonraki dolu satırı al
      const lines = text.split(/\r?\n/);
      for (let i = 0; i < lines.length; i++) {
        const L = lines[i];
        if (/Tescil\s*Edilen\s*Hususlar?/i.test(L)) {
          const after = L.split(/[:\-]/).slice(1).join(":").trim();
          if (after) return after;
          let j = i + 1;
          while (j < lines.length) {
            const candidate = (lines[j] || '').trim();
            if (candidate) return candidate;
            j++;
          }
          break;
        }
      }
    } catch { }
    return null;
  };

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
      } catch { }
    }
  }, [open, isFetching, isError, (data as any)?.company?.id]);

  // Debug logging to help identify data issues
  // Debug logging disabled
  // useEffect(() => {
  //   if (data && open && !isFetching) {
  //     console.log('[CompanyDetailModal] Data loaded:', {
  //       companyId: data.company?.id,
  //       companyName: data.company?.firma_unvani,
  //       personsCount: Array.isArray(data.persons) ? data.persons.length : 0,
  //       announcementsCount: Array.isArray(data.announcements) ? data.announcements.length : 0,
  //       koordinatType: data.company?.koordinat ? typeof data.company.koordinat : 'null',
  //       koordinatValue: data.company?.koordinat,
  //       hasNearby: !!nearby,
  //       nearbyCount: Array.isArray(nearby) ? nearby.length : 0,
  //     });
  //   }
  // }, [data, open, isFetching, nearby]);

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



  // Eski Ünvan(lar)ını company alanlarından ve history processed_text metinlerinden basit regex ile çıkar
  const oldTradeNames: string[] = useMemo(() => {
    const out: string[] = [];
    const push = (s?: any) => {
      if (!s) return;
      if (Array.isArray(s)) { s.forEach(push); return; }
      const v = String(s).trim();
      if (!v) return;
      if (!out.includes(v)) out.push(v);
    };
    try {
      push((company as any)?.old_trade_name);
      push((company as any)?.old_trade_names);
      push((company as any)?.previous_trade_names);
      push((company as any)?.eski_unvan);
      push((company as any)?.eski_unvanlar);
      push((data as any)?.old_trade_names);
    } catch { }
    try {
      // Gazete geçmişinden olası "Eski Unvan:" satırlarını tara (değer aynı satırda ya da bir sonraki dolu satırda olabilir)
      const hist: any[] = Array.isArray((data as any)?.history) ? (data as any).history : [];
      const labelSameLine = /(Eski\s*(Ticaret\s*)?Unvan[ıiİI]\s*[:\-]\s*)(.+)$/i;
      const labelOnly = /^\s*Eski\s*(Ticaret\s*)?Unvan[ıiİI]\s*[:\-]?\s*$/i;
      for (const h of hist) {
        const txt = (h?.processed_text || '') as string;
        if (!txt) continue;
        const lines = txt.split(/\r?\n/);
        for (let i = 0; i < lines.length; i++) {
          const line = lines[i] || '';
          const m = line.match(labelSameLine);
          if (m && m[3]) { push(m[3]); continue; }
          if (labelOnly.test(line)) {
            // sonraki dolu satırı al
            let j = i + 1;
            while (j < lines.length) {
              const cand = (lines[j] || '').trim();
              if (cand) { push(cand); break; }
              j++;
            }
          }
        }
      }
    } catch { }
    try {
      // İlan metinlerinden de "Eski Unvan:" yakala
      // Use unique announcements for scanning
      const anns: any[] = uniqueAnnouncements;
      const reLine = /(Eski\s*(Ticaret\s*)?Unvan[ıiİI]\s*[:\-]\s*)(.+)$/i;
      for (const a of anns) {
        const txt = (a?.original_text || '') as string;
        if (!txt) continue;
        for (const line of txt.split(/\r?\n/)) {
          const m = line.match(reLine);
          if (m && m[3]) push(m[3]);
        }
      }
    } catch { }
    return out.slice(0, 5); // güvenlik: en fazla 5 tanesini göster
  }, [data, company, uniqueAnnouncements]);

  // PERFORMANCE: Removed announcement prefetch - announcements will load on-demand when user expands them
  const [oldNamesPrefetched] = useState<string[]>([]);

  // Başlıkta kullanılmak üzere eski unvanların birleşimi (company + prefetch)
  const oldNamesAll = useMemo(() => {
    const set = new Set<string>([...oldTradeNames, ...oldNamesPrefetched]);
    return Array.from(set);
  }, [oldTradeNames, oldNamesPrefetched]);

  // Başlıkta en güncel unvan: ilanlar varsa en son ilan başlığını kullan
  const latestAnnTitle = useMemo(() => {
    // Use unique announcements
    const anns: any[] = uniqueAnnouncements;
    if (!anns.length) return null;
    const cand = anns[0]; // Already sorted desc
    const rawT = cand?.title || cand?.company_title || cand?.company_name;
    const t = typeof rawT === 'string' ? rawT : (rawT ? String(rawT) : '');
    const tt = t.trim();
    if (!tt) return null;
    // Müdürlüğü gibi başlıkları başlıkta göstermeyelim (ör: "... Ticaret Sicil Müdürlüğü")
    const isOffice = /ticaret\s*sicil.*m[üu]d[üu]rl[üu][ğg][üu]/i.test(tt)
      || (/m[üu]d[üu]rl[üu][ğg][üu]/i.test(tt) && tt.toLowerCase().includes('ticaret'));
    return isOffice ? null : tt;
  }, [uniqueAnnouncements]);
  const headerTitle = company?.firma_unvani || company?.unvan || latestAnnTitle || 'Şirket Detayı';

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="company-modal-print-target w-[min(100vw-1rem,1100px)] sm:w-[min(96vw,1100px)] max-w-[100vw] max-h-[85vh] bg-white dark:bg-slate-900 text-slate-900 dark:text-slate-100 p-0 overflow-y-auto overflow-x-hidden break-words min-w-0" ref={printRef} style={{ hyphens: 'auto', WebkitHyphens: 'auto', overflowWrap: 'anywhere', wordBreak: 'break-word' }}>
        <DialogHeader className="px-4 pt-4 overflow-hidden min-w-0">
          <DialogTitle className="text-slate-900 dark:text-slate-100 break-all sm:break-words whitespace-normal leading-snug min-w-0" style={{ hyphens: 'auto', overflowWrap: 'anywhere', wordBreak: 'break-word' }}>{headerTitle}</DialogTitle>

          {oldNamesAll.length > 0 && (
            <div className="mt-1 text-xs text-slate-600 dark:text-slate-300">
              <div className="font-medium">Eski Ünvan:</div>
              <div className="mt-0.5 space-y-0.5">
                {oldNamesAll.map((n: string, i: number) => (
                  <div key={`${i}-${n}`} className="break-words whitespace-normal" style={{ overflowWrap: 'anywhere' }} title={n}>{n}</div>
                ))}
              </div>
            </div>
          )}
          <DialogDescription className="text-slate-600 dark:text-slate-300">
            Bu içerik yalnızca bilgilendirme amaçlıdır; ayrıntılı hükümler ve koşullar için
            <a href="/kullanici-sozlesmesi" target="_blank" rel="noopener noreferrer" className="underline text-primary">Kullanıcı Sözleşmesi</a>'ni inceleyiniz.
          </DialogDescription>
        </DialogHeader>

        {/* Sticky summary chips */}
        <div className="sticky top-0 z-10 bg-white/75 dark:bg-slate-900/75 backdrop-blur border-b border-slate-200/70 dark:border-slate-700/70">
          <div className="px-4 py-2 flex flex-wrap items-center gap-2 text-xs">
            <span className="inline-flex items-center gap-1 rounded-full border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 px-2.5 py-1 text-slate-700 dark:text-slate-200"><Users size={14} /> {personsCount} kişi</span>
            <span className="inline-flex items-center gap-1 rounded-full border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 px-2.5 py-1 text-slate-700 dark:text-slate-200"><FileText size={14} /> {annCount} ilan</span>
            <span className="inline-flex items-center gap-1 rounded-full border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 px-2.5 py-1 text-slate-700 dark:text-slate-200"><Clock size={14} /> {histCount} geçmiş</span>
            {!isFetching && (
              <>
                <div
                  role="button"
                  tabIndex={0}
                  onClick={handlePrint}
                  onKeyDown={(e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); handlePrint(); } }}
                  className="inline-flex items-center gap-1 rounded-full border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 px-2.5 py-1 text-slate-700 dark:text-slate-200 hover:bg-slate-50 dark:hover:bg-slate-800 transition-colors cursor-pointer"
                  aria-label="PDF olarak indir"
                  title="PDF olarak indir"
                >
                  <FileDown size={14} /> PDF
                </div>
                <div
                  role="button"
                  tabIndex={0}
                  onClick={() => setReportErrorOpen(true)}
                  className="inline-flex items-center gap-1 rounded-full border border-red-200 dark:border-red-800 bg-red-50 dark:bg-red-900/20 px-2.5 py-1 text-red-700 dark:text-red-300 hover:bg-red-100 dark:hover:bg-red-900/30 transition-colors cursor-pointer"
                  aria-label="Hata Bildir"
                  title="Hata Bildir"
                >
                  <AlertTriangle size={14} /> Hata Bildir
                </div>
              </>
            )}
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
          <div className="space-y-6 p-4 break-words">
            <section>
              <h3 className="text-sm font-semibold text-slate-700 dark:text-slate-200">Şirket Bilgileri</h3>
              <div className="mt-2 space-y-1 text-sm">
                <div><span className="text-slate-500 dark:text-slate-400">Sicil No:</span> {company.sicil_no || '-'}</div>
                <div><span className="text-slate-500 dark:text-slate-400">MERSİS No:</span> {maskMersisUi(company.mersis_number || company.mersis_number_ocr)}</div>
                <div><span className="text-slate-500 dark:text-slate-400">Müdürlük:</span> {company.sicil_office_header || company.sicil_mudurluk || '-'}</div>
                <div><span className="text-slate-500 dark:text-slate-400">Adres:</span> {company.adres || company.address || '-'}</div>
                <div><span className="text-slate-500 dark:text-slate-400">Son Güncelleme:</span> {formatDateTime(company.last_update || company.updated_at || company.last_scraped_at || company.created_at || '-')}</div>
              </div>
            </section>
            {/* İlanlar */}
            {uniqueAnnouncements.length > 0 && (
              <section className="text-left">
                <div className="flex items-center justify-between text-left">
                  <h3 className="text-sm font-semibold text-slate-700 dark:text-slate-200">İlanlar</h3>
                  {uniqueAnnouncements.length > 5 ? (
                    <Button type="button" size="sm" variant="outline" className="h-auto px-2 py-1"
                      onClick={() => setAnnOpenAll(v => !v)}
                      aria-pressed={annOpenAll}
                    >
                      {annOpenAll ? 'Gizle' : 'Tümünü göster'}
                    </Button>
                  ) : null}
                </div>
                {uniqueAnnouncements.length ? (
                  <ul className="mt-2 space-y-2 text-sm max-h-60 overflow-auto pr-1 text-left print-unclamp">
                    {(annOpenAll || printMode ? uniqueAnnouncements : uniqueAnnouncements.slice(0, 5)).map((a: any) => (
                      <AnnouncementItem key={a.id} ann={a} extractHususFn={extractHusus} forceOpenOnPrint={printMode} />
                    ))}
                  </ul>
                ) : (
                  <div className="mt-2 text-xs text-muted-foreground dark:text-slate-400">İlan bulunamadı.</div>
                )}
              </section>
            )}

            {/* NEXUS Ağ Analizi */}
            {company?.id && (
              <NexusAnalysisSection companyId={company.id} />
            )}

            {/* Konkordato */}
            {/* Konum & Aynı Adresteki Firmalar - TEMPORARILY DISABLED
            <section>
              <div className="flex items-center justify-between">
                <h3 className="text-sm font-semibold text-slate-700 dark:text-slate-200 flex items-center gap-2"><MapPin size={16} /> Konum ve Aynı Adresteki Firmalar</h3>
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
              <div className="mt-2 grid grid-cols-1 md:grid-cols-2 gap-3">
                <div>
                  {centerLatLon ? (
                    <div data-testid="company-minimap">
                      <MiniMap
                        center={centerLatLon}
                        pins={[]}
                        height={260}
                        zoom={15}
                      />
                    </div>
                  ) : (
                    <div className="text-xs text-muted-foreground dark:text-slate-400 border rounded p-3">
                      Harita için koordinat bulunamadı.
                    </div>
                  )}
                </div>
                <div>
                  {(() => {
                    const sameAddrList: any[] = Array.isArray((data as any)?.same_address_companies) ? (data as any).same_address_companies : [];
                    if (sameAddrList.length > 0) {
                      return (
                        <ul className="space-y-2 text-sm max-h-[260px] overflow-auto pr-1" data-testid="same-address-list">
                          {sameAddrList.map((c: any) => {
                            const title = c.firma_unvani || c.unvan || 'Şirket';
                            const mersis = c.mersis_number || c.mersis_number_ocr || '';
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
                                    {mersis && (
                                      <div className="text-[11px] text-slate-500 dark:text-slate-400 mt-0.5">
                                        MERSİS: {mersis}
                                      </div>
                                    )}
                                   </div>
                                  <Badge variant="outline" className="shrink-0 dark:border-slate-700 dark:text-slate-300">Aynı Adres</Badge>
                                </div>
                              </li>
                            );
                          })}
                        </ul>
                      );
                    }
                    return (
                      <div className="text-xs text-muted-foreground dark:text-slate-400 border rounded p-3">
                        Bu adreste başka firma bulunamadı.
                      </div>
                    );
                  })()}
                </div>
              </div>
            </section>
            */}

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
                          <span className="font-medium truncate inline-block max-w-[16rem] align-middle" title={maskUiName(name)}>{maskUiName(name)}</span>
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
                <div className="text-xs text-muted-foreground dark:text-slate-400 border rounded p-3">
                  Kişi bulunamadı.
                </div>
              )}
            </section>
            {Array.isArray((data as any)?.old_addresses) && (
              <section>
                <h3 className="text-sm font-semibold text-slate-700 dark:text-slate-200">Eski Adresler</h3>
                {(data as any).old_addresses.length ? (
                  <ul className="mt-2 space-y-2 text-sm max-h-60 overflow-auto pr-1">
                    {(data as any).old_addresses.map((oa: any, idx: number) => {
                      const addr = oa?.address || '-';
                      const mcid = oa?.matched_company_id as string | undefined;
                      const mcomp = oa?.matched_company as any | undefined;
                      const title = mcomp?.firma_unvani || mcomp?.unvan || '';
                      const clickable = !!mcid && typeof onOpenCompany === 'function';
                      const handleClick = () => { if (clickable) onOpenCompany!(mcid!); };
                      return (
                        <li
                          key={`${mcid || 'addr'}-${idx}`}
                          className={
                            "border rounded p-2 bg-white dark:bg-slate-900 dark:border-slate-700 transition-colors " +
                            (clickable ? "hover:bg-slate-50 dark:hover:bg-slate-800 cursor-pointer" : "")
                          }
                          role={clickable ? 'button' : undefined}
                          onClick={handleClick}
                        >
                          <div className="flex items-start justify-between gap-2">
                            <div className="min-w-0">
                              <div className="font-medium truncate" title={addr}>{addr}</div>
                              {title ? (
                                <div className="text-[11px] text-slate-500 dark:text-slate-400 mt-0.5 truncate" title={title}>
                                  {title}
                                </div>
                              ) : null}
                            </div>
                            {mcid ? (
                              <Badge variant="outline" className="shrink-0 dark:border-slate-700 dark:text-slate-300">Firma</Badge>
                            ) : null}
                          </div>
                        </li>
                      );
                    })}
                  </ul>
                ) : (
                  <div className="mt-2 text-xs text-muted-foreground dark:text-slate-400">Eski adres bulunamadı.</div>
                )}
              </section>
            )}


            {Array.isArray((data as any)?.registry_related_companies) && (
              <section>
                <h3 className="text-sm font-semibold text-slate-700 dark:text-slate-200">İlişkiler (MERSİS/Sicil)</h3>
                {(data as any).registry_related_companies.length ? (
                  <ul className="mt-2 space-y-2 text-sm max-h-60 overflow-auto pr-1">
                    {(data as any).registry_related_companies.map((c: any) => {
                      const title = c.firma_unvani || c.unvan || 'Bilinmeyen Firma';
                      const mersis = c.mersis_number || c.mersis_number_ocr || '';
                      const sicil = c.sicil_no || '';
                      const addr = c.adres || c.address || '';
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
                          <div className="flex items-center justify-between">
                            <div className="min-w-0">
                              <div className="font-medium truncate" title={title}>{title}</div>
                              <div className="text-xs text-slate-500 dark:text-slate-400 mt-1 flex flex-wrap gap-x-3 gap-y-1">
                                <span>MERSİS: {mersis || '-'}</span>
                                {sicil ? <span>Sicil: {sicil}</span> : null}
                              </div>
                              {addr ? <div className="text-xs text-slate-500 dark:text-slate-400 mt-1 truncate" title={addr}>{addr}</div> : null}
                            </div>
                          </div>
                        </li>
                      );
                    })}
                  </ul>
                ) : (
                  <div className="mt-2 text-xs text-muted-foreground dark:text-slate-400">MERSİS/Sicil üzerinden ilişki bulunamadı.</div>
                )}
              </section>
            )}


            {/* İlişkiler (Aynı Adres) ve İlişkiler (Ortak Kişiler) bölümleri NEXUS entegrasyonu sonrası kaldırıldı. turgaykirkil */}
          </div>
        )}

        {/* Yazdırma için basitleştirilmiş tek sütun metin bloğu */}
        {!isFetching && !isError && (
          <div className="print-linear print-only p-4 text-slate-900">
            <div className="text-xl font-semibold">{headerTitle}</div>
            {oldNamesAll.length > 0 && (
              <div className="mt-1 text-sm">
                <div className="font-medium">Eski Ünvan:</div>
                {oldNamesAll.map((n: string, i: number) => (
                  <div key={`po-old-${i}`}>{n}</div>
                ))}
              </div>
            )}
            <div className="mt-2 text-sm">
              Bu içerik yalnızca bilgilendirme amaçlıdır; ayrıntılı hükümler ve koşullar için Kullanıcı Sözleşmesi'ni inceleyiniz.
            </div>

            {company && (
              <div className="mt-4">
                <div className="text-base font-semibold">Şirket Bilgileri</div>
                <div className="mt-1 text-sm space-y-1">
                  <div>Sicil No: {company.sicil_no || '-'}</div>
                  <div>MERSİS No: {company.mersis_number || company.mersis_number_ocr || '-'}</div>
                  <div>Müdürlük: {company.sicil_office_header || company.sicil_mudurluk || '-'}</div>
                  <div>Adres: {company.adres || company.address || '-'}</div>
                  <div>Son Güncelleme: {formatDateTime(company.last_update || company.updated_at || company.last_scraped_at || company.created_at || '-')}</div>
                </div>
              </div>
            )}

            {Array.isArray((data as any)?.announcements) && (data as any).announcements.length > 0 && (
              <div className="mt-4">
                <div className="text-base font-semibold">İlanlar</div>
                <div className="mt-1 text-sm space-y-2">
                  {(data as any).announcements.map((a: any) => {
                    const dt = a?.publication_date || a?.created_at || null;
                    const issue = a?.issue_number || '';
                    const page = a?.page_number || '';
                    const gazette = a?.newspaper_name || '';
                    const dateText = dt ? new Date(dt).toLocaleDateString('tr-TR') : '-';
                    const title = a?.title || a?.announcement_type || 'İlan';
                    return (
                      <div key={`po-ann-${a?.id || Math.random()}`}>
                        <div className="font-medium">{title}</div>
                        <div className="text-[12px] text-slate-700">
                          Tarih: {dateText}{gazette ? ` • Bülten: ${gazette}` : ''}{issue ? ` • Sayı: ${issue}` : ''}{page ? ` • Sayfa: ${page}` : ''}
                        </div>
                        {a?.original_text ? (
                          <div className="mt-1 whitespace-pre-wrap text-[12px]">{a.original_text}</div>
                        ) : null}
                      </div>
                    );
                  })}
                </div>
              </div>
            )}

            {/* Konum ve Aynı Adresteki Firmalar - TEMPORARILY DISABLED
            <div className="mt-4">
              <div className="text-base font-semibold">Konum ve Aynı Adresteki Firmalar</div>
              {centerLatLon ? (
                Array.isArray(nearby) && nearby.length > 0 ? (
                  <div className="mt-1 text-sm space-y-1">
                    {nearby.map((c: any) => (
                      <div key={`po-near-${c.id}`}>
                        <div className="font-medium">{c.unvan || c.title || 'Şirket'}</div>
                        <div className="text-[12px] text-slate-700">{c.address || '-'}</div>
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="mt-1 text-sm text-slate-700">{isNearbyFetching ? 'Yakın şirketler yükleniyor...' : 'Yakında şirket bulunamadı.'}</div>
                )
              ) : (
                <div className="mt-1 text-sm text-slate-700">Harita için koordinat bulunamadı.</div>
              )}
            </div>
            */}

            {Array.isArray((data as any)?.persons) && (data as any).persons.length > 0 && (
              <div className="mt-4">
                <div className="text-base font-semibold">Kişiler</div>
                <div className="mt-1 text-sm space-y-1">
                  {(data as any).persons.map((p: any, i: number) => {
                    const nameRaw = p.full_name || `${p.first_name || ''} ${p.last_name || ''}`.trim();
                    const name = nameRaw && nameRaw.length > 0 ? nameRaw : 'Ad Bilinmiyor';
                    const roleRaw = p.relation_type || p.position || '';
                    const role = (roleRaw === 'MASKELI_KIMLIK' || roleRaw === 'OCR') ? '' : roleRaw;
                    const status = p.is_current === false ? 'Geçmiş' : 'Aktif';
                    const mids: string[] = Array.isArray(p.masked_ids) ? p.masked_ids : [];
                    return (
                      <div key={`po-person-${p.id || i}`}>
                        <span className="font-medium">{name}</span>
                        {role ? <span> • {role}</span> : null}
                        <span> • {status}</span>
                        {mids.length ? <span> • {mids.map(m => `Kimlik: ${m}`).join(' • ')}</span> : null}
                      </div>
                    );
                  })}
                </div>
              </div>
            )}

            {Array.isArray((data as any)?.old_addresses) && (
              <div className="mt-4">
                <div className="text-base font-semibold">Eski Adresler</div>
                {(data as any).old_addresses.length ? (
                  <div className="mt-1 text-sm space-y-1">
                    {(data as any).old_addresses.map((oa: any, idx: number) => (
                      <div key={`po-oldaddr-${idx}`}>{oa?.address || '-'}</div>
                    ))}
                  </div>
                ) : (
                  <div className="mt-1 text-sm text-slate-700">Eski adres bulunamadı.</div>
                )}
              </div>
            )}

            {Array.isArray((data as any)?.same_address_companies) && (
              <div className="mt-4">
                <div className="text-base font-semibold">İlişkiler (Aynı Adres)</div>
                {(data as any).same_address_companies.length ? (
                  <div className="mt-1 text-sm space-y-2">
                    {(data as any).same_address_companies.map((c: any) => (
                      <div key={`po-sameaddr-${c.id}`}>
                        <div className="font-medium">{c.firma_unvani || c.unvan || 'Bilinmeyen Firma'}</div>
                        <div className="text-[12px] text-slate-700">MERSİS: {c.mersis_number || c.mersis_number_ocr || '-'}</div>
                        <div className="text-[12px] text-slate-700">{c.adres || c.address || '-'}</div>
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="mt-1 text-sm text-slate-700">Aynı adres üzerinden ilişki bulunamadı.</div>
                )}
              </div>
            )}

            {Array.isArray((data as any)?.registry_related_companies) && (
              <div className="mt-4">
                <div className="text-base font-semibold">İlişkiler (MERSİS/Sicil)</div>
                {(data as any).registry_related_companies.length ? (
                  <div className="mt-1 text-sm space-y-2">
                    {(data as any).registry_related_companies.map((c: any) => (
                      <div key={`po-regrel-${c.id}`}>
                        <div className="font-medium">{c.firma_unvani || c.unvan || 'Bilinmeyen Firma'}</div>
                        <div className="text-[12px] text-slate-700">MERSİS: {c.mersis_number || c.mersis_number_ocr || '-'}</div>
                        {c.adres || c.address ? <div className="text-[12px] text-slate-700">{c.adres || c.address}</div> : null}
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="mt-1 text-sm text-slate-700">MERSİS/Sicil üzerinden ilişki bulunamadı.</div>
                )}
              </div>
            )}

            {Array.isArray((data as any)?.related_companies) && (
              <div className="mt-4">
                <div className="text-base font-semibold">İlişkiler (Ortak Kişiler)</div>
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
                  return (
                    <div className="mt-1 text-sm space-y-2">
                      {strong.length > 0 && (
                        <div>
                          <div className="font-semibold">İsim + Kimlik ile eşleşenler (yüksek güven)</div>
                          {strong.map((rc: any) => (
                            <div key={`po-rel-strong-${rc.id}`}>
                              <span className="font-medium">{rc.firma_unvani || rc.unvan || 'Şirket'}</span>
                              {Array.isArray(rc.shared_persons) && rc.shared_persons.length > 0 ? (
                                <span> • {rc.shared_persons.length} ortak kişi</span>
                              ) : null}
                            </div>
                          ))}
                        </div>
                      )}
                      {weak.length > 0 && (
                        <div>
                          <div className="font-semibold">Sadece Kimlik ile eşleşenler</div>
                          {weak.map((rc: any) => (
                            <div key={`po-rel-weak-${rc.id}`}>
                              <span className="font-medium">{rc.firma_unvani || rc.unvan || 'Şirket'}</span>
                              {Array.isArray(rc.shared_persons) && rc.shared_persons.length > 0 ? (
                                <span> • {rc.shared_persons.length} ortak kişi</span>
                              ) : null}
                            </div>
                          ))}
                        </div>
                      )}
                    </div>
                  );
                })()}
              </div>
            )}
          </div>
        )}

        <style jsx global>{`
          @media print {
            /* Sayfanın geri kalanını tamamen gizle, sadece modal basılsın */
            body.print-company-modal * { display: none !important; }
            body.print-company-modal .company-modal-print-target,
            body.print-company-modal .company-modal-print-target * { display: initial !important; }
            body.print-company-modal .company-modal-print-target { display: block !important; width: 100% !important; }

            /* Tek sütun zorla ve tüm içerikleri dikey akışa çevir */
            .company-modal-print-target { width: 100% !important; }
            .company-modal-print-target .sticky { position: static !important; top: auto !important; }
            .company-modal-print-target .backdrop-blur { backdrop-filter: none !important; }
            .company-modal-print-target .grid { display: block !important; }
            .company-modal-print-target [class*="grid-cols-"] { grid-template-columns: 1fr !important; }
            .company-modal-print-target .grid > * { width: 100% !important; }
            .company-modal-print-target .flex { flex-direction: column !important; align-items: stretch !important; }
            .company-modal-print-target .flex > * { width: 100% !important; }
            .company-modal-print-target .truncate { overflow: visible !important; text-overflow: initial !important; white-space: normal !important; }
            .company-modal-print-target .overflow-auto, 
            .company-modal-print-target .overflow-y-auto, 
            .company-modal-print-target .overflow-x-auto { overflow: visible !important; }
            .company-modal-print-target .max-h-64, 
            .company-modal-print-target .max-h-72, 
            .company-modal-print-target .max-h-60, 
            .company-modal-print-target .max-h-[85vh] { max-height: none !important; }
            /* Kart/öğe kırılmalarını engelle */
            .company-modal-print-target .print-avoid-break { break-inside: avoid !important; page-break-inside: avoid !important; }
            /* Yalnızca print-linear kalsın: tüm içerikleri gizle, print-linear ve altını yeniden göster */
            .company-modal-print-target * { display: none !important; }
            .company-modal-print-target .print-linear, 
            .company-modal-print-target .print-linear * { display: initial !important; }
            .company-modal-print-target .print-linear { display: block !important; }
          }
        `}</style>
      </DialogContent>

      {/* Error Reporting Modal */}
      <ReportErrorModal
        open={reportErrorOpen}
        onOpenChange={setReportErrorOpen}
        companyId={companyId || ''}
        companyName={company?.unvan || ''}
      />
    </Dialog>
  );
}
