'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { useRouter, useSearchParams } from 'next/navigation';
import { toast } from 'sonner';
import { cn } from '@/lib/utils';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { useAuth } from '@/hooks/useAuth';
import { Loader2, Eye, EyeOff, AlertCircle } from 'lucide-react';

export default function LoginPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const callbackUrl = searchParams.get('callbackUrl') || '/dashboard';
  
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [isMounted, setIsMounted] = useState(false);
  const [error, setError] = useState('');
  const { login, isAuthenticated, isLoading: isAuthLoading } = useAuth();
  const [loginError, setLoginError] = useState('');
  
  // Redirect if already authenticated
  useEffect(() => {
    if (isAuthenticated) {
      console.log('Kullanıcı zaten giriş yapmış, yönlendiriliyor:', callbackUrl);
      window.location.assign(callbackUrl);
    }
    setIsMounted(true);
  }, [isAuthenticated, callbackUrl, router]);
  
  // Show error toast if any
  useEffect(() => {
    if (searchParams.get('error') === 'SessionRequired') {
      toast.error('Lütfen tekrar giriş yapın', {
        description: 'Oturumunuz sona erdi veya geçersiz.'
      });
    }
  }, [searchParams]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoginError('');
    console.log('Login form gönderildi');
    
    if (!email || !password) {
      setError('Lütfen tüm alanları doldurun');
      return;
    }
    
    setIsLoading(true);
    
    try {
      console.log('Giriş denemesi başlatılıyor...');
      const result = await login(email, password, callbackUrl);
      
      if (result.success) {
        console.log('Giriş başarılı, yönlendiriliyor:', callbackUrl);
        window.location.assign(callbackUrl);
      } else {
        setLoginError(result.error || 'Giriş başarısız');
        toast.error(result.error || 'Giriş başarısız');
      }
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Bilinmeyen bir hata oluştu';
      console.error('Giriş hatası:', errorMessage);
      setLoginError(errorMessage);
      toast.error('Giriş sırasında bir hata oluştu');
    } finally {
      setIsLoading(false);
    }
    if (!email.trim()) {
      const errorMsg = 'E-posta adresi gereklidir';
      setError(errorMsg);
      return;
    }
    
    if (!/^\S+@\S+\.\S+$/.test(email)) {
      const errorMsg = 'Geçerli bir e-posta adresi giriniz';
      setError(errorMsg);
      return;
    }
    
    if (!password) {
      const errorMsg = 'Lütfen şifrenizi giriniz';
      setError(errorMsg);
      return;
    }
    
    if (password.length < 6) {
      const errorMsg = 'Şifre en az 6 karakter olmalıdır';
      setError(errorMsg);
      return;
    }

    try {
      console.log('Giriş işlemi başlatılıyor...');
      setIsLoading(true);
      
      // Toast bildirimi göster
      const toastId = toast.loading('Giriş yapılıyor...');
      
      console.log('Login fonksiyonu çağrılıyor...');
      const { success, error } = await login(email, password, callbackUrl);
      console.log('Login fonksiyonu tamamlandı:', { success, error });
      
      if (success) {
        // Başarılı giriş bildirimi
        toast.success('Giriş başarılı!', { id: toastId });
        
        // 1 saniye bekle ve yönlendir
        setTimeout(() => {
          console.log('Yönlendiriliyor:', callbackUrl);
          window.location.assign(callbackUrl);
        }, 300);
      } else {
        // Hata durumunda
        const errorMsg = error || 'Giriş başarısız. Lütfen tekrar deneyin.';
        console.error('Giriş hatası:', errorMsg);
        setError(errorMsg);
        
        // Hata bildirimini göster
        toast.error('Giriş başarısız', {
          description: errorMsg,
          icon: <AlertCircle className="h-5 w-5" />
        });
      }
      
    } catch (err) {
      console.error('Beklenmeyen hata:', err);
      const errorMessage = err instanceof Error ? 
        (err.message === 'CredentialsSignin' ? 'Geçersiz e-posta veya şifre' : err.message) : 
        'Beklenmeyen bir hata oluştu. Lütfen tekrar deneyin.';
      
      setError(errorMessage);
      
      // Hata bildirimini göster
      toast.error('Giriş başarısız', {
        description: errorMessage,
        icon: <AlertCircle className="h-5 w-5" />
      });
      
    } finally {
      console.log('Giriş işlemi tamamlandı');
      setIsLoading(false);
      toast.dismiss();
    }
  };
  
  if (!isMounted || isAuthLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-gray-50">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-500"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 to-white flex items-center justify-center p-4">
      <div className="w-full max-w-md space-y-8">
        <div className="text-center">
          <h1 className="text-3xl font-extrabold text-gray-900">Hoş Geldiniz</h1>
          <p className="mt-2 text-sm text-gray-600">
            Devam etmek için hesabınıza giriş yapın
          </p>
        </div>

        <div className="bg-white p-8 rounded-2xl shadow-xl border border-gray-100">
          {error && (
            <div className="mb-6 p-4 bg-red-50 rounded-lg flex items-start">
              <AlertCircle className="h-5 w-5 text-red-500 mt-0.5 mr-2 flex-shrink-0" />
              <div>
                <p className="text-sm font-medium text-red-800">Hata</p>
                <p className="text-sm text-red-700">{error}</p>
              </div>
            </div>
          )}

          <form className="space-y-6" onSubmit={handleSubmit}>
            <div>
              <Label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">
                E-posta Adresi
              </Label>
              <div className="relative">
                <Input
                  id="email"
                  name="email"
                  type="email"
                  autoComplete="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  disabled={isLoading}
                  className={cn(
                    'block w-full rounded-lg border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 py-3 px-4 text-base',
                    error && 'border-red-300 focus:border-red-500 focus:ring-red-500'
                  )}
                  placeholder="ornek@email.com"
                />
              </div>
            </div>

            <div>
              <div className="flex items-center justify-between mb-1">
                <Label htmlFor="password" className="block text-sm font-medium text-gray-700">
                  Şifre
                </Label>
                <Link
                  href="/forgot-password"
                  className="text-sm font-medium text-indigo-600 hover:text-indigo-500 hover:underline"
                >
                  Şifremi unuttum?
                </Link>
              </div>
              <div className="relative">
                <div className="relative">
                  <Input
                    id="password"
                    name="password"
                    type={showPassword ? 'text' : 'password'}
                    autoComplete="current-password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    disabled={isLoading}
                    className={cn(
                      'block w-full rounded-lg border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 py-3 px-4 pr-12 text-base',
                      error && 'border-red-300 focus:border-red-500 focus:ring-red-500'
                    )}
                    placeholder="••••••••"
                  />
                  <button
                    type="button"
                    className="absolute inset-y-0 right-0 pr-3 flex items-center"
                    onClick={() => setShowPassword(!showPassword)}
                    tabIndex={-1}
                  >
                    {showPassword ? (
                      <EyeOff className="h-5 w-5 text-gray-400 hover:text-gray-500" />
                    ) : (
                      <Eye className="h-5 w-5 text-gray-400 hover:text-gray-500" />
                    )}
                  </button>
                </div>
              </div>
            </div>

            <div className="flex items-center justify-between">
              <div className="flex items-center">
                <input
                  id="remember-me"
                  name="remember-me"
                  type="checkbox"
                  className="h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-600"
                  disabled={isLoading}
                />
                <label htmlFor="remember-me" className="ml-3 block text-sm leading-6 text-gray-900">
                  Beni hatırla
                </label>
              </div>
              <div className="text-sm">
                <Link href="/auth/register" className="font-semibold text-indigo-600 hover:text-indigo-500">
                  Hesabınız yok mu? Kaydolun
                </Link>
              </div>
            </div>

            <div>
              <Button
                type="submit"
                disabled={isLoading}
                className="w-full justify-center py-3 px-4 text-base font-medium rounded-lg bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-colors duration-200"
              >
                {isLoading ? (
                  <>
                    <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                    Giriş Yapılıyor...
                  </>
                ) : (
                  'Giriş Yap'
                )}
              </Button>
            </div>

            <div className="text-center text-sm text-gray-600">
              Hesabınız yok mu?{' '}
              <Link
                href={`/register${callbackUrl ? `?callbackUrl=${encodeURIComponent(callbackUrl)}` : ''}`}
                className="font-medium text-indigo-600 hover:text-indigo-500 hover:underline"
              >
                Kayıt Olun
              </Link>
            </div>
          </form>

          <div className="mt-8 pt-6 border-t border-gray-200">
            <div className="text-center text-xs text-gray-500">
              <p>&copy; {new Date().getFullYear()} TSG Platform. Tüm hakları saklıdır.</p>
              <div className="mt-2 flex items-center justify-center space-x-4">
                <Link href="/privacy" className="hover:text-indigo-600 hover:underline">
                  Gizlilik Politikası
                </Link>
                <span>&bull;</span>
                <Link href="/terms" className="hover:text-indigo-600 hover:underline">
                  Kullanım Koşulları
                </Link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
