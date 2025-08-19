'use client';

import HistoryItem from './HistoryItem';
import type { SearchEntry } from '../../hooks/useSearchHistory';
import ProfileCard from '@/app/(app)/dashboard/components/sidebar/ProfileCard';
import { useRef } from 'react';
import { PanelLeftClose } from 'lucide-react';

export default function HistorySidebar({
  items,
  onSelect,
  onRemove,
  onClear,
  onTogglePin,
  onCollapse,
}: {
  items: SearchEntry[];
  onSelect: (query: string) => void;
  onRemove: (id: string) => void;
  onClear: () => void;
  onTogglePin: (id: string) => void;
  onCollapse?: () => void;
}) {
  const asideRef = useRef<HTMLDivElement>(null);

  const onKeyDown: React.KeyboardEventHandler<HTMLDivElement> = (e) => {
    // Liste içinde ↑/↓ ve Enter
    if (!asideRef.current) return;
    if (!(e.key === 'ArrowDown' || e.key === 'ArrowUp' || e.key === 'Enter')) return;
    const items = asideRef.current.querySelectorAll<HTMLButtonElement>('[data-history-item] button[data-role="select"]');
    if (!items.length) return;
    if (e.key === 'Enter') {
      const el = document.activeElement as HTMLButtonElement | null;
      if (el && el.dataset.role === 'select' && el.dataset.query) {
        onSelect(el.dataset.query);
      }
      return;
    }
    e.preventDefault();
    const current = Array.from(items).findIndex((el) => el === document.activeElement);
    let next = current;
    if (e.key === 'ArrowDown') next = current < items.length - 1 ? current + 1 : 0;
    else next = current > 0 ? current - 1 : items.length - 1;
    (items[next] || items[0]).focus();
  };

  return (
    <aside
      className="hidden lg:sticky lg:top-0 lg:flex lg:h-screen min-h-0 lg:flex-col lg:w-72 xl:w-80 border-r border-slate-200/70 bg-white/60 backdrop-blur-sm"
      role="complementary"
      aria-label="Arama geçmişi"
      ref={asideRef as unknown as React.RefObject<HTMLDivElement>}
      onKeyDown={onKeyDown}
    >
      <div className="flex items-center justify-between px-4 pt-4 pb-2">
        <h2 id="history-heading-desktop" className="text-sm font-semibold text-slate-700 text-left">Geçmiş Aramalar</h2>
        <div className="flex items-center gap-2">
          <button
            type="button"
            className="text-xs text-slate-500 hover:text-slate-700"
            onClick={() => {
              if (confirm('Tüm geçmişi temizlemek istediğine emin misin?')) onClear();
            }}
          >
            Temizle
          </button>
          {onCollapse && (
            <button
              type="button"
              className="hidden lg:inline-flex h-7 w-7 items-center justify-center rounded border border-slate-200 text-slate-600 hover:bg-slate-50"
              aria-label="Paneli daralt"
              title="Paneli daralt"
              onClick={onCollapse}
            >
              <PanelLeftClose size={16} />
            </button>
          )}
        </div>
      </div>
      <div className="flex-1 overflow-y-auto px-3 pb-4">
        {items.length === 0 ? (
          <div className="text-xs text-slate-400 px-2 py-2" role="status" aria-live="polite">Henüz bir geçmiş yok</div>
        ) : (
          <ul className="space-y-1.5" role="list" aria-labelledby="history-heading-desktop">
            {items.map((it) => (
              <li key={it.id}>
                <HistoryItem entry={it} onSelect={onSelect} onRemove={onRemove} onTogglePin={onTogglePin} />
              </li>
            ))}
          </ul>
        )}
      </div>
      <div className="mt-auto p-4 border-t border-slate-200/70">
        <ProfileCard />
      </div>
    </aside>
  );
}
