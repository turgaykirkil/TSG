"use client";

interface QueryInsightsProps {
  text: string;
  onPick?: (value: string) => void;
}

// Basit sezgisel etiketleyici (bilimsel değil, UX amaçlı ipucu üretir)
// - Maskeli TCKN, 11 haneli sayı, MERSİS, Sicil, İlan No, Şehir (küçük set)
const CITIES = [
  "İSTANBUL",
  "ANKARA",
  "İZMİR",
  "BURSA",
  "ANTALYA",
  "KOCAELİ",
  "KONYA",
];

function analyze(text: string): string[] {
  const raw = text || "";
  const t = raw.trim();
  if (!t) return [];
  const upper = t.toUpperCase();
  const tags: string[] = [];
  if (/\d{1,4}\*+\d{1,3}/.test(t)) tags.push("Maskeli TCKN/VKN");
  if (/\b\d{11}\b/.test(t)) tags.push("11 haneli kimlik");
  if (/MERSIS|MERSİS/i.test(t)) tags.push("MERSİS");
  if (/SICIL|SİCİL/i.test(t)) tags.push("Sicil No");
  if (/ILAN\s*NO|İLAN\s*NO/i.test(t)) tags.push("İlan No");
  if (/VKN|VERGI|VERGİ/i.test(t)) tags.push("VKN/Vergi");
  const foundCity = CITIES.find((c) => upper.includes(c));
  if (foundCity) tags.push(foundCity);
  return Array.from(new Set(tags));
}

export default function QueryInsights({ text, onPick }: QueryInsightsProps) {
  const tags = analyze(text);
  if (tags.length === 0) return null;
  return (
    <div className="mt-2 flex flex-wrap items-center justify-center gap-2">
      {tags.map((tag) => (
        <button
          type="button"
          key={tag}
          onClick={() => onPick?.(tag)}
          className="text-[11px] md:text-xs rounded-full border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 px-2.5 py-1 text-slate-600 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-800 shadow-sm"
          aria-label={`İpucu: ${tag}`}
        >
          {tag}
        </button>
      ))}
    </div>
  );
}
