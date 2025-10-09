'use client';
import React from "react";

// Basit, marka renklerine uyumlu ekip illüstrasyonu
// Light/Dark modda kontrastı korur, düşük animasyon (prefers-reduced-motion saygılı)
export default function TeamIllustration({ className = "" }: { className?: string }) {
  return (
    <div className={"relative mx-auto w-full max-w-3xl " + className}>
      <svg
        viewBox="0 0 960 520"
        role="img"
        aria-label="Sicilius Ekibi – stüdyo sahnesi"
        className="w-full h-auto"
      >
        <defs>
          {/* Marka degrade */}
          <linearGradient id="brand" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stopColor="hsl(var(--primary))" />
            <stop offset="100%" stopColor="hsl(var(--secondary))" />
          </linearGradient>

          {/* Ekran camı */}
          <linearGradient id="screen" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" stopColor="rgba(255,255,255,0.12)" />
            <stop offset="100%" stopColor="rgba(255,255,255,0.04)" />
          </linearGradient>

          {/* Grid pattern */}
          <pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse">
            <path d="M24 0H0V24" fill="none" stroke="currentColor" strokeOpacity="0.08" />
          </pattern>
        </defs>

        {/* Arka plan grid + marka dalgası */}
        <rect x="0" y="0" width="960" height="520" fill="url(#grid)" />
        <path d="M0,340 C200,300 320,420 520,380 C720,340 820,460 960,420 L960,520 L0,520 Z" fill="url(#brand)" opacity="0.12" />

        {/* Masa üstü gölge */}
        <ellipse cx="480" cy="468" rx="360" ry="24" fill="currentColor" opacity="0.08" />

        {/* Üç ekranlı UI sahnesi */}
        <g transform="translate(100, 90)">
          {/* Sol ekran: Arama & liste skeleton */}
          <g className="float-slow">
            <rect x="0" y="0" width="260" height="180" rx="14" fill="currentColor" opacity="0.06" />
            <rect x="0" y="0" width="260" height="180" rx="14" fill="url(#screen)" />
            {/* Search bar */}
            <rect x="18" y="22" width="200" height="16" rx="8" className="shimmer" />
            {/* List */}
            {[0,1,2,3,4].map((i) => (
              <g key={i} transform={`translate(18, ${54 + i*24})`}>
                <rect x="0" y="0" width="160" height="12" rx="6" className="shimmer" />
                <rect x="170" y="2" width="48" height="8" rx="4" fill="hsl(var(--primary) / 0.35)" />
              </g>
            ))}
          </g>

          {/* Orta ekran: İlişki grafiği */}
          <g transform="translate(280, -10)" className="float">
            <rect x="0" y="0" width="280" height="210" rx="16" fill="currentColor" opacity="0.06" />
            <rect x="0" y="0" width="280" height="210" rx="16" fill="url(#screen)" />
            {/* Edges */}
            <g stroke="hsl(var(--primary))" strokeOpacity="0.6" strokeWidth="2" fill="none" className="draw">
              <path d="M60 140 Q140 70 220 120" />
              <path d="M80 50 Q150 110 200 50" />
              <path d="M140 160 Q180 120 240 160" />
            </g>
            {/* Nodes */}
            {[{x:60,y:140},{x:220,y:120},{x:80,y:50},{x:200,y:50},{x:140,y:160},{x:240,y:160}].map((n, i) => (
              <circle key={i} cx={n.x} cy={n.y} r="7" fill="hsl(var(--primary))" className="pulse" />
            ))}
          </g>

          {/* Sağ ekran: Harita & pinler */}
          <g transform="translate(590, 10)" className="float-fast">
            <rect x="0" y="0" width="240" height="180" rx="14" fill="currentColor" opacity="0.06" />
            <rect x="0" y="0" width="240" height="180" rx="14" fill="url(#screen)" />
            {/* Basit kıta şekli */}
            <path d="M28 120 C54 88 120 70 150 82 C200 98 210 140 180 152 C150 164 88 160 54 148 Z" fill="hsl(var(--secondary) / 0.25)" />
            {/* Pinler */}
            {[{x:72,y:120},{x:136,y:96},{x:168,y:132}].map((p, i) => (
              <g key={i} transform={`translate(${p.x}, ${p.y})`}>
                <circle cx="0" cy="0" r="3" fill="hsl(var(--primary))" />
                <circle cx="0" cy="0" r="10" fill="hsl(var(--primary) / 0.18)" className="ping" />
              </g>
            ))}
          </g>
        </g>

        {/* Önde ekip avatarları */}
        <g transform="translate(120, 300)">
          {[
            { x: 0 }, { x: 120 }, { x: 240 }, { x: 360 }, { x: 480 }, { x: 600 }
          ].map((p, i) => (
            <g key={i} transform={`translate(${p.x}, 0)`} className="bob">
              {/* torso */}
              <rect x="-40" y="36" width="80" height="90" rx="18" fill="url(#brand)" />
              {/* head */}
              <g>
                <circle cx="0" cy="10" r="26" className="fill-white dark:fill-slate-950" />
                {/* eyes */}
                <rect x="-10" y="6" width="8" height="2" rx="1" className="fill-slate-400 dark:fill-slate-600 blink" />
                <rect x="2" y="6" width="8" height="2" rx="1" className="fill-slate-400 dark:fill-slate-600 blink" />
              </g>
              {/* name badge */}
              <rect x="-16" y="70" width="32" height="8" rx="4" className="fill-white/70 dark:fill-slate-900/70" />
            </g>
          ))}
        </g>

        {/* İnce çerçeve */}
        <rect x="12" y="12" width="936" height="496" rx="18" stroke="currentColor" strokeOpacity="0.10" fill="none" />
      </svg>

      {/* Stil */}
      <style jsx>{`
        /* Float/bob */
        .float { animation: float 6s ease-in-out infinite; }
        .float-slow { animation: float 8s ease-in-out infinite; }
        .float-fast { animation: float 4.8s ease-in-out infinite; }
        .bob { animation: bob 3.6s ease-in-out -0.6s infinite; }
        @keyframes float { 0%, 100% { transform: translateY(0px) } 50% { transform: translateY(-6px) } }
        @keyframes bob { 0%, 100% { transform: translateY(0px) } 50% { transform: translateY(-3px) } }

        /* Shimmer */
        .shimmer { fill: rgba(148,163,184,0.25); position: relative; }
        .shimmer { animation: shimmer 2.2s ease-in-out infinite; }
        @keyframes shimmer { 0% { opacity: 0.5 } 50% { opacity: 0.9 } 100% { opacity: 0.5 } }

        /* Pulse nodes */
        .pulse { animation: pulse 2s ease-in-out infinite; transform-origin: center; }
        @keyframes pulse { 0%,100% { transform: scale(1) } 50% { transform: scale(1.18) } }

        /* Draw edges */
        .draw path { stroke-dasharray: 140 280; animation: draw 5s ease-in-out infinite; }
        @keyframes draw { 0% { stroke-dashoffset: 280 } 50% { stroke-dashoffset: 70 } 100% { stroke-dashoffset: 280 } }

        /* Ping pins */
        .ping { animation: ping 2.2s ease-out infinite; transform-origin: center; }
        @keyframes ping { 0% { transform: scale(0.5); opacity: 0.6 } 80% { transform: scale(1.6); opacity: 0 } 100% { opacity: 0 } }

        /* Blink eyes */
        .blink { animation: blink 5s ease-in-out infinite; }
        @keyframes blink { 0%, 97%, 100% { transform: scaleY(1) } 98% { transform: scaleY(0.1) } 99% { transform: scaleY(1) } }

        @media (prefers-reduced-motion: reduce) {
          .float, .float-slow, .float-fast, .bob, .shimmer, .pulse, .draw path, .ping, .blink { animation: none; }
        }
      `}</style>
    </div>
  );
}
