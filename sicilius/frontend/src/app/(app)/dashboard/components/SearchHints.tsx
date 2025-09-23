"use client";

interface SearchHintsProps {
  onPick: (query: string) => void;
}

const HINTS: string[] = [
  "BARLAK AND BARLAK İÇ VE DIŞ TİCARET LİMİTED ŞİRKETİ",
  "pars global",
  "675******38",
  "67572947938",
  "MERSİS 0************",
  "İstanbul",
  "Ankara",
  "Anonim Şirketi",
  "LİMİTED ŞİRKETİ",
  "İlan No 2024/12345",
  "Sicil No 123456",
];

export default function SearchHints({ onPick }: SearchHintsProps) {
  return (
    <div className="mt-3 flex flex-wrap items-center justify-center gap-2">
      {HINTS.map((h) => (
        <button
          key={h}
          type="button"
          onClick={() => onPick(h)}
          className="text-xs md:text-[13px] rounded-full border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 px-3 py-1.5 text-slate-600 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-800 shadow-sm"
          aria-label={`Öneri: ${h}`}
        >
          {h}
        </button>
      ))}
    </div>
  );
}
