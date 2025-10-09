import { cn } from '@/lib/utils';
import LogoSpinner from '@/components/ui/LogoSpinner';

// This is the full-screen loader with the main logo
export const FullScreenLoader = () => {
  return (
    <div className="fixed inset-0 z-50 flex flex-col items-center justify-center bg-background/80 backdrop-blur-sm">
      <LogoSpinner size={112} />
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
    <div className={cn("flex justify-center items-center", className)}>
      <LogoSpinner size={size} />
    </div>
  );
};

export default LoadingSpinner;
