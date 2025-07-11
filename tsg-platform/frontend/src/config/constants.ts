// API Base URL
export const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5001';

// API Endpoints
export const API_ENDPOINTS = {
  AUTH: {
    LOGIN: '/api/v1/auth/login',
    LOGOUT: '/api/v1/auth/logout',
    REGISTER: '/api/v1/auth/register',
    CHANGE_PASSWORD: '/api/v1/auth/change-password',
    FORGOT_PASSWORD: '/api/v1/auth/forgot-password',
    RESET_PASSWORD: '/api/v1/auth/reset-password',
    REFRESH: '/api/v1/auth/refresh', 
  },
  USERS: {
    BASE: '/api/v1/users',
    ME: '/api/v1/users/me',
  },
  COMPANIES: {
    BASE: '/api/v1/companies',
    UNCOORDINATED: '/api/v1/companies/uncoordinated/',
  },
  STATS: {
    BASE: '/api/v1/stats',
    COORDINATES: '/api/v1/stats/coordinates',
  },
  PROCESS: {
    COORDINATES: '/api/v1/process/process-coordinates',
    CONFLICTS: '/api/v1/process/resolve-conflicts',
  },
  // Add other endpoints as needed
} as const;

// Local Storage Keys
export const STORAGE_KEYS = {
  AUTH_TOKEN: 'auth_token',
  REFRESH_TOKEN: 'refresh_token',
  USER: 'user',
} as const;

// Cookie Names
export const COOKIE_NAMES = {
  SESSION: 'session',
  REFRESH_TOKEN: 'refresh_token',
} as const;
