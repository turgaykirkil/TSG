'use client';

import { createContext, useContext, useEffect, useState, ReactNode, useCallback } from 'react';
import { useRouter, usePathname, useSearchParams } from 'next/navigation';
// Notifications are shown via modal alerts
import { useAlert } from '@/contexts/AlertContext';
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
  const { showAlert } = useAlert();

  const checkAuth = useCallback(async () => {
    try {
      const response = await api.get(API_ENDPOINTS.USERS.ME);
      setSession({ user: response.data, status: 'authenticated' });
    } catch (error) {
      // Clear stale cookie if backend rejects the token
      try { await api.post(API_ENDPOINTS.AUTH.LOGOUT); } catch {}
      setSession({ user: null, status: 'unauthenticated' });
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    const protectedPaths = ['/dashboard', '/admin', '/profile'];
    const isProtectedPath = protectedPaths.some(path => pathname.startsWith(path));

    // Only check authentication status if the user is on a protected path.
    // On public paths, we don't need to make this API call.
    if (isProtectedPath) {
      checkAuth();
    } else {
      // For public paths, we can assume the user is not logged in initially.
      // If they have a valid session from another tab, it will be handled upon navigation to a protected route.
      setLoading(false);
      setSession({ user: null, status: 'unauthenticated' });
    }
  }, [pathname, checkAuth]);

  useEffect(() => {
    if (loading) return;

    // Define protected paths that require authentication
    const protectedPaths = ['/dashboard', '/admin', '/profile']; // Add any other protected routes here
    const isProtectedPath = protectedPaths.some(path => pathname.startsWith(path));

    // If the user is not authenticated and is trying to access a protected route,
    // redirect them to the login page.
    if (session.status === 'unauthenticated' && isProtectedPath) {
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
      // Fetch user to decide the correct landing route (admin vs user)
      let role: string | undefined;
      try {
        const me = await api.get(API_ENDPOINTS.USERS.ME);
        // robust role extraction in case of enum-like value
        const rawRole = me?.data?.role as any;
        role = typeof rawRole === 'string' ? rawRole : (rawRole?.value || rawRole?.name);
        setSession({ user: me.data, status: 'authenticated' });
      } catch {
        await checkAuth();
      }
      const callbackUrl = searchParams.get('callbackUrl');
      const defaultTarget = role === 'admin' ? '/admin' : '/dashboard';
      router.push(callbackUrl || defaultTarget);
      showAlert({ title: 'Giriş başarılı!', description: 'Hoş geldiniz.' , variant: 'success' });
      return { success: true };
    } catch (error) {
      const errorMessage = getErrorMessage(error);
      showAlert({ title: 'Giriş başarısız', description: errorMessage, variant: 'destructive' });
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
      showAlert({ title: 'Çıkış yapıldı', description: 'Başarıyla çıkış yaptınız.', variant: 'info' });
    } catch (error) {
      showAlert({ title: 'Hata', description: 'Çıkış yapılırken bir hata oluştu.', variant: 'destructive' });
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
