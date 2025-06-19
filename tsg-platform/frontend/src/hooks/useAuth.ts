'use client';

import { signIn, signOut, useSession } from 'next-auth/react';
import { useRouter } from 'next/navigation';
import { useCallback, useState } from 'react';
import { toast } from 'sonner';

type User = {
  id: string;
  email: string;
  name: string;
  role: string;
  image?: string;
};

type AuthResult = {
  success: boolean;
  error?: string;
};

export const useAuth = () => {
  const { data: session, status, update } = useSession();
  const router = useRouter();
  const [isLoading, setIsLoading] = useState(false);

  const login = useCallback(
    async (email: string, password: string, redirectTo: string = '/dashboard'): Promise<AuthResult> => {
      console.log('[useAuth] Giriş işlemi başlatılıyor...');
      setIsLoading(true);
      
      try {
        // 1. NextAuth ile giriş yap
        console.log('[useAuth] NextAuth ile giriş yapılıyor...');
        const result = await signIn('credentials', {
          redirect: false,
          email,
          password,
          callbackUrl: redirectTo,
        });

        console.log('[useAuth] NextAuth yanıtı:', result);

        // 2. Hata kontrolü
        if (result?.error) {
          const errorMsg = result.error === 'CredentialsSignin' 
            ? 'Geçersiz e-posta veya şifre' 
            : result.error;
          console.error('[useAuth] Giriş hatası:', errorMsg);
          return { success: false, error: errorMsg };
        }

        // Başarılı giriş - session otomatik olarak yenilenecek
        console.log('[useAuth] Giriş başarılı, yönlendiriliyor:', redirectTo);
        // İsteğe bağlı olarak router.refresh() çağrısı eklenebilir
        await update(); // Sessiyonu arka planda yenile, hata fırlatma
        
        return { success: true };
        
      } catch (error) {
        const errorMessage = error instanceof Error ? error.message : 'Bilinmeyen bir hata oluştu';
        console.error('[useAuth] Giriş işleminde hata:', errorMessage);
        return { success: false, error: errorMessage };
      } finally {
        setIsLoading(false);
      }
    },
    [update]
  );

  const logout = useCallback(async (): Promise<void> => {
    try {
      setIsLoading(true);
      await signOut({ redirect: false });
      router.push('/login');
      router.refresh();
    } catch (error) {
      console.error('Çıkış hatası:', error);
      toast.error('Çıkış yapılırken bir hata oluştu');
    } finally {
      setIsLoading(false);
    }
  }, [router]);

  const register = useCallback(async (name: string, email: string, password: string) => {
    try {
      const response = await fetch('/api/auth/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, email, password }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Kayıt sırasında bir hata oluştu');
      }

      // Auto-login after registration
      await login(email, password);
      toast.success('Hesabınız başarıyla oluşturuldu!');
    } catch (error) {
      console.error('Kayıt hatası:', error);
      toast.error(error instanceof Error ? error.message : 'Kayıt sırasında bir hata oluştu');
      throw error;
    }
  }, [login]);

  const refreshSession = useCallback(async (): Promise<void> => {
    try {
      setIsLoading(true);
      await update();
    } catch (error) {
      console.error('Session yenileme hatası:', error);
      throw error;
    } finally {
      setIsLoading(false);
    }
  }, [update]);

  return {
    login,
    logout,
    register,
    refreshSession,
    isAuthenticated: status === 'authenticated',
    isLoading,
    user: session?.user as User | undefined,
  };
};
