"use client";

import React from "react";

export default function WhySiciliusAnimated({ className = "" }: { className?: string }) {
  return (
    <div className={(className ? className + " " : "") + "relative overflow-hidden rounded-xl border border-border/60 bg-card/60 shadow-soft h-96"} aria-hidden>
      {/* UI skeleton (left) */}
      <div className="absolute inset-y-0 left-0 w-[54%] p-5 flex flex-col gap-4">
        {/* search */}
        <div className="h-10 rounded-xl shimmer bg-muted/50 border border-border/60" />
        {/* filters */}
        <div className="flex gap-3">
          <div className="h-8 w-24 rounded-full bg-muted/40 shimmer" />
          <div className="h-8 w-20 rounded-full bg-muted/40 shimmer" />
          <div className="h-8 w-28 rounded-full bg-muted/40 shimmer" />
        </div>
        {/* result list */}
        <div className="flex-1 space-y-3 pr-2 overflow-hidden">
          {Array.from({ length: 6 }).map((_, i) => (
            <div key={i} className="relative h-12 rounded-xl bg-muted/30 border border-border/50">
              <div className="absolute inset-0 rounded-xl highlight" style={{ animationDelay: `${i * 0.6}s` }} />
            </div>
          ))}
        </div>
      </div>

      {/* Network + map (right) */}
      <svg viewBox="0 0 600 400" className="absolute inset-0 w-full h-full">
        <defs>
          <pattern id="grid-sic" width="30" height="30" patternUnits="userSpaceOnUse">
            <path d="M 30 0 L 0 0 0 30" fill="none" stroke="currentColor" opacity="0.06" />
          </pattern>
        </defs>
        <rect width="600" height="400" fill="url(#grid-sic)" className="text-foreground" />

        {/* links (draw animation) */}
        <g stroke="currentColor" strokeOpacity="0.2" strokeWidth="2" className="text-foreground">
          {[{ x1: 360, y1: 110, x2: 470, y2: 170 }, { x1: 470, y1: 170, x2: 520, y2: 260 }, { x1: 420, y1: 250, x2: 520, y2: 260 }, { x1: 360, y1: 110, x2: 420, y2: 250 }].map((l, i) => (
            <line key={i} x1={l.x1} y1={l.y1} x2={l.x2} y2={l.y2} className="path-draw" style={{ animationDelay: `${i * 0.5}s` }} />
          ))}
        </g>

        {/* nodes (pulse) */}
        <g className="text-foreground">
          {[
            { cx: 360, cy: 110, r: 9 },
            { cx: 470, cy: 170, r: 10 },
            { cx: 520, cy: 260, r: 8 },
            { cx: 420, cy: 250, r: 9 },
          ].map((n, i) => (
            <g key={i}>
              <circle cx={n.cx} cy={n.cy} r={n.r} fill="currentColor" opacity="0.8" />
              <circle cx={n.cx} cy={n.cy} r={n.r + 10} fill="currentColor" opacity="0.08" className="ring-pulse" style={{ animationDelay: `${i * 0.8}s` }} />
            </g>
          ))}
        </g>

        {/* map pins (right-bottom) */}
        <g>
          {[
            { tx: 540, ty: 140, color: "var(--secondary)" },
            { tx: 320, ty: 300, color: "var(--accent)" },
          ].map((p, i) => (
            <g key={i} transform={`translate(${p.tx}, ${p.ty})`}>
              <circle r="9" fill={`hsl(${p.color})`} opacity="0.85" />
              <circle r="18" fill={`hsl(${p.color})`} opacity="0.2" className="pin-ping" style={{ animationDelay: `${i * 0.7}s` }} />
              <path d="M0,10 L-4,20 L4,20 Z" fill={`hsl(${p.color})`} opacity="0.7" />
            </g>
          ))}
        </g>
      </svg>

      {/* moving magnifier (sweeps over right side) */}
      <div className="lens" />

      <style jsx>{`
        .shimmer { position: relative; overflow: hidden; }
        .shimmer::after {
          content: ""; position: absolute; inset: 0; transform: translateX(-100%);
          background: linear-gradient(90deg, transparent, rgba(255,255,255,0.25), transparent);
          animation: shimmer 1.8s infinite;
        }
        @keyframes shimmer { 100% { transform: translateX(100%); } }

        .highlight { background: linear-gradient(90deg, rgba(59,130,246,0.13), rgba(59,130,246,0.22)); opacity: 0; }
        .highlight { animation: highlight 3s ease-in-out infinite; }
        @keyframes highlight { 10%{opacity:.9} 35%{opacity:.15} 100%{opacity:0} }

        .path-draw { stroke-dasharray: 180; stroke-dashoffset: 180; animation: draw 2.2s ease forwards; }
        @keyframes draw { to { stroke-dashoffset: 0; } }

        .ring-pulse { animation: ring 2.4s ease-out infinite; transform-origin: center; }
        @keyframes ring { 0%{transform:scale(0.6);opacity:.25} 60%{transform:scale(1.15);opacity:.06} 100%{opacity:0} }

        .pin-ping { animation: ping 2s cubic-bezier(0,0,.2,1) infinite; transform-origin: center; }
        @keyframes ping { 0% { transform: scale(1); opacity:.25 } 80%,100% { transform: scale(1.8); opacity: 0; } }

        .lens {
          position: absolute; top: 12%; left: 58%; width: 82px; height: 82px; border-radius: 9999px;
          border: 2px solid hsl(var(--primary)); background: rgba(255,255,255,0.06); backdrop-filter: blur(2px);
          animation: sweep 6s ease-in-out infinite;
        }
        @keyframes sweep {
          0% { transform: translate(0,0); }
          25% { transform: translate(40px, 60px); }
          50% { transform: translate(80px, 10px); }
          75% { transform: translate(-10px, 80px); }
          100% { transform: translate(0,0); }
        }
      `}</style>
    </div>
  );
}
