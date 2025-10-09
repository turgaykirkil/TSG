'use client';

import React from 'react';

// Monoline (tek çizgi) ekip illüstrasyonu — premium, minimal ve marka uyumlu
export default function TeamIllustrationMonoline({ className = '' }: { className?: string }) {
  return (
    <div className={(className ? className + ' ' : '') + 'relative mx-auto w-full max-w-4xl'}>
      <svg
        viewBox="0 0 960 420"
        role="img"
        aria-label="Sicilius Ekibi — monoline illüstrasyon"
        className="w-full h-auto"
      >
        <defs>
          <linearGradient id="brandStroke" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stopColor={`hsl(var(--primary))`} />
            <stop offset="100%" stopColor={`hsl(var(--secondary))`} />
          </linearGradient>
          <linearGradient id="bgWave" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" stopColor={`hsl(var(--primary) / 0.08)`} />
            <stop offset="100%" stopColor={`hsl(var(--secondary) / 0.06)`} />
          </linearGradient>
          <pattern id="softGrid" width="24" height="24" patternUnits="userSpaceOnUse">
            <path d="M24 0H0V24" fill="none" stroke="currentColor" strokeOpacity="0.06" />
          </pattern>
        </defs>

        {/* Arka plan: soft grid + dalga */}
        <rect x="0" y="0" width="960" height="420" fill="url(#softGrid)" />
        <path d="M0,300 C200,260 320,360 520,320 C720,280 820,360 960,330 L960,420 L0,420 Z" fill="url(#bgWave)" />

        {/* Alt gölge */}
        <ellipse cx="480" cy="370" rx="360" ry="18" fill="currentColor" opacity="0.06" />

        {/* Tek çizgi ekip kompozisyonu */}
        <g transform="translate(80, 80)" strokeWidth="2.5" fill="none" strokeLinecap="round" strokeLinejoin="round">
          {/* Sol grup (2 kişi + cihaz) */}
          <path
            className="draw"
            stroke="url(#brandStroke)"
            d="M40 160 q40 -40 80 0 q-24 0 -24 28 q0 28 24 28 q44 0 72 -44 q-8 -12 -8 -24 q0 -42 44 -70 q26 18 26 44 q0 18 -12 30 q22 24 64 24"
          />
          {/* Orta grup (lider silüet + masa) */}
          <path
            className="draw"
            stroke="url(#brandStroke)"
            d="M300 190 q26 -26 56 -26 q38 0 62 26 q-10 6 -10 20 q0 26 28 26 q44 0 66 -38 q-8 -14 -8 -26 q0 -20 12 -36 q18 -20 48 -30"
          />
          {/* Sağ grup (2 kişi + pano) */}
          <path
            className="draw"
            stroke="url(#brandStroke)"
            d="M560 150 q30 -30 64 -30 q34 0 64 30 q-14 8 -14 22 q0 26 30 26 q30 0 56 -26 q-6 -18 -6 -28 q0 -24 18 -40 q30 -18 68 -22"
          />

          {/* İnce detaylar: ekran çerçeveleri (stroke tek çizgi devamı hissi) */}
          <path className="fade" stroke="currentColor" strokeOpacity="0.25" d="M118 126 h62 q10 0 10 10 v42 q0 10 -10 10 h-62 q-10 0 -10 -10 v-42 q0 -10 10 -10 z" />
          <path className="fade" stroke="currentColor" strokeOpacity="0.25" d="M382 118 h86 q10 0 10 10 v54 q0 10 -10 10 h-86 q-10 0 -10 -10 v-54 q0 -10 10 -10 z" />
          <path className="fade" stroke="currentColor" strokeOpacity="0.25" d="M706 130 h78 q10 0 10 10 v46 q0 10 -10 10 h-78 q-10 0 -10 -10 v-46 q0 -10 10 -10 z" />
        </g>

        {/* Parıltı vurgu (ince) */}
        <g opacity="0.18">
          <ellipse cx="240" cy="210" rx="140" ry="14" fill={`hsl(var(--primary))`} />
          <ellipse cx="480" cy="230" rx="160" ry="14" fill={`hsl(var(--secondary))`} />
          <ellipse cx="720" cy="210" rx="140" ry="14" fill={`hsl(var(--primary))`} />
        </g>

        {/* İnce çerçeve */}
        <rect x="10" y="10" width="940" height="400" rx="16" stroke="currentColor" strokeOpacity="0.10" fill="none" />
      </svg>

      <style jsx>{`
        .draw {
          stroke-dasharray: 900;
          stroke-dashoffset: 900;
          animation: draw 3.6s ease-in-out forwards;
        }
        .fade { opacity: 0; animation: fade 0.9s 1.2s ease forwards; }
        @keyframes draw { to { stroke-dashoffset: 0; } }
        @keyframes fade { to { opacity: 1; } }
        @media (prefers-reduced-motion: reduce) {
          .draw, .fade { animation: none; stroke-dashoffset: 0; opacity: 1; }
        }
      `}</style>
    </div>
  );
}
