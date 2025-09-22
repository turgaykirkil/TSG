'use client';

import { useState, useEffect } from 'react';
import { Search, X } from 'lucide-react';
import { Button } from '@/components/ui/button';
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
  suggestions?: string[];
  onPickSuggestion?: (value: string) => void;
  disableSuggestions?: boolean;
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
  suggestions = [],
  onPickSuggestion,
  disableSuggestions = false,
}: SearchBarProps) {
  const [input, setInput] = useState(value);
  // Placeholder typing animation state
  const [tp, setTp] = useState({ phraseIndex: 0, charIndex: 0, deleting: false });
  const [typedPlaceholder, setTypedPlaceholder] = useState('');
  const showShortcutHint = input.length === 0;
  const [sel, setSel] = useState<number>(-1); // selected suggestion index
  const [focused, setFocused] = useState(false);

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
    if (sel >= 0 && filtered.length > 0) {
      const pick = filtered[sel];
      onPickSuggestion?.(pick);
      setFocused(false);
      return;
    }
    onSubmit?.(input.trim());
    setFocused(false);
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

  // Suggestions filtering (case-insensitive distinct)
  const q = input.trim();
  const filtered = q.length
    ? Array.from(new Set(
        (suggestions || [])
          .filter(Boolean)
          .map((s) => String(s))
          .filter((s) => s.toLowerCase().includes(q.toLowerCase()))
      )).slice(0, 8)
    : [];

  const onKeyDown: React.KeyboardEventHandler<HTMLInputElement> = (e) => {
    if (!filtered.length) return;
    if (e.key === 'ArrowDown') {
      e.preventDefault();
      setSel((v) => (v + 1) % filtered.length);
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      setSel((v) => (v <= 0 ? filtered.length - 1 : v - 1));
    } else if (e.key === 'Enter' && sel >= 0) {
      e.preventDefault();
      const pick = filtered[sel];
      onPickSuggestion?.(pick);
      setFocused(false);
    } else if (e.key === 'Escape') {
      setSel(-1);
      setFocused(false);
    }
  };

  const highlight = (text: string, query: string) => {
    const i = text.toLowerCase().indexOf(query.toLowerCase());
    if (i === -1) return text;
    const before = text.slice(0, i);
    const match = text.slice(i, i + query.length);
    const after = text.slice(i + query.length);
    return (
      <>
        {before}
        <mark className="bg-amber-100 text-inherit rounded px-0.5">{match}</mark>
        {after}
      </>
    );
  };

  return (
    <form onSubmit={handleSubmit} role="search" aria-label="Genel arama" aria-controls="results" className={"w-full " + (className ?? '')}>
      <div className="relative rounded-full bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 shadow-sm transition-all duration-150 ease-out focus-within:shadow-md focus-within:scale-[1.005]">
        <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400" size={20} aria-hidden />
        <SimpleTooltip content={<span>Kısayollar: <kbd>/</kbd>, <kbd>⌘K</kbd>, <kbd>Ctrl K</kbd></span>}>
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onFocus={() => setFocused(true)}
            onBlur={() => setTimeout(() => setFocused(false), 120)}
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
            className="w-full rounded-full bg-white dark:bg-slate-900 text-slate-900 dark:text-slate-100 pl-12 pr-28 py-3 md:py-3 text-sm md:text-base outline-none transition focus-visible:ring-2 focus-visible:ring-slate-300 dark:focus-visible:ring-slate-600"
            onKeyDown={onKeyDown}
          />
        </SimpleTooltip>
        {input && (
          <button
            type="button"
            onClick={clear}
            aria-label="Aramayı temizle"
            className="absolute right-20 top-1/2 -translate-y-1/2 rounded-full p-2 text-slate-500 hover:bg-slate-100 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-slate-300"
          >
            <X size={16} />
          </button>
        )}
        <Button
          type="submit"
          aria-label="Ara"
          variant="gradientText"
          className="absolute right-3 top-1/2 -translate-y-1/2 px-4 py-2 text-sm font-medium"
        >
          Ara
        </Button>
      </div>
      {filtered.length > 0 && focused && !disableSuggestions && (
        <div className="absolute mt-1 w-full max-w-inherit z-40">
          <div className="rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 shadow-lg overflow-hidden">
            <ul role="listbox" aria-label="Öneriler">
              {filtered.map((s, i) => (
                <li key={`${s}-${i}`}>
                  <button
                    type="button"
                    role="option"
                    aria-selected={sel === i}
                    className={`w-full text-left px-3 py-2 text-sm hover:bg-slate-50 dark:hover:bg-slate-800 ${sel === i ? 'bg-slate-50 dark:bg-slate-800' : ''}`}
                    onMouseEnter={() => setSel(i)}
                    onMouseLeave={() => setSel(-1)}
                    onClick={() => { onPickSuggestion?.(s); setFocused(false); }}
                    title={s}
                  >
                    {highlight(s, q)}
                  </button>
                </li>
              ))}
            </ul>
          </div>
        </div>
      )}
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
