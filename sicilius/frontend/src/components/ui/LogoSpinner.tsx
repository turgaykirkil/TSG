"use client";

import React from "react";
import { SiciliusLogo as Logo } from "@/components/icons/SiciliusLogo";

type Props = {
  size?: number;
  className?: string;
};

export default function LogoSpinner({ size = 96, className = "" }: Props) {
  const px = `${size}px`;
  return (
    <div
      className={(className ? className + " " : "") + "relative inline-grid place-items-center"}
      style={{ width: px, height: px }}
    >
      <div className="relative breath">
        <Logo style={{ width: px, height: px }} className="text-primary" />
      </div>
      <style jsx>{`
        .breath { animation: breath 2.4s ease-in-out infinite; }
        @keyframes breath { 0%,100% { transform: scale(0.98) } 50% { transform: scale(1.02) } }
      `}</style>
    </div>
  );
}
