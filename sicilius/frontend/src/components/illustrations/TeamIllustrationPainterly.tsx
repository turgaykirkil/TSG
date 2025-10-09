'use client';

import React from 'react';

// Painterly (yağlıboya hissi) ekip illüstrasyonu
// - Marka paletine uyumlu degrade katmanlar
// - Fırça/tuval dokusu için SVG filter (feTurbulence + feDisplacementMap)
// - Hafif parallax/float; prefers-reduced-motion'a saygı
export default function TeamIllustrationPainterly({ className = '' }: { className?: string }) {
  return (
    <div className={(className ? className + ' ' : '') + 'relative mx-auto w-full max-w-5xl'}>
      <svg
        viewBox="0 0 960 520"
        role="img"
        aria-label="Sicilius Ekibi — yağlıboya illüstrasyon"
        className="w-full h-auto"
      >
        <defs>
          {/* Marka degrade */}
          <linearGradient id="brandGrad" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stopColor={`hsl(var(--primary))`} />
            <stop offset="100%" stopColor={`hsl(var(--secondary))`} />
          </linearGradient>

          {/* Sıcak ve soğuk tonlar (katman vurguları) */}
          <linearGradient id="warm" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stopColor={`hsl(var(--primary) / 0.85)`} />
            <stop offset="100%" stopColor={`hsl(var(--secondary) / 0.75)`} />
          </linearGradient>
          <linearGradient id="cool" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stopColor={`hsl(220 25% 72% / 0.35)`} />
            <stop offset="100%" stopColor={`hsl(260 38% 62% / 0.35)`} />
          </linearGradient>

          {/* Işık lekesi */}
          <radialGradient id="lightSpot" cx="50%" cy="35%" r="60%">
            <stop offset="0%" stopColor={`hsl(var(--primary) / 0.10)`} />
            <stop offset="100%" stopColor="transparent" />
          </radialGradient>

          {/* Tuval dokusu */}
          <filter id="canvas" x="-20%" y="-20%" width="140%" height="140%">
            <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" stitchTiles="stitch" result="noise" />
            <feColorMatrix in="noise" type="saturate" values="0" />
            <feComponentTransfer>
              <feFuncA type="table" tableValues="0 0.06" />
            </feComponentTransfer>
            <feBlend in2="SourceGraphic" mode="multiply" />
          </filter>

          {/* Fırça kılları/bozulma */}
          <filter id="bristle" x="-20%" y="-20%" width="140%" height="140%">
            <feTurbulence type="fractalNoise" baseFrequency="0.02" numOctaves="3" seed="3" result="turb" />
            <feDisplacementMap in="SourceGraphic" in2="turb" scale="6" xChannelSelector="R" yChannelSelector="G" />
          </filter>

          {/* Hafif film/grain */}
          <filter id="grain" x="-20%" y="-20%" width="140%" height="140%">
            <feTurbulence type="fractalNoise" baseFrequency="0.8" numOctaves="1" seed="7" result="g" />
            <feColorMatrix in="g" type="matrix" values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 .12 0" />
            <feBlend in2="SourceGraphic" mode="overlay" />
          </filter>
        </defs>

        {/* Arka plan tabanı: ışık lekesi + tuval */}
        <rect x="0" y="0" width="960" height="520" fill="url(#lightSpot)" />
        <rect x="0" y="0" width="960" height="520" fill="transparent" filter="url(#canvas)" />

        {/* Arka fırça lekeleri (geniş, yumuşak) */}
        <g filter="url(#bristle)" opacity="0.85" className="layer-slow">
          <path d="M-40 300 C 160 220, 360 380, 560 320 S 920 360, 1000 340" fill="none" stroke="url(#cool)" strokeWidth="68" strokeLinecap="round" />
          <path d="M-60 360 C 180 300, 360 420, 580 380 S 920 420, 1040 380" fill="none" stroke="url(#warm)" strokeWidth="64" strokeLinecap="round" opacity="0.6" />
        </g>

        {/* Orta plan — pano/ekran soyut lekeleri */}
        <g filter="url(#grain)" opacity="0.9" className="layer">
          <rect x="120" y="120" width="240" height="140" rx="22" fill="url(#cool)" />
          <rect x="370" y="100" width="260" height="160" rx="24" fill="url(#warm)" opacity="0.7" />
          <rect x="650" y="130" width="210" height="130" rx="20" fill="url(#cool)" opacity="0.8" />
        </g>

        {/* Ön plan — ekip silüetleri (yağlıboya blob + kenar vurguları) */}
        <g filter="url(#bristle)" className="layer-fast">
          {[
            { x: 160, s: 0.96 },
            { x: 300, s: 1.05 },
            { x: 460, s: 1.18 }, // merkez
            { x: 620, s: 1.05 },
            { x: 760, s: 0.96 },
          ].map((p, i) => (
            <g key={i} transform={`translate(${p.x}, 300) scale(${p.s})`}>
              {/* torso blob */}
              <path d="M-60 40 C -40 -10, 40 -10, 60 40 C 64 80, -64 80, -60 40 Z" fill="url(#brandGrad)" opacity="0.92" />
              {/* head blob */}
              <path d="M-20 -6 C 0 -28, 32 -8, 20 18 C 10 36, -12 30, -20 12 Z" fill="url(#warm)" opacity="0.95" />
              {/* kenar vurgusu */}
              <path d="M-58 40 C -36 -4, 36 -4, 58 40" fill="none" stroke="white" strokeOpacity="0.14" strokeWidth="3" />
            </g>
          ))}
        </g>

        {/* İnce çerçeve */}
        <rect x="12" y="12" width="936" height="496" rx="18" stroke="currentColor" strokeOpacity="0.08" fill="none" />
      </svg>

      <style jsx>{`
        .layer { animation: drift 18s ease-in-out infinite; }
        .layer-slow { animation: drift 26s ease-in-out infinite; }
        .layer-fast { animation: drift 12s ease-in-out infinite; }
        @keyframes drift { 0% { transform: translateY(0px) } 50% { transform: translateY(-6px) } 100% { transform: translateY(0px) } }
        @media (prefers-reduced-motion: reduce) {
          .layer, .layer-slow, .layer-fast { animation: none; }
        }
      `}</style>
    </div>
  );
}
