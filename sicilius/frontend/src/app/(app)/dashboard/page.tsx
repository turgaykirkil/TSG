'use client';

import { useEffect, useMemo, useRef, useState } from 'react';
import SearchBar from './components/SearchBar';
import { useUnifiedSearch } from '@/hooks/useUnifiedSearch';
import EmptyState from './components/EmptyState';
import HistorySidebar from './components/sidebar/HistorySidebar';
import { useSearchHistory } from './hooks/useSearchHistory';
import MobileHistoryDrawer from './components/sidebar/MobileHistoryDrawer';
import { Menu, PanelLeftOpen, PanelLeftClose } from 'lucide-react';
import CompanyDetailModal from './components/CompanyDetailModal';
import CompaniesTable from './components/tables/CompaniesTable';
import PeopleTable from './components/tables/PeopleTable';
import CompanyHistoryTable from './components/tables/CompanyHistoryTable';

export default function DashboardPage() {
  const [query, setQuery] = useState('');
  const [draft, setDraft] = useState('');
  const { data: unified, isFetching, isError, error } = useUnifiedSearch(query);
  const companies = unified?.companies ?? [];
  const persons = unified?.persons ?? [];
  const historyEntries = unified?.history ?? [];
  const [submitted, setSubmitted] = useState(false);
  const history = useSearchHistory();
  const [mobileOpen, setMobileOpen] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(false);
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
    <div
      className={
        "min-h-screen lg:h-screen relative overflow-x-hidden lg:overflow-x-hidden lg:grid " +
        (sidebarOpen ? "lg:grid-cols-[18rem_1fr]" : "lg:grid-cols-[0_1fr]") +
        " lg:gap-6"
      }
    >
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
      {/* Desktop history open toggle (only when closed) */}
      {!sidebarOpen && (
        <button
          type="button"
          className="hidden lg:flex fixed left-4 top-4 z-40 rounded-full bg-white/80 backdrop-blur px-3 py-2 shadow border border-slate-200 text-slate-700"
          onClick={() => setSidebarOpen(true)}
          aria-label={'Geçmiş panelini aç'}
        >
          <PanelLeftOpen size={18} className="inline mr-2" />
          Geçmiş
        </button>
      )}
      {/* Sidebar grid column (kept present for layout) */}
      <div className="hidden lg:block lg:h-full">
        {sidebarOpen ? (
          <HistorySidebar
            items={history.items}
            onSelect={handleSelectFromHistory}
            onRemove={history.remove}
            onClear={history.clear}
            onTogglePin={history.togglePin}
            onCollapse={() => setSidebarOpen(false)}
          />
        ) : null}
      </div>
      <div className="flex flex-col gap-6 px-4 lg:px-6 min-h-0 lg:h-screen lg:overflow-y-auto">
      {/* Hero / Centered Search */}
      <section
        className={
          "relative overflow-hidden grid transition-all duration-500 ease-out " +
          (submitted ? "min-h-[10vh] place-content-start justify-items-center pt-1" : "min-h-[68vh] place-content-center")
        }
      >
        <div className="mx-auto w-full max-w-screen-2xl text-center px-4">
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
          <div className={
            "mt-4 transition-all duration-500 " + (submitted ? "mt-0.5" : "mt-4")
          }>
            <div className={submitted ? "sticky top-2 z-40 w-full searchbar-compact" : "flex justify-center"}>
              <div className="mx-auto w-full max-w-xl">
              <SearchBar
              value={draft}
              onChange={setDraft}
              onSubmit={handleSubmit}
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
            />
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Results */}
      <section id="results" data-testid="results" aria-live="polite" aria-busy={isFetching} className={"min-h-[200px] flex-1 bg-transparent pb-16 " + (submitted ? "pt-4" : "") }>
        {isError && (
          <div className="mx-auto max-w-5xl text-sm text-red-600" role="alert">
            {(error as Error)?.message || 'Arama sırasında bir hata oluştu.'}
          </div>
        )}

        {/* Başlangıç boş durumu gösterme: kullanıcı arama yapmadıysa hiç kart gösterme */}

        {submitted && query.trim() && isFetching && (
          <div className="mx-auto max-w-5xl text-sm text-muted-foreground">Aranıyor…</div>
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
