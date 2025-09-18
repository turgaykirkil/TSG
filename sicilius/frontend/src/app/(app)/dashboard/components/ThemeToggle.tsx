"use client";

import { useEffect, useRef, useState } from "react";
import { Moon, Sun } from "lucide-react";

const STORAGE_KEY = "sicilius.theme";

type Theme = "light" | "dark";

export default function ThemeToggle() {
  const [theme, setTheme] = useState<Theme>("light");
  const autoRef = useRef<boolean>(true); // track auto-sync with system when no user pref

  useEffect(() => {
    const saved = (typeof window !== "undefined" && window.localStorage.getItem(STORAGE_KEY)) as Theme | null;
    const mql = window.matchMedia('(prefers-color-scheme: dark)');
    const initial: Theme = saved || (mql.matches ? 'dark' : 'light');
    autoRef.current = !saved; // if user saved, no auto-sync
    apply(initial);
    const onChange = (e: MediaQueryListEvent) => {
      if (!autoRef.current) return;
      apply(e.matches ? 'dark' : 'light');
    };
    mql.addEventListener('change', onChange);
    return () => mql.removeEventListener('change', onChange);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const apply = (t: Theme) => {
    setTheme(t);
    const root = document.documentElement;
    if (t === "dark") root.classList.add("dark");
    else root.classList.remove("dark");
    // only persist if user explicitly toggled (autoRef false handled in toggle)
  };

  const toggle = () => {
    autoRef.current = false;
    const next = theme === "dark" ? "light" : "dark";
    apply(next);
    try { window.localStorage.setItem(STORAGE_KEY, next); } catch {}
  };

  return (
    <button
      type="button"
      onClick={toggle}
      aria-label={theme === 'dark' ? 'Açık tema' : 'Koyu tema'}
      title={theme === 'dark' ? 'Açık tema' : 'Koyu tema'}
      className="fixed top-4 right-14 z-50 rounded-full p-2.5 bg-white/90 dark:bg-slate-900/90 border border-slate-200 dark:border-slate-700 text-slate-700 dark:text-slate-200 shadow hover:bg-white dark:hover:bg-slate-900"
    >
      {theme === 'dark' ? <Sun size={18} /> : <Moon size={18} />}
    </button>
  );
}
