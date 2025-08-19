'use client';

import { useEffect, useRef } from 'react';
import { X } from 'lucide-react';
import type { SearchEntry } from '../../hooks/useSearchHistory';
import HistoryItem from './HistoryItem';
import ProfileCard from './ProfileCard';

export default function MobileHistoryDrawer({
  open,
  onClose,
  items,
  onSelect,
  onRemove,
  onClear,
  onTogglePin,
}: {
  open: boolean;
  onClose: () => void;
  items: SearchEntry[];
  onSelect: (query: string) => void;
  onRemove: (id: string) => void;
  onClear: () => void;
  onTogglePin: (id: string) => void;
}) {
  const panelRef = useRef<HTMLDivElement>(null);
  const lastFocusedRef = useRef<HTMLElement | null>(null);

  // ESC ile kapat ve focus'u geri yükle
  useEffect(() => {
    if (!open) return;
    const onKey = (e: KeyboardEvent) => {
      if (e.key === 'Escape') handleClose();
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [open]);

  // Drawer açıkken body scroll'u kilitle
  useEffect(() => {
    if (!open) return;
    const previous = document.body.style.overflow;
    document.body.style.overflow = 'hidden';
    return () => {
      document.body.style.overflow = previous;
    };
  }, [open]);

  // Açılınca focus-trap başlat, ilk odaklanabilir elemana odakla
  useEffect(() => {
    if (!open) return;
    lastFocusedRef.current = (document.activeElement as HTMLElement) || null;
    const t = setTimeout(() => {
      const focusables = panelRef.current?.querySelectorAll<HTMLElement>(
        'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
      );
      focusables && focusables[0]?.focus();
    }, 0);
    return () => clearTimeout(t);
  }, [open]);

  const trapKeyDown: React.KeyboardEventHandler<HTMLDivElement> = (e) => {
    if (!panelRef.current) return;
    if (e.key === 'Tab') {
      const focusables = panelRef.current.querySelectorAll<HTMLElement>(
        'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
      );
      if (!focusables.length) return;
      const first = focusables[0];
      const last = focusables[focusables.length - 1];
      if (e.shiftKey && document.activeElement === first) {
        e.preventDefault();
        last.focus();
      } else if (!e.shiftKey && document.activeElement === last) {
        e.preventDefault();
        first.focus();
      }
    }

    // Liste içinde ↑/↓ ile gezin, Enter ile seç
    if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
      e.preventDefault();
      const items = panelRef.current.querySelectorAll<HTMLButtonElement>(
        '[data-history-item] button[data-role="select"]'
      );
      if (!items.length) return;
      const current = Array.from(items).findIndex((el) => el === document.activeElement);
      let next = current;
      if (e.key === 'ArrowDown') next = current < items.length - 1 ? current + 1 : 0;
      else next = current > 0 ? current - 1 : items.length - 1;
      (items[next] || items[0]).focus();
    }

    if (e.key === 'Enter') {
      const el = document.activeElement as HTMLButtonElement | null;
      if (el && el.dataset.role === 'select' && el.dataset.query) {
        onSelect(el.dataset.query);
        handleClose();
      }
    }
  };

  const handleClose = () => {
    onClose();
    const last = lastFocusedRef.current;
    requestAnimationFrame(() => last?.focus());
  };

  return (
    <div className={`lg:hidden ${open ? 'fixed' : 'hidden'} inset-0 z-50`} aria-hidden={!open}>
      {/* backdrop */}
      <button
        aria-label="Kapat"
        className="absolute inset-0 bg-black/30 backdrop-blur-[1px]"
        onClick={handleClose}
      />
      {/* panel */}
      <div
        className="fixed inset-y-0 left-0 w-80 max-w-[85vw] bg-white shadow-xl flex flex-col"
        role="dialog"
        aria-modal="true"
        aria-labelledby="drawer-title"
        ref={panelRef}
        onKeyDown={trapKeyDown}
      >
        <div className="flex items-center justify-between p-4 border-b border-slate-200/70">
          <span id="drawer-title" className="text-sm font-semibold text-slate-700">Geçmiş</span>
          <button className="p-1 text-slate-600 hover:text-slate-900" aria-label="Kapat" onClick={handleClose}>
            <X size={18} />
          </button>
        </div>
        <div className="p-4 border-b border-slate-200/70">
          <ProfileCard />
        </div>
        <div className="flex items-center justify-between px-4 pt-4 pb-2">
          <h2 id="history-heading" className="text-sm font-semibold text-slate-700 text-left">Geçmiş Aramalar</h2>
          <button
            type="button"
            className="text-xs text-slate-500 hover:text-slate-700"
            onClick={() => {
              if (confirm('Tüm geçmişi temizlemek istediğine emin misin?')) onClear();
            }}
          >
            Temizle
          </button>
        </div>
        <div className="flex-1 overflow-y-auto px-3 pb-4">
          {items.length === 0 ? (
            <div className="text-xs text-slate-400 px-2 py-2" role="status" aria-live="polite">Henüz bir geçmiş yok</div>
          ) : (
            <ul className="space-y-1.5" role="list" aria-labelledby="history-heading">
              {items.map((it) => (
                <li key={it.id}>
                  <HistoryItem
                    entry={it}
                    onSelect={(q) => {
                      onSelect(q);
                      onClose();
                    }}
                    onRemove={onRemove}
                    onTogglePin={onTogglePin}
                  />
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>
    </div>
  );
}
