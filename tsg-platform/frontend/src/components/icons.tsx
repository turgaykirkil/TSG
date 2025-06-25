import { cn } from '@/lib/utils';
import * as LucideIcons from 'lucide-react';
import type { LucideProps } from 'lucide-react';
import React from 'react';

// Base icon component
type IconProps = React.SVGProps<SVGSVGElement>;

export type Icon = React.FC<IconProps>;

// Logo icon
export const Logo: Icon = ({ className, ...props }) => {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
      className={cn('h-8 w-8', className)} // Boyut artırıldı
      {...props}
    >
      <path d="M15.6 12.8c-1.2 1.2-2.8 2-4.6 2s-3.4-.8-4.6-2c-1.2-1.2-2-2.8-2-4.6s.8-3.4 2-4.6c1.2-1.2 2.8-2 4.6-2s3.4.8 4.6 2" />
      <path d="M8.4 11.2c1.2-1.2 2.8-2 4.6-2s3.4.8 4.6 2c1.2 1.2 2 2.8 2 4.6s-.8 3.4-2 4.6c-1.2 1.2-2.8 2-4.6 2s-3.4-.8-4.6-2" />
    </svg>
  );
}

// Create icon component with proper typing
const createIcon = (Icon: React.ForwardRefExoticComponent<Omit<LucideProps, 'ref'> & React.RefAttributes<SVGSVGElement>>) => {
  const IconComponent = (props: IconProps) => (
    <Icon className={cn('h-5 w-5', props.className)} {...props} />
  );
  
  // Add displayName for better debugging
  IconComponent.displayName = Icon.displayName || 'Icon';
  
  return IconComponent;
};

// Export all icons
export const Icons = {
  // Custom icons
  logo: Logo,
  history: (() => {
    const HistoryIcon = ({ className, ...props }: IconProps) => (
      <svg
        xmlns="http://www.w3.org/2000/svg"
        width="24"
        height="24"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        strokeWidth="2"
        strokeLinecap="round"
        strokeLinejoin="round"
        className={cn('h-5 w-5', className)}
        {...props}
      >
        <path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8" />
        <path d="M3 3v5h5" />
        <path d="M12 7v5l3 3" />
      </svg>
    );
    HistoryIcon.displayName = 'History';
    return HistoryIcon;
  })(),
  
  // Common icons
  home: createIcon(LucideIcons.Home),
  settings: createIcon(LucideIcons.Settings),
  user: createIcon(LucideIcons.User),
  users: createIcon(LucideIcons.Users),
  fileText: createIcon(LucideIcons.FileText),
  file: createIcon(LucideIcons.File),
  menu: createIcon(LucideIcons.Menu),
  sun: createIcon(LucideIcons.Sun),
  moon: createIcon(LucideIcons.Moon),
  logOut: createIcon(LucideIcons.LogOut),
  folder: createIcon(LucideIcons.Folder),
  download: createIcon(LucideIcons.Download),
  upload: createIcon(LucideIcons.UploadCloud),
  trash: createIcon(LucideIcons.Trash2),
  edit: createIcon(LucideIcons.Pencil),
  plus: createIcon(LucideIcons.Plus),
  minus: createIcon(LucideIcons.Minus),
  x: createIcon(LucideIcons.X),
  check: createIcon(LucideIcons.Check),
  chevronRight: createIcon(LucideIcons.ChevronRight),
  chevronLeft: createIcon(LucideIcons.ChevronLeft),
  chevronDown: createIcon(LucideIcons.ChevronDown),
  chevronUp: createIcon(LucideIcons.ChevronUp),
  search: createIcon(LucideIcons.Search),
  filter: createIcon(LucideIcons.Filter),
  arrowRight: createIcon(LucideIcons.ArrowRight),
  arrowLeft: createIcon(LucideIcons.ArrowLeft),
  arrowUp: createIcon(LucideIcons.ArrowUp),
  arrowDown: createIcon(LucideIcons.ArrowDown),
  
  // Dashboard icons
  layoutDashboard: createIcon(LucideIcons.LayoutDashboard),
  building2: createIcon(LucideIcons.Building2),
  newspaper: createIcon(LucideIcons.Newspaper),
  
  // Status icons
  info: createIcon(LucideIcons.Info),
  alertCircle: createIcon(LucideIcons.AlertCircle),
  alertTriangle: createIcon(LucideIcons.AlertTriangle),
  checkCircle: createIcon(LucideIcons.CheckCircle2),
  xCircle: createIcon(LucideIcons.XCircle),
  
  // Navigation
  arrowLeftCircle: createIcon(LucideIcons.ArrowLeftCircle),
  arrowRightCircle: createIcon(LucideIcons.ArrowRightCircle),
  
  // Actions
  refreshCw: createIcon(LucideIcons.RefreshCw),
  rotateCw: createIcon(LucideIcons.RotateCw),
  copy: createIcon(LucideIcons.Copy),
  externalLink: createIcon(LucideIcons.ExternalLink),
  link: createIcon(LucideIcons.Link2),
  
  // Media
  image: createIcon(LucideIcons.Image),
  fileImage: createIcon(LucideIcons.FileImage),
  filePdf: createIcon(LucideIcons.FileType),
  fileTextIcon: createIcon(LucideIcons.FileText),
  
  // Social
  github: createIcon(LucideIcons.Github), // Note: GitHub is now exported as Github
  twitter: createIcon(LucideIcons.Twitter),
  linkedin: createIcon(LucideIcons.Linkedin),
  facebook: createIcon(LucideIcons.Facebook),
  instagram: createIcon(LucideIcons.Instagram),
  
  // Toggle
  toggleLeft: createIcon(LucideIcons.ToggleLeft),
  toggleRight: createIcon(LucideIcons.ToggleRight),
  
  // Other
  hash: createIcon(LucideIcons.Hash),
  calendar: createIcon(LucideIcons.Calendar),
  clock: createIcon(LucideIcons.Clock),
  mail: createIcon(LucideIcons.Mail),
  phone: createIcon(LucideIcons.Phone),
  mapPin: createIcon(LucideIcons.MapPin),
  mapPinOff: createIcon(LucideIcons.MapPinOff),
  spinner: createIcon(LucideIcons.Loader2),
};


