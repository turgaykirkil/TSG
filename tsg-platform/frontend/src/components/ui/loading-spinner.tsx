import { cn } from '@/lib/utils';
import { Icons } from '@/components/icons';
import Image from 'next/image';

// This is the full-screen loader with the main logo
export const FullScreenLoader = () => {
  return (
    <div className="fixed inset-0 z-50 flex flex-col items-center justify-center bg-background/80 backdrop-blur-sm">
      <div className="relative mb-6">
        <Image 
          src="/sicilius-logo.svg" 
          alt="Sicilius Logo" 
          width={150} 
          height={150} 
          className="animate-pulse duration-1000"
          style={{ height: 'auto' }}
          priority
        />
      </div>

    </div>
  );
};

// This is a smaller, generic spinner component
interface LoadingSpinnerProps {
  className?: string;
  size?: number;
}

const LoadingSpinner = ({ className, size = 48 }: LoadingSpinnerProps) => {
  return (
    <div role="status" className={cn("flex justify-center items-center", className)}>
      {/* Using inline style to make size dynamic */}
      <Icons.spinner className="animate-spin" style={{ width: size, height: size }} />
      <span className="sr-only">Loading...</span>
    </div>
  );
};

export default LoadingSpinner;
