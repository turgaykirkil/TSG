'use client';

import { useEffect, useMemo, useRef, useState } from 'react';
import SearchBar from './components/SearchBar';
import SearchHints from './components/SearchHints';
import QueryInsights from './components/QueryInsights';
import ResultStats from './components/ResultStats';
import ThemeToggle from './components/ThemeToggle';
import { Clock, Heart, UserPlus } from 'lucide-react';
import { useUnifiedSearchInfinite } from '@/hooks/useUnifiedSearchInfinite';
import { useDailyUsage } from '@/hooks/useDailyUsage';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription, DialogFooter } from '@/components/ui/dialog';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
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
  const { data: unifiedPages, isFetching, isError, error, fetchNextPage, hasNextPage, isFetchingNextPage } = useUnifiedSearchInfinite(query);
  const firstPage = unifiedPages?.pages?.[0];
  const companies = unifiedPages?.pages ? unifiedPages.pages.flatMap((p) => p.companies || []) : [];
  const persons = firstPage?.persons ?? [];
  const historyEntries = firstPage?.history ?? [];
  const totalMatches = firstPage?.total_matches ?? undefined;
  // İlk yükleme mi? (henüz hiç veri yokken isFetching)
  const hasAnyResults = (companies.length + persons.length + historyEntries.length) > 0;
  const initialLoading = isFetching && !hasAnyResults;
  const [submitted, setSubmitted] = useState(false);
  const history = useSearchHistory();
  const [mobileOpen, setMobileOpen] = useState(false);
  // Sol sidebar tamamen kaldırıldı; sağ çekmece (drawer) kullanılıyor
  const inputRef = useRef<HTMLInputElement>(null);
  const [detailOpen, setDetailOpen] = useState(false);
  const [selectedCompanyId, setSelectedCompanyId] = useState<string | undefined>(undefined);
  const sentinelRef = useRef<HTMLDivElement | null>(null);
  const { data: daily, loading: usageLoading } = useDailyUsage();
  const [inviteOpen, setInviteOpen] = useState(false);
  const [inviteEmail, setInviteEmail] = useState('');
  const [inviteResult, setInviteResult] = useState<{ token: string } | null>(null);
  const [inviteBusy, setInviteBusy] = useState(false);
  const [limitOpen, setLimitOpen] = useState(false);

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

  // Sonsuz kaydırma: sentinel görünür olunca bir sonraki sayfayı çek
  useEffect(() => {
    if (!submitted || !query.trim()) return;
    const el = sentinelRef.current;
    if (!el) return;
    const observer = new IntersectionObserver((entries) => {
      const entry = entries[0];
      if (entry.isIntersecting && hasNextPage && !isFetchingNextPage) {
        fetchNextPage();
      }
    }, { root: null, rootMargin: '200px', threshold: 0 });
    observer.observe(el);
    return () => observer.disconnect();
  }, [submitted, query, hasNextPage, isFetchingNextPage, fetchNextPage]);

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
      {/* Toolbar – Desktop (top-right) */}
      {!detailOpen && (
      <div className="hidden md:flex fixed top-3 right-3 z-20 items-center gap-2">
        <button
          type="button"
          aria-label="Arama geçmişi"
          className="rounded-full p-2.5 bg-white/90 dark:bg-slate-900/90 border border-slate-200 dark:border-slate-700 text-slate-700 dark:text-slate-200 shadow hover:bg-white dark:hover:bg-slate-900"
          onClick={() => setMobileOpen(true)}
          data-testid="mobile-history-button"
        >
          <span className="relative inline-flex">
            <Clock size={18} />
            {history.items.length > 0 && (
              <span className="absolute -top-0.5 -right-0.5 h-2 w-2 rounded-full bg-blue-500 ring-2 ring-white dark:ring-slate-900" aria-hidden />
            )}
          </span>
        </button>
        <ThemeToggle fixed={false} />
        <Button
          type="button"
          onClick={() => setInviteOpen(true)}
          variant="gradientText"
          className="rounded-full px-3 py-2 shadow"
        >
          Davet Et
        </Button>
      </div>
      )}

      {/* Toolbar – Mobile (bottom-right) */}
      {!detailOpen && (
      <div className="md:hidden fixed bottom-3 right-3 z-20 flex items-center gap-2">
        <button
          type="button"
          aria-label="Arama geçmişi"
          className="rounded-full p-2.5 bg-white/90 dark:bg-slate-900/90 border border-slate-200 dark:border-slate-700 text-slate-700 dark:text-slate-200 shadow hover:bg-white dark:hover:bg-slate-900"
          onClick={() => setMobileOpen(true)}
          data-testid="mobile-history-button"
        >
          <span className="relative inline-flex">
            <Clock size={18} />
            {history.items.length > 0 && (
              <span className="absolute -top-0.5 -right-0.5 h-2 w-2 rounded-full bg-blue-500 ring-2 ring-white dark:ring-slate-900" aria-hidden />
            )}
          </span>
        </button>
        <ThemeToggle fixed={false} />
        <button
          type="button"
          onClick={() => setInviteOpen(true)}
          aria-label="Davet Et"
          className="rounded-full p-2.5 bg-white/90 dark:bg-slate-900/90 border border-slate-200 dark:border-slate-700 text-slate-700 dark:text-slate-200 shadow hover:bg-white dark:hover:bg-slate-900"
        >
          <UserPlus size={18} />
        </button>
      </div>

      )}

      {/* Usage badge – Desktop (top-right under toolbar) */}
      {!detailOpen && (
      <div className="hidden md:block fixed top-16 right-3 z-10 rounded-full px-3 py-1 text-xs font-medium border border-slate-200 dark:border-slate-700 bg-white/90 dark:bg-slate-900/90 text-slate-700 dark:text-slate-200">
        {usageLoading ? 'Kullanım yükleniyor…' : `Kalan: ${daily?.remaining ?? 0}/${daily?.limit ?? 20}`}
      </div>
      )}

      {/* Usage badge – Mobile (above bottom toolbar) */}
      {!detailOpen && (
      <div className="md:hidden fixed bottom-16 right-3 z-10 rounded-full px-3 py-1 text-xs font-medium border border-slate-200 dark:border-slate-700 bg-white/90 dark:bg-slate-900/90 text-slate-700 dark:text-slate-200">
        {usageLoading ? 'Kullanım yükleniyor…' : `Kalan: ${daily?.remaining ?? 0}/${daily?.limit ?? 20}`}
      </div>
      )}
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
            capped={companies.length > SEARCH_MAX_COMPANIES}
            capSize={SEARCH_MAX_COMPANIES}
          />
        )}
        {submitted && query.trim() && (companies.length > SEARCH_MAX_COMPANIES) && (
          <div className="mx-auto max-w-5xl w-full mb-3">
            <div className="rounded-md border border-amber-200 dark:border-amber-900 bg-amber-50 dark:bg-amber-950 text-amber-900 dark:text-amber-100 px-3 py-2 text-xs md:text-sm">
              Aramanız çok sayıda şirkete karşılık geliyor. Liste, en iyi {SEARCH_MAX_COMPANIES} sonucu gösterecek şekilde sınırlandırıldı. Daha hedefli sonuçlar için aramanıza mahalle/cadde, şehir veya sicil no gibi ayrıntılar ekleyebilirsiniz. Devam etmek için alttaki “Daha fazla yükle” butonunu kullanabilirsiniz.
            </div>
          </div>
        )}
        {isError && (
          <div className="mx-auto max-w-5xl text-sm text-red-600" role="alert">
            {(error as Error)?.message || 'Arama sırasında bir hata oluştu.'}
          </div>
        )}

        {/* Başlangıç boş durumu gösterme: kullanıcı arama yapmadıysa hiç kart gösterme */}

        {submitted && query.trim() && initialLoading && (
          <div className="mx-auto max-w-5xl">
            <TableSkeleton rows={6} />
          </div>
        )}

        {submitted && query.trim() && !initialLoading && !isError && (companies.length + persons.length + historyEntries.length === 0) && (
          <div className="mx-auto max-w-5xl">
            <EmptyState type="no-results" query={query} />
          </div>
        )}

        {submitted && query.trim() && !isError && (companies.length + persons.length + historyEntries.length > 0) && (
          <div className="mx-auto max-w-5xl space-y-8">
            {/* Şirketler */}
            <CompaniesTable companies={companies} onSelectCompany={handleSelectCompany} />
            {hasNextPage && (
              <div className="flex justify-center mt-2">
                <Button
                  type="button"
                  variant="gradientText"
                  className="px-4 py-2 text-sm rounded"
                  onClick={() => fetchNextPage()}
                  disabled={isFetchingNextPage}
                  data-testid="load-more"
                >
                  {isFetchingNextPage ? 'Yükleniyor...' : 'Daha fazla yükle'}
                </Button>
              </div>
            )}
            {/* Sentinel: Görününce otomatik olarak bir sonraki sayfayı getirir */}
            {hasNextPage && (
              <div ref={sentinelRef} aria-hidden className="h-6" data-testid="infinite-sentinel" />
            )}

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
      {/* Davet Dialog */}
      <Dialog open={inviteOpen} onOpenChange={setInviteOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>E-posta ile Davet Et</DialogTitle>
            <DialogDescription>
              Aylık davet hakkı: mevcut kullanıcı ayda yalnızca 1 e-posta davet edebilir.
            </DialogDescription>
          </DialogHeader>
          {!inviteResult ? (
            <div className="space-y-4">
              <div>
                <label className="block text-sm mb-1">E-posta</label>
                <Input
                  type="email"
                  placeholder="ornek@alan.com"
                  value={inviteEmail}
                  onChange={(e) => setInviteEmail(e.target.value)}
                />
              </div>
              <DialogFooter>
                <Button
                  variant="gradientText"
                  onClick={async () => {
                    try {
                      setInviteBusy(true);
                      const res = await fetch('/api/v1/auth/invite', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        credentials: 'include',
                        body: JSON.stringify({ email: inviteEmail }),
                      });
                      const json = await res.json();
                      if (!res.ok) throw new Error(json?.detail || 'Davet oluşturulamadı');
                      setInviteResult({ token: json.token });
                    } catch (e: any) {
                      alert(e?.message || 'Bilinmeyen hata');
                    } finally {
                      setInviteBusy(false);
                    }
                  }}
                  disabled={!inviteEmail || inviteBusy}
                >
                  {inviteBusy ? 'Gönderiliyor…' : 'Davet Oluştur'}
                </Button>
              </DialogFooter>
            </div>
          ) : (
            <div className="space-y-3 text-sm">
              <p>Davet oluşturuldu. E-posta gönderimi henüz entegre edilmediği için bağlantıyı kendin iletebilirsin.</p>
              <div className="p-3 rounded border bg-slate-50 dark:bg-slate-900/40 break-all">
                {typeof window !== 'undefined' ? `${window.location.origin}/davet?token=${inviteResult.token}` : `/davet?token=${inviteResult.token}`}
              </div>
              <div className="flex gap-2">
                <Button
                  variant="outline"
                  onClick={() => {
                    const link = (typeof window !== 'undefined' ? `${window.location.origin}/davet?token=${inviteResult.token}` : `/davet?token=${inviteResult.token}`);
                    navigator.clipboard?.writeText(link).then(() => alert('Bağlantı kopyalandı'));
                  }}
                >Bağlantıyı Kopyala</Button>
                <Button variant="gradientText" onClick={() => setInviteOpen(false)}>Kapat</Button>
              </div>
            </div>
          )}
        </DialogContent>
      </Dialog>
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
        onLimitReached={() => setLimitOpen(true)}
      />
      {/* Günlük limit bilgilendirme dialogu */}
      <Dialog open={limitOpen} onOpenChange={setLimitOpen}>
        <DialogContent className="max-w-md">
          <DialogHeader>
            <DialogTitle>
              <span className="inline-flex items-center gap-2">
                <Heart size={18} className="text-emerald-600" />
                Günlük sorgu limitine ulaştınız
              </span>
            </DialogTitle>
            <DialogDescription>
              {`Kalan: ${daily?.remaining ?? 0}/${daily?.limit ?? 20}`} — Sistemlerimizin yavaşlamasını engellemek ve
              herkes için adil kullanım sağlamak amacıyla günlük bir sınır uyguluyoruz. Anlayışınız için teşekkür ederiz.
              Limitler her gece otomatik olarak sıfırlanır. Yarın görüşmek üzere!
            </DialogDescription>
          </DialogHeader>
          <div className="space-y-2 text-sm text-slate-600 dark:text-slate-300">
            <p>
              Sicilius bağımsız ve ücretsiz bir platformdur. Bilgiye erişiminizi kesintisiz ve adil bir şekilde
              sürdürebilmek için bu günlük sınırı uyguluyoruz.
            </p>
          </div>
          <DialogFooter>
            <Button variant="gradientText" onClick={() => setLimitOpen(false)}>Tamam</Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
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
