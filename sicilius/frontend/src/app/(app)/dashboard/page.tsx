'use client';

import { useEffect, useMemo, useRef, useState } from 'react';
import SearchBar from './components/SearchBar';
import SearchHints from './components/SearchHints';
import QueryInsights from './components/QueryInsights';
import ResultStats from './components/ResultStats';
import ThemeToggle from './components/ThemeToggle';
import { Clock } from 'lucide-react';
import { useUnifiedSearch } from '@/hooks/useUnifiedSearch';
import { SEARCH_MAX_COMPANIES } from '@/config/constants';
import EmptyState from './components/EmptyState';
import { useSearchHistory } from './hooks/useSearchHistory';
import MobileHistoryDrawer from './components/sidebar/MobileHistoryDrawer';
import CompanyDetailModal from './components/CompanyDetailModal';
import CompaniesTable from './components/tables/CompaniesTable';
import PeopleTable from './components/tables/PeopleTable';
import CompanyHistoryTable from './components/tables/CompanyHistoryTable';
import TableSkeleton from './components/tables/TableSkeleton';

export default function DashboardPage() {
  const [query, setQuery] = useState('');
  const [draft, setDraft] = useState('');
  const { data: unified, isFetching, isError, error } = useUnifiedSearch(query);
  const companies = unified?.companies ?? [];
  const persons = unified?.persons ?? [];
  const historyEntries = unified?.history ?? [];
  const totalMatches = unified?.total_matches ?? undefined;
  const [submitted, setSubmitted] = useState(false);
  const history = useSearchHistory();
  const [mobileOpen, setMobileOpen] = useState(false);
  // Sol sidebar tamamen kaldırıldı; sağ çekmece (drawer) kullanılıyor
  const inputRef = useRef<HTMLInputElement>(null);
  const [detailOpen, setDetailOpen] = useState(false);
  const [selectedCompanyId, setSelectedCompanyId] = useState<string | undefined>(undefined);

  // Hero altında typing animasyonu için tek kaynaklı cümle listesi
  const phrases = useMemo(
    () => [
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
    ],
    []
  );
  
  // Typeahead kaynakları: geçmiş + mevcut şirket unvanları + temel etiketler
  const typeaheadSuggestions = useMemo(() => {
    const fromHistory = (history.items || []).map((i) => i.query).filter(Boolean);
    const fromCompanies = (companies || [])
      .map((c: any) => c?.firma_unvani || c?.unvan || '')
      .filter((s: string) => !!s);
    const basics = [
      'MERSİS', 'Sicil No', 'İlan No', 'Anonim Şirketi', 'Limited Şirketi',
      'İstanbul', 'Ankara', 'İzmir', 'Bursa', 'Antalya'
    ];
    return Array.from(new Set([...fromHistory, ...fromCompanies, ...basics]));
  }, [history.items, companies]);
  

  // Submit ile küçült/yukarı taşı ve sonuçlara kaydır
  const handleSubmit = (q: string) => {
    const v = q.trim();
    setQuery(v);
    setDraft(v);
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

  const handleSelectCompany = (id: string) => {
    setSelectedCompanyId(id);
    setDetailOpen(true);
  };

  // Input tamamen temizlenirse (submit etmeden) hero tekrar büyüsün
  useEffect(() => {
    if (!draft.trim()) setSubmitted(false);
  }, [draft]);

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
    <div className={"min-h-screen relative overflow-x-hidden bg-slate-50 text-slate-900 dark:bg-slate-950 dark:text-slate-100"}>
      {isFetching && <div className="top-progress" aria-hidden />}
      {/* Skip link: klavye ile hızlı erişim */}
      <a
        href="#results"
        className="sr-only focus:not-sr-only focus:fixed focus:top-2 focus:left-2 focus:z-50 focus:px-3 focus:py-2 focus:bg-white focus:text-slate-900 focus:shadow focus:rounded"
      >
        Sonuçlara atla
      </a>
      {/* Üst sağ sabit aksiyonlar */}
      <button
        type="button"
        aria-label="Arama geçmişi"
        className="fixed top-4 right-4 z-50 rounded-full p-2.5 bg-white/90 dark:bg-slate-900/90 border border-slate-200 dark:border-slate-700 text-slate-700 dark:text-slate-200 shadow hover:bg-white dark:hover:bg-slate-900"
        onClick={() => setMobileOpen(true)}
      >
        <span className="relative inline-flex">
          <Clock size={18} />
          {history.items.length > 0 && (
            <span className="absolute -top-0.5 -right-0.5 h-2 w-2 rounded-full bg-blue-500 ring-2 ring-white dark:ring-slate-900" aria-hidden />
          )}
        </span>
      </button>
      <ThemeToggle />
      <div className="flex flex-col gap-6 px-4 lg:px-6">
      {/* Hero / Centered Search */}
      <section
        className={
          "relative overflow-hidden grid transition-all duration-500 ease-out " +
          (submitted ? "min-h-[10vh] place-content-start justify-items-center pt-1" : "min-h-[68vh] place-content-center")
        }
      >
        <div className="mx-auto w-full max-w-screen-2xl text-center px-4">
          {!submitted && (
            <div
              className={
                "transition-all duration-500 ease-out " +
                (submitted ? "scale-95 -translate-y-1" : "scale-100 translate-y-0")
              }
            >
              <h1 className="text-4xl md:text-5xl font-semibold tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-[#0A192F] via-[#1E3A8A] to-[#0EA5E9]">
                Sicilius
              </h1>
            </div>
          )}
          <div className={
            "mt-4 transition-all duration-500 " + (submitted ? "mt-0.5" : "mt-4")
          }>
            <div className={submitted ? "sticky top-6 z-40 w-full searchbar-compact" : "flex justify-center"}>
              <div className="mx-auto w-full max-w-lg search-spotlight">
              <SearchBar
              value={draft}
              onChange={setDraft}
              onSubmit={handleSubmit}
              onPickSuggestion={(q) => handleSubmit(q)}
              onClear={() => {
                setDraft('');
                setQuery('');
                setSubmitted(false);
              }}
              className={
                "mx-auto w-full transition-all duration-500 " +
                (submitted ? "max-w-xl" : "max-w-screen-2xl")
              }
              inputRef={inputRef}
              placeholderPhrases={phrases}
              rotateIntervalMs={1800}
              suggestions={typeaheadSuggestions}
              disableSuggestions={submitted || isFetching}
            />
              {!submitted && !draft.trim() && (
                <SearchHints onPick={(q) => handleSubmit(q)} />
              )}
              {!submitted && !!draft.trim() && (
                <QueryInsights text={draft} onPick={(q) => handleSubmit(q)} />
              )}
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Results */}
      <section id="results" data-testid="results" aria-live="polite" aria-busy={isFetching} className={"min-h-[200px] flex-1 bg-transparent pb-16 " + (submitted ? "pt-2" : "") }>
        {submitted && query.trim() && (
          <ResultStats
            companies={companies.length}
            persons={persons.length}
            history={historyEntries.length}
            query={query}
            capped={typeof totalMatches === 'number' ? totalMatches > companies.length : companies.length >= SEARCH_MAX_COMPANIES}
            capSize={SEARCH_MAX_COMPANIES}
          />
        )}
        {isError && (
          <div className="mx-auto max-w-5xl text-sm text-red-600" role="alert">
            {(error as Error)?.message || 'Arama sırasında bir hata oluştu.'}
          </div>
        )}

        {/* Başlangıç boş durumu gösterme: kullanıcı arama yapmadıysa hiç kart gösterme */}

        {submitted && query.trim() && isFetching && (
          <div className="mx-auto max-w-5xl">
            <TableSkeleton rows={6} />
          </div>
        )}

        {submitted && query.trim() && !isFetching && !isError && (companies.length + persons.length + historyEntries.length === 0) && (
          <div className="mx-auto max-w-5xl">
            <EmptyState type="no-results" query={query} />
          </div>
        )}

        {submitted && query.trim() && !isFetching && !isError && (companies.length + persons.length + historyEntries.length > 0) && (
          <div className="mx-auto max-w-5xl space-y-8">
            {/* Şirketler */}
            <CompaniesTable companies={companies} onSelectCompany={handleSelectCompany} />

            {/* Kişiler */}
            {persons.length > 0 && (
              <section aria-label="Kişiler sonuçları">
                <div className="mb-2 text-sm font-semibold text-slate-700">Kişiler</div>
                <PeopleTable people={persons} />
              </section>
            )}

            {/* Geçmiş / Gazette Entries */}
            {historyEntries.length > 0 && (
              <section aria-label="Geçmiş sonuçları">
                <div className="mb-2 text-sm font-semibold text-slate-700">Gazete Geçmişi</div>
                <CompanyHistoryTable entries={historyEntries} />
              </section>
            )}
          </div>
        )}
      </section>
      <CompanyDetailModal
        open={detailOpen}
        onOpenChange={(o) => {
          setDetailOpen(o);
          if (!o) setSelectedCompanyId(undefined);
        }}
        companyId={selectedCompanyId}
        onOpenCompany={(id) => {
          if (!id) return;
          setSelectedCompanyId(id);
          setDetailOpen(true);
        }}
      />
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
