// API Base URL
export const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:5001';

// API Endpoints
export const API_ENDPOINTS = {
  AUTH: {
    LOGIN: '/api/v1/auth/login',
    LOGOUT: '/api/v1/auth/logout',
    REGISTER: '/api/v1/auth/register',
    CHANGE_PASSWORD: '/api/v1/auth/change-password',
    // Backend expects POST /password-recovery/{email}
    FORGOT_PASSWORD: (email: string) => `/api/v1/auth/password-recovery/${encodeURIComponent(email)}`,
    // Backend expects POST /reset-password/ with { token, new_password }
    RESET_PASSWORD: '/api/v1/auth/reset-password/',
    REFRESH: '/api/v1/auth/refresh', 
    INVITE_CREATE: '/api/v1/auth/invite',
    INVITE_LIST_MY: '/api/v1/auth/invite/my',
    INVITE_REVOKE: (token: string) => `/api/v1/auth/invite/${encodeURIComponent(token)}`,
  },
  SETTINGS: {
    EMAIL: '/api/v1/settings/email',
    EMAIL_TEST: '/api/v1/settings/email/test',
    USER: '/api/v1/settings/user',
    SECURITY: '/api/v1/settings/security',
    SSO: '/api/v1/settings/sso',
    NOTIFICATIONS: '/api/v1/settings/notifications',
    PRIVACY: '/api/v1/settings/privacy',
    INTEGRATIONS: '/api/v1/settings/integrations',
  },
  USERS: {
    BASE: '/api/v1/users',
    ME: '/api/v1/users/me',
  },
  COMPANIES: {
    BASE: '/api/v1/companies',
    UNCOORDINATED: '/api/v1/companies/uncoordinated/',
    NEARBY: (id: string, max_km: number = 5, limit: number = 10) => `/api/v1/companies/${id}/nearby?max_km=${encodeURIComponent(String(max_km))}&limit=${encodeURIComponent(String(limit))}`,
  },
  STATS: {
    BASE: '/api/v1/stats',
    COORDINATES: '/api/v1/stats/coordinates',
  },
  PROCESSING: {
    PROCESS_COORDINATES: '/api/v1/process/process-coordinates',
    RESOLVE_CONFLICTS: '/api/v1/process/resolve-conflicts',
  },
  OCR: {
    // Current OCR technical preview endpoint
    PROCESS_AND_PREVIEW: '/api/v1/parsing/technical-preview',
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

// Search limits
export const SEARCH_MAX_COMPANIES = (() => {
  const raw = process.env.NEXT_PUBLIC_SEARCH_MAX_COMPANIES || '20';
  const n = parseInt(raw, 10);
  if (Number.isNaN(n)) return 20;
  return Math.min(Math.max(n, 1), 200);
})();
