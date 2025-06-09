import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '@/contexts/AuthContext';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Icons } from '@/components/icons';

export function Register() {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const { register } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    
    if (password !== confirmPassword) {
      // TODO: Show error toast
      console.error('Passwords do not match');
      return;
    }

    try {
      setIsLoading(true);
      await register(name, email, password);
      navigate('/dashboard', { replace: true });
    } catch (error) {
      console.error('Registration error:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="container flex h-screen w-screen flex-col items-center justify-center">
      <div className="mx-auto flex w-full flex-col justify-center space-y-6 sm:w-[400px]">
        <div className="flex flex-col space-y-2 text-center">
          <h1 className="text-2xl font-semibold tracking-tight">Hesap oluştur</h1>
          <p className="text-sm text-muted-foreground">
            Yeni bir hesap oluşturmak için bilgilerinizi girin
          </p>
        </div>
        
        <div className="grid gap-6">
          <form onSubmit={handleSubmit}>
            <div className="grid gap-4">
              <div className="grid gap-1">
                <Label className="sr-only" htmlFor="name">
                  Ad Soyad
                </Label>
                <Input
                  id="name"
                  placeholder="Adınız Soyadınız"
                  type="text"
                  autoCapitalize="words"
                  autoComplete="name"
                  autoCorrect="off"
                  disabled={isLoading}
                  value={name}
                  onChange={(e: React.ChangeEvent<HTMLInputElement>) => setName(e.target.value)}
                  className="h-10"
                />
              </div>
              
              <div className="grid gap-1">
                <Label className="sr-only" htmlFor="email">
                  E-posta
                </Label>
                <Input
                  id="email"
                  placeholder="E-posta adresiniz"
                  type="email"
                  autoCapitalize="none"
                  autoComplete="email"
                  autoCorrect="off"
                  disabled={isLoading}
                  value={email}
                  onChange={(e: React.ChangeEvent<HTMLInputElement>) => setEmail(e.target.value)}
                  className="h-10"
                />
              </div>
              
              <div className="grid gap-1">
                <Label className="sr-only" htmlFor="password">
                  Şifre
                </Label>
                <Input
                  id="password"
                  placeholder="Şifreniz"
                  type="password"
                  autoComplete="new-password"
                  disabled={isLoading}
                  value={password}
                  onChange={(e: React.ChangeEvent<HTMLInputElement>) => setPassword(e.target.value)}
                  className="h-10"
                />
              </div>
              
              <div className="grid gap-1">
                <Label className="sr-only" htmlFor="confirmPassword">
                  Şifre Tekrar
                </Label>
                <Input
                  id="confirmPassword"
                  placeholder="Şifrenizi tekrar girin"
                  type="password"
                  autoComplete="new-password"
                  disabled={isLoading}
                  value={confirmPassword}
                  onChange={(e: React.ChangeEvent<HTMLInputElement>) => setConfirmPassword(e.target.value)}
                  className="h-10"
                />
              </div>
              
              <Button disabled={isLoading} type="submit" className="mt-2">
                {isLoading && (
                  <Icons.spinner className="mr-2 h-4 w-4 animate-spin" />
                )}
                Kayıt Ol
              </Button>
            </div>
          </form>
          
          <div className="relative">
            <div className="absolute inset-0 flex items-center">
              <span className="w-full border-t" />
            </div>
            <div className="relative flex justify-center text-xs uppercase">
              <span className="bg-background px-2 text-muted-foreground">
                ZATEN HESABINIZ VAR MI?
              </span>
            </div>
          </div>
          
          <div className="text-center text-sm">
            Zaten bir hesabınız var mı?{' '}
            <Link
              to="/auth/login"
              className="underline underline-offset-4 hover:text-primary"
            >
              Giriş yapın
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Register;
