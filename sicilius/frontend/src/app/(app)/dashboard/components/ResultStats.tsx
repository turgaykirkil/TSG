"use client";

import { useEffect, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";

function CountUp({ value, duration = 0.6 }: { value: number; duration?: number }) {
  const [display, setDisplay] = useState(0);
  useEffect(() => {
    const start = performance.now();
    const from = display;
    const to = value;
    const diff = to - from;
    const tick = (t: number) => {
      const p = Math.min(1, (t - start) / (duration * 1000));
      setDisplay(Math.round(from + diff * p));
      if (p < 1) requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [value]);
  return <span>{display}</span>;
}

interface ResultStatsProps {
  companies: number;
  persons: number;
  history: number;
  query: string;
  capped?: boolean; // en iyi N gösteriliyor
  capSize?: number; // N
}

export default function ResultStats({
  companies,
  persons,
  history,
  query,
  capped,
  capSize,
}: ResultStatsProps) {
  const total = companies + persons + history;
  return (
    <AnimatePresence>
      <motion.div
        initial={{ opacity: 0, y: -6 }}
        animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0, y: -6 }}
        transition={{ duration: 0.2 }}
        className="mx-auto max-w-5xl w-full pb-2 md:pb-3"
      >
        <div className="flex flex-wrap items-center justify-between gap-2 text-sm text-slate-600 dark:text-slate-300">
          <div className="flex items-center gap-3">
            <div className="inline-flex items-center gap-1.5 rounded-full border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 px-3 py-1 shadow-sm">
              <span className="font-medium">Toplam</span>
              <CountUp value={total} />
            </div>
            <div className="inline-flex items-center gap-1.5 rounded-full border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 px-3 py-1 shadow-sm">
              <span>Şirket</span>
              <CountUp value={companies} />
            </div>
            <div className="inline-flex items-center gap-1.5 rounded-full border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 px-3 py-1 shadow-sm">
              <span>Kişi</span>
              <CountUp value={persons} />
            </div>
            <div className="inline-flex items-center gap-1.5 rounded-full border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 px-3 py-1 shadow-sm">
              <span>Geçmiş</span>
              <CountUp value={history} />
            </div>
          </div>
          <div className="flex items-center gap-2">
            {capped && (
              <span className="inline-flex items-center rounded-full border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 px-2 py-0.5 text-[11px] md:text-xs text-slate-600 dark:text-slate-300">
                En iyi {capSize} şirket
              </span>
            )}
            <span className="truncate text-xs md:text-sm text-slate-500 dark:text-slate-400">"{query}" için sonuçlar</span>
          </div>
        </div>
      </motion.div>
    </AnimatePresence>
  );
}
