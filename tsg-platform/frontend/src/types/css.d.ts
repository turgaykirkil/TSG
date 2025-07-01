// This file helps VS Code understand Tailwind CSS directives
// and prevents warnings for @tailwind, @apply, @screen, etc.

declare module '*.css' {
  const classes: { [key: string]: string };
  export default classes;
}

declare module '*.scss' {
  const classes: { [key: string]: string };
  export default classes;
}

declare module '*.sass' {
  const classes: { [key: string]: string };
  export default classes;
}

// Allow CSS Modules to be imported in TypeScript
declare module '*.module.css' {
  const classes: { [key: string]: string };
  export default classes;
}

declare module '*.module.scss' {
  const classes: { [key: string]: string };
  export default classes;
}

declare module '*.module.sass' {
  const classes: { [key: string]: string };
  export default classes;
}

// Allow Tailwind CSS directives in CSS/SCSS files
declare module 'tailwindcss/plugin' {
  import { PluginCreator } from 'postcss';
  const plugin: PluginCreator<unknown>;
  export default plugin;
}

declare module 'tailwindcss/colors' {
  export const colors: Record<string, Record<string, string>>;
}

// Add type definitions for Tailwind CSS directives
declare module 'tailwindcss/lib/util/withAlphaVariable' {
  export default function withAlphaVariable(
    config: Record<string, unknown>
  ): Record<string, unknown>;
}

// Add type definitions for @tailwind, @apply, @screen, etc.
declare module 'tailwindcss/plugin' {
  import { PluginCreator } from 'postcss';
  const plugin: PluginCreator<unknown>;
  export default plugin;
}

// Add type definitions for @tailwind rules
declare module 'postcss' {
  interface AtRule {
    name: string;
    params: string;
  }
}

// Add type definitions for @apply
interface CSSProperties {
  [key: `--${string}`]: string | number | undefined;
}

// Add type definitions for @screen
declare function screen(screen: string, css: string): string;
