'use client';

import React from 'react';

// Grup portresi: 9 kişi (3-3-3), net insan silüetleri, marka paleti, hafif parallax
export default function TeamIllustrationGroup({ className = '' }: { className?: string }) {
  return (
    <div className={(className ? className + ' ' : '') + 'relative mx-auto w-full max-w-5xl'}>
      <svg
        viewBox="0 0 960 520"
        role="img"
        aria-label="Sicilius Ekibi — grup portresi illüstrasyonu"
        className="w-full h-auto"
      >
        <defs>
          {/* Marka degrade */}
          <linearGradient id="brand" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stopColor={`hsl(var(--primary))`} />
            <stop offset="100%" stopColor={`hsl(var(--secondary))`} />
          </linearGradient>

          {/* Yumuşak arka plan dalgaları */}
          <linearGradient id="backWave" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" stopColor={`hsl(var(--primary) / 0.12)`} />
            <stop offset="100%" stopColor={`hsl(var(--secondary) / 0.10)`} />
          </linearGradient>

          {/* Kıyafet/ten tonları için yumuşak degrade */}
          <linearGradient id="cloth" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stopColor={`hsl(var(--primary) / 0.85)`} />
            <stop offset="100%" stopColor={`hsl(var(--secondary) / 0.80)`} />
          </linearGradient>
          <linearGradient id="skin" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stopColor={`hsl(26 80% 82% / 0.85)`} />
            <stop offset="100%" stopColor={`hsl(12 62% 72% / 0.85)`} />
          </linearGradient>

          {/* Tuval/grain dokusu */}
          <filter id="grain" x="-20%" y="-20%" width="140%" height="140%">
            <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="1" seed="3" result="g" />
            <feColorMatrix in="g" type="matrix" values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 .10 0" />
            <feBlend in2="SourceGraphic" mode="overlay" />
          </filter>
        </defs>

        {/* Arka plan */}
        <rect x="0" y="0" width="960" height="520" fill="url(#backWave)" />
        <ellipse cx="480" cy="468" rx="360" ry="20" fill="currentColor" opacity="0.06" />

        {/* 1. sıra (arka) — 3 kişi */}
        <g transform="translate(160, 130)" className="parallax-slow">
          {[
            { x: 0, w: 120 },
            { x: 320, w: 130 },
            { x: 640, w: 120 },
          ].map((p, i) => (
            <g key={i} transform={`translate(${p.x}, 0)`}>
              {/* shoulders/torso */}
              <path d={`M${-p.w/2} 110 Q0 60 ${p.w/2} 110 L${p.w/2} 180 L${-p.w/2} 180 Z`} fill="url(#cloth)" opacity="0.9" />
              {/* head */}
              <ellipse cx="0" cy="56" rx="34" ry="42" fill="url(#skin)" />
              {/* hair (stilize) */}
              <path d="M-36 52 Q0 18 36 52 Q18 28 -18 22 Z" fill="hsl(var(--primary) / 0.65)" />
              {/* collar highlight */}
              <path d={`M${-p.w/2+8} 112 Q0 82 ${p.w/2-8} 112`} stroke="white" strokeOpacity="0.18" strokeWidth="3" fill="none" />
            </g>
          ))}
        </g>

        {/* 2. sıra (orta) — 3 kişi */}
        <g transform="translate(120, 210)" className="parallax">
          {[
            { x: 0, w: 140 },
            { x: 360, w: 150 },
            { x: 720, w: 140 },
          ].map((p, i) => (
            <g key={i} transform={`translate(${p.x}, 0)`}>
              <path d={`M${-p.w/2} 120 Q0 66 ${p.w/2} 120 L${p.w/2} 192 L${-p.w/2} 192 Z`} fill="url(#cloth)" />
              <ellipse cx="0" cy="64" rx="36" ry="44" fill="url(#skin)" />
              {/* farklı saç stilleri */}
              {i === 0 && <path d="M-38 60 Q0 16 38 60 Q28 36 -12 26 Z" fill="hsl(var(--secondary) / 0.65)" />}
              {i === 1 && <path d="M-40 54 Q0 6 40 54 L40 40 Q0 0 -40 40 Z" fill="hsl(var(--primary) / 0.7)" />}
              {i === 2 && <path d="M-36 58 Q0 22 36 58 Q-6 36 6 28 Z" fill="hsl(var(--primary) / 0.6)" />}
              <path d={`M${-p.w/2+10} 124 Q0 90 ${p.w/2-10} 124`} stroke="white" strokeOpacity="0.18" strokeWidth="3" fill="none" />
            </g>
          ))}
        </g>

        {/* 3. sıra (ön) — 3 kişi */}
        <g transform="translate(80, 300)" className="parallax-fast">
          {[
            { x: 0, w: 160 },
            { x: 400, w: 176 },
            { x: 800, w: 160 },
          ].map((p, i) => (
            <g key={i} transform={`translate(${p.x}, 0)`}>
              <path d={`M${-p.w/2} 132 Q0 78 ${p.w/2} 132 L${p.w/2} 208 L${-p.w/2} 208 Z`} fill="url(#cloth)" />
              <ellipse cx="0" cy="74" rx="40" ry="48" fill="url(#skin)" />
              {/* saç varyasyonları */}
              {i === 0 && <path d="M-42 70 Q0 18 42 70 Q24 22 -6 16 Z" fill="hsl(var(--secondary) / 0.7)" />}
              {i === 1 && <path d="M-44 64 Q0 8 44 64 L44 46 Q0 -4 -44 46 Z" fill="hsl(var(--primary))" opacity="0.75" />}
              {i === 2 && <path d="M-40 66 Q0 20 40 66 Q-8 30 12 24 Z" fill="hsl(var(--primary) / 0.68)" />}
              <path d={`M${-p.w/2+12} 136 Q0 100 ${p.w/2-12} 136`} stroke="white" strokeOpacity="0.2" strokeWidth="3.2" fill="none" />
            </g>
          ))}
        </g>

        {/* İnce çerçeve ve grain */}
        <rect x="10" y="10" width="940" height="500" rx="18" stroke="currentColor" strokeOpacity="0.10" fill="none" />
        <rect x="0" y="0" width="960" height="520" fill="transparent" filter="url(#grain)" />
      </svg>

      <style jsx>{`
        .parallax-slow { animation: drift 18s ease-in-out infinite; }
        .parallax { animation: drift 14s ease-in-out infinite; }
        .parallax-fast { animation: drift 10s ease-in-out infinite; }
        @keyframes drift { 0% { transform: translateY(0px) } 50% { transform: translateY(-6px) } 100% { transform: translateY(0px) } }
        @media (prefers-reduced-motion: reduce) {
          .parallax-slow, .parallax, .parallax-fast { animation: none; }
        }
      `}</style>
    </div>
  );
}
