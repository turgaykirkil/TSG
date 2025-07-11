'use client';

import { createContext, useContext, useEffect, useState, ReactNode, useCallback } from 'react';
import { useRouter, usePathname, useSearchParams } from 'next/navigation';
import { toast } from 'sonner';
import { AxiosError } from 'axios';
import api from '@/lib/axios';
import { API_ENDPOINTS } from '@/config/constants';
import type { AuthContextType, ApiErrorResponse, Session, AuthResult } from '../types/auth';

// --- HELPER FUNCTION ---
const getErrorMessage = (error: unknown): string => {
  if (error instanceof AxiosError) {
    const errorData = error.response?.data as ApiErrorResponse;
    if (errorData?.detail) {
      if (typeof errorData.detail === 'string') return errorData.detail;
      if (Array.isArray(errorData.detail) && errorData.detail[0]?.msg) return errorData.detail[0].msg;
    }
  }
  return 'Beklenmeyen bir hata oluştu.';
};



// --- CONTEXT CREATION ---
const AuthContext = createContext<AuthContextType | undefined>(undefined);

// --- AUTH PROVIDER COMPONENT ---
export function AuthProvider({ children }: { children: ReactNode }) {
  const [session, setSession] = useState<Session>({ user: null, status: 'loading' });
  const [loading, setLoading] = useState(true);
  const router = useRouter();
  const pathname = usePathname();
  const searchParams = useSearchParams();

  const checkAuth = useCallback(async () => {
    try {
      const response = await api.get(API_ENDPOINTS.USERS.ME);
      setSession({ user: response.data, status: 'authenticated' });
    } catch (error) {
      setSession({ user: null, status: 'unauthenticated' });
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    checkAuth();
  }, [checkAuth]);

  useEffect(() => {
    if (loading) return;

    const publicPaths = ['/login', '/register', '/forgot-password'];
    const isPublicPath = publicPaths.some(path => pathname.startsWith(path));

    if (session.status === 'unauthenticated' && !isPublicPath) {
      router.push('/login');
    }
  }, [session, loading, pathname, router]);

  const login = async (email: string, password: string): Promise<AuthResult> => {
    setLoading(true);
    const params = new URLSearchParams();
    params.append('username', email);
    params.append('password', password);

    try {
      await api.post(API_ENDPOINTS.AUTH.LOGIN, params, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
      });
      await checkAuth();
      const callbackUrl = searchParams.get('callbackUrl') || '/dashboard';
      router.push(callbackUrl);
      toast.success('Giriş başarılı!');
      return { success: true };
    } catch (error) {
      const errorMessage = getErrorMessage(error);
      toast.error(errorMessage);
      return { success: false, error: errorMessage };
    } finally {
      setLoading(false);
    }
  };

  const logout = async () => {
    try {
      await api.post(API_ENDPOINTS.AUTH.LOGOUT);
      setSession({ user: null, status: 'unauthenticated' });
      router.push('/login');
      toast.info('Başarıyla çıkış yapıldı.');
    } catch (error) {
      toast.error('Çıkış yapılırken bir hata oluştu.');
    }
  };

  const value: AuthContextType = {
    session,
    isAuthenticated: session.status === 'authenticated',
    loading,
    login,
    logout,
    checkAuth,
    // Placeholder functions for missing implementations
    register: async (data) => { console.log('register not implemented', data); return { success: false, error: 'Not implemented' }; },
    updateProfile: async (data) => { console.log('updateProfile not implemented', data); return { success: false, error: 'Not implemented' }; },
    changePassword: async (currentPassword, newPassword) => { console.log('changePassword not implemented'); return { success: false, error: 'Not implemented' }; },
    forgotPassword: async (email) => { console.log('forgotPassword not implemented', email); return { success: false, error: 'Not implemented' }; },
    resetPassword: async (token, newPassword) => { console.log('resetPassword not implemented'); return { success: false, error: 'Not implemented' }; },
  };

  return (
    <AuthContext.Provider value={value}>
      {loading ? <div className="flex h-screen items-center justify-center">Yükleniyor...</div> : children}
    </AuthContext.Provider>
  );
}

// --- CUSTOM HOOK ---
export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
