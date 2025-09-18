export default function TableSkeleton({ rows = 6 }: { rows?: number }) {
  return (
    <div className="rounded-md border bg-white dark:bg-slate-900 dark:border-slate-700 overflow-hidden">
      <div className="grid grid-cols-4 gap-0 px-4 py-3 border-b bg-slate-50 dark:bg-slate-900 text-sm text-slate-600 dark:text-slate-300 dark:border-slate-700">
        <div>Unvan</div>
        <div>Eşleşme</div>
        <div>Şehir</div>
        <div className="text-right">Son Güncelleme</div>
      </div>
      <ul className="divide-y dark:divide-slate-800">
        {Array.from({ length: rows }).map((_, i) => (
          <li key={i} className="grid grid-cols-4 gap-0 px-4 py-3 animate-pulse">
            <div className="h-4 bg-slate-200 dark:bg-slate-700 rounded w-3/4" />
            <div className="h-4 bg-slate-200 dark:bg-slate-700 rounded w-12" />
            <div className="h-4 bg-slate-200 dark:bg-slate-700 rounded w-24" />
            <div className="h-4 bg-slate-200 dark:bg-slate-700 rounded w-28 ml-auto" />
          </li>
        ))}
      </ul>
      <div className="px-4 py-2 text-xs text-slate-400 dark:text-slate-500 bg-slate-50 dark:bg-slate-900">Yükleniyor…</div>
    </div>
  );
}
