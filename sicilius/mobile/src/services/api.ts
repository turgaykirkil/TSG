import axios, { 
  AxiosInstance, 
  AxiosRequestConfig, 
  AxiosResponse, 
  AxiosError 
} from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { Platform } from 'react-native';
import NetInfo from '@react-native-community/netinfo';

// Daha spesifik ve güvenli tip tanımları
interface User {
  id: string;
  role: string;
  email?: string;
}

interface APIParams {
  search?: string;
  status?: string[];
  tags?: string[];
  priority?: string[];
  sortBy?: string;
  sortOrder?: 'asc' | 'desc';
  page?: number;
  limit?: number;
}

// IP adresini al ve değişkene ata
let DEVICE_IP: string | null = null;
NetInfo.fetch().then((state: any) => {
  DEVICE_IP = state.details?.ipAddress || null;
});

// Güvenli, dinamik ve esnek BASE_URL yapılandırması
const PROD_URL = 'https://sicilius.com.tr';
const LOCAL_URL = Platform.select({
  ios: 'http://192.168.1.17:5001',
  android: 'http://10.0.2.2:5001',
  default: 'http://localhost:5001',
});

export const BASE_URL = process.env.EXPO_PUBLIC_API_URL || (
  __DEV__ ? LOCAL_URL : PROD_URL
);

// Gelişmiş ve detaylı hata yönetimi
class APIError extends Error {
  constructor(
    public message: string, 
    public status?: number, 
    public data?: any,
    public originalError?: Error
  ) {
    super(message);
    this.name = 'APIError';
    
    // Hata izleme için seviyeli bilgi (404/500 isteğe özel yönetildiği için ekranı kilitlemez)
    if (originalError && this.status !== 404) {
      if (this.status && this.status >= 500) {
        console.warn('Sunucu API Bildirimi (5xx):', {
          message: this.message,
          status: this.status,
          data: this.data,
        });
      } else {
        console.log(`[API ${this.status || 'İstek'}] ${this.data?.detail || this.message}`);
      }
    }
  }
}

// Güvenli token yönetimi
const getAuthToken = async (): Promise<string | null> => {
  try {
    return await AsyncStorage.getItem('authToken');
  } catch (error) {
    console.warn('Token alınamadı:', error);
    return null;
  }
};

// API oluşturma fonksiyonu
const createAPIClient = (): AxiosInstance => {
  const api = axios.create({
    baseURL: BASE_URL,
    timeout: 15000, // Zaman aşımını biraz artırdık
    headers: {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
      'X-App-Platform': Platform.OS,
      'X-App-Version': '1.0.0' // Versiyon takibi için
    }
  });

  // Request interceptor
  api.interceptors.request.use(
    async (config: any) => {
      try {
        const token = await getAuthToken();
        const userStr = await AsyncStorage.getItem('user');
        
        if (token) {
          config.headers = {
            ...config.headers,
            'Authorization': `Bearer ${token}`
          };
        }
        
        if (userStr) {
          const user: User = JSON.parse(userStr);
          config.headers = {
            ...config.headers,
            'x-user-id': user.id,
            'x-user-role': user.role
          };
        }
      } catch (error) {
        console.warn('İstek öncesi uyarı:', error);
      }
      return config;
    },
    (error: AxiosError) => {
      return Promise.reject(new APIError(
        'İstek Hatası', 
        error.response?.status, 
        error.response?.data, 
        error
      ));
    }
  );

  // Response interceptor
  api.interceptors.response.use(
    (response: AxiosResponse) => response,
    (error: AxiosError) => {
      const apiError = new APIError(
        error.message || 'Bilinmeyen Hata', 
        error.response?.status, 
        error.response?.data,
        error
      );
      
      // Özel hata yönetimi
      switch (apiError.status) {
        case 401:
          // Token süresi dolmuş veya geçersiz
          AsyncStorage.removeItem('authToken');
          AsyncStorage.removeItem('user');
          break;
        case 403:
          // Yetkisiz erişim
          console.warn('Yetkisiz erişim');
          break;
        case 404:
          // 404 Sessiz yönetilir (Fallback verileri kullanılır)
          break;
        case 500:
          // Sunucu uyarısı
          console.warn('Sunucu uyarısı (500)');
          break;
      }
      
      return Promise.reject(apiError);
    }
  );

  return api;
};

const api = createAPIClient();

// Performans ve hata toleransı yüksek generic CRUD operasyonları
const createCRUDOperations = <T>(endpoint: string) => ({
  getAll: async (params?: APIParams): Promise<T[]> => {
    try {
      const response = await api.get(endpoint, { 
        params,
        headers: { 'Cache-Control': 'no-cache' }
      });
      if (Array.isArray(response.data)) return response.data;
      if (Array.isArray(response.data?.data)) return response.data.data;
      if (Array.isArray(response.data?.items)) return response.data.items;
      return [];
    } catch (error: any) {
      if (error?.status !== 404) {
        console.warn(`${endpoint} listesi alınamadı, boş liste dönülüyor:`, error);
      }
      return [];
    }
  },
  
  getById: async (id: string): Promise<T | null> => {
    try {
      const response = await api.get(`${endpoint}/${id}`);
      return response.data;
    } catch (error) {
      console.warn(`${endpoint}/${id} detayı alınamadı:`, error);
      return null;
    }
  },
  
  create: async (data: Partial<T>): Promise<T> => {
    try {
      const response = await api.post(endpoint, data);
      return response.data;
    } catch (error) {
      console.error(`${endpoint} oluşturulamadı:`, error);
      throw error;
    }
  },
  
  update: async (id: string, data: Partial<T>): Promise<T> => {
    try {
      const response = await api.put(`${endpoint}/${id}`, data);
      return response.data;
    } catch (error) {
      console.error(`${endpoint} güncellenemedi:`, error);
      throw error;
    }
  },
  
  delete: async (id: string): Promise<void> => {
    try {
      await api.delete(`${endpoint}/${id}`);
    } catch (error) {
      console.error(`${endpoint} silinemedi:`, error);
      throw error;
    }
  }
});

// Auth API
export const authAPI = {
  login: async (email: string, password: string) => {
    try {
      console.log('Login attempt to backend:', { email });
      let response: any;
      
      try {
        response = await api.post('/api/v1/auth/login', { email, password });
      } catch (jsonErr: any) {
        // FastAPI OAuth2 fallback with form-urlencoded
        const formData = new URLSearchParams();
        formData.append('username', email);
        formData.append('password', password);
        
        response = await api.post('/api/v1/auth/login', formData.toString(), {
          headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
        });
      }

      console.log('Login successful:', response.data);
      const token = response.data.access_token || response.data.token || '';
      const user = response.data.user || { id: '1', email, role: 'admin' };
      
      await AsyncStorage.multiSet([
        ['authToken', token],
        ['user', JSON.stringify(user)]
      ]);
      
      return { token, user };
    } catch (error: any) {
      console.log('[Login Response]', error?.response?.data || error.message);
      throw error;
    }
  },
  
  register: async (data: { email: string; password: string; full_name?: string; firstName?: string; lastName?: string }) => {
    try {
      const fullName = data.full_name || `${data.firstName || ''} ${data.lastName || ''}`.trim() || data.email;
      console.log('Register attempt to backend:', { email: data.email, full_name: fullName });
      const response = await api.post('/api/v1/auth/register', {
        email: data.email,
        password: data.password,
        full_name: fullName,
      });
      console.log('Register response:', response.data);
      return response.data;
    } catch (error: any) {
      console.log('[Register Response]', error?.response?.data || error.message);
      throw error;
    }
  },

  logout: async () => {
    try {
      // Tüm depolanan kullanıcı bilgilerini temizle
      await AsyncStorage.multiRemove(['authToken', 'user']);
      return true;
    } catch (error) {
      console.error('Çıkış hatası:', error);
      return false;
    }
  }
};

// Detaylı ve tam uyumlu API tanımları
export const customerAPI = createCRUDOperations<any>('/api/v1/b2b-customers');
export const companyAPI = createCRUDOperations<any>('/api/v1/companies');
export const taskAPI = createCRUDOperations<any>('/api/v1/tasks');
export const salesAPI = createCRUDOperations<any>('/api/v1/stats');

export default api;