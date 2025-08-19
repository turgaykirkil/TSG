'use client';

import { useState, useEffect } from 'react';
import { Search, X } from 'lucide-react';
import SimpleTooltip from '@/components/ui/SimpleTooltip';

interface SearchBarProps {
  value?: string;
  placeholder?: string;
  onChange?: (value: string) => void;
  onSubmit?: (value: string) => void;
  onClear?: () => void;
  autoFocus?: boolean;
  className?: string;
  placeholderPhrases?: string[];
  rotateIntervalMs?: number;
  inputRef?: React.RefObject<HTMLInputElement>;
}

export default function SearchBar({
  value = '',
  placeholder = 'Şirket, kişi, TCKN/VKN veya unvan ara...',
  onChange,
  onSubmit,
  onClear,
  autoFocus = true,
  className,
  placeholderPhrases = [],
  rotateIntervalMs = 2000,
  inputRef,
}: SearchBarProps) {
  const [input, setInput] = useState(value);
  // Placeholder typing animation state
  const [tp, setTp] = useState({ phraseIndex: 0, charIndex: 0, deleting: false });
  const [typedPlaceholder, setTypedPlaceholder] = useState('');
  const showShortcutHint = input.length === 0;

  useEffect(() => {
    setInput(value);
  }, [value]);

  // Basit 300ms debounce
  const debouncedInput = useDebounce(input, 300);
  useEffect(() => {
    if (onChange) onChange(debouncedInput);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [debouncedInput]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit?.(input.trim());
  };

  const clear = () => {
    setInput('');
    onChange?.('');
    onClear?.();
  };

  // Typing animation for placeholder when input is empty
  useEffect(() => {
    if (!placeholderPhrases || placeholderPhrases.length === 0) return;
    // Pause typing when user is typing
    if (input.length > 0) {
      setTypedPlaceholder('');
      return;
    }

    const phrase = placeholderPhrases[tp.phraseIndex] ?? '';
    const isDeleting = tp.deleting;
    const delay = isDeleting ? 40 : 85; // typing speed

    const timer = setTimeout(() => {
      if (!isDeleting) {
        const next = tp.charIndex + 1;
        setTypedPlaceholder(phrase.slice(0, next));
        if (next === phrase.length) {
          // hold before deleting
          setTimeout(() => setTp({ ...tp, deleting: true, charIndex: phrase.length }), 700);
        } else {
          setTp({ ...tp, charIndex: next, deleting: false });
        }
      } else {
        const next = tp.charIndex - 1;
        setTypedPlaceholder(phrase.slice(0, next));
        if (next <= 0) {
          setTp({ phraseIndex: (tp.phraseIndex + 1) % placeholderPhrases.length, charIndex: 0, deleting: false });
        } else {
          setTp({ ...tp, charIndex: next, deleting: true });
        }
      }
    }, delay);

    return () => clearTimeout(timer);
  }, [tp, input, placeholderPhrases]);

  const placeholderToShow =
    input.length === 0 && placeholderPhrases.length > 0
      ? (typedPlaceholder || placeholderPhrases[0])
      : placeholder;

  return (
    <form onSubmit={handleSubmit} role="search" aria-label="Genel arama" aria-controls="results" className={"w-full " + (className ?? '')}>
      <div className="rounded-full p-[1.5px] animated-gradient-border">
        <div className="relative rounded-full bg-white animated-gradient-bg">
          <Search className="absolute left-5 top-1/2 -translate-y-1/2 text-slate-400" size={20} aria-hidden />
          <SimpleTooltip content={<span>Kısayollar: <kbd>/</kbd>, <kbd>⌘K</kbd>, <kbd>Ctrl K</kbd></span>}>
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder={placeholderToShow}
              autoFocus={autoFocus}
              aria-label="Arama"
              id="dashboard-search-input"
              data-testid="search-input"
              autoComplete="off"
              enterKeyHint="search"
              inputMode="search"
              aria-keyshortcuts="/ Control+K Meta+K"
              aria-describedby={showShortcutHint ? 'search-shortcut-hint' : undefined}
              ref={inputRef}
              title="Kısayol: / veya Cmd/Ctrl+K ile arama kutusuna odaklan"
              className="w-full rounded-full bg-white pl-12 pr-28 py-4 md:py-5 text-base md:text-lg shadow-sm outline-none ring-offset-background transition focus:border-transparent focus:shadow focus-visible:ring-2 focus-visible:ring-[#0A192F] focus-visible:ring-offset-2"
            />
          </SimpleTooltip>
          {input && (
            <button
              type="button"
              onClick={clear}
              aria-label="Aramayı temizle"
              className="absolute right-20 top-1/2 -translate-y-1/2 rounded-full p-2 text-slate-500 hover:bg-slate-100 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#0A192F] focus-visible:ring-offset-2"
            >
              <X size={16} />
            </button>
          )}
          <button
            type="submit"
            aria-label="Ara"
            className="absolute right-3 top-1/2 -translate-y-1/2 rounded-full px-4 py-2 text-white text-sm font-medium bg-gradient-to-r from-[#1E3A8A] to-[#0EA5E9] shadow-sm hover:opacity-95 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#0A192F] focus-visible:ring-offset-2"
          >
            Ara
          </button>
        </div>
      </div>
      {showShortcutHint && (
        <div id="search-shortcut-hint" className="flex justify-end mt-1 pr-1 select-none text-[11px] text-slate-500">
          <span className="hidden sm:inline">Kısayol:</span>
          <kbd className="ml-1 rounded border border-slate-300 bg-slate-50 px-1.5 py-[1px] text-[11px]">/</kbd>
          <span className="mx-1">veya</span>
          <kbd className="rounded border border-slate-300 bg-slate-50 px-1.5 py-[1px] text-[11px]">⌘K</kbd>
          <span className="mx-1">/</span>
          <kbd className="rounded border border-slate-300 bg-slate-50 px-1.5 py-[1px] text-[11px]">Ctrl K</kbd>
        </div>
      )}
    </form>
  );
}

function useDebounce<T>(value: T, delay = 300) {
  const [debounced, setDebounced] = useState(value);
  useEffect(() => {
    const id = setTimeout(() => setDebounced(value), delay);
    return () => clearTimeout(id);
  }, [value, delay]);
  return debounced;
}
