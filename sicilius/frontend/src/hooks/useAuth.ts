'use client';

import { useState, useCallback, useEffect } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { toast } from 'sonner';
import { AxiosError } from 'axios';
import api from '@/lib/axios';
import { API_ENDPOINTS } from '@/config/constants';
import type { User, Session, AuthResult, RegisterData, ApiErrorResponse, AuthContextType } from '../types/auth';

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

export const useAuth = (): AuthContextType => {
  const [session, setSession] = useState<Session>({ user: null, status: 'loading' });
  const [loading, setLoading] = useState(true);
  const router = useRouter();
  const searchParams = useSearchParams();

  const checkAuth = useCallback(async () => {
    setLoading(true);
    try {
      const response = await api.get<User>(API_ENDPOINTS.USERS.ME);
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

  const login = useCallback(async (email: string, password: string): Promise<AuthResult> => {
    setLoading(true);
    try {
      const formData = new URLSearchParams();
      formData.append('username', email);
      formData.append('password', password);
      await api.post(API_ENDPOINTS.AUTH.LOGIN, formData, { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } });
      const { data: user } = await api.get<User>(API_ENDPOINTS.USERS.ME);
      setSession({ user, status: 'authenticated' });
      toast.success('Giriş başarılı!');
      const callbackUrl = searchParams.get('callbackUrl') || '/dashboard';
      router.push(callbackUrl);
      return { success: true, user };
    } catch (error) {
      const errorMessage = getErrorMessage(error);
      toast.error(errorMessage);
      setSession({ user: null, status: 'unauthenticated' });
      return { success: false, error: errorMessage };
    } finally {
      setLoading(false);
    }
  }, [router, searchParams]);

  const register = useCallback(async (userData: RegisterData): Promise<AuthResult> => {
    setLoading(true);
    try {
      const { data: user } = await api.post<User>(API_ENDPOINTS.AUTH.REGISTER, userData);
      toast.success('Kayıt başarılı! Lütfen giriş yapın.');
      router.push('/login');
      return { success: true, user };
    } catch (error) {
      const errorMessage = getErrorMessage(error);
      toast.error(errorMessage);
      return { success: false, error: errorMessage };
    } finally {
      setLoading(false);
    }
  }, [router]);

  const logout = useCallback(async () => {
    setLoading(true);
    try {
      await api.post(API_ENDPOINTS.AUTH.LOGOUT);
      toast.info('Başarıyla çıkış yaptınız.');
    } catch (error) {
      console.error('Logout error:', getErrorMessage(error));
    } finally {
      setSession({ user: null, status: 'unauthenticated' });
      router.push('/login');
      setLoading(false);
    }
  }, [router]);

  const updateProfile = useCallback(async (userData: Partial<User>): Promise<AuthResult> => {
    setLoading(true);
    try {
      const { data: updatedUser } = await api.patch<User>(API_ENDPOINTS.USERS.ME, userData);
      setSession((prev: Session) => ({ ...prev, user: { ...(prev.user || {}), ...updatedUser } as User }));
      toast.success('Profil başarıyla güncellendi!');
      return { success: true, user: updatedUser };
    } catch (error) {
      const errorMessage = getErrorMessage(error);
      toast.error(errorMessage);
      return { success: false, error: errorMessage };
    } finally {
      setLoading(false);
    }
  }, []);

  const changePassword = useCallback(async (currentPassword: string, newPassword: string): Promise<AuthResult> => {
    setLoading(true);
    try {
      await api.post(API_ENDPOINTS.AUTH.CHANGE_PASSWORD, { current_password: currentPassword, new_password: newPassword });
      toast.success('Şifre başarıyla değiştirildi!');
      return { success: true };
    } catch (error) {
      const errorMessage = getErrorMessage(error);
      toast.error(errorMessage);
      return { success: false, error: errorMessage };
    } finally {
      setLoading(false);
    }
  }, []);

  const forgotPassword = useCallback(async (email: string): Promise<AuthResult> => {
    setLoading(true);
    try {
      // Backend expects POST to /password-recovery/{email}
      await api.post(API_ENDPOINTS.AUTH.FORGOT_PASSWORD(email));
      toast.info('Şifre sıfırlama e-postası gönderildi.');
      return { success: true };
    } catch (error) {
      const errorMessage = getErrorMessage(error);
      toast.error(errorMessage);
      return { success: false, error: errorMessage };
    } finally {
      setLoading(false);
    }
  }, []);

  const resetPassword = useCallback(async (token: string, password: string): Promise<AuthResult> => {
    setLoading(true);
    try {
      // Backend expects body { token, new_password }
      await api.post(API_ENDPOINTS.AUTH.RESET_PASSWORD, { token, new_password: password });
      toast.success('Şifre başarıyla sıfırlandı. Giriş yapabilirsiniz.');
      router.push('/login');
      return { success: true };
    } catch (error) {
      const errorMessage = getErrorMessage(error);
      toast.error(errorMessage);
      return { success: false, error: errorMessage };
    } finally {
      setLoading(false);
    }
  }, [router]);

  return {
    session,
    loading: session.status === 'loading' || loading,
    isAuthenticated: session.status === 'authenticated',
    login,
    register,
    logout,
    updateProfile,
    changePassword,
    forgotPassword,
    resetPassword,
    checkAuth,
  };
};
