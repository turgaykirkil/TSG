import { cn } from '@/lib/utils';

interface LogoProps {
  className?: string;
}

export function Logo({ className }: LogoProps) {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
      className={cn("mr-2 h-8 w-8", className)}
    >
      <path d="M15.6 12.8c-1.2 1.2-2.8 2-4.6 2s-3.4-.8-4.6-2c-1.2-1.2-2-2.8-2-4.6s.8-3.4 2-4.6c1.2-1.2 2.8-2 4.6-2s3.4.8 4.6 2" />
      <path d="M8.4 11.2c1.2-1.2 2.8-2 4.6-2s3.4.8 4.6 2c1.2 1.2 2 2.8 2 4.6s-.8 3.4-2 4.6c-1.2 1.2-2.8 2-4.6 2s-3.4-.8-4.6-2" />
    </svg>
  );
}
