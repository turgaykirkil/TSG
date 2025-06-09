/// <reference types="vite/client" />

// For CSS modules
declare module '*.module.css' {
  const classes: { readonly [key: string]: string };
  export default classes;
}

// For SCSS modules
declare module '*.module.scss' {
  const classes: { readonly [key: string]: string };
  export default classes;
}

// For SVG imports
declare module '*.svg' {
  import * as React from 'react';
  export const ReactComponent: React.FunctionComponent<
    React.SVGProps<SVGSVGElement> & { title?: string }
  >;
  const src: string;
  export default src;
}

// For image imports
declare module '*.png';
declare module '*.jpg';
declare module '*.jpeg';
declare module '*.gif';
declare module '*.bmp';
declare module '*.webp';
// Add component module declarations
declare module '@/components/ui/input' {
  import { InputHTMLAttributes, ForwardRefExoticComponent, RefAttributes } from 'react';
  
  export interface InputProps extends InputHTMLAttributes<HTMLInputElement> {}
  
  const Input: ForwardRefExoticComponent<
    InputProps & RefAttributes<HTMLInputElement>
  >;
  
  export { Input };
}

declare module '@/components/ui/label' {
  import { LabelHTMLAttributes, ForwardRefExoticComponent, RefAttributes } from 'react';
  import { VariantProps } from 'class-variance-authority/types';
  
  const labelVariants: any;
  
  export interface LabelProps 
    extends LabelHTMLAttributes<HTMLLabelElement>,
      VariantProps<typeof labelVariants> {}
  
  const Label: ForwardRefExoticComponent<
    LabelProps & RefAttributes<HTMLLabelElement>
  >;
  
  export { Label, labelVariants };
}
