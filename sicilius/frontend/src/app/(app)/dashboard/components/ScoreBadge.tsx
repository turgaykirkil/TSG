"use client";

export default function ScoreBadge({ score }: { score?: number }) {
  if (typeof score !== "number") return <span>-</span>;
  const s = Math.max(0, Math.min(100, Math.round(score)));
  let cls = "bg-slate-100 text-slate-700 border-slate-200";
  if (s >= 95) cls = "bg-gradient-to-r from-emerald-500 to-blue-500 text-white border-transparent shadow-sm";
  else if (s >= 88) cls = "bg-gradient-to-r from-blue-600 to-cyan-500 text-white border-transparent shadow-sm";
  else if (s >= 80) cls = "bg-gradient-to-r from-indigo-600 to-blue-500 text-white border-transparent shadow-sm";
  else if (s >= 70) cls = "bg-gradient-to-r from-violet-600 to-indigo-500 text-white border-transparent shadow-sm";
  else if (s >= 60) cls = "bg-amber-100 text-amber-800 border-amber-200";
  return (
    <span
      className={
        "inline-flex items-center justify-center rounded-full border px-2.5 py-0.5 text-xs font-semibold transition-colors " +
        cls
      }
      title="Eşleşme kuvveti"
    >
      {s}
    </span>
  );
}
