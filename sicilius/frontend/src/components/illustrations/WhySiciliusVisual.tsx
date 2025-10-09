"use client";

import React from "react";

type Props = { className?: string };

export default function WhySiciliusVisual({ className = "" }: Props) {
  return (
    <div className={(className ? className + " " : "") + "grid grid-cols-1 md:grid-cols-2 gap-8 items-center"}>
      {/* UI Skeleton (no text) */}
      <div className="relative rounded-2xl border border-border/60 bg-card/60 backdrop-blur-sm p-6 shadow-soft overflow-hidden" aria-hidden>
        <div className="absolute -top-24 -left-24 w-72 h-72 rounded-full bg-primary/10 blur-3xl" />
        <div className="absolute -bottom-24 -right-24 w-72 h-72 rounded-full bg-secondary/10 blur-3xl" />
        <div className="relative space-y-4">
          {/* search bar */}
          <div className="h-10 rounded-xl bg-muted/60 border border-border/60 animate-pulse-slow" />
          {/* filters */}
          <div className="flex gap-3">
            <div className="h-8 w-24 rounded-full bg-muted/50 animate-pulse-slow" />
            <div className="h-8 w-20 rounded-full bg-muted/50 animate-pulse-slow" />
            <div className="h-8 w-28 rounded-full bg-muted/50 animate-pulse-slow" />
          </div>
          {/* list items */}
          <div className="space-y-3">
            {[...Array(5)].map((_, i) => (
              <div key={i} className="h-12 rounded-xl bg-muted/40 border border-border/50 animate-pulse-slow" />
            ))}
          </div>
        </div>
      </div>

      {/* Network + Map pins (no text) */}
      <div className="relative rounded-2xl border border-border/60 bg-card/60 backdrop-blur-sm p-0 shadow-soft overflow-hidden h-80 md:h-96" aria-hidden>
        {/* soft blobs */}
        <div className="absolute -top-10 -left-10 w-56 h-56 rounded-full bg-primary/15 blur-3xl" />
        <div className="absolute -bottom-10 right-0 w-64 h-64 rounded-full bg-accent/10 blur-3xl" />
        {/* grid */}
        <svg viewBox="0 0 600 400" className="absolute inset-0 w-full h-full">
          <defs>
            <pattern id="grid" width="30" height="30" patternUnits="userSpaceOnUse">
              <path d="M 30 0 L 0 0 0 30" fill="none" stroke="currentColor" opacity="0.06" />
            </pattern>
          </defs>
          <rect width="600" height="400" fill="url(#grid)" className="text-foreground" />

          {/* links */}
          <g stroke="currentColor" strokeOpacity="0.15" strokeWidth="2">
            <line x1="120" y1="120" x2="280" y2="160" />
            <line x1="280" y1="160" x2="420" y2="120" />
            <line x1="280" y1="160" x2="340" y2="260" />
            <line x1="200" y1="250" x2="340" y2="260" />
            <line x1="200" y1="250" x2="120" y2="120" />
          </g>

          {/* nodes */}
          <g>
            {[
              { x: 120, y: 120, r: 8 },
              { x: 280, y: 160, r: 10 },
              { x: 420, y: 120, r: 7 },
              { x: 340, y: 260, r: 9 },
              { x: 200, y: 250, r: 7 },
            ].map((n, i) => (
              <circle
                key={i}
                cx={n.x}
                cy={n.y}
                r={n.r}
                className="fill-primary/80 animate-pulse-slow"
              />
            ))}
          </g>

          {/* map pins */}
          <g>
            {[
              { x: 500, y: 200 },
              { x: 80, y: 300 },
            ].map((p, i) => (
              <g key={i} transform={`translate(${p.x}, ${p.y})`}>
                <circle r="10" className="fill-secondary/80" />
                <circle r="18" className="fill-secondary/30 animate-ping" />
                <path d="M0,12 L-4,22 L4,22 Z" className="fill-secondary/80 opacity-70" />
              </g>
            ))}
          </g>

          {/* focus ring */}
          <circle cx="280" cy="160" r="28" className="stroke-primary/40 fill-transparent animate-pulse-slow" strokeWidth="2" />
        </svg>

        {/* magnifier */}
        <div className="absolute -top-6 left-10 w-20 h-20 rounded-full border-2 border-primary/60 bg-background/40 backdrop-blur-md shadow-soft animate-float" />
      </div>
    </div>
  );
}
