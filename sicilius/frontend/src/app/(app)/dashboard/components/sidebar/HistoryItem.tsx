'use client';

import { Trash2, Pin, PinOff } from 'lucide-react';
import type { SearchEntry } from '../../hooks/useSearchHistory';

export default function HistoryItem({
  entry,
  onSelect,
  onRemove,
  onTogglePin,
}: {
  entry: SearchEntry;
  onSelect: (query: string) => void;
  onRemove: (id: string) => void;
  onTogglePin: (id: string) => void;
}) {
  return (
    <div
      className="group flex items-center gap-2 px-2 py-1.5 rounded-md hover:bg-white/60 focus-within:bg-white/60"
      data-history-item
    >
      <button
        type="button"
        className="flex-1 text-left truncate text-sm text-slate-700 hover:underline focus:outline-none"
        onClick={() => onSelect(entry.query)}
        title={entry.query}
        data-role="select"
        data-query={entry.query}
      >
        {entry.query}
      </button>
      <button
        type="button"
        aria-label={entry.pinned ? 'Sabitlemeyi kaldır' : 'Sabitle'}
        className={
          'invisible group-hover:visible group-focus-within:visible p-1 ' +
          (entry.pinned ? 'text-amber-600 hover:text-amber-700' : 'text-slate-500 hover:text-slate-700')
        }
        onClick={() => onTogglePin(entry.id)}
        title={entry.pinned ? 'Sabitlemeyi kaldır' : 'Sabitle'}
      >
        {entry.pinned ? <Pin size={16} /> : <PinOff size={16} />}
      </button>
      <button
        type="button"
        aria-label="Kayıt sil"
        className="invisible group-hover:visible group-focus-within:visible p-1 text-slate-500 hover:text-red-600"
        onClick={() => onRemove(entry.id)}
        title="Sil"
      >
        <Trash2 size={16} />
      </button>
    </div>
  );
}
