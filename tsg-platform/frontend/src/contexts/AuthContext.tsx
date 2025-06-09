import { createContext, useContext, useState, useEffect, useCallback } from 'react';
import type { ReactNode } from 'react';
import { useNavigate } from 'react-router-dom';
import { toast } from 'react-hot-toast';

interface User {
  id: string;
  email: string;
  name: string;
  role: string;
  avatar?: string;
}

interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (name: string, email: string, password: string) => Promise<void>;
  logout: () => void;
  updateUser: (userData: Partial<User>) => void;
}

const AuthContext = createContext<AuthContextType | null>(null);

interface AuthProviderProps {
  children: ReactNode;
}

export function AuthProvider({ children }: AuthProviderProps) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const navigate = useNavigate();

  // Check if user is logged in on initial load
  useEffect(() => {
    const checkAuth = async () => {
      try {
        // TODO: Implement token validation with backend
        const token = localStorage.getItem('token');
        if (token) {
          // TODO: Fetch user data from backend with the token
          // const userData = await fetchUserData(token);
          // setUser(userData);
        }
      } catch (error) {
        console.error('Auth check failed:', error);
        localStorage.removeItem('token');
      } finally {
        setIsLoading(false);
      }
    };

    checkAuth();
  }, []);

  const login = useCallback(async (email: string, _password: string) => {
    try {
      setIsLoading(true);
      // TODO: Implement actual login with backend
      // const { token, user } = await loginUser(email, password);
      // localStorage.setItem('token', token);
      // setUser(user);
      
      // Mock login for now
      const mockUser = {
        id: '1',
        email,
        name: 'Demo User',
        role: 'user',
      };
      
      localStorage.setItem('token', 'mock-token');
      setUser(mockUser);
      
      toast.success('Başarıyla giriş yapıldı');
      navigate('/dashboard');
    } catch (error) {
      console.error('Login failed:', error);
      toast.error('Giriş başarısız. Lütfen bilgilerinizi kontrol edin.');
      throw error;
    } finally {
      setIsLoading(false);
    }
  }, [navigate]);

  const register = useCallback(async (name: string, email: string, _password: string) => {
    try {
      setIsLoading(true);
      // TODO: Implement actual registration with backend
      // const { token, user } = await registerUser({ name, email, password });
      // localStorage.setItem('token', token);
      // setUser(user);
      
      // Mock registration for now
      const mockUser = {
        id: '1',
        email,
        name,
        role: 'user',
      };
      
      localStorage.setItem('token', 'mock-token');
      setUser(mockUser);
      
      toast.success('Hesap başarıyla oluşturuldu');
      navigate('/dashboard');
    } catch (error) {
      console.error('Registration failed:', error);
      toast.error('Kayıt başarısız. Lütfen tekrar deneyin.');
      throw error;
    } finally {
      setIsLoading(false);
    }
  }, [navigate]);

  const logout = useCallback(() => {
    localStorage.removeItem('token');
    setUser(null);
    toast.success('Başarıyla çıkış yapıldı');
    navigate('/');
  }, [navigate]);

  const updateUser = useCallback((userData: Partial<User>) => {
    if (user) {
      setUser({ ...user, ...userData });
    }
  }, [user]);

  const value = {
    user,
    isAuthenticated: !!user,
    isLoading,
    login,
    register,
    logout,
    updateUser,
  };

  return (
    <AuthContext.Provider value={value}>
      {!isLoading && children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

// Mock API functions - Replace with actual API calls
// Types for API responses
// type LoginResponse = { token: string; user: User };
// type RegisterResponse = { token: string; user: User };

// TODO: Implement these functions with actual API calls
// async function loginUser(email: string, password: string): Promise<LoginResponse> {
//   const response = await fetch('/api/auth/login', {
//     method: 'POST',
//     headers: { 'Content-Type': 'application/json' },
//     body: JSON.stringify({ email, password }),
//   });
//   if (!response.ok) {
//     throw new Error('Login failed');
//   }
//   return response.json();
// }

// async function registerUser(userData: { name: string; email: string; password: string }): Promise<RegisterResponse> {
//   const response = await fetch('/api/auth/register', {
//     method: 'POST',
//     headers: { 'Content-Type': 'application/json' },
//     body: JSON.stringify(userData),
//   });
//   if (!response.ok) {
//     throw new Error('Registration failed');
//   }
//   return response.json();
// }

// async function fetchUserData(token: string): Promise<User> {
//   const response = await fetch('/api/auth/me', {
//     headers: { 'Authorization': `Bearer ${token}` },
//   });
//   if (!response.ok) {
//     throw new Error('Failed to fetch user data');
//   }
//   return response.json();
// }
