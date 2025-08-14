'use client';

import { useEffect, useRef, useState } from 'react';
import SearchBar from './components/SearchBar';
import { useUnifiedSearch } from '@/hooks/useUnifiedSearch';
import ResultsHeader from './components/ResultsHeader';
import { EntityTabs } from './components/EntityTabs';
import EmptyState from './components/EmptyState';
import HistorySidebar from './components/sidebar/HistorySidebar';
import { useSearchHistory } from './hooks/useSearchHistory';
import MobileHistoryDrawer from './components/sidebar/MobileHistoryDrawer';
import { Menu } from 'lucide-react';

export default function DashboardPage() {
  const [query, setQuery] = useState('');
  const { data: unified, isFetching, isError, error } = useUnifiedSearch(query);
  const companies = unified?.companies ?? [];
  const persons = unified?.persons ?? [];
  const historyEntries = unified?.history ?? [];
  const [submitted, setSubmitted] = useState(false);
  const history = useSearchHistory();
  const [mobileOpen, setMobileOpen] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);

  // Submit ile küçült/yukarı taşı ve sonuçlara kaydır
  const handleSubmit = (q: string) => {
    const v = q.trim();
    setQuery(v);
    const willSubmit = v.length > 0;
    setSubmitted(willSubmit);
    if (!willSubmit) return;
    // geçmişe ekle
    history.add(v);
    // Küçülme animasyonuna eşlik eden yumuşak kaydırma
    setTimeout(() => {
      const el = document.getElementById('results');
      if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }, 300);
  };

  const handleSelectFromHistory = (q: string) => {
    handleSubmit(q);
  };

  // Input tamamen temizlenirse hero tekrar büyüsün
  useEffect(() => {
    if (!query.trim()) setSubmitted(false);
  }, [query]);

  // '/' ile arama kutusuna odaklan (input/textarea içinde değilken)
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      const target = e.target as HTMLElement | null;
      const tag = (target?.tagName || '').toLowerCase();
      const isTyping = tag === 'input' || tag === 'textarea' || target?.isContentEditable;
      if (isTyping) return;
      if (e.key === '/' && !e.metaKey && !e.ctrlKey && !e.altKey) {
        e.preventDefault();
        inputRef.current?.focus();
      }
      // Cmd/Ctrl+K ile odaklan
      if ((e.key === 'k' || e.key === 'K') && (e.metaKey || e.ctrlKey)) {
        e.preventDefault();
        inputRef.current?.focus();
      }
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, []);

  return (
    <div className="min-h-screen relative overflow-hidden lg:grid lg:grid-cols-[18rem_1fr]">
      {/* Skip link: klavye ile hızlı erişim */}
      <a
        href="#results"
        className="sr-only focus:not-sr-only focus:fixed focus:top-2 focus:left-2 focus:z-50 focus:px-3 focus:py-2 focus:bg-white focus:text-slate-900 focus:shadow focus:rounded"
      >
        Sonuçlara atla
      </a>
      {/* Mobile history trigger */}
      <button
        type="button"
        className="lg:hidden fixed left-4 top-4 z-40 rounded-full bg-white/80 backdrop-blur px-3 py-2 shadow border border-slate-200 text-slate-700"
        data-testid="mobile-history-button"
        onClick={() => setMobileOpen(true)}
        aria-label="Geçmişi aç"
      >
        <Menu size={18} className="inline mr-2" /> Geçmiş
      </button>
      <HistorySidebar
        items={history.items}
        onSelect={handleSelectFromHistory}
        onRemove={history.remove}
        onClear={history.clear}
        onTogglePin={history.togglePin}
      />
      <div className="flex flex-col gap-6">
      {/* Hero / Centered Search */}
      <section
        className={
          "relative overflow-hidden grid transition-all duration-500 ease-out " +
          (submitted ? "min-h-[22vh] place-content-start pt-6" : "min-h-[68vh] place-content-center")
        }
      >
        <div className="mx-auto w-full max-w-screen-2xl text-center px-4">
          <div
            className={
              "transition-all duration-500 ease-out " +
              (submitted ? "scale-95 -translate-y-1" : "scale-100 translate-y-0")
            }
          >
            <h1 className="text-3xl md:text-4xl font-semibold tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-[#0A192F] via-[#1E3A8A] to-[#0EA5E9]">
              Sicilius Arama
            </h1>
          </div>
          <div className={
            "mt-4 transition-all duration-500 " + (submitted ? "mt-2" : "mt-4")
          }>
            <div className={submitted ? "sticky top-4 z-30" : ""}>
              <SearchBar
              value={query}
              onChange={setQuery}
              onSubmit={handleSubmit}
              className={
                "mx-auto w-full transition-all duration-500 " +
                (submitted ? "max-w-2xl" : "max-w-screen-2xl")
              }
              inputRef={inputRef}
              placeholderPhrases={[
                'Şirket ara',
                'Kişi ara',
                'TCKN ara',
                'VKN ara',
                'Unvan ara',
                'Adres ara',
                'Sicil No ara',
                'İlan No ara',
                'Gazete ara',
                'MERSİS ara',
              ]}
              rotateIntervalMs={1800}
            />
            </div>
          </div>
        </div>
      </section>

      {/* Results */}
      <section id="results" data-testid="results" aria-live="polite" aria-busy={isFetching} className="min-h-[200px] flex-1 bg-transparent pb-16">
        {isError && (
          <div className="mx-auto max-w-5xl text-sm text-red-600" role="alert">
            {(error as Error)?.message || 'Arama sırasında bir hata oluştu.'}
          </div>
        )}

        {/* Başlangıç boş durumu gösterme: kullanıcı arama yapmadıysa hiç kart gösterme */}

        {query.trim() && isFetching && (
          <div className="mx-auto max-w-5xl text-sm text-muted-foreground">Aranıyor…</div>
        )}

        {query.trim() && !isFetching && !isError && (companies.length + persons.length + historyEntries.length === 0) && (
          <div className="mx-auto max-w-5xl">
            <EmptyState type="no-results" query={query} />
          </div>
        )}

        {query.trim() && !isFetching && !isError && (companies.length + persons.length + historyEntries.length > 0) && (
          <div className="mx-auto max-w-5xl">
            <ResultsHeader title="Sonuçlar" count={companies.length + persons.length + historyEntries.length} />
            <EntityTabs companies={companies} persons={persons} history={historyEntries} />
          </div>
        )}
      </section>
      <MobileHistoryDrawer
        open={mobileOpen}
        onClose={() => setMobileOpen(false)}
        items={history.items}
        onSelect={handleSelectFromHistory}
        onRemove={history.remove}
        onClear={history.clear}
        onTogglePin={history.togglePin}
      />
      </div>
    </div>
  );
}
