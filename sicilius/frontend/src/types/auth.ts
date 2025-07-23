// --- TYPES AND INTERFACES ---

export interface ApiErrorResponse {
  detail?: string | { msg: string }[];
}

export type User = {
  id: string;
  email: string;
  name: string;
  role: string;
  image?: string;
  is_active?: boolean;
};

export type AuthResult = {
  success: boolean;
  error?: string;
  user?: User;
};

export type RegisterData = Omit<User, 'id' | 'role' | 'is_active' | 'image'> & { password: string };

export type Session = {
  user: User | null;
  status: 'authenticated' | 'loading' | 'unauthenticated';
};

export interface AuthContextType {
  session: Session;
  loading: boolean;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<AuthResult>;
  register: (data: RegisterData) => Promise<AuthResult>;
  logout: () => Promise<void>;
  updateProfile: (data: Partial<User>) => Promise<AuthResult>;
  changePassword: (currentPassword: string, newPassword: string) => Promise<AuthResult>;
  forgotPassword: (email: string) => Promise<AuthResult>;
  resetPassword: (token: string, newPassword: string) => Promise<AuthResult>;
  checkAuth: () => Promise<void>;
}
