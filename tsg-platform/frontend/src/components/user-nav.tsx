import { useState } from 'react';
import { Link } from 'react-router-dom';
import { useTheme } from '@/contexts/ThemeContext';
import { Icons } from '@/components/icons';
import { Button } from '@/components/ui/button';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuGroup,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';

export function UserNav() {
  const { theme, setTheme } = useTheme();
  const [isProfileMenuOpen, setIsProfileMenuOpen] = useState(false);

  const toggleTheme = () => {
    setTheme(theme === 'dark' ? 'light' : 'dark');
  };

  return (
    <div className="flex items-center space-x-4">
      <Button
        variant="ghost"
        size="icon"
        className="hidden md:flex"
        onClick={toggleTheme}
        aria-label="Tema değiştir"
      >
        <Icons.sun className="h-5 w-5 rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0" />
        <Icons.moon className="absolute h-5 w-5 rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100" />
      </Button>

      <DropdownMenu open={isProfileMenuOpen} onOpenChange={setIsProfileMenuOpen}>
        <DropdownMenuTrigger asChild>
          <Button variant="ghost" className="relative h-8 w-8 rounded-full">
            <div className="h-8 w-8 rounded-full bg-primary/10 flex items-center justify-center">
              <Icons.user className="h-4 w-4 text-primary" />
            </div>
          </Button>
        </DropdownMenuTrigger>
        <DropdownMenuContent className="w-56" align="end" forceMount>
          <DropdownMenuLabel className="font-normal">
            <div className="flex flex-col space-y-1">
              <p className="text-sm font-medium leading-none">Kullanıcı Adı</p>
              <p className="text-xs leading-none text-muted-foreground">
                kullanici@example.com
              </p>
            </div>
          </DropdownMenuLabel>
          <DropdownMenuSeparator />
          <DropdownMenuGroup>
            <DropdownMenuItem asChild>
              <Link to="/dashboard/settings">
                <Icons.settings className="mr-2 h-4 w-4" />
                <span>Hesap Ayarları</span>
              </Link>
            </DropdownMenuItem>
            <DropdownMenuItem onClick={toggleTheme}>
              <Icons.sun className="mr-2 h-4 w-4 dark:hidden" />
              <Icons.moon className="mr-2 hidden h-4 w-4 dark:block" />
              <span>{theme === 'dark' ? 'Açık Tema' : 'Koyu Tema'}</span>
            </DropdownMenuItem>
          </DropdownMenuGroup>
          <DropdownMenuSeparator />
          <DropdownMenuItem>
            <Icons.logOut className="mr-2 h-4 w-4" />
            <span>Çıkış Yap</span>
          </DropdownMenuItem>
        </DropdownMenuContent>
      </DropdownMenu>
    </div>
  );
}
